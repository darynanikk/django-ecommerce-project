from django.db import models

from customer.models import Customer


class Item(models.Model):
    SIZES_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
    CATEGORIES_CHOICES = [('M', 'Men'), ('W', 'Women'), ('Ch', 'Children')]
    FAVORITE_COLORS_CHOICES = [
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('purple', 'Purple')
    ]

    title = models.CharField(max_length=100)
    categories = models.CharField(max_length=25, choices=CATEGORIES_CHOICES, null=True, blank=True)
    sizes = models.CharField(max_length=25, choices=SIZES_CHOICES, null=True, blank=True)
    colours = models.CharField(max_length=25, choices=FAVORITE_COLORS_CHOICES, null=True, blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(default='product')
    description = models.TextField(max_length=355, null=True, blank=True)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def get_total_price(self):
        item = self.item
        current_price = item.price
        if item.discount_price:
            current_price = item.discount_price
        return current_price * self.quantity

    def __str__(self):
        return str(self.item)


class Order(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer)

    @property
    def get_cart_total_price(self):
        order_items = self.items.all()
        return sum([item.get_total_price for item in order_items])

    @property
    def get_total_count(self):
        order_items = self.items.all()
        return len(order_items)


class Address(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.SET_NULL, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name_plural = 'Addresses'
