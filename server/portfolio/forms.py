# portfolio/forms.py
from django import forms
from portfolio.models import Portfolio, Reply

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = '__all__'
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
            'fast': '작은 이동평균선',
            'slow' : '큰 이동평균선',
            'crossover': '크로스오버',
            'size':'회당 매수,매도 크기',
            'charge': '수수료율',
            'stockcode':'주가코드',
            'start_date': '시작일',
            'end_date': '종료일',
            'create_date':'생성일',
            'modify_date':'수정일',
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        labels = {
            'content': '답변내용',
        }