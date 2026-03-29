from django.shortcuts import render
from .models import Product
from rest_framework import viewsets, filters, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import ProductSerializer, RegisterSerializer, UserProfileSerializer
from django.db import connection  # connection gives us access to the raw SQL execution and query logging   


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

class ProductStatsView(APIView):
    # IsAuthenticated — only logged in users can see stats
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access stats

    def get(self, request):
        # RAW SQL approach
        # connection.cursor() opens a database cursor
        # A cursor is like a pointer that lets you execute SQL and fetch results
        # Use raw SQL when:
        # 1. The query is too complex for ORM
        # 2. You need maximum performance
        # 3. You need database-specific features (window functions, CTEs etc.)

        with connection.cursor() as cursor:
            # %s is a placeholder — never use f-strings or string formatting
            # in SQL queries, always use parameterized queries like %s
            # This prevents SQL injection attacks
            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_products,
                    AVG(price) AS avg_price,
                    MAX(price) AS max_price,
                    MIN(price) AS min_price,
                    SUM(stock) AS total_stock
                FROM api_product
                WHERE created_by_id = %s AND is_active = TRUE
            """, [request.user.id])  # request.user.id replaces %s safely
            
            # fetchone() returns the first row as a tuple
            # fetchall() returns all rows as a list of tuples
            row = cursor.fetchone()


        from django.db.models import Count, Avg, Max, Min, Sum
        # ORM approach — more readable and maintainable, but may be less performant for complex queries
        orm_stats = Product.objects.filter(created_by=request.user, is_active=True).aggregate(
            # aggregate() computes a single value across all matching rows
            # Count, Avg, Max, Min, Sum are aggregation functions that take a field name and return the computed value
            total_products=Count('id'),
            avg_price=Avg('price'),
            max_price=Max('price'),
            min_price=Min('price'),
            total_stock=Sum('stock')
        )


        return Response({'raw_sql_results': {
            'total_products': row[0],
            'average_price': float(row[1]) if row[1] is not None else 0.0,
            'max_price': float(row[2]) if row[2] is not None else 0.0,
            'min_price': float(row[3]) if row[3] is not None else 0.0,
            'total_stock': row[4],
            # Both results should be identical — this proves ORM and raw SQL
            # produce the same output, just with different syntax
            }, 
            'orm_results': orm_stats
            })