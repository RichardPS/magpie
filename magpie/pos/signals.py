from django.db.models.signals import post_save
from django.dispatch import receiver

import pdb
"""
from .models import Order
from .models import Item


@receiver(post_save, sender=Order)
def order_saved(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if created:
        pk = instance.pk
        items = Item.objects.all().filter(order__pk=pk)
        total = 0
        pdb.set_trace()
        for item in items:
            total = total + item.item_price
        print('signal fired: {0}'.format(pk))
        print('Total: {0}'.format(total))
"""
