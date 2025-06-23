from django.urls import path
from django.contrib.auth.views import LogoutView

from nxt.security.views import base, reset_password


app_name = 'security'


urlpatterns = [
    path('usuarios/', base.user_list, name='user_list'),
    path('usuarios/novo/', base.user_create, name='user_create'),
    path('usuarios/<int:pk>/atualizar/', base.user_update, name='user_update'),
    path('usuarios/clientes/<int:pk>/', base.client_user_list, name='client_user_list'),
    path('usuarios/clientes/<int:pk>/novo/', base.client_user_create, name='client_user_create'),
    path(
        'usuarios/clientes/<int:pk>/<int:client>/atualizar/', base.client_user_update,
        name='client_user_update'
    ),
    path('alterar-dados/', base.update_me, name='update_me'),
    path('alterar-senha/', base.password_change, name='password_change'),
    path('alterar-empresa/', base.user_company_update, name='user_company_update'),
    path('entrar/', base.ClientLoginView.as_view(template_name='security/login.html'), name='login'),
    path('sair/', LogoutView.as_view(next_page='security:login'), name='logout'),
    # reset password
    path('esquecia-a-senha/', reset_password.reset_password, name='reset_password'),
    path('esquecia-a-senha/<int:pk>/', reset_password.check_reset_password, name='check_reset_password'),
    path(
        'esquecia-a-senha/<int:pk>/<int:code>/', reset_password.set_password, name='set_password'
    ),
]
