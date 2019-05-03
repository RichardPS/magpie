from django.conf import settings
from django.db import models

from .config import STATUS_OPTIONS


# Create your models here.
class Order(models.Model):
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    address_one = models.CharField(max_length=255)
    address_two = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    delivery_date = models.DateField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=10, choices=STATUS_OPTIONS)

    def __str__(self):
        return '{0}'.format(self.company_name)


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_qty = models.IntegerField()
    item_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return '{0}'.format(self.item_name)
