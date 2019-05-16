# 3rd party
from django.contrib import admin

# local
from .models import Order
from .models import Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    can_delete = False
    readonly_fields = (
        'item_name',
        'item_qty',
        'item_price',
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'ordered_by',
        'date_ordered',
        'delivery_date',
        'auth_required',
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
        'auth_required',
    )
    readonly_fields = (
        'date_ordered',
    )
    inlines = [
        ItemInline,
    ]


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
