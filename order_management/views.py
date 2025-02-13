from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, DetailView
from django.urls import reverse_lazy

from .models import Order
from .forms import OrderAddForm, OrderItemFormSet


status_mapping = {
    'pending': Order.Status.PENDING,
    'ready': Order.Status.READY,
    'paid': Order.Status.PAID,
}

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order_management/order/confirm_delete.html'
    success_url = reverse_lazy('orders:order_list')

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


def orders_list(request):
    orders_list = Order.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        if query.isdigit():
            orders_list = orders_list.filter(
                Q(table_number=query)
            )
        else:
            code = status_mapping.get(query.lower())
            if code:
                orders_list = orders_list.filter(
                    Q(status=code)
                )
            else:
                orders_list = orders_list.filter(
                    Q(status=query.upper())
                )
    
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
        'query': query,
    }

    return render(request, 'order_management/order/list.html', context)