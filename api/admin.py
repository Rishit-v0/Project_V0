from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Product


# Register your models here.
# UserAdmin is Django's built-in admin configuration for user models.
# It handles password hashing, permission groups, and the admin UI
# for users correctly. If you just used admin.register(User) without
# UserAdmin, passwords would show as plain text and break.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Columns shown in the user list view in admin panel
    list_display = ['email', 'username', 'is_staff','is_active','created_at']

    # Add 'bio' to the user detail/edit form in admin
    # fieldsets controls the layout of the edit page for a user in the admin interface.
    fieldsets = UserAdmin.fieldsets + ( 
        ('Additional Info', {'fields': ('bio',)}),
    )
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'price', 'stock', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']