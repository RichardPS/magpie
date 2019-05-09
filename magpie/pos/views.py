from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

import pdb

from .forms import ItemFormSet
from .forms import ItemForm
from .forms import OrderForm

from .functions import order_saved
from .functions import order_value

from .models import Item
from .models import Order


# Create your views here.
def index(
        request,
        template_name='pos/index.html',
        page_name='POS System'):

    if request.method == 'POST':
        """ get post data """
        order_form = OrderForm(request.POST)
        item_form_set = ItemFormSet(request.POST)

        """ get order variables - order total and if auth if required """
        if item_form_set.is_valid():
            pos_required = order_variables(item_form_set)

        """ get auth required or reject order request """
        if pos_required['order_total'] >= 200:
            """ auth required """
            auth_required = pos_required['auth_option']
        else:
            """ no auth required redirect to exit page """
            return redirect('index')

        """ process order """
        if order_form.is_valid() & item_form_set.is_valid():
            _order = order_form.save(commit=False)
            _order.ordered_by = request.user
            _order.auth_required = auth_required
            _order.save()

        """ get pk for order for ForeignKey assignment """
        order_object = get_object_or_404(Order, pk=_order.pk)

        """ process order items """
        for item in item_form_set:
            if item.is_valid():
                _item = item.save(commit=False)
                _item.order = order_object
                _item.save()

        """ send email to required auth persons """
        order_saved(_order.pk)

        """ redirect to order summary page """
        return redirect('index')
    else:
        """ get empty forms """
        order_form = OrderForm()
        item_form_set = ItemFormSet()

    context = {
        'item_form_set': item_form_set,
        'order_form': order_form,
        'page_name': page_name,
    }

    return render(
        request,
        template_name,
        context,
    )
