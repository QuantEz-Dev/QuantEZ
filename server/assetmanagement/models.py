from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bond = models.IntegerField(null=True, blank=True)
    fund = models.IntegerField(null=True, blank=True) #펀드
    etf = models.IntegerField(null=True, blank=True) #ETF
    etc = models.IntegerField(null=True, blank=True) #기타
    create_date = models.DateTimeField(null=True, blank=True) #생성일
    modify_date = models.DateTimeField(null=True, blank=True) #수정일

    # id대신 subject로 표시되게
    def __str__(self):
        return self.subject