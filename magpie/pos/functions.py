from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

import pdb

from .config import GROUP_MANAGERS
from .config import MD_EMAIL

from .models import Item
from .models import Order


def order_saved(pk):
    """ get order information """
    order_items = Item.objects.all().filter(order__pk=pk)
    order = Order.objects.get(pk=pk)

    """ get user object that placed the order and their group """
    user = order.ordered_by
    groups = user.groups.all()
    user_group = ""
    for group in groups:
        user_group = group
    # print(user_group)
    email_dict = GROUP_MANAGERS
    manager_email = email_dict.get(str(user_group))
    # print(manager_email)

    send_email(manager_email, 'tm', pk)

    """ get total value of order """
    grand_total = 0
    for item in order_items:
        grand_total = grand_total + item.item_price * item.item_qty
    # print(grand_total)
    if grand_total > 2000:
        send_email(MD_EMAIL, 'md', pk)


def order_variables(items):
    """ calculate and return order value """
    order_total = 0
    items = items
    for item in items:
        cd = item.cleaned_data
        _price = cd.get('item_price')
        _qty = cd.get('item_qty')
        order_total = order_total + _price * _qty

    auth_option = auth_required(order_total)
    order = {
        'order_total': order_total,
        'auth_option': auth_option,
    }

    return order


def auth_required(order_value):
    if order_value < 200:
        """ no PO required """
        auth_option = 'none'
    elif order_value < 2000:
        """ manager auth required """
        auth_option = 0
    else:
        """ manager and MD auth required """
        auth_option = 1
    return auth_option


def send_email(email, type, pk):
    type = type
    subject = 'Auth Order'
    message = 'Email Message'
    from_email = 'my@email.com'
    to_email = email

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False,
    )
