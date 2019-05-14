from django.contrib import messages
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView

# import pdb

from .config import AUTH_OPTIONS
from .config import STATUS_OPTIONS

from .forms import ItemFormSet
# from .forms import ItemForm
from .forms import OrderForm

from .functions import order_saved
from .functions import order_variables

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
            """ get auth required and op total """
            pos_required = order_variables(item_form_set)
            """ get auth required or reject order request """
            if pos_required['order_total'] >= 200:
                """ auth required """
                auth_required = pos_required['auth_option']
            else:
                """ no auth required render order page with info message """
                """ get empty forms """
                order_form = OrderForm()
                item_form_set = ItemFormSet()
                """ set message """
                messages.info(
                    request,
                    'No Purchase Order Required for orders under £200')

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

        """ process order """
        if order_form.is_valid() & item_form_set.is_valid():
            _order = order_form.save(commit=False)
            _order.ordered_by = request.user
            _order.auth_required = AUTH_OPTIONS[auth_required][0]
            _order.save()

            """ get pk for order for ForeignKey assignment """
            order_object = get_object_or_404(Order, pk=_order.pk)

            """ process order items """
            for item in item_form_set:
                if item.is_valid():
                    _item = item.save(commit=False)
                    _item.order = order_object
                    _item.save()

            """ send email to required auth persons, move to summary view?"""
            order_saved(_order.pk)

            """ redirect to order summary page """
            return redirect('summary/' + str(_order.pk))
        else:
            """ no auth required render order page with info message """
            """ get empty forms """
            order_form = OrderForm()
            item_form_set = ItemFormSet()
            """ set message """
            messages.error(
                request,
                'Error in data')

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


def order_summary(
        request,
        pk,
        template_name='pos/summary.html',
        page_name='Order Summary'):

    order_details = get_object_or_404(Order, pk=pk)
    item_details = Item.objects.filter(order__pk=pk)
    order_total = 0
    for item in item_details:
        order_total = order_total + item.item_price * item.item_qty

    context = {
        'page_name': page_name,
        'order_details': order_details,
        'item_details': item_details,
        'order_total': order_total
    }

    return render(
        request,
        template_name,
        context,
    )


class AdminOrders(ListView):
    model = Order
    template_name = 'admin/order_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AdminOrders, self).get_context_data(**kwargs)
        context['page_name'] = self.kwargs['area'].capitalize()
        return context

    def get_queryset(self):
        return super(AdminOrders, self).get_queryset().filter(
            order_status=self.kwargs['area'])


class AdminOrderDetails(DetailView):
    model = Order
    template_name = 'admin/order_details.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(AdminOrderDetails, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(order=self.kwargs['pk'])
        context['page_name'] = 'Details for {0} order'.format(
            self.object.company_name)
        return context

def cancel_order(
        request,
        pk):

    order_to_cancel = get_object_or_404(Order, pk=pk)
    order_to_cancel.order_status = STATUS_OPTIONS[4][0]
    order_to_cancel.save()

    return redirect('/orders/canceled')


def clear_order(
        request,
        pk):

    order_to_clear = get_object_or_404(Order, pk=pk)
    order_to_clear.order_status = STATUS_OPTIONS[3][0]
    order_to_clear.save()

    return redirect('/orders/cleared')
