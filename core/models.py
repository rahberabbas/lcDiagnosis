from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from account.models import Profile


class Item(models.Model):
    sid = models.CharField(max_length=10, null=True, blank=True)
    testname = models.CharField(max_length=1000, null=True, blank=True)
    testcode = models.CharField(max_length=1000, null=True, blank=True)
    price = models.CharField(max_length=256, null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.testcode
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.product.price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancled', 'Cancled')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_cost(self):
        return self.product.price

class PaymentDone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, null=True, blank=True)

