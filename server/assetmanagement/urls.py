# assetmanagement/urls.py
from django.urls import path
from . import views
from django.urls import path, include

app_name = 'assetmanagement'

urlpatterns = [
    path('', views.index, name='index'),
    path('asset/create/', views.asset_create, name='asset_create'),
    path('asset/modify/<int:asset_id>/', views.asset_modify, name='asset_modify'),
    path('asset/delete/<int:asset_id>/', views.asset_delete, name='asset_delete'),
    path('api/', include('rest_framework.urls')),

]
