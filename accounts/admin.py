from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'username', 'is_active', 'is_staff', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)
