from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.orders_list, name='order_list'),
    path('<int:pk>/detail', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
    path('add/', views.create_order, name='order_add'),
]