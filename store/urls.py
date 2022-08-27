from django.urls import path
from .views import *

app_name = 'store'

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("shop/", ShopListView.as_view(), name='shop'),
    path("about/", about, name='about'),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name='product'),
    # cart
    path("cart/", cart, name='cart'),
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('checkout/', ProductCheckoutPageView.as_view(), name='checkout'),
]