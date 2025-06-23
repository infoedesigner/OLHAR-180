from django.urls import path

from nxt.companies import views


app_name = 'companies'


urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('nova/', views.company_create, name='company_create'),
    path('<int:pk>/atualizar/', views.company_update, name='company_update'),
    path('<int:company>/documentos/', views.document_list, name='document_list'),
    path('<int:company>/documentos/novo/', views.document_create, name='document_create'),
    path('<int:company>/documentos/<int:pk>/atualizar/', views.document_update, name='document_update'),
]
