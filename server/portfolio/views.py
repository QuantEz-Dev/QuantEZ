from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, Reply
from .forms import PortfolioForm, ReplyForm
from .serializers import PortfolioSerializer, ReplySerializer

@api_view(['GET'])
def index(request):
    page = request.GET.get('page', '1')
    portfolio_list = Portfolio.objects.order_by('-create_date')
    paginator = Paginator(portfolio_list, 10)
    page_obj = paginator.get_page(page)
    serializer = PortfolioSerializer(page_obj, many=True)
    return Response({'portfolio_list': serializer.data})

@api_view(['GET'])
def detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    serializer = PortfolioSerializer(portfolio)
    return Response({'portfolio': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.author = request.user
            portfolio.create_date = timezone.now()
            portfolio.save()
            serializer = PortfolioSerializer(portfolio)
            return Response({'detail': '포트폴리오가 생성되었습니다.', 'portfolio': serializer.data})
    else:
        form = PortfolioForm()
    context = {'form': form}
    return Response(context)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def portfolio_modify(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.user != portfolio.author:
        messages.error(request, '수정권한이 없습니다')
        return Response({'detail': '수정 권한이 없습니다.'})
    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.modify_date = timezone.now()
            portfolio.save()
            serializer = PortfolioSerializer(portfolio)
            return Response({'detail': '포트폴리오가 수정되었습니다.', 'portfolio': serializer.data})
    else:
        form = PortfolioForm(instance=portfolio)
    context = {'form': form}
    return Response(context)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def portfolio_delete(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.user != portfolio.author:
        messages.error(request, '삭제권한이 없습니다')
        return Response({'detail': '삭제 권한이 없습니다.'})
    portfolio.delete()
    return Response({'detail': '포트폴리오가 삭제되었습니다.'})

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def reply_create(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.create_date = timezone.now()
            reply.portfolio = portfolio
            reply.save()
            serializer = ReplySerializer(reply)
            return Response({'detail': '댓글이 생성되었습니다.', 'reply': serializer.data})
    else:
        form = ReplyForm()
    context = {'portfolio': portfolio, 'form': form}
    return Response(context)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def reply_modify(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user != reply.author:
        messages.error(request, '수정권한이 없습니다')
        return Response({'detail': '수정 권한이 없습니다.'})
    if request.method == "POST":
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.modify_date = timezone.now()
            reply.save()
            serializer = ReplySerializer(reply)
            return Response({'detail': '댓글이 수정되었습니다.', 'reply': serializer.data})
    else:
        form = ReplyForm(instance=reply)
    context = {'reply': reply, 'form': form}
    return Response(context)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def reply_delete(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user != reply.author:
        messages.error(request, '삭제권한이 없습니다')
        return Response({'detail': '삭제 권한이 없습니다.'})
    reply.delete()
    return Response({'detail': '댓글이 삭제되었습니다.'})
