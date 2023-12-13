import math
import yfinance as yf
import plotly
import plotly.express as px
import plotly.graph_objs as go
import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta
from .forms import StockHistoryForm
from django.shortcuts import render, redirect
from .models import Signup
import pandas as df
"""
def formdata(request):
    if request.method == 'POST':
        form = StockHistoryForm(request.POST)
        if form.is_valid():
            # 폼이 유효하면, 폼에서 데이터 가져오기
            n = form.cleaned_data['fast_period']  # form 필드 이름에 따라 변경
            order_percentage = form.cleaned_data['stop_loss']

            # ATR class params 업데이트
            class ATR(bt.Strategy):
                params = (('n', n), ('order_percentage', order_percentage))
"""
# 그래프 만듬
def make_plots(sell_dates, buy_dates, cash, ticker, hist, initcash):
    hist['Date'] = hist.index
    sell_prices = [hist['Close'][date] for date in sell_dates] #sell_dates의 close만
    buy_prices = [hist['Close'][date] for date in buy_dates] # buy_dates의 close만
    pct_changes = []
    initial_cash = initcash
    for i in range(len(sell_prices)):
        net_gain_or_loss = sell_prices[i] - buy_prices[i] # 순이익
        pct_changes.append((net_gain_or_loss/buy_prices[i])*100) # 주식 백분율 변화

    #BUY SELL 그래프 1번
    buy_sell_fig = px.line(hist, x="Date", y="Close", title='과거 {} Buy/Sell 그래프'.format(ticker))
    buy_sell_fig.add_trace(
        go.Scatter(
            x=sell_dates,
            y=sell_prices,
            mode='markers',
            marker=dict
            (
            color='Red',
            size=10
            ),
            name='Sell'
        )
    )
    buy_sell_fig.add_trace(
        go.Scatter(
            x=buy_dates,
            y=buy_prices,
            mode='markers',
            marker=dict
            (
            color='mediumspringgreen',
            size=10
            ),
            name='Buy'
        )
    )

    #GAIN/LOSS 그래프 2번

    outcomes = ["Gain" if pct_change > 0 else "Loss" for pct_change in pct_changes]
    df = pd.DataFrame({'a':cash, 'sell_dates':sell_dates, 'pct_changes':pct_changes, 'outcomes':outcomes})
    gain_loss_fig = px.scatter(data_frame= df,x='sell_dates', y='pct_changes',
                                    color='outcomes',
                                    color_discrete_map={'Gain': '#7386e6', 'Loss':'red'},
                                    title="거래 손익 백분율",
                                    labels={
                                    "sell_dates": "Date",
                                    "pct_changes": "Percent Gain/Loss",
                                    "outcomes": "",
                                    "a": "Total Cash"
                                    },
                                    size_max=10,
                                    size=[1 for i in sell_dates],
                                    hover_data="a"
                               )
    #TOTAL CASH 그래프 3번
    total_cash_fig = px.line(data_frame= df,x='sell_dates', y='a',
                                title="매 회 판매 후 총 금액 (${} 기준)".format(initial_cash),
                                labels={
                                    "sell_dates": "Date",
                                    "a": "Cash",
                                }
                            )

    #TOTAL_CASH_BUY_HOLD 그래프 4번
    shares_bought = math.floor(10000 / hist['Close'][0])
    leftover_cash = 10000 -  (shares_bought * hist['Close'][0])
    total_cash_buy_hold_fig = px.line(x=hist['Date'], y=shares_bought * hist['Close'] + leftover_cash,
                                            title="Buy Hold 전략 사용한 총 금액 (${} 기준)".format(initial_cash),
                                            labels={
                                                'x':"Date",
                                                'y':"Total Cash"
                                            }
                                      )

    # plotly
    buy_sell_graph = plotly.offline.plot(buy_sell_fig, auto_open = False, output_type="div")
    gain_loss_graph = plotly.offline.plot(gain_loss_fig, auto_open = False, output_type="div")
    total_cash_graph = plotly.offline.plot(total_cash_fig, auto_open = False, output_type="div")
    total_cash_buy_hold_graph = plotly.offline.plot(total_cash_buy_hold_fig, auto_open = False, output_type="div")

    return buy_sell_graph, gain_loss_graph, total_cash_graph, total_cash_buy_hold_graph


    plotly.write_image(buy_sell_graph, 'buy_sell_graph.png')

# 계산
def get_plots(request, ticker, strategy, initcash):
    stock_data = yf.Ticker(ticker)
    hist = stock_data.history(period="MAX")

    sell_dates = []
    buy_dates = []
    cash = []
    initial_cash = initcash


# strategy별로 계산

    # atrlimitorder
    class ATR(bt.Strategy):
        params = (('n', 20), ('order_percentage', 1)) # default 50/1 설정
        # n(period) - 계산에 사용되는 일 수
        # order_percentage - 주문에 사용될 자본 백분율 / 주문 시 얼마나 투자할 지

        #buy/sell 업데이트
        def log(self, order_type, dt=None):
            dt = dt or self.datas[0].datetime.date(0)
            if order_type == 'Buy':
                buy_dates.append(dt.isoformat())
            elif order_type == 'Sell':
                sell_dates.append(dt.isoformat())
                cash.append(self.broker.cash)

        def __init__(self):
            self.n_day_high = bt.ind.Highest(self.data.high, period=65)
            self.atr = bt.indicators.ATR(self.datas[0]) * 2

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                return

            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('Buy')
                elif order.issell():
                    self.log('Sell')
                self.bar_executed = len(self)

            self.order = None

        def next(self):
            if self.position.size == 0:
                if self.data.close[0] > self.n_day_high[-1]:
                    amount_to_invest = (self.params.order_percentage * self.broker.cash)
                    self.size = math.floor(amount_to_invest / self.data.close)
                    buy_price = self.data.low[0] - self.atr[0]
                    self.buy_order = self.buy(size=self.size, exectype=bt.Order.Limit,
                            price=buy_price,
                            valid=self.datetime.date(ago=0) + timedelta(days=10))

            if self.position.size > 0:
                sell = True
                for i in range(1,50):
                    neg_i = i * -1
                    if self.data.close[0] < self.data.close[neg_i]:
                        sell = False
                if sell == True:
                    self.close()

    class GoldenCross(bt.Strategy):
        params = (('fast', 50), ('slow', 200), ('order_percentage', 1)) # 50 200 그냥 기본값들

        #buy/sell 업데이트
        def log(self, order_type, dt=None):
            dt = dt or self.datas[0].datetime.date(0)
            if order_type == 'Buy':
                buy_dates.append(dt.isoformat())
            elif order_type == 'Sell':
                sell_dates.append(dt.isoformat())
                cash.append(self.broker.cash)

        def __init__(self):
            self.fast_moving_average = bt.indicators.SMA(self.data.close,
                                                        period = self.params.fast,
                                                        plotname = 'SMA {}'.format(self.params.fast))
            self.slow_moving_average = bt.indicators.SMA(self.data.close,
                                                        period = self.params.slow,
                                                        plotname = 'SMA {}'.format(self.params.slow))
            self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                return

            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('Buy')
                elif order.issell():
                    self.log('Sell')
                self.bar_executed = len(self)

            self.order = None

        def next(self):
            if self.position.size == 0:
                if self.crossover > 0:
                    amount_to_invest = (self.params.order_percentage * self.broker.cash)
                    self.size = math.floor(amount_to_invest / self.data.close)
                    self.buy(size=self.size)

            if self.position.size > 0:
                if self.crossover < 0:
                    self.close()

    # smacross
    class SmaCross(bt.Strategy):
        params = dict(
            pfast=10,  # fast_period
            pslow=30   # slow_period
        )
        def log(self, order_type, dt=None):
            dt = dt or self.datas[0].datetime.date(0)
            if order_type == 'Buy':
                buy_dates.append(dt.isoformat())
            elif order_type == 'Sell':
                sell_dates.append(dt.isoformat())
                cash.append(self.broker.cash)

        def __init__(self):
            sma1 = bt.ind.SMA(period=self.p.pfast)  # pfast 평균
            sma2 = bt.ind.SMA(period=self.p.pslow)  # pslow 평균
            self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover 신호

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                return

            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('Buy')
                elif order.issell():
                    self.log('Sell')
                self.bar_executed = len(self)

            self.order = None
        def next(self):
            if not self.position:
                if self.crossover > 0:
                    self.buy()

            elif self.crossover < 0:
                self.close()

    class BollingerBands(bt.Strategy):
        params = (('n', 20), ('devfactor', 2), ('order_percentage', 1))

        def log(self, order_type, dt=None):
            dt = dt or self.datas[0].datetime.date(0)
            if order_type == 'Buy':
                buy_dates.append(dt.isoformat())
            elif order_type == 'Sell':
                sell_dates.append(dt.isoformat())
                cash.append(self.broker.cash)

        def __init__(self):
            self.bbands = bt.indicators.BollingerBands(self.datas[0].close,
                                                       period=self.params.n,
                                                       devfactor=self.params.devfactor)

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                return

            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('Buy')
                elif order.issell():
                    self.log('Sell')
                self.bar_executed = len(self)

            self.order = None

        def next(self):
            if self.position.size == 0:
                if self.data.close[0] < self.bbands.lines.bot[0]:
                    amount_to_invest = (self.params.order_percentage * self.broker.cash)
                    self.size = math.floor(amount_to_invest / self.data.close[0])
                    buy_price = self.data.low[0]
                    self.buy(size=self.size, exectype=bt.Order.Limit, price=buy_price)

            if self.position.size > 0:
                if self.data.close[0] > self.bbands.lines.top[0]:
                    self.close()


    class Rsi(bt.Strategy):
        params = (
            ('rsi_period', 14),        # RSI 기간
            ('rsi_oversold', 30),     # 매수 신호
            ('rsi_overbought', 70),   # 매도 신호
        )

        def log(self, order_type, dt=None):
            dt = dt or self.datas[0].datetime.date(0)
            if order_type == 'Buy':
                buy_dates.append(dt.isoformat())
            elif order_type == 'Sell':
                sell_dates.append(dt.isoformat())
                cash.append(self.broker.cash)

        def __init__(self):
            self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
            self.order = None

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                return

            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('Buy')
                elif order.issell():
                    self.log('Sell')
                self.bar_executed = len(self)

            self.order = None

        def next(self):
            if self.order:
                return  # 주문 실행 중 -> 추가 주문 x

            if self.rsi < self.params.rsi_oversold: # 매수 주문 생성
                self.order = self.buy()

            elif self.rsi > self.params.rsi_overbought: # 매도 주문 생성
                self.order = self.sell()


# strategy end

    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(initial_cash) # 초기 자금으로 broker 세팅
    feed = bt.feeds.PandasData(dataname=hist)
    cerebro.adddata(feed)


    if strategy == "ATR":
        context = get_model_data(request)
        slow_period = int(context['slow_period'])
        fast_period = int(context['fast_period'])
        cerebro.addstrategy(ATR, n = (fast_period - slow_period)) # period -> fast - slow
    elif strategy == "GC":
        context = get_model_data(request)
        slow_period = int(context['slow_period'])
        fast_period = int(context['fast_period'])
        cerebro.addstrategy(GoldenCross, fast = fast_period, slow=slow_period)
    elif strategy == "SmaCross":
        context = get_model_data(request)
        slow_period = int(context['slow_period'])
        fast_period = int(context['fast_period'])
        cerebro.addstrategy(SmaCross, pfast = fast_period, pslow = slow_period)
    elif strategy == "BollingerBands":
        context = get_model_data(request)
        slow_period = int(context['slow_period'])
        fast_period = int(context['fast_period'])
        devfac = int(context['devfactor'])
        cerebro.addstrategy(BollingerBands, period = (fast_period - slow_period), devfactor = devfac)
    elif strategy == "RSI":
        context = get_model_data(request)
        slow_period = int(context['slow_period'])
        fast_period = int(context['fast_period'])
        rsi_oversold = int(context['rsi_oversold'])
        rsi_overbought = int(context['rsi_overbought'])
        cerebro.addstrategy(Rsi, rsi_period = (fast_period - slow_period), rsi_oversold = rsi_oversold, rsi_overbought = rsi_overbought)

    cerebro.run()
    return make_plots(sell_dates, buy_dates, cash, ticker, hist, initcash)

def get_model_data(request):
    context = []
    user = request.user
    records = Signup.objects.filter(author_id=user.id)
    if records.exists():
        for info in records:
            slow_period = info.slow_period = request.POST.get('slow_period') # 로그인 한 아이디에 해당하는 값 가져오기
            fast_period = info.slow_period = request.POST.get('fast_period')
            devfac = info.devfactor = request.POST.get('devfactor')
            rsi_overbought = info.rsi_overbought = request.POST.get('rsi_overbought')
            rsi_oversold = info.rsi_oversold = request.POST.get('rsi_oversold')
        context = { 'slow_period' : slow_period, 'fast_period' : fast_period, 'devfactor' : devfac,
                    'rsi_overbought' : rsi_overbought, 'rsi_oversold' : rsi_oversold}
    return context
