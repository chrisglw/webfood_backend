from django.core.management.base import BaseCommand
from menu.models import Order, OrderItem
from django.db import connection

class Command(BaseCommand):
    help = 'Delete all orders and reset primary key sequence'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting all orders and order items...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()

        self.stdout.write('Resetting primary key sequence...')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='menu_order';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='menu_orderitem';")

        self.stdout.write(self.style.SUCCESS('Successfully reset orders and order items!'))

# Run python manage.py reset_orders   