from rest_framework.routers import DefaultRouter
from .views import MenuCategoryViewSet, MenuItemViewSet, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'categories', MenuCategoryViewSet, basename='category')
router.register(r'items', MenuItemViewSet, basename='item')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = router.urls
