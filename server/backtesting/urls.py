# backtesting/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


app_name = 'backtesting'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include('rest_framework.urls')),
]
