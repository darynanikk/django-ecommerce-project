from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from customer.forms import CustomerCreationForm
from customer.models import Customer


class CustomerAuthViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        customer = Customer.objects.create(
            first_name='Henry',
            last_name='Miles',
            email='henry123@mail.com',
            password='1X<ISRUkw+tuK',
            phone_number='+48698246035'
        )
        customer.set_password(customer.password)
        customer.save()

    def test_not_logged_in_uses_correct_template(self):
        response = self.client.get(reverse('customer:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/login_register.html')

    def test_logged_in_uses_correct_template(self):
        customer = Customer.objects.get(email='henry123@mail.com')
        self.client.force_login(customer)
        response = self.client.get(reverse('store:shop'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'henry123@mail.com')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'store/shop.html')

    def test_logout_customer_redirect_is_correct(self):
        customer = Customer.objects.get(email='henry123@mail.com')
        self.client.force_login(customer)
        self.client.logout()
        response = self.client.get(reverse('customer:logout'))
        self.assertRedirects(response, status_code=302, expected_url='/auth/login')

    def test_registered_customer_redirect_is_correct(self):
        response = self.client.post(reverse('customer:register'))
        self.assertRedirects(response, status_code=302, expected_url='/auth/login')
