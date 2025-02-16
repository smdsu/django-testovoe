from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ItemViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'items', ItemViewSet)
router.register(r'order-items', OrderItemViewSet)

app_name = 'orders_api'

urlpatterns = [
    path('api/', include(router.urls)),
]
