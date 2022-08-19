from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import *

# Register your models here.
admin.site.register(Customer, UserAdmin)
admin.site.unregister(Group)