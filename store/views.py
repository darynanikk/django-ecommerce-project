import json
import stripe
import os

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from customer.models import Customer
from .cart import Cart
from django.views.generic import ListView, DetailView, TemplateView
from store.models import Item, Order, OrderItem
from .filters import item_filter, ItemsFilter
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


class HomeListView(ListView):
    model = Order
    template_name = "store/main.html"

    def get_queryset(self):
        order = super(HomeListView, self).get_queryset()[0]
        if self.request.user.is_authenticated:
            return order.items.filter(customer=self.request.user)
        else:
            return order.items.all()


class ShopListView(View):
    model = Item
    context = {}
    template_name = "store/shop.html"

    def get(self, request, *args, **kwargs):
        qs = item_filter(request)
        self.context["items"] = qs
        self.context["filter"] = ItemsFilter(request.GET, queryset=qs)
        return render(request, self.template_name, self.context)


class ProductDetailView(DetailView):
    model = Item
    template_name = "store/shop-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def cart(request):
    context = {}
    method = request.method
    customer = request.user
    if customer.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, ordered=False)
    else:
        device = request.COOKIES["device"]
        customer, created = Customer.objects.get_or_create(device=device)
        order, created = Order.objects.get_or_create(customer=customer, ordered=False)

    if method != "GET":
        data = json.loads(request.body)
        product_id = data["ProductId"]
        quantity = data["Quantity"]
        item, created = Item.objects.get_or_create(slug=product_id)
        order_item, created = OrderItem.objects.get_or_create(
            customer=customer, ordered=False, item=item
        )
        c = Cart(
            item=item,
            order=order,
            customer=customer,
            quantity=quantity,
            order_item=order_item,
            created=created,
        )

        if method == "POST":
            c.add_to_cart()
        elif method == "PUT":
            c.update_cart()
        elif method == "DELETE":
            c.remove_from_cart()

    context["order_items"] = order.items.all()
    context["order"] = order
    return render(request, "store/cart.html", context)


def about(request):
    context = {}
    return render(request, "store/about.html", context)


class ProductCheckoutPageView(TemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(ProductCheckoutPageView, self).get_context_data(**kwargs)
        customer = self.request.user
        if customer.is_authenticated:
            order = get_object_or_404(Customer, email=customer.email)
        else:
            device = self.request.COOKIES["device"]
            customer = Customer.objects.get(device=device)
            order = Order.objects.get(customer=customer)

        order_items = order.items.all()
        context.update(
            {
                "STRIPE_PUBLIC_KEY": os.getenv("STRIPE_PUBLIC_KEY", ""),
                "order": order,
                "order_items": order_items,
            }
        )
        return context


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET", "")
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer["email"]
        order_id = intent["metadata"]["order_id"]
        order = Order.objects.get(id=order_id)

        message = "Thanks for your purchase. Here is the product(s) you ordered."

        for order in order.items.all():
            message += f" {order.item.title}"

        send_mail(
            subject="Here is your product(s)",
            message=message,
            recipient_list=[customer_email],
            from_email="admin@mail.com",
        )

        return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            data = json.loads(body.decode("utf-8"))
            if request.user.is_authenticated:
                email = str(request.user)
            else:
                email = data.get("email")

            customer, created = stripe.Customer.get_or_create(email=email)
            order = request.order

            shipping = {
                "address": {
                    "country": data.get("country"),
                    "city": data.get("city"),
                    "postal_code": data.get("postal_code"),
                    "line1": data.get("street_address"),
                },
                "name": email,
                "phone": data.get("phone_number"),
            }
            intent = stripe.PaymentIntent.create(
                amount=int(order.get_cart_total_price),
                currency="usd",
                customer=customer["id"],
                shipping=shipping,
                receipt_email=email,
                metadata={
                    "order_id": order.id,
                },
            )
            print(intent)
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
