from django.test import SimpleTestCase, TestCase
from customer.models import Customer
from customer.forms import CustomerCreationForm, CustomerChangeForm


class CustomerCreationFormTest(TestCase):

    def test_password_label(self):
        form = CustomerCreationForm()
        self.assertTrue(
            form.fields['password1'].label == 'Password')

    def test_password_confirm_label(self):
        form = CustomerCreationForm()
        self.assertTrue(
            form.fields['password2'].label == 'Password confirmation')

    def test_check_passwords_match(self):
        form = CustomerCreationForm(data=
        {
            'first_name': 'First name',
            'last_name': 'Last name',
            'phone_number': '+48698246035',
            'email': 'test@mail.com',
            'password1': 'secret',
            'password2': 'secret'}
        )
        self.assertTrue(form.is_valid())


class CustomerChangeFormTest(TestCase):
    pass
