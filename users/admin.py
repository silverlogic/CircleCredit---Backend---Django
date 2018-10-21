from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = [
        ('Advanced options', {
            'fields': ('first_name', 'last_name', 'email', 'stars', 'job', 'friends', 'paypal_token'),
        }),
    ]
    fieldsets.insert(0, UserAdmin.fieldsets[0])
    model = User


admin.site.register(User, CustomUserAdmin)
