from django.urls import path

from nxt.core.views import base

app_name = 'core'


urlpatterns = [
    path('', base.index, name='index'),
]
