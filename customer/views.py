from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def login_user(request):
    context = {
        'page': 'login'
    }
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        customer = authenticate(request, username=email, password=password)

        if customer is not None:
            login(request, customer)
            return redirect('store:shop')

    return render(request, 'customer/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('customer:login')


def register_user(request):
    page = 'register'
    form = CustomerCreationForm()

    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            customer.set_password(password)
            customer.save()
        return redirect('customer:login')

    context = {'form': form, 'page': page}
    return render(request, 'customer/login_register.html', context)
