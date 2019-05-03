from django.contrib import admin

# Register your models here.
from .models import Order
from .models import Item


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'ordered_by',
        'date_ordered',
        'delivery_date',
        'order_status',
    )
    search_fields = (
        'company_name',
        'ordered_by',
        'date_ordered',
        'delivery_date',
        'order_status',
    )
    list_filter = (
        'order_status',
    )
    readonly_fields = (
        'date_ordered',
    )


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'item_name',
        'item_qty',
        'item_price',
    )
    search_fields = (
        'order',
        'item_name',
        'item_qty',
        'item_price',
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
