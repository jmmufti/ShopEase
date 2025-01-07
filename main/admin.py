from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Cart, CartItem

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except Exception as e:
            print(f"Error saving object: {e}")
            raise

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except Exception as e:
            print(f"Error deleting object: {e}")
            raise

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'price']
    search_fields = ['name', 'genre']
    list_filter = ['genre']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    list_filter = ['created_at']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)