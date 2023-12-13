from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from common.forms import UserForm, UserChangeForm
from .forms import UserFormSerializer, UserChangeFormSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return Response({'detail': '회원가입이 완료되었습니다.', 'username': username})
    else:
        form = UserForm()
    return Response({'form': form})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return Response({'detail': '회원정보가 업데이트되었습니다.'})
    else:
        form = UserChangeForm(instance=request.user)
    context = {'form': form}
    return Response(context)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete(request):
    user = request.user
    user.delete()
    return Response({'detail': '회원 탈퇴가 완료되었습니다.'})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return Response({'detail': '비밀번호가 변경되었습니다.'})
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return Response(context)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password1')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return Response({'detail': '로그인이 성공적으로 완료되었습니다.', 'username': username})
    else:
        return Response({'detail': '아이디 또는 비밀번호가 일치하지 않습니다.'})