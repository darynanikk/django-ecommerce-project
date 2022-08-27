from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

from customer.models import Customer
from store.models import Order


class OrderMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(customer=request.user)
                request.order = order
                return
            except Order.DoesNotExist:
                print('customer does not make any order')

        if request.user.is_anonymous:
            try:
                customer = get_object_or_404(Customer, email='anonym@ecommerce.com')
                order = Order.objects.get(customer=customer)
                request.order = order
                return
            except Http404:
                print('anonymous customer does not make any order')
