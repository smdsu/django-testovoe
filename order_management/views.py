from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Order
from .forms import OrderAddForm, OrderItemFormSet


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


def orders_list(request, status: str = None):
    if status:
        orders_list = Order.objects.filter(status=status)
    else:
        orders_list = Order.objects.all()
    
    paginator = Paginator(orders_list, 5)
    page_number = request.GET.get('page', 1)

    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'orders': orders,
    }

    return render(request, 'order_management/order/list.html', context)