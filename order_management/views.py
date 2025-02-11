from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Order


class OrderListView(ListView):
    queryset = Order.objects.all()
    context_object_name = 'orders'
    paginate_by = 10
    template_name = 'order_management/order/list.html'
