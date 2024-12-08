from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MenuCategoryViewSet, MenuItemViewSet, OrderViewSet, OrderItemViewSet
from .reports import total_orders, total_revenue, order_trends

router = DefaultRouter()
router.register(r'categories', MenuCategoryViewSet, basename='category')
router.register(r'items', MenuItemViewSet, basename='item')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

report_urls = [
    path('reports/orders/total/', total_orders, name='total_orders'),
    path('reports/revenue/', total_revenue, name='total_revenue'),
    path('reports/orders/trends/', order_trends, name='order_trends'),
]

urlpatterns = router.urls + report_urls

