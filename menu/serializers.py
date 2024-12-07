from rest_framework import serializers
from .models import MenuCategory, MenuItem, Order, OrderItem

# Serializer for MenuCategory
class MenuCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'items'] 

    def get_items(self, obj):
        # Fetch related items for the category
        items = MenuItem.objects.filter(category=obj)
        return MenuItemSerializer(items, many=True).data

# Serializer for MenuItem
# class MenuItemSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=MenuCategory.objects.all())
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)  # Ensure it's serialized as a number

#     class Meta:
#         model = MenuItem
#         fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MenuCategory.objects.all())
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)  # Ensure price is required

    class Meta:
        model = MenuItem
        fields = '__all__'

    def get_price(self, obj):
        # Ensure price is serialized as a float
        return float(obj.price)
        

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

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.email = validated_data.get('email', instance.email)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Clear existing items and recreate them
        instance.items.all().delete()
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)

        return instance
