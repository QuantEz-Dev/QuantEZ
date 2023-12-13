from django import forms
from .models import Signup

# stock form
class StockHistoryForm(forms.ModelForm):

    class Meta:
        model = Signup
        fields = ('Ticker', 'start_date', 'end_date', 'strategy', 'initial_cash','fast_period',
                  'slow_period', 'rsi_period', 'rsi_overbought', 'rsi_oversold', 'stop_loss', 'devfactor',)
    def __init__(self, *args, **kwargs):
        super(StockHistoryForm, self).__init__(*args, **kwargs)# 기본값 설정
        self.fields['Ticker'].initial = 'MSFT'
        self.fields['start_date'].initial = '2023-01-01'
        self.fields['end_date'].initial = '2023-06-30'
        self.fields['strategy'].initial = 'GC'
        self.fields['initial_cash'].initial = 1000000
        self.fields['fast_period'].initial = 20
        self.fields['slow_period'].initial = 30
        self.fields['rsi_period'].initial = 2
        self.fields['rsi_overbought'].initial = 2
        self.fields['rsi_oversold'].initial = 1
        self.fields['stop_loss'].initial = 0.02
        self.fields['devfactor'].initial = 2 #bollingerbands

