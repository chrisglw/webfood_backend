from rest_framework import serializers
from .models import MenuCategory, MenuItem, Order, OrderItem

# Serializer for MenuCategory
class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'

# Serializer for MenuItem
class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MenuCategory.objects.all())

    class Meta:
        model = MenuItem
        fields = '__all__'

# Serializer for OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']

# Serializer for Order
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    


