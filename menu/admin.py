from django.contrib import admin
from .models import MenuCategory, MenuItem, Order, OrderItem

admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
