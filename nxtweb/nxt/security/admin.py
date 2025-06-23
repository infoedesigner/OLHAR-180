from django.contrib import admin

from nxt.security.models import User
from nxt.security.forms import UserAdminForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['name', 'email', 'is_active', 'created', 'modified']
    search_fields = ['name', 'email', 'phone']
    exclude = ['password']
    fieldsets = (
        (None, {
            'fields': (
                'email', 'name', 'phone'
            )
        }),
        ('Configurações', {
            'fields': (
                'company', 'client', 'created_by', 'expiration', 'companies'
            )
        }),
        (
            'Permissões', {
                'fields': ('profile', 'is_staff', 'is_active', 'is_superuser', 'new_password'),
        }),
    )
    form = UserAdminForm
    filter_horizontal = ('groups', 'user_permissions',)
