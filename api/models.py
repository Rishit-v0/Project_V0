from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='products'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            # Single column index — speeds up searching products by name
            # db_index=True on the field itself does the same for single columns
            # but Meta indexes gives you more control and composite index support
            models.Index(fields=['name'], name='idx_name'),
            
            # Single column index — we almost always filter is_active=True
            models.Index(fields=['is_active'], name='idx_product_is_active'),
            
            # Composite index — covers our most common query pattern:
            # Product.objects.filter(is_active=True, created_by=user)
            # The order here matches the order you filter in get_queryset()
            models.Index(fields=['is_active', 'created_by'], name='idx_product_active_created_by'),
        ]