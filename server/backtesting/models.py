from django.db import models
from django.contrib.auth.models import User

class Signup(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    Ticker = models.CharField(max_length=5, default = 'META') # 검색창에 기본 META
    strategies = [ # 왼쪽 디비 저장 - 오른쪽 사용자 표시 # 목록 리스트
        ('GC', "GoldenCross"), # golden cross
        ("ATR", "ATR"), # atrlimitorder
        ("RSI", "RSI"), # rsi
        ("BB", "Bollingerbands"), # bollingerbands
        ("SMA", "Sma"), # smacross
    ]

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    strategy = models.CharField(max_length=100,choices=strategies,default='GC') ## 그냥 default
    initial_cash = models.IntegerField(null=True, blank=True)
    fast_period = models.IntegerField(null=True, blank=True)
    slow_period = models.IntegerField(null=True, blank=True)
    rsi_period = models.IntegerField(null=True, blank=True)
    rsi_overbought = models.IntegerField(null=True, blank=True)
    rsi_oversold = models.IntegerField(null=True, blank=True)
    stop_loss = models.FloatField(null=True, blank=True)
    devfactor = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author