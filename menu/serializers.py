from rest_framework import serializers
from django.core.mail import send_mail
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
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)  
    description = serializers.CharField(required=False, allow_blank=True)
    is_available = serializers.BooleanField(default=True)  

    class Meta:
        model = MenuItem
        fields = '__all__'

    def get_price(self, obj):
        # Ensure price is serialized as a float
        return float(obj.price)
    
    def update(self, instance, validated_data):
        # Update only the fields provided in the request
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        

# Serializer for OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']

# Serializer for Order
# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = '__all__'

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         order = Order.objects.create(**validated_data)
#         for item_data in items_data:
#             OrderItem.objects.create(order=order, **item_data)
#         return order

#     def update(self, instance, validated_data):
#         items_data = validated_data.pop('items', [])
#         instance.customer_name = validated_data.get('customer_name', instance.customer_name)
#         instance.email = validated_data.get('email', instance.email)
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()

#         # Clear existing items and recreate them
#         instance.items.all().delete()
#         for item_data in items_data:
#             OrderItem.objects.create(order=instance, **item_data)

#         return instance

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
        old_status = instance.status  # Track the old status before update

        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.email = validated_data.get('email', instance.email)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Re-create the order items
        instance.items.all().delete()
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)

        # Check if the status has changed
        if instance.status != old_status:
            subject = None
            message = None

            # Determine the subject and message based on the new status
            if instance.status == 'Accepted':
                subject = 'Your order has been accepted!'
                message = f"Hello {instance.customer_name},\n\nYour order #{instance.id} has been accepted and is being prepared."
            elif instance.status == 'Declined':
                subject = 'Your order has been declined'
                message = f"Hello {instance.customer_name},\n\nWe are sorry, but your order #{instance.id} has been declined."
            elif instance.status == 'Ready for Pick Up':
                subject = 'Your order is ready for pick up!'
                message = f"Hello {instance.customer_name},\n\nYour order #{instance.id} is now ready for pick up!"

            # If we have a subject, message, and a customer email, send the email
            if subject and message and instance.email:
                try:
                    send_mail(
                        subject,
                        message,
                        'your_email@gmail.com',  # matches DEFAULT_FROM_EMAIL
                        [instance.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Error sending email:", e)

        return instance