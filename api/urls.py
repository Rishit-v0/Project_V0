from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,ProductStatsView, RegisterView, UserProfileView
from django.urls import path

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('products/stats/', ProductStatsView.as_view(), name='product-stats'),
]+ router.urls