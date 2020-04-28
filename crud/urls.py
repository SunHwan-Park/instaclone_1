"""crud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from articles import views as articles_views


urlpatterns = [
    path('', articles_views.index, name='root'),
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
    path('<str:username>/', accounts_views.profile, name='profile'),
    # 순서가 매우 중요..! 앞에서부터 찾아보고 마지막에 걸리게
    # 그리고 admin, articles, accouunts 는 가입할 수 없게 만들어야 함
    path('<str:username>/follow/', accounts_views.follow, name='follow'),
]
