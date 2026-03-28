from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RegisterView, UserProfileView
from django.urls import path

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]+ router.urls