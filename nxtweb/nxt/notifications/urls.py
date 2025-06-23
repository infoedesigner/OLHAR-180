from django.urls import path

from nxt.notifications.views import notification_model


app_name = 'notifications'


urlpatterns = [
    path('modelos/', notification_model.notification_model_list, name='notification_model_list'),
    path('modelos/novo/', notification_model.notification_model_create, name='notification_model_create'),
    path(
        'modelos/<int:pk>/atualizar', notification_model.notification_model_update,
        name='notification_model_update'
    ),
]
