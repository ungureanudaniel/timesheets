from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved']
    list_filter = ['username', 'is_approved']
    search_fields = ['username', 'is_approved']