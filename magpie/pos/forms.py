from django import forms
from django.forms import formset_factory
from django.forms import Textarea
from django.forms.widgets import TextInput

from .models import Order
from .models import Item


class DateInput(TextInput):
    input_type = 'date'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'company_name',
            'address_one',
            'address_two',
            'city',
            'county',
            'post_code',
            'telephone',
            'reason',
            'delivery_date',
        ]
        widgets = {
            'reason': Textarea(attrs={'cols': 80, 'rows': 10}),
            'delivery_date': DateInput(attrs={'class': 'date'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_name',
            'item_qty',
            'item_price',
        ]


ItemFormSet = formset_factory(ItemForm, extra=1)
