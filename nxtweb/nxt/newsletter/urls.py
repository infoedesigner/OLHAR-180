from django.urls import path

from nxt.newsletter import views

app_name = 'newsletter'


urlpatterns = [

    path('contatos/<int:pk>/', views.contact_list, name='contact_list'),
    path(
        'contatos/<int:pk>/novo/', views.contact_create, 
        name='contact_create'
    ),
    path(
        'contatos/<int:pk>/<int:contact>/atualizar/', views.contact_update, 
        name='contact_update'
    ),

    path('contatos/<int:pk>/importar/', views.contact_import, name='contact_import'),


############----NEWSLETTER-----####################

    path(
        'newsletter/<int:pk>/', views.newsletter_list, name='newsletter_list'
    ),

    path(
        'newsletter/<int:pk>/nova/', views.newsletter_create, name='newsletter_create'
    ),

    path(
        'newsletter/<int:pk>/<int:newsletter>/atualizar/', views.newsletter_update,
        name='newsletter_update'
    ),

    path(
        'newsletter/<int:pk>/<int:newsletter>/atualizar-layout/', views.newsletter_layout_update,
        name='newsletter_layout_update'
    ),
#PREVIEW->
     path('newsletter/<int:pk>/<int:newsletter>/preview/', views.newsletter_preview, name='newsletter_preview'),
]
