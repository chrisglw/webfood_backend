from django.db import models

class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True) 
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUSES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('ReadyForPickUp', 'Ready for Pick Up'),
        ('Completed', 'Completed'),
    ]

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUSES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
class Order(models.Model):
    STATUSES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('ReadyForPickUp', 'Ready for Pick Up'),
        ('Completed', 'Completed'),
    ]

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUSES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add this field

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order #{self.order.id})"
