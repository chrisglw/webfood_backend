from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
from .models import OrderItem, Order

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    Update the total field in the Order model whenever an OrderItem is created, updated, or deleted.
    """
    order = instance.order  # Get the associated order
    total = order.items.aggregate(
        total=Sum(F('quantity') * F('menu_item__price'))
    )['total'] or 0

    order.total = total
    order.save()
