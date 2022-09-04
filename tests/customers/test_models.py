from django.test import TestCase
from customer.models import Customer


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(
            first_name='Henry',
            last_name='Miles',
            email='henry123@mail.com',
            password='password',
            phone_number='+48698246035'
        )

    def test_email_label(self):
        print("test email label")
        customer = Customer.objects.get(id=1)
        field_label = customer._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email address')

    def test_first_name_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 55)

    def test_last_name_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 55)

    def test_device_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('device').max_length
        self.assertEqual(max_length, 200)

    def test_email_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('email').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_customer_email(self):
        customer = Customer.objects.get(id=1)
        self.assertEqual(str(customer), customer.email)


