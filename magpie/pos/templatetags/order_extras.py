from django import template

register = template.Library()


@register.simple_tag
def get_total(item_set):
    total = 0
    # pdb.set_trace()
    for item in item_set:
        total = total + item.item_price * item.item_qty

    return total
