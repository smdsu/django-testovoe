from django.contrib import admin
from .models import Order, OrderItems


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'table_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'price', 'quantity']
    list_filter = ['order']
    search_fields = ['name']
    raw_id_fields = ['order']
    show_facets = admin.ShowFacets.ALWAYS
