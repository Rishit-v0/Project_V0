from django.shortcuts import render
from .models import Product
from rest_framework import viewsets, filters, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import ProductSerializer, RegisterSerializer, UserProfileSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer   
    permission_classes = [permissions.AllowAny] # Allow anyone to register

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access their profile

    def get_object(self):
        return self.request.user # Return the currently authenticated user

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can manage products
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = [ 'price', 'created_at']

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)