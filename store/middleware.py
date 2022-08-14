from django.utils.deprecation import MiddlewareMixin

from customer.models import Customer
from store.models import Order


class CountOrderedItemsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        order = {}
        try:
            customer = Customer.objects.get(user=request.user)
            request.customer = customer
            order = Order.objects.get(customer=customer)
        except:
            pass
        request.order = order
