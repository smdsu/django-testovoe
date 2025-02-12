from django.contrib import admin
from .models import Order, Item, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'table_number', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    fields = ('table_number', 'status')
    inlines = [OrderItemInline,]
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']


