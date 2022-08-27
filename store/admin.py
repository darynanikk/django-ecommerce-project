from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Address)
admin.site.register(ImageItem)