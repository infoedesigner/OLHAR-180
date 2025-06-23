from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from nxt.media.views import api as media_api_views
from nxt.crawlers.views import api as crawlers_api_views
from nxt.clients.views import api as clients_api_views
from nxt.core.views import api as core_api_views


router = DefaultRouter()
router.register('execution', crawlers_api_views.ExecutionViewSet, basename='execution')
router.register('source', media_api_views.SourceViewSet, basename='source')
router.register('media', media_api_views.MediaViewSet, basename='media')
router.register('media-content', media_api_views.MediaContentViewSet, basename='media-content')
router.register('editorial', media_api_views.EditorialViewSet, basename='editorial')
router.register('category', clients_api_views.CategoryViewSet, basename='category')
router.register('city', core_api_views.CityViewSet, basename='city')


urlpatterns = [
    path('', include('nxt.core.urls', namespace='core')),
    path('seguranca/', include('nxt.security.urls', namespace='security')),
    path('clientes/', include('nxt.clients.urls', namespace='clients')),
    path('veiculos/', include('nxt.media.urls', namespace='media')),
    path('empresas/', include('nxt.companies.urls', namespace='companies')),
    path('newsletter/', include('nxt.newsletter.urls', namespace='newsletter')),
    path('notificacoes/', include('nxt.notifications.urls', namespace='notifications')),
    path('api/', include((router.urls, 'api'), namespace='api')),
    path('api-auth/', include('rest_framework.urls')),
    path('django-admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('500/', TemplateView.as_view(template_name='500.html')),
        path('404/', TemplateView.as_view(template_name='404.html')),
        path('403/', TemplateView.as_view(template_name='403.html')),
        # path('__debug__/', include(debug_toolbar.urls)),
    ]
