from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'shop_preference', 'saved_size', 'is_staff')
    list_filter = ('shop_preference', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Prime Athletes profile', {
            'fields': ('phone_number', 'shop_preference', 'saved_size', 'date_of_birth')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Prime Athletes profile', {
            'fields': ('email', 'shop_preference', 'saved_size')
        }),
    )
