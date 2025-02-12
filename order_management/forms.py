from django import forms
from django.forms.models import inlineformset_factory

from .models import Order, OrderItem


class OrderAddForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number']  # Тут заполняется только № столика, т.к. все остальные данные заполняются автоматически


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['item', 'quantity'],
    extra=1,
    can_delete=True
)