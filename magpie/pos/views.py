from django.shortcuts import render

from .forms import ItemFormSet
# from .forms import ItemForm
from .forms import OrderForm


# Create your views here.
def index(
        request,
        template_name='pos/index.html',
        page_name='Index'):

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        item_form_set = ItemFormSet(request.POST)
        if item_form_set.is_vaild():
            print('Valid')
    else:
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
