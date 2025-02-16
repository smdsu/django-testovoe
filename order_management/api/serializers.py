from rest_framework import serializers
from ..models import Item, Order, OrderItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'price')

class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )
    
    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'item_id', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id', 
            'table_number', 
            'status', 
            'total_price', 
            'created_at', 
            'updated_at', 
            'order_items'
        )
