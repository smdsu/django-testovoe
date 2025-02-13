from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.orders_list, name='order_list'),
    path('<str:status>/', views.orders_list, name='order_status_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('add/', views.create_order, name='order_add'),
]