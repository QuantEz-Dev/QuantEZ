# QEZ_main/urls.py
from django.contrib import admin
from django.urls import path, include
#from board import views
from QuentEZ_main import views


urlpatterns = [
    # 관리자
    path('admin/', admin.site.urls),
    # 메인
    path('', views.home, name='home'),
    # 게시판
    path('board/', include('board.urls')),
    # 회원
    path('common/', include('common.urls')),
    # 포트폴리오
    path('portfolio/', include('portfolio.urls')),
    # 뉴스
    path('news/', include('news.urls')),
    # 백테스팅
    path('backtesting/', include('backtesting.urls')),
    # 자산관리
    path('assetmanagement/', include('assetmanagement.urls')),
    # api
    path('api/', include('rest_framework.urls')),
]
