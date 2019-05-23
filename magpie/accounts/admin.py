# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local
from .models import User


class AuthUserAdmin(UserAdmin):

    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_active'
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Extras', {'fields': ('department', 'is_manager', 'is_director')}),
    )


admin.site.register(User, AuthUserAdmin)
