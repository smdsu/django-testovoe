from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Order
from .forms import OrderAddForm, OrderItemFormSet


class OrderListView(ListView):
    queryset = Order.objects.all()
    context_object_name = 'orders'
    paginate_by = 10
    template_name = 'order_management/order/list.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_management/order/detail.html'


def create_order(request):
    if request.method == 'POST':
        form = OrderAddForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            order = form.save()

            formset.instance = order
            formset.save()

            return redirect(order.get_abs_url())
    else:
        form = OrderAddForm()
        formset = OrderItemFormSet()

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'order_management/order/add.html', context)
