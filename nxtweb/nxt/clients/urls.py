from django.urls import path

from nxt.clients.views import base, clipping

app_name = 'clients'


urlpatterns = [
    path('admin/', base.client_list, name='client_list'),
    path('admin/novo/', base.client_create, name='client_create'),
    path('admin/<int:pk>/atualizar/', base.client_update, name='client_update'),
    path('admin/<int:pk>/visualizar/', base.client_detail, name='client_detail'),
    path('admin/<int:pk>/contrato/', base.client_contract, name='client_contract'),
    path('admin/<int:pk>/principais/', base.client_main, name='client_main'),
    path('admin/<int:pk>/atendimento/', base.client_attendance, name='client_attendance'),
    path('admin/recortes/<int:pk>/apagar/', clipping.clipping_delete, name='clipping_delete'),
    path('<slug:slug>/recortes/', clipping.clipping_list, name='clipping_list'),
    path('<slug:slug>/recortes/pesquisa/', clipping.clipping_search, name='clipping_search'),
    path('<slug:slug>/recortes/<int:pk>/', clipping.clipping_detail, name='clipping_detail'),
    path('<slug:slug>/recortes/daily', clipping.clipping_daily, name='clipping_daily'),
]
