# 3rd party
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator

# local
from .config import AUTH_OPTIONS
from .config import STATUS_OPTIONS

from .forms import DeclineMessage
from .forms import ItemFormSet
from .forms import OrderForm
# from .forms import UserEditForm

from .functions import accept_auth
from .functions import auth_complete
from .functions import decline_auth
from .functions import order_saved
from .functions import order_variables

from .models import Item
from .models import Order


class Index(TemplateView):
    template_name = 'pos/index.html'


@login_required
def raise_pos(
        request,
        template_name='pos/raise_pos.html',
        page_name='Raise Purchase Order'):

    """ purchase order form """
    """ POST request - process order """
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
        """ render blank order form """
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
    """ display summery of order """
    order = get_object_or_404(Order, pk=pk)

    context = {
        'page_name': page_name,
        'order': order
    }

    return render(
        request,
        template_name,
        context,
    )


@method_decorator(staff_member_required, name='dispatch')
class AdminOrders(ListView):
    model = Order
    template_name = 'admin/order_list.html'
    paginate_by = 10

    """ admin area, view orders in each stage """
    def get_context_data(self, **kwargs):
        context = super(AdminOrders, self).get_context_data(**kwargs)
        context['page_name'] = self.kwargs['area'].capitalize()
        return context

    def get_queryset(self):
        return super(AdminOrders, self).get_queryset().filter(
            order_status=self.kwargs['area'])


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetails(DetailView):
    model = Order
    template_name = 'admin/order_details.html'
    pk_url_kwarg = 'pk'

    """ admin view order details """
    def get_context_data(self, **kwargs):
        context = super(AdminOrderDetails, self).get_context_data(**kwargs)
        context['page_name'] = 'Details for {0} order'.format(
            self.object.company_name)
        return context


def cancel_order(
        request,
        pk):

    """ change order status to cenceled """
    order_to_cancel = get_object_or_404(Order, pk=pk)
    order_to_cancel.order_status = STATUS_OPTIONS[4][0]
    order_to_cancel.save()

    return redirect('/orders/canceled')


def clear_order(
        request,
        pk):

    """ change order status to cleared """
    order_to_clear = get_object_or_404(Order, pk=pk)
    order_to_clear.order_status = STATUS_OPTIONS[3][0]
    order_to_clear.save()

    return redirect('/orders/cleared')


@method_decorator(staff_member_required, name='dispatch')
class AuthOrder(DetailView):
    model = Order
    template_name = 'admin/auth_order.html'
    pk_url_kwarg = 'pk'
    form_class = DeclineMessage

    """ page to accept/decline order """
    def get_context_data(self, **kwargs):
        context = super(AuthOrder, self).get_context_data(**kwargs)
        context['page_name'] = 'Authorise order for {0}'.format(
            self.object.company_name)
        context['auth'] = self.kwargs['pk']
        context['actioned'] = auth_complete(
            self.kwargs['pk'],
            self.kwargs['auth'])
        context['form'] = DeclineMessage(initial={'post': self.object})
        return context

    """ process form post data """
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.kwargs['pk']
        auth = self.kwargs['auth']
        action = request.POST.get('action')
        if action == 'accept':
            accept_auth(pk, auth)
        else:
            message = request.POST.get('decline_message')
            decline_auth(pk, auth, message)

        return HttpResponseRedirect(self.request.path_info)


@method_decorator(staff_member_required, name='dispatch')
class UserManagement(ListView):
    model = User
    template_name = 'admin/user_management.html'

    def get_context_data(self, **kwargs):
        context = super(UserManagement, self).get_context_data(**kwargs)
        context['page_name'] = 'User Management'
        return context

@method_decorator(staff_member_required, name='dispatch')
class EditUser(UpdateView):
    model = User
    fields = [
        'first_name',
        'last_name',
        'username',
        'is_active',
        'groups',
        'is_staff'
        ]
    template_name_suffix = '_update_form'
