from django.template import Library


register = Library()


@register.filter
def check_nxt_permission(user, code):
    if user is None:
        return False
    return user.profile == 'administrador' or user.nxt_permissions.filter(code=code).exists()
