from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DeleteView, DetailView
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from django.urls import reverse_lazy

from .models import Order
from .forms import OrderAddForm, OrderItemFormSet


status_mapping = {
    'pending': Order.Status.PENDING,
    'ready': Order.Status.READY,
    'paid': Order.Status.PAID,
}

def is_cafe_staff(user):
    return user.is_authenticated and user.groups.filter(name="cafe_staff").exists()

class CafeStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name="cafe_staff").exists()

class OrderDeleteView(LoginRequiredMixin, CafeStaffRequiredMixin, DeleteView):
    model = Order
    template_name = 'order_management/order/confirm_delete.html'
    success_url = reverse_lazy('orders:order_list')

class OrderDetailView(LoginRequiredMixin, CafeStaffRequiredMixin, DetailView):
    model = Order
    template_name = 'order_management/order/detail.html'


@login_required
@user_passes_test(is_cafe_staff)
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


@login_required
@user_passes_test(is_cafe_staff)
def edit_order(request, pk):
    order = get_object_or_404(Order, id=pk)

    if request.method == 'POST':
        form = OrderAddForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(order.get_abs_url())

    else:
        form = OrderAddForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    context = {
        'form': form,
        'formset': formset,
        'order': order,
    }
    return render(request, 'order_management/order/add.html', context)


@login_required
@user_passes_test(is_cafe_staff)
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

@login_required
@user_passes_test(is_cafe_staff)
@require_POST
def update_status(request, pk):
    order = get_object_or_404(Order, id=pk)
    new_status = request.POST.get('status')

    valid_statuses = [choice[0] for choice in Order.Status.choices]

    if new_status in valid_statuses:
        order.status = new_status
        order.save()

    return redirect(order.get_abs_url())
