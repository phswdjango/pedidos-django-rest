from django import forms
from phsw_site.orders.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ()
