# Django
from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms import Textarea
from django.forms.widgets import TextInput

# Local
from .models import Order
from .models import Item

from accounts.models import User


class DateInput(TextInput):
    """ custom method for date field """

    input_type = "date"


class OrderForm(forms.ModelForm):
    """ form for order model """

    class Meta:
        model = Order
        fields = [
            "company_name",
            "address_one",
            "address_two",
            "city",
            "county",
            "post_code",
            "telephone",
            "reason",
            "delivery_date",
        ]
        widgets = {
            "reason": Textarea(attrs={"cols": 80, "rows": 10}),
            "delivery_date": DateInput(attrs={"class": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["company_name"].widget.attrs["class"] = "form-control"
        self.fields["address_one"].widget.attrs["class"] = "form-control"
        self.fields["address_two"].widget.attrs["class"] = "form-control"
        self.fields["city"].widget.attrs["class"] = "form-control"
        self.fields["county"].widget.attrs["class"] = "form-control"
        self.fields["post_code"].widget.attrs["class"] = "form-control"
        self.fields["telephone"].widget.attrs["class"] = "form-control"
        self.fields["reason"].widget.attrs["class"] = "form-control"


class ItemForm(forms.ModelForm):
    """ form for item model """

    class Meta:
        model = Item
        fields = ["item_name", "item_qty", "item_price"]


class DeclineMessage(forms.Form):
    """ decline message form """

    decline_message = forms.CharField(widget=forms.Textarea)


""" item formset """
ItemFormSet = formset_factory(ItemForm, extra=1)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "department",
            "is_active",
            "is_manager",
        ]
        labels = {
            "first_name": "Forename",
            "last_name": "Surname",
            "is_active": "Active User",
            "is_staff": "Is Manager",
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["readonly"] = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["username"].required = True
        self.fields["email"].required = True
        self.fields["department"].required = True


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_active",
            "department",
            "is_manager",
        ]

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["readonly"] = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["username"].required = True
        self.fields["email"].required = True
        self.fields["department"].required = True
