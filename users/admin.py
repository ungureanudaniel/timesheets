from django.contrib import admin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved']
    list_filter = ['username', 'is_approved']
    search_fields = ['username', 'is_approved']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', ]
    list_filter = ['user',]
    search_fields = ['user',]