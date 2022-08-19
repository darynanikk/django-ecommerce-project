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
        customer = self.request.customer
        order = Order.objects.get(customer=customer)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "order": order
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

    if event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        order_id = intent["metadata"]["order_id"]
        order = Order.objects.get(id=order_id)

        message = 'Thanks for your purchase. Here is the product(s) you ordered.'

        for order in order.items.all():
            message += f' {order.item.title}'

        send_mail(
            subject="Here is your product(s)",
            message=message,
            recipient_list=[customer_email],
            from_email="admin@mail.com"
        )

        return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            data = json.loads(body.decode('utf-8'))
            customer = stripe.Customer.create(email=data.get('email'))
            # if user is logged in
            order = Order.objects.get(customer=request.customer)
            intent = stripe.PaymentIntent.create(
                amount=int(order.get_cart_total_price),
                currency='usd',
                customer=customer['id'],
                metadata={
                    "order_id": order.id,
                },
            )
            print(intent)
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})