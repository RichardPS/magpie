# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local
from .models import User


class AuthUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'department',
        'is_manager',
        'is_accounts_admin',
        'is_director',
        'last_login',
        'date_joined'
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Extras', {'fields': (
            'department',
            'is_manager',
            'is_director',
            'is_accounts_admin'
        )}),
    )
    list_filter = (
        'department',
        'is_manager',
        'is_accounts_admin',
        'is_director'
    ) + UserAdmin.list_filter


admin.site.register(User, AuthUserAdmin)
