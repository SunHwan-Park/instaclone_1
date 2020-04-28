from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/like_root/', views.like_root, name='like_root'),
    path('<int:article_pk>/like_profile/', views.like_profile, name='like_profile'),
    path('<str:tag_name>/', views.tag_search, name='tag_search'),
]