# Django
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

# local
from accounts.models import User

from .config import AUTH_RESPONSE
from .config import MD_EMAIL
from .config import STATUS_OPTIONS

from .models import Item
from .models import Order


def order_saved(pk):
    """ process raised order """
    """ get order information """
    order_items = Item.objects.all().filter(order__pk=pk)
    order = Order.objects.get(pk=pk)

    """ get user object that placed the order and their department """
    user = order.ordered_by
    department = user.department

    department_manager = User.objects.get(department=department, is_manager=True)

    department_manager_email = department_manager.email
    send_email(department_manager_email, "dm", pk, order, order_items)

    """ get total value of order """
    if get_order_total(order_items) > 2000:
        send_email(MD_EMAIL, "md", pk, order, order_items)


def check_order_value(items):
    order_total = 0
    for item in items:
        cd = item.cleaned_data
        _price = cd.get("item_price")
        _qty = cd.get("item_qty")
        order_total = order_total + _price * _qty
    if order_total >= 200:
        return True
    else:
        return False


def get_order_total(items):
    order_total = 0
    for item in items:
        cd = item.cleaned_data
        _price = cd.get("item_price")
        _qty = cd.get("item_qty")
        order_total = order_total + _price * _qty
    return order_total


def get_auth_required(items):
    """ get total value of order """
    order_value = get_order_total(items)
    """ get authorisation required """
    if order_value < 200:
        """ no PO required """
        auth_option = "none"
    elif order_value < 2000:
        """ manager auth required """
        auth_option = 0
    else:
        """ manager and MD auth required """
        auth_option = 1
    return auth_option


def send_email(email, auth, pk, order, order_items):
    """ get email templates """
    msg_plain = render_to_string(
        "pos_email.txt", {"auth": auth, "pk": pk, "order": order, "items": order_items}
    )
    msg_html = render_to_string(
        "pos_email.html", {"auth": auth, "pk": pk, "order": order, "items": order_items}
    )

    """ send email to recipient to accept of decline """
    subject = "Authorise {0} Order for {1}".format(
        order.company_name, order.ordered_by.get_full_name
    )
    from_email = "no-reply@primarysite.net"
    to_email = email

    send_mail(subject, msg_plain, from_email, [to_email], html_message=msg_html)


def auth_complete(pk, auth):
    complete = False
    order = get_object_or_404(Order, pk=pk)
    current_dm_auth = order.dm_auth
    current_md_auth = order.md_auth
    if auth == "dm":
        if current_dm_auth == "accepted" or current_dm_auth == "declined":
            complete = True
    else:
        if current_md_auth == "accepted" or current_md_auth == "declined":
            complete = True
    return complete


def accept_auth(pk, auth):
    """ process order accepted request """
    order = get_object_or_404(Order, pk=pk)
    """ set auth for DM/MD to accept """
    if auth == "dm":
        """ set dm auth to accepted """
        order.dm_auth = AUTH_RESPONSE[1][0]
    else:
        """ set md auth to accepted """
        order.md_auth = AUTH_RESPONSE[1][0]

    """ change order status upon accepted """
    if order.auth_required == "dm" and order.dm_auth == AUTH_RESPONSE[1][0]:
        """ set order status to authorised """
        order.order_status = STATUS_OPTIONS[1][0]
    elif order.auth_required == "dmmd":
        """ check auth for dm and md and set order status """
        """ do not change order status if already rejected """
        if (
            order.dm_auth == AUTH_RESPONSE[1][0]
            and order.md_auth == AUTH_RESPONSE[1][0]
        ):
            order.order_status = STATUS_OPTIONS[1][0]

    order.save()
    return


def decline_auth(pk, auth, message):
    """ set order status to declined and add decline message """
    order = get_object_or_404(Order, pk=pk)
    if auth == "dm":
        order.dm_auth = AUTH_RESPONSE[2][0]
        order.decline_message = order.decline_message + " -dm- " + message
        order.order_status = STATUS_OPTIONS[2][0]
    else:
        order.md_auth = AUTH_RESPONSE[2][0]
        order.decline_message = order.decline_message + " -md- " + message
        order.order_status = STATUS_OPTIONS[2][0]

    order.save()
    return
