from django import forms
from phonenumber_field.formfields import PhoneNumberField

country_choices = [
    ('Armenia', 'AM'),
    ('Ukraine', 'UA'),
    ('United Arab Emirates', 'AE'),
    ('United Kingdom of Great Britain and Northern Ireland', 'GB'),
    ('United States of America', 'US')
]


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=55, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name', 'id': 'f_name'}))
    last_name = forms.CharField(max_length=55, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'id': 'l_name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'id': 'email'}))
    password = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Password', 'id': 'c_password'}), required=False)
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'id': 'c_phone'}))
    country = forms.ChoiceField(choices=country_choices, required=True)
    city = forms.CharField(max_length=55,required=True, widget=forms.TextInput(attrs={'placeholder': 'City', 'id': 'c_city'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'address', 'id': 'c_address'}))
    zip_code = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'Postal code', 'id': 'c_zip'}))
    registered = forms.BooleanField(label='Register?', required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if request.user.is_authenticated:
            self.fields['password'].widget = forms.HiddenInput()
            self.fields['registered'].widget = forms.HiddenInput()
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['last_name'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()