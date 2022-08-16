import json
import stripe

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from shop import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .cart import Cart
from django.views.generic import ListView, DetailView, TemplateView
from customer.models import Customer
from store.models import Item, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeListView(ListView):
    model = Order
    template_name = 'store/main.html'

    def get_queryset(self):
        item_qs = super(HomeListView, self).get_queryset()
        print(self.request.order)
        try:
            # TODO filter featured items (anonymous user\ registered)
            featured_items = item_qs.filter(user=self.request)
        except:
            pass
        return super(HomeListView, self).get_queryset()


class ShopListView(ListView):
    model = Item
    template_name = 'store/shop.html'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'store/shop-single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def cart(request):
    context = {}
    method = request.method
    customer, created = Customer.objects.get_or_create(user=request.user)

    if customer.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, ordered=False)

    else:
        # TODO handle later
        device = request.COOKIES['device']
        return JsonResponse({"cool": "cool"}, safe=False)

    if method != 'GET':
        data = json.loads(request.body)
        product_id = data['ProductId']
        quantity = data['Quantity']
        item, created = Item.objects.get_or_create(slug=product_id)
        order_item, created = OrderItem.objects.get_or_create(customer=customer, ordered=False, item=item)
        c = Cart(item=item, order=order, customer=customer, quantity=quantity, order_item=order_item, created=created)

        if method == 'POST':
            c.add_to_cart()
        elif method == 'PUT':
            c.update_cart()
        elif method == 'DELETE':
            c.remove_from_cart()

    context['order_items'] = order.items.all()
    context['order'] = order
    return render(request, 'store/cart.html', context)


def about(request):
    context = {}
    return render(request, 'store/about.html', context)


def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)


class SuccessTemplateView(TemplateView):
    template_name = 'store/thankyou.html'


class CancelTemplateView(TemplateView):
    template_name = 'store/cancel.html'


class ProductCheckoutPageView(TemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(ProductCheckoutPageView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "order": self.request.order
        })
        return context


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Item.objects.get(slug=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]

        product = Item.objects.get(slug=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            customer = stripe.Customer.create(email="daryandobro@gmail.com")
            order = request.order
            product = order.items.all()[0]
            intent = stripe.PaymentIntent.create(
                amount=300,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })
