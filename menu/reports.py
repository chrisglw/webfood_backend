from django.db.models import Sum, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order

@api_view(['GET'])
def total_orders(request):
    total = Order.objects.count()
    return Response({'total_orders': total})

@api_view(['GET'])
def total_revenue(request):
    revenue = Order.objects.filter(status='Completed').aggregate(Sum('total'))['total__sum'] or 0
    return Response({'total_revenue': revenue})

@api_view(['GET'])
def order_trends(request):
    trends = Order.objects.values('created_at__date').annotate(
        order_count=Count('id')
    ).order_by('created_at__date')
    return Response({'trends': trends})
