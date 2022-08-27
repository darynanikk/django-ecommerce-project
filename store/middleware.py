from django.utils.deprecation import MiddlewareMixin

from customer.models import Customer
from store.models import Order


class OrderMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            request.order = Order.objects.get(customer=request.user)
        else:
            device = request.COOKIES["device"]
            customer = Customer.objects.get(device=device)
            request.order = Order.objects.get(customer=customer)