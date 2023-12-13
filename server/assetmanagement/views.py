from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Asset
from .forms import AssetForm
from .serializers import AssetSerializer

@api_view(['GET'])
# @login_required(login_url='common:login')
def index(request):
    assets = Asset.objects.filter(author_id=request.user)
    serializer = AssetSerializer(assets, many=True)
    return Response({'assets': serializer.data})

@api_view(['GET'])
# @login_required(login_url='common:login')
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.author = request.user
            asset.create_date = timezone.now()
            asset.save()
            serializer = AssetSerializer(asset)
            return Response({'detail': '자산이 생성되었습니다.', 'asset': serializer.data})
    else:
        form = AssetForm()
    context = {'form': form}
    return Response(context)

@api_view(['GET'])
# @login_required(login_url='common:login')
def asset_modify(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    if request.user != asset.author:
        messages.error(request, '수정권한이 없습니다')
        return Response({'detail': '수정 권한이 없습니다.'})
    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.modify_date = timezone.now()
            asset.save()
            serializer = AssetSerializer(asset)
            return Response({'detail': '자산이 수정되었습니다.', 'asset': serializer.data})
    else:
        form = AssetForm(instance=asset)
    context = {'form': form}
    return Response(context)

@api_view(['GET'])
@login_required(login_url='common:login')
def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    if request.user != asset.author:
        messages.error(request, '삭제권한이 없습니다')
        return Response({'detail': '삭제 권한이 없습니다.'})
    asset.delete()
    return Response({'detail': '자산이 삭제되었습니다.'})
