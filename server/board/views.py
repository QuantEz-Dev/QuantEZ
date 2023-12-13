from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from .serializers import QuestionSerializer, AnswerSerializer

@api_view(['GET'])
def index(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    serializer = QuestionSerializer(page_obj, many=True)
    return Response({'question_list': serializer.data})

@api_view(['GET'])
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionSerializer(question)
    return Response({'question': serializer.data})

@api_view(['GET'])
# @login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            serializer = QuestionSerializer(question)
            return Response({'question': serializer.data})
    else:
        form = QuestionForm()
    return Response({'form': form})

@api_view(['GET'])
# @login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            serializer = AnswerSerializer(answer)
            return Response({'answer': serializer.data})
    else:
        form = AnswerForm()
    return Response({'question': question, 'form': form})

@api_view(['GET'])
# @login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return Response({'error': '수정권한이 없습니다'})
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            serializer = QuestionSerializer(question)
            return Response({'question': serializer.data})
    else:
        form = QuestionForm(instance=question)
    return Response({'form': form})

@api_view(['GET'])
# @login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return Response({'error': '삭제권한이 없습니다'})
    question.delete()
    return Response({'result': '삭제되었습니다'})

@api_view(['GET'])
# @login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return Response({'error': '수정권한이 없습니다'})
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            serializer = AnswerSerializer(answer)
            return Response({'answer': serializer.data})
    else:
        form = AnswerForm(instance=answer)
    return Response({'form': form})

@api_view(['GET'])
# @login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
        return Response({'error': '삭제권한이 없습니다'})
    answer.delete()
    return Response({'result': '삭제되었습니다'})
