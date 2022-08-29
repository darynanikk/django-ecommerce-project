from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

from customer.models import Customer
from store.models import Order


class OrderMiddleware(MiddlewareMixin):

    def process_request(self, request):
        device_id = request.COOKIES.get('device')
        try:
            if request.user.is_authenticated:
                order = get_object_or_404(Order, customer=request.user)
            else:
                customer, created = Customer.objects.get_or_create(device=device_id)
                order = get_object_or_404(Order, customer=customer)

            request.order = order
        except Http404:
            pass

