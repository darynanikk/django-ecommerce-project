from django.utils.deprecation import MiddlewareMixin

from customer.models import Customer
from store.models import Order


class OrderMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            request.order = Order.objects.get(customer=request.user)
        except:
            pass