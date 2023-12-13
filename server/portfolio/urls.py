# portfolio/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

app_name = 'portfolio'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:portfolio_id>/', views.detail, name='detail'),
    path('portfolio/create/', views.portfolio_create, name='portfolio_create'),
    path('reply/create/<int:portfolio_id>/', views.reply_create, name='reply_create'),
    path('portfolio/modify/<int:portfolio_id>/', views.portfolio_modify, name='portfolio_modify'),
    path('portfolio/delete/<int:portfolio_id>/', views.portfolio_delete, name='portfolio_delete'),
    path('reply/modify/<int:reply_id>/', views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:reply_id>/', views.reply_delete, name='reply_delete'),
    # api
    path('api/', include('rest_framework.urls')),
]