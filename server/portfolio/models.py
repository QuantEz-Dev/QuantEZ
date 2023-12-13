from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Portfolio(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    fast = models.IntegerField() # 이동평균선 작은
    slow = models.IntegerField() # 이동평균선 큰
    crossover = models.IntegerField() # 크로스 오버 시그널
    size = models.IntegerField() # 회당 매수, 매도 양
    charge = models.FloatField() # 수수료율
    stockcode = models.CharField(max_length=50) # 주가코드
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
