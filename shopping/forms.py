from django import forms


class ShoppingForm(forms.Form):
    item = forms.CharField(max_length=100)
