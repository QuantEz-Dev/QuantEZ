from django.contrib import admin
from .models import Asset

class AssetAdmin(admin.ModelAdmin):
    search_fields = ['subject']

# 관리자 모드에서 모델 관리 가능하게(검색해서)
admin.site.register(Asset, AssetAdmin)

