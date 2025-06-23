from django.urls import path

from nxt.media import views
from nxt.media.views import news, editorial, newspaper


app_name = 'media'


urlpatterns = [
    # source
    path('', views.source_list, name='source_list'),
    path('novo/', views.source_create, name='source_create'),
    path('<int:pk>/atualizar/', views.source_update, name='source_update'),
    path('<int:pk>/ativar/', views.source_activate, name='source_activate'),
    path('<int:pk>/desativar/', views.source_deactivate, name='source_deactivate'),
    # news
    path('notícias/', news.news_list, name='news_list'),
    path('notícias/nova/', news.news_create, name='news_create'),
    path('notícias/<int:pk>/atualizar/', news.news_update, name='news_update'),
    path('notícias/buscar-categoria-por-palavras/', news.search_category, name='search_category_by_words'),
    # editorial
    path('editorias/<int:pk>/', editorial.editorial_list, name='editorial_list'),
    path('editorias/<int:pk>/novo/', editorial.editorial_create, name='editorial_create'),
    path('editorias/<int:pk>/atualizar/', editorial.editorial_update, name='editorial_update'),
    # newspaper
    path('impressos/', newspaper.newspaper_list, name='newspaper_list'),
    path('impressos/novo/', newspaper.newspaper_create, name='newspaper_create'),
    path('impressos/<int:pk>/atualizar/', newspaper.newspaper_update, name='newspaper_update'),
    path(
        'impressos/verificar-veiculo/', newspaper.check_newspaper_source, name='check_newspaper_source'
    ),
]
