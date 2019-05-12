from django.conf import settings
from django.db import models

from .config import AUTH_OPTIONS
from .config import STATUS_OPTIONS


# Create your models here.
class Order(models.Model):
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(
        max_length=255, verbose_name='Company Name')
    address_one = models.CharField(max_length=255, verbose_name='Address One')
    address_two = models.CharField(
        max_length=255, blank=True, verbose_name='Address Two')
    city = models.CharField(max_length=255, verbose_name='City')
    county = models.CharField(max_length=255, blank=True, verbose_name='County')
    post_code = models.CharField(max_length=255, verbose_name='Postcode')
    telephone = models.CharField(max_length=255, verbose_name='Telephone')
    reason = models.CharField(max_length=255, verbose_name='Reason for Order')
    delivery_date = models.DateField(verbose_name='Expected Delivery Date')
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        max_length=10,
        choices=STATUS_OPTIONS,
        default=STATUS_OPTIONS[0][0],
        blank=True)
    auth_required = models.CharField(
        max_length=50,
        choices=AUTH_OPTIONS,
        blank=True)
    dm_auth = models.BooleanField(default=False)
    md_auth = models.BooleanField(default=False)
    decline_message = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{0}'.format(self.company_name)


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, verbose_name='Description')
    item_qty = models.IntegerField(verbose_name='Qty')
    item_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Price')

    def __str__(self):
        return '{0}'.format(self.item_name)
