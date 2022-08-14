from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    
