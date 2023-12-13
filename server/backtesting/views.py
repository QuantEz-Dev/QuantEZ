# backtesting/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .yfinance import is_valid_ticker
from .plots import get_plots
from .forms import StockHistoryForm
from .models import Signup
from django.contrib.auth.decorators import login_required
import math
import backtrader as bt
from datetime import timedelta

# @login_required(login_url='common:login')
def index(request):
    if request.method == 'POST':
        form = StockHistoryForm(request.POST)
        if form.is_valid():
            strategy = form.cleaned_data.get('strategy')
            initcash = form.cleaned_data.get('initial_cash')
            return execute_strategy(request, form, strategy, initcash)
    else:
        form = StockHistoryForm()

    return render(request, "backtesting/selectstrategies.html", {'form': form})

# strategy 동적으로 전달하게
# @login_required(login_url='common:login')
def execute_strategy(request, form, strategy, initcash):
    if request.method == 'POST':
        if form.is_valid():
            ticker = form.cleaned_data.get('Ticker')
            if is_valid_ticker(ticker):
                # DB
                user = request.user
                existing_records = Signup.objects.filter(author_id=user.id, Ticker=request.POST.get('Ticker'))
                if existing_records.exists():
                    for stockinfo in existing_records: #업데이트
                        stockinfo.Ticker = request.POST.get('Ticker')
                        stockinfo.strategy = request.POST.get('strategy')
                        stockinfo.start_date = request.POST.get('start_date')
                        stockinfo.end_date = request.POST.get('end_date')
                        stockinfo.slow_period = request.POST.get('slow_period')
                        stockinfo.fast_period = request.POST.get('fast_period')
                        stockinfo.initial_cash = request.POST.get('initial_cash')
                        stockinfo.rsi_overbought = request.POST.get('rsi_overbought')
                        stockinfo.rsi_oversold = request.POST.get('rsi_oversold')
                        stockinfo.rsi_period = request.POST.get('rsi_period')
                        stockinfo.stop_loss = request.POST.get('stop_loss')
                        stockinfo.save()
                else: # 없으면 새로 생성
                    stockinfo = Signup()
                    stockinfo.author_id = user.id
                    stockinfo.Ticker = request.POST.get('Ticker')
                    stockinfo.strategy = request.POST.get('strategy')
                    stockinfo.start_date = request.POST.get('start_date')
                    stockinfo.end_date = request.POST.get('end_date')
                    stockinfo.slow_period = request.POST.get('slow_period')
                    stockinfo.fast_period = request.POST.get('fast_period')
                    stockinfo.initial_cash = request.POST.get('initial_cash')
                    stockinfo.rsi_overbought = request.POST.get('rsi_overbought')
                    stockinfo.rsi_oversold = request.POST.get('rsi_oversold')
                    stockinfo.rsi_period = request.POST.get('rsi_period')
                    stockinfo.stop_loss = request.POST.get('stop_loss')
                    stockinfo.save()


                buy_sell_graph, gain_loss_graph, total_cash_graph, total_cash_buy_hold_graph = get_plots(request, ticker, strategy, initcash)
                return render(request,
                              "backtesting/selectstrategiesplots.html",
                              {'form': form, 'buy_sell_graph': buy_sell_graph, 'gain_loss_graph': gain_loss_graph, 'total_cash_graph': total_cash_graph, 'total_cash_buy_hold_graph': total_cash_buy_hold_graph})
            else:
                messages.error(request, "잘못된 티커")
                return redirect("backtesting:index")

    return render(request, "backtesting/selectstrategies.html", {'form': form})

# golden cross
def goldencross(request, form):
    if request.method == "POST":
        if form.is_valid():
            ticker = form.cleaned_data.get('Ticker')
            initcash = form.cleaned_data.get('initial_cash')
            if is_valid_ticker(ticker) == False:
                messages.error(request, "INVALID TICKER")
                return redirect("backtesting:index")
            else:
                buy_sell_graph, gain_loss_graph, total_cash_graph, total_cash_buy_hold_graph = get_plots(ticker, 'GC', initcash)
                return render(request,
                              "backtesting/selectstrategiesplots.html",
                              {'form': form, 'buy_sell_graph': buy_sell_graph, 'gain_loss_graph': gain_loss_graph, 'total_cash_graph': total_cash_graph, 'total_cash_buy_hold_graph': total_cash_buy_hold_graph})

    return render(request, "backtesting/selectstrategies.html", {'form': form})

# atr
def atr(request):
    form = StockHistoryForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            ticker = form.cleaned_data.get('Ticker')
            initcash = form.cleaned_data.get('initial_cash')
            if is_valid_ticker(ticker) == False:
                messages.error(request, "INVALID TICKER")
                return redirect("backtesting:index") # go to select page
            else:
                buy_sell_graph, gain_loss_graph, total_cash_graph, total_cash_buy_hold_graph = get_plots(ticker, 'ATR', initcash)
                return render(request,
                              "backtesting/selectstrategiesplots.html",
                              {'form': form, 'buy_sell_graph': buy_sell_graph, 'gain_loss_graph': gain_loss_graph, 'total_cash_graph': total_cash_graph, 'total_cash_buy_hold_graph': total_cash_buy_hold_graph})

    return render(request, "backtesting/selectstrategies.html", {'form': form})

# smacross - 아직 작동 x
def sma(request):
    form = StockHistoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            ticker = form.cleaned_data.get('Ticker')
            if is_valid_ticker(ticker) == False:
                messages.error(request, "INVALID TICKER")
                return redirect("backtesting:index")
            else:
                buy_sell_graph, gain_loss_graph, total_cash_graph, total_cash_buy_hold_graph = get_plots(form.instance.Ticker, 'SMACROSS')
                return render(request,
                              "backtesting/selectstrategiesplots.html",
                              {'form': form, 'buy_sell_graph': buy_sell_graph, 'gain_loss_graph': gain_loss_graph, 'total_cash_graph': total_cash_graph, 'total_cash_buy_hold_graph': total_cash_buy_hold_graph})

    return render(request, "backtesting/selectstrategies.html", {'form': form})

# rsi - 아직 작동 x
def rsi(request):
    form = StockHistoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            ticker = form.cleaned_data.get('Ticker')
            if is_valid_ticker(ticker) == False:
                messages.error(request, "INVALID TICKER")
                return redirect("backtesting:index")
            else:
                buy_sell_graph, gain_loss_graph, total_cash_graph, total_cash_buy_hold_graph = get_plots(form.instance.Ticker, 'RSI')
                return render(request,
                              "backtesting/selectstrategiesplots.html",
                              {'form': form, 'buy_sell_graph': buy_sell_graph, 'gain_loss_graph': gain_loss_graph, 'total_cash_graph': total_cash_graph, 'total_cash_buy_hold_graph': total_cash_buy_hold_graph})

    return render(request, "backtesting/selectstrategies.html", {'form': form})

# bollingerbands - 아직 작동 x
def bollingerbands(request):
    form = StockHistoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            ticker = form.cleaned_data.get('Ticker')
            if is_valid_ticker(ticker) == False:
                messages.error(request, "INVALID TICKER")
                return redirect("backtesting:index")
            else:
                buy_sell_graph, gain_loss_graph, total_cash_graph, total_cash_buy_hold_graph = get_plots(form.instance.Ticker, 'BB')
                return render(request,
                              "backtesting/selectstrategiesplots.html",
                              {'form': form, 'buy_sell_graph': buy_sell_graph, 'gain_loss_graph': gain_loss_graph, 'total_cash_graph': total_cash_graph, 'total_cash_buy_hold_graph': total_cash_buy_hold_graph})

    return render(request, "backtesting/selectstrategies.html", {'form': form})
