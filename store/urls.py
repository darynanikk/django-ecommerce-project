from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("shop/", ShopListView.as_view(), name='shop'),
    path("about/", about, name='about'),
    path("contact/", contact, name='contact'),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name='product'),
    # cart
    path("cart/", cart, name='cart'),
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('checkout/', ProductCheckoutPageView.as_view(), name='checkout'),
]