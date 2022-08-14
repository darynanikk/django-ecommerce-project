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


class ProcessCheckoutSessionView(View):

    def get(self, *args, **kwargs):
        context = {}
        order = self.request.order
        order_items = order.items.all()
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        context['order_items'] = order_items
        context['order'] = order
        return render(self.request, 'store/checkout.html', context)

    def post(self, *args, **kwargs):
        order = self.request.order
        order_items = order.items.all()

        data = [
            {
                'price': stripe.Price.create(
                    # TODO format me
                    unit_amount=int(order_item.get_total_price),
                    currency="pln",
                    product=stripe.Product.create(name=order_item.item.title),
                ),
                'quantity': order_item.quantity
            } for order_item in order_items
        ]
        checkout_session = stripe.checkout.Session.create(
            line_items=data,
            metadata={
                'order_id': order.id
            },
            mode='payment',
            success_url=settings.DOMAIN + '/success/',
            cancel_url=settings.DOMAIN + '/cancel/',
        )

        return redirect(checkout_session.url, status=303)


@csrf_exempt
def stripe_webhook_view(request):
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

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    print("Fulfilling order")
    customer_email = session['customer_details']['email']
    order_id = session['metadata']['order_id']

    order = Order.objects.get(id=order_id)
    message = "Thank you for the purchase. "
    for order_item in order.items.all():
        message += f"{order_item.item.price} x {order_item.quantity}"
    send_mail(
        subject="Here is your product",
        message=message,
        recipient_list=[customer_email],
        from_email="daryna@test.com"
    )




