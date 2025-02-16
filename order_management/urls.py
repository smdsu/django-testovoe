from django.urls import path, include

from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.orders_list, name='order_list'),
    path('<int:pk>/detail', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update_status', views.update_status, name='update_status'),
    path('<int:pk>/update_order', views.edit_order, name='edit_order'),
    path('<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
    path('add/', views.create_order, name='order_add'),
    path('total_revenue/', views.get_revenue, name='total_revenue'),
    path('', include('order_management.api.urls', namespace='orders')),
]