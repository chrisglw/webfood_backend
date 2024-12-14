from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import MenuCategory, MenuItem, Order, OrderItem
from .serializers import MenuCategorySerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer
from django.db.models import Sum, Count, F
from rest_framework.decorators import action
from datetime import timedelta
from django.utils.timezone import now

class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ['category']

    def create(self, request, *args, **kwargs):
        print("Incoming Request Data:", request.data)  # Debug log
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation Errors:", serializer.errors)  # Debug validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'], url_path='sales-report')
    def sales_report(self, request):
        # Filter orders by date range (e.g., last 30 days)
        last_30_days = now() - timedelta(days=30)
        orders = Order.objects.filter(created_at__gte=last_30_days)

        # Calculate total revenue
        total_revenue = orders.aggregate(total=Sum('total'))['total'] or 0  # Changed to 'total'

        # Calculate total orders
        total_orders = orders.count()

        # Get most popular items
        popular_items = (
            OrderItem.objects
            .filter(order__in=orders)
            .values(item_name=F('menu_item__name'))  # Adjust as per your model
            .annotate(quantity_sold=Sum('quantity'))
            .order_by('-quantity_sold')[:5]
        )

        # Return the sales data
        return Response({
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'popular_items': list(popular_items),
        })


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


