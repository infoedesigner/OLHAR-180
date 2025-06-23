from rest_framework.routers import DefaultRouter

from nxt.crawlers import views


app_name = 'crawlers'

router = DefaultRouter()
router.register('execution', views.ExecutionViewSet, basename='execution')

urlpatterns = router.urls
