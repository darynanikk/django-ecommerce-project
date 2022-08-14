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

    # payment
    path('create-checkout-session/', ProcessCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelTemplateView.as_view(), name='cancel'),
    path('success/', SuccessTemplateView.as_view(), name='success'),

    #webhooks
    path('webhooks/stripe/', stripe_webhook_view, name='stripe-webhook')
]