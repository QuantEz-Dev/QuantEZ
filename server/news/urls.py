# news/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    # 아래 주소는 다 의미 없음
    path('top3/', views.top3, name='top3'),
    path('top7/', views.top7, name='top7'),
    path('top10/', views.top10, name='top10'),
    path('pop/', views.pop, name='pop'),
    path('kospitop50/', views.kospitop50, name='kospitop10'),
    path('api/', include('rest_framework.urls')),
]