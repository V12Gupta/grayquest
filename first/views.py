from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm
from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
import pandas as pd
import numpy as np
#import talib
import os
import pytz
from pandas.tseries.offsets import BDay
from datetime import datetime, timedelta
import winsound
import shutil
import time
import requests
import json

##from ibapi.client import EClient
##from ibapi.order import Order
##from ibapi.order_state import OrderState
##from ibapi.wrapper import EWrapper
##from ibapi.contract import Contract
##from ibapi.common import *
##from ibapi.tag_value import TagValue

tz = 'Asia/Kolkata'


dict_out = {}
dict_out_backup = {}


def home(request):
    return render(request, 'first/index.html')


def event(request):
    if request.method == 'GET':
        print('Helloworld12345')
        df = pd.read_csv("C://equity_application//media//Upstox_stocklist.csv")
        lst = os.listdir("C://equity_application//media//market_watchlist")
        fullmarketwatchlist = []
        for watchlist in lst:
            fullmarketwatchlist.append(watchlist.split('.')[0])

        contract = df['ContractSymbol'].tolist()

        contract2 = fullmarketwatchlist
        context = {'contract': contract, 'contract2': contract2}
        return render(request, 'first/event.html', context=context)

    if request.method == 'POST':
        print('Helloworld')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('Helloworld123')
                df = pd.read_csv("C://equity_application//media//Upstox_stocklist.csv")
                lst = os.listdir("C://equity_application//media//market_watchlist")
                fullmarketwatchlist = []
                for watchlist in lst:
                    fullmarketwatchlist.append(watchlist.split('.')[0])

                contract = df['ContractSymbol'].tolist()

                contract2 = fullmarketwatchlist
                context = {'contract': contract, 'contract2': contract2}
                #if request.COOKIES.has_key( 'visits' ):
                    #v = request.COOKIES[ 'visits' ]
                #else:
                    #v = 0
                return render(request, 'first/event.html', context=context)
                
                #return render(request, 'first/event.html')
            else:
                return render(request, 'first/userdetails.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'first/userdetails.html', {'error_message': 'Invalid login'})
        


def login_user(request):
    if request.method == "GET":
        return render(request, 'first/userdetails.html')
    if request.method == "POST":
        print('Helloworld')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'first/event.html')
            else:
                return render(request, 'first/userdetails.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'first/userdetails.html', {'error_message': 'Invalid login'})


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return render(request, 'first/userdetails.html')
    context = {
        "form": form,
    }
    return render(request, 'first/register.html', context)


def initial_capital(request):
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    params = str(params).split('$$')[0]

    print(params)

    try:
        df_StockDetail = pd.read_csv('C://equity_application//media//Initial_Capital.csv')
        df_StockDetail['Risk_Percentage'].iloc[0] = str(params).split('*')[0]
        df_StockDetail.to_csv('C://equity_application//media//Initial_Capital.csv', index=False)

    except:
        print("error in updating")

    error = ""
    return JsonResponse({"error": error})

def update_expiry_month(request):
    
    url = request.get_full_path
    print("Hello_world")
    print(url)
    params = str(url)[:-3].split('?')[1]
    expiry_month_rollover=params.split('***')[1]
    df1 = pd.DataFrame([[str(expiry_month_rollover).split('$%$')[0],str(expiry_month_rollover).split('$%$')[1]]],columns = ["Expiry_Date","Rollover_Time"]) 
    df1.to_csv("C:\\equity_application\\media\\rolloverexpiry_time.csv",index=False)

    error=""
    return JsonResponse({"error": error})


def update_expiry_date(request):
    
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    expiry_month=params.split('***')[1]
    df1 = pd.DataFrame([[expiry_month]],columns = ["Expiry"]) 
    df1.to_csv("C:\\equity_application\\media\\expiry_month.csv",index=False)
    error=""
    return JsonResponse({"error": error})


def update_ema_value(request):
    
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    emavalue=params.split('***')[1]
    df1 = pd.DataFrame([[emavalue]],columns = ["emavalue"]) 
    df1.to_csv("C:\\equity_application\\media\\emavaluedata.csv",index=False)
    error=""
    return JsonResponse({"error": error})


##class TestAppGainer(EWrapper, EClient):
##
##    def __init__(self, broker=None):
##        EClient.__init__(self, self)
##
##        self.stock_of_5 = pd.DataFrame(columns=["Symbol", "Date", "Open", "High", "Low", "Close","Volume"])
##
##    def historicalData(self, reqId: int, bar: BarData):
##        c = self.contracts[reqId]
##
##        df = pd.DataFrame([[c.symbol, bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume]],
##                          columns=["Symbol", "Date", "Open", "High", "Low", "Close","Volume"])
##        self.stock_of_5 = pd.concat([self.stock_of_5, df])
##
##    def historicalDataEnd(self, reqId: int, start: str, end: str):
##        super().historicalDataEnd(reqId, start, end)
##        c = self.contracts[reqId]
##        
##        Close = self.stock_of_5['Close']
##        emavalue = pd.read_csv("C://equity_application//media//emavaluedata.csv")
##        
##        #self.stock_of_5[str(emavalue['emavalue'].iloc[0])+'EMA'] = talib.EMA(Close, int(emavalue['emavalue'].iloc[0]))
##        
##
##        self.stock_of_5.to_csv('C://equity_application//media//Stock_Data_5//' + c.symbol + '.csv',index=False)
##        self.stock_of_5 = pd.DataFrame(columns=["Symbol", "Date", "Open", "High", "Low", "Close","Volume"])
##        winsound.Beep(500, 400)
##
##
##def get_historic(request):
##    app = TestAppGainer()
##    app.connect('127.0.0.1', 7497, 0)
##
##    contracts = []
##    # Read the csv file for Contract Symbols
##    stockmarketwatch = pd.read_csv("C://equity_application//media//UpstoxList_marketwatch.csv")
##    stocklist = pd.read_csv("C://equity_application//media//Upstox_stocklist.csv")
##    expirymonth = pd.read_csv("C://equity_application//media//expiry_month.csv")
##    emavalue = pd.read_csv("C://equity_application//media//emavaluedata.csv")
##    
##    for i in range(len(stockmarketwatch)):
##        print(stockmarketwatch['ContractSymbol'].iloc[i])
##        
##        c = Contract()
##        c.symbol = stockmarketwatch['ContractSymbol'].iloc[i]
##        if(stocklist.loc[stocklist["ContractSymbol"] == str(stockmarketwatch['ContractSymbol'].iloc[i]), 'sectype'].iloc[0] == "FUT"):
##            c.secType = 'FUT'
##            c.lastTradeDateOrContractMonth = str(expirymonth['Expiry'].iloc[0])
##        else:
##            c.secType = 'STK'
##        c.exchange = stockmarketwatch['ExchangeSymbol'].iloc[i]
##        c.currency = 'INR'
##        contracts.append(c)
##
##    app.contracts = contracts
##
##
##
##        
##    for i in range(len(contracts)):
##        if(stocklist.loc[stocklist["ContractSymbol"] == str(stockmarketwatch['ContractSymbol'].iloc[i]), 'Timeframe'].iloc[0] == "1D"):
##            app.reqHistoricalData(i, contracts[i], "", str(int(emavalue['emavalue'].iloc[0])+20)+" D", "1 day", "TRADES", 1, 1, False, [])
##        elif(stocklist.loc[stocklist["ContractSymbol"] == str(stockmarketwatch['ContractSymbol'].iloc[i]), 'Timeframe'].iloc[0] == "1H"):
##            app.reqHistoricalData(i, contracts[i], "", "20 D", "1 hour", "TRADES", 1, 1, False, [])
##        elif(stocklist.loc[stocklist["ContractSymbol"] == str(stockmarketwatch['ContractSymbol'].iloc[i]), 'Timeframe'].iloc[0] == "1"):
##            app.reqHistoricalData(i, contracts[i], "", "10 D", "1 min", "TRADES", 1, 1, False, [])
##        else:
##            timeframe = str(stocklist.loc[stocklist["ContractSymbol"] == str(stockmarketwatch['ContractSymbol'].iloc[i]), 'Timeframe'].iloc[0]) + " mins"
##            app.reqHistoricalData(i, contracts[i], "", "10 D", timeframe, "TRADES", 1, 1, False, [])
##            
##
##    app.run()
##    return HttpResponse("Get Historic Data")
##
##
##class TestApp(EWrapper, EClient):
##
##    def __init__(self):
##        EClient.__init__(self, self)
##
##        self.contracts = []
##        self.stocklist_marketwatch = pd.read_csv("C://equity_application//media//UpstoxList_marketwatch.csv")
##        self.stocklist = pd.read_csv("C://equity_application//media//Upstox_stocklist.csv")
##        self.emavaluedata = pd.read_csv("C://equity_application//media//emavaluedata.csv")
##        self.expirymonth = pd.read_csv("C://equity_application//media//expiry_month.csv")
##        
##        self.rollovertime = pd.read_csv("C://equity_application//media//rolloverexpiry_time.csv")
##
##        try:
##            self.df_signal = pd.read_csv('C://equity_application//media//Upstox_Tradesheet//' + datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y") + '_signal_Upstox.csv')
##        except:
##            self.df_signal = pd.DataFrame()
##
##       
##        self.bar_open = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##        self.bar_high = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##        self.bar_low = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##        self.bar_close = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##        self.bar_volume = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##        self.bar_written = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##        
##        self.rollover_happen = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##
##        self.trade_happen = dict.fromkeys(self.stocklist_marketwatch['ContractSymbol'], 0)
##
##        self.dfdatabase = pd.read_csv("C://equity_application//media//Signal_DataBase.csv")
##        
##
##        
##
##    def realtimeBar(self, reqId:TickerId, time:int, open:float, high:float,
##                         low:float, close:float, volume:int, wap:float, count:int):
##             
##        super().realtimeBar(reqId, time, open, high, low, close, volume, wap, count)
##        
##        c = self.contracts[reqId]
##
##        time = datetime.now(pytz.timezone(tz)).strftime("%H:%M:%S")
##        if "09:15:00" <= time < "15:30:00":
##            try:
##
##                print(str(c.symbol) + "->", str(close))
##                dict_out.update({c.symbol: close})
##                
##               
##                if time < "15:15:00" and self.bar_written[c.symbol] == 1:
##                    self.bar_written[c.symbol] = 0
##    
##    
##                if self.trade_happen[c.symbol] == 0 and (str(c.symbol) in self.dfdatabase['Symbol'].tolist()):
##                    self.trade_happen[c.symbol] = 1
##                    
##    
##                self.bar_volume[c.symbol]+=volume
##                
##                if self.bar_open[c.symbol]==0:
##                    self.bar_open[c.symbol]=open
##                if self.bar_high[c.symbol]==0 or high > self.bar_high[c.symbol]:
##                    self.bar_high[c.symbol]=high
##                if self.bar_low[c.symbol]==0 or low < self.bar_low[c.symbol]:
##                    self.bar_low[c.symbol]=low 
##    
##                ##################Daily_Candle###################################################
##                
##                if time >= "15:15:00" and self.bar_written[c.symbol] == 0 and time > "09:16:00":
##                    
##                    stock_data = pd.read_csv('C://equity_application//media//Stock_Data_5//' + c.symbol + '.csv')
##                    self.bar_close[c.symbol] = close
##    
##                    print('******************************************************')
##    
##                    idx = len(stock_data)
##                    stock_data.at[idx, 'timestamp'] =  datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y %H:%M:%S")
##                    stock_data.at[idx, 'Open'] =  self.bar_open[c.symbol]
##                    stock_data.at[idx, 'High'] =  self.bar_high[c.symbol]
##                    stock_data.at[idx, 'Low'] =  self.bar_low[c.symbol]
##                    stock_data.at[idx, 'Close'] =  self.bar_close[c.symbol]
##                    stock_data.at[idx, 'Volume'] =  self.bar_volume[c.symbol]
##                    
##                    Close = stock_data['Close']
##                    
##                    #stock_data[str(self.emavaluedata['emavalue'].iloc[0])+'EMA'] = talib.EMA(Close, int(self.emavaluedata['emavalue'].iloc[0]))
## 
##                    stock_data.to_csv('C://equity_application//media//Stock_Data_5//' + c.symbol + '.csv',index=False)
##    
##                    self.bar_open[c.symbol] = 0
##                    self.bar_high[c.symbol] = 0
##                    self.bar_low[c.symbol] = 0
##                    self.bar_close[c.symbol] = 0
##                    self.bar_volume[c.symbol] = 0
##                    self.bar_written[c.symbol] = 1
##                    
##                ##################Daily_Candle End###################################################
##        
##                df_stock_5 = pd.read_csv('C://equity_application//media//Stock_Data_5//' + c.symbol + '.csv')
##                i = len(df_stock_5) - 1
##    
##                # LONG POSITION daily TIMEFRAME
##                
##                if (df_stock_5["Close"].iloc[i] > df_stock_5[str(self.emavaluedata['emavalue'].iloc[0])+"EMA"].iloc[i] and  self.trade_happen[c.symbol] == 0):
##    
##                    nu_of_lot = int(self.stocklist.loc[self.stocklist['ContractSymbol'] == str(c.symbol), 'no_of_lot'].iloc[0])
##                    Quantity = int(self.stocklist.loc[self.stocklist['ContractSymbol'] == str(c.symbol), 'Quantity'].iloc[0])
##    
##                    self.trade_happen[c.symbol] = 1
##    
##                    df1 = pd.DataFrame([[c.symbol,datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y %H:%M:%S"),
##                                         "LONG",
##                                         close, nu_of_lot, Quantity]],
##                                       columns=["Symbol", "Date", "Signal", "Price", "Lots", "Qty"])
##    
##                    self.df_signal = pd.concat([self.df_signal, df1])
##                    self.df_signal.to_csv(
##                        'C://equity_application//media//Upstox_Tradesheet//' + datetime.now(pytz.timezone(tz)).strftime(
##                            "%d-%m-%y") + '_signal_Upstox.csv', index=False)
##    
##                    self.dfdatabase = self.dfdatabase.drop_duplicates()
##                    self.dfdatabase = pd.concat([self.dfdatabase, df1])
##                    self.dfdatabase = self.dfdatabase.drop_duplicates()
##                    self.dfdatabase.to_csv("C://equity_application//media//Signal_DataBase.csv", index=False)
##                    
##                    #self._send_order(self.contracts[reqId],"BUY",Quantity,reqId)
##    
##                    winsound.Beep(2500, 1000)
##    
##    
##                # LONG EXIT POSITION daily TIMEFRAME
##                elif (self.trade_happen[c.symbol] == 1 and df_stock_5["Close"].iloc[i] < df_stock_5[str(self.emavaluedata['emavalue'].iloc[0])+"EMA"].iloc[i]):
##                        
##                    nu_of_lot = int(self.dfdatabase.loc[self.dfdatabase["Symbol"] == str(c.symbol), 'Lots'].iloc[0])
##                    Quantity = int(self.dfdatabase.loc[self.dfdatabase["Symbol"] == str(c.symbol), 'Qty'].iloc[0])
##    
##    
##                    df1 = pd.DataFrame([[c.symbol, datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y %H:%M:%S"),
##                                         "LONGEXIT", close, nu_of_lot, Quantity]],
##                                       columns=["Symbol", "Date", "Signal", "Price", "Lots", "Qty"])
##    
##                    self.trade_happen[c.symbol] = 0
##
##                    self.df_signal = pd.concat([self.df_signal, df1])
##                    self.df_signal.to_csv(
##                        'C://equity_application//media//Upstox_Tradesheet//' + datetime.now(pytz.timezone(tz)).strftime(
##                            "%d-%m-%y") + '_signal_Upstox.csv', index=False)
##    
##    
##                    self.dfdatabase = self.dfdatabase.drop_duplicates()
##                    self.dfdatabase = self.dfdatabase[self.dfdatabase.Symbol != str(c.symbol)]  # delete the exit position symbol
##                    self.dfdatabase = self.dfdatabase.drop_duplicates()
##    
##                    self.dfdatabase.to_csv("C://equity_application//media//Signal_DataBase.csv", index=False)
##                    
##                    #self._send_order(self.contracts[reqId],"SELL",Quantity,reqId)
##                    winsound.Beep(2500, 1000)
##                    
##                    
##                #*********************************************Rollover started********************************#
##                if(self.stocklist.loc[self.stocklist["ContractSymbol"] == str(c.symbol), 'sectype'].iloc[0] == "FUT"):
##                    
##                    if(datetime.now(pytz.timezone(tz)).strftime("%d-%m-%Y") == self.rollovertime["Expiry_Date"].iloc[0] and\
##                       time >= self.rollovertime["Rollover_Time"].iloc[0]):
##                        
##                        if(str(c.symbol) in self.dfdatabase['Symbol'].tolist() and self.rollover_happen[c.symbol]==0):
##                            
##                            nu_of_lot = self.dfdatabase.loc[self.dfdatabase["Symbol"] == str(c.symbol),'Lots'].iloc[0] 
##                            Quantity = int(self.dfdatabase.loc[self.dfdatabase["Symbol"] == str(c.symbol), 'Qty'].iloc[0])
##                            Signal_type = self.dfdatabase.loc[self.dfdatabase["Symbol"] == str(c.symbol),'Signal'].iloc[0] 
##                            
##                            Close_entry_target = self.entry_price[c.symbol]
##                            
##                            if(Signal_type == "LONG"):
##                                df1 = pd.DataFrame([[c.symbol,datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y %H:%M:%S"),\
##                                                     "LONGEXIT",close,nu_of_lot,Quantity]],\
##                                                    columns = ["Symbol","Date","Signal","Price","Lots","Qty"])  
##                                #self._send_order(self.contracts[reqId],"SELL",Quantity,reqId)
##                                
##                                winsound.Beep(2500, 1000)
##                                
##                                expiry_date = self.expirymonth['Expiry'].iloc[0]
##                                
##                                if(int(str(expiry_date)[4:])==12):
##                                    expiry_date_stock=str(int(str(expiry_date)[0:4])+1) +'01'
##                                elif(int(str(expiry_date)[4:]) == 9 or int(str(expiry_date)[4:]) == 10 or int(str(expiry_date)[4:]) == 11):    
##                                    expiry_date_stock = str(expiry_date)[0:4] + str(int(str(expiry_date)[4:])+1)
##                                else:
##                                    expiry_date_stock = str(expiry_date)[0:4] + '0' +str(int(str(expiry_date)[4:])+1)
##                                    
##                                c.lastTradeDateOrContractMonth = expiry_date_stock
##                                
##                                df1_rollover = pd.DataFrame([[c.symbol,datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y %H:%M:%S"),\
##                                                     "LONG",Close_entry_target,nu_of_lot,Quantity]],\
##                                                    columns = ["Symbol","Date","Signal","Price","Lots","Qty"])
##                                
##                                #self._send_order(self.contracts[reqId],"BUY",Quantity,reqId)
##                                
##                        
##                            
##                            self.df_signal = pd.concat([self.df_signal, df1])
##                            self.df_signal.to_csv('C://equity_application//media//Upstox_Tradesheet//' + datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y") + '_signal_Upstox.csv', index=False)
##                            
##                            self.dfdatabase=self.dfdatabase.drop_duplicates()
##                            self.dfdatabase=self.dfdatabase.loc[self.dfdatabase['Symbol'] != str(c.symbol)]
##                            self.dfdatabase=self.dfdatabase.drop_duplicates()
##                            self.dfdatabase.to_csv("C://equity_application//media//Signal_DataBase.csv", index=False)
##                            
##                            self.df_signal = pd.concat([self.df_signal, df1_rollover])
##                            self.df_signal.to_csv('C://equity_application//media//Upstox_Tradesheet//' + datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y") + '_signal_Upstox.csv', index=False)
##                            
##                            self.dfdatabase = pd.concat([self.dfdatabase, df1_rollover])
##                            self.dfdatabase.to_csv("C://equity_application//media//Signal_DataBase.csv", index=False)
##                            
##                            self.rollover_happen[c.symbol] = 1
##                            
##                        
##                        
##                        
##                #******************************************Rollover end************************************#  
##    
##
##            except:
##                pass
##
###**************************************Start Order Routing********************************************#             
##
##           
##    # Method to place an order.
##    # Whether it's a "BUY" or "SELL" is decided on the basis of 'action'
##    def _send_order(self, contract, action, qty, reqId):
##        order = Order()
##        order.action = action
##        order.orderType = "MKT"
##        order.totalQuantity = qty
##        
##        order_id = self.newOrderId()
##        
##        self.placeOrder(order_id, contract, order)
##        print(action, order.orderType, 'Order placed for', contract.symbol, 'Order Id', order_id,
##              'qty = ', qty)
##
##
##    def nextValidId(self, orderId:int):
##        self._order_id = orderId
##        
##    def newOrderId(self):
##        oid = self._order_id
##        self._order_id+=1
##        return oid
##    #**************************************End Order Routing********************************************#
##
##
##                            
##                    
##
##def get_started(request):
##    url = request.get_full_path
##    url = str(url)
##    print(url)
##
##    if url.find('_s') == -1:
##
##        app = TestApp()
##        app.connect('127.0.0.1', 7497, 2)
##
##        contracts = []
##        # Read the csv file for Contract Symbols
##
##        stockmarketwatch = pd.read_csv("C://equity_application//media//UpstoxList_marketwatch.csv")
##        stocklist = pd.read_csv("C://equity_application//media//Upstox_stocklist.csv")
##        expirymonth = pd.read_csv("C://equity_application//media//expiry_month.csv")
##        
##        
##        for i in range(len(stockmarketwatch)):
##            print(stockmarketwatch['ContractSymbol'].iloc[i])
##            
##            c = Contract()
##            c.symbol = stockmarketwatch['ContractSymbol'].iloc[i]
##            if(stocklist.loc[stocklist["ContractSymbol"] == str(stockmarketwatch['ContractSymbol'].iloc[i]), 'sectype'].iloc[0] == "FUT"):
##                c.secType = 'FUT'
##                c.lastTradeDateOrContractMonth = str(expirymonth['Expiry'].iloc[0])
##            else:
##                c.secType = 'STK'
##            c.exchange = stockmarketwatch['ExchangeSymbol'].iloc[i]
##            c.currency = 'INR'
##            contracts.append(c)
##    
##        app.contracts = contracts
##
##        for i in range(len(contracts)):
##            app.reqRealTimeBars(i, contracts[i], 5, 'TRADES', True, [])
##
##        app.run()
##
##
##    elif url.find('_s') != -1:
##        os._exit(0)
##
##    return HttpResponse("Algo started")
##

def get_log(request):
    results1 = ""

    #try:
    if 1==1:
        #data = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
        #'Price': [22000,25000,27000,35000]
        #}

        #stocks_signal = pd.DataFrame(cars, columns = ['Brand', 'Price'])
        #stocks_signal = stocks_signal.to_html(index=False).replace('<th>',
                                                                   #'<th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">')
        #results1 += stocks_signal
        url="https://api.imgflip.com/get_memes"
        res = requests.get(url)

        print (res.json())
        #data = json.loads(res)
        df = pd.DataFrame.from_dict(res.json()['data']['memes'], orient='columns')
        df = df.to_html(index=False).replace('<th>','<th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">')
    #except:
        
        results1 += df

    

    return HttpResponse(results1)


def get_color_for_ticker(value2, value3):
    if value2 > value3:
        return "green"
    elif value2 < value3:
        return "Red"
    else:
        return "#4d4d4d"


def updatemarketwatchstrike(request):
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    params = str(params).split('*%*')

    df1 = pd.read_csv("C://equity_application//media//Upstox_stocklist.csv")
    error = ""
    try:

        idx = len(df1)

        df1.at[idx, 'ContractSymbol'] = str(params[0])
        df1.at[idx, 'ExchangeSymbol'] = str(params[1])
        df1.at[idx, 'Expiry'] =  params[2]
        df1.at[idx, 'sectype'] =  params[3]
        
        df1.drop_duplicates(subset="ContractSymbol", keep="first", inplace=True)
    
        df1.to_csv("C://equity_application//media//Upstox_stocklist.csv", index=False)
    except:
        error = "error in adding Stock"
    return JsonResponse({"error": error})


def update_maindatabase(request):
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    params = str(params).split('$$')[0]

    print(params)

    try:
        df_StockDetail = pd.read_csv('C://equity_application//media//Upstox_stocklist.csv')

        df_stock_index = df_StockDetail.index[df_StockDetail['ContractSymbol'] == str(params).split('*')[0]].tolist()

        df_StockDetail['Timeframe'].iloc[df_stock_index[0]] = str(params).split('*')[1]
        df_StockDetail['no_of_lot'].iloc[df_stock_index[0]] = str(params).split('*')[2]
        df_StockDetail['Quantity'].iloc[df_stock_index[0]] = str(params).split('*')[3]
        df_StockDetail['sectype'].iloc[df_stock_index[0]] = str(params).split('*')[4]

        df_StockDetail = df_StockDetail.drop_duplicates()
        df_StockDetail.to_csv('C://equity_application//media//Upstox_stocklist.csv', index=False)

    except:
        print("error in updating")

    error = ""
    return JsonResponse({"error": error})


def get_stocklistmkt(request):
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    nameofmktwatch = params.split('***')[1]
    params = params.split('***')[0]
    df1 = pd.DataFrame([[params]], columns=["ContractSymbol"])
    df1.to_csv("C://equity_application//media//market_watchlist//" + nameofmktwatch + ".csv", index=False)
    error = ""
    return JsonResponse({"error": error})


def scrip_master_updation(request):
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    stocklist123 = pd.read_csv("C://equity_application//media//market_watchlist//" + params.split('*&*')[0] + ".csv")
    main_stocklist = pd.read_csv("C://equity_application//media//Upstox_stocklist.csv")
    stocks_name = []
    df_stocks = pd.DataFrame()
    stocks_name = str(stocklist123["ContractSymbol"].iloc[0]).split(',')
    for i in range(len(stocks_name)):
        df1 = pd.DataFrame([[str(stocks_name[i]), str(params.split('*&*')[0]), main_stocklist.loc[
            main_stocklist['ContractSymbol'] == str(stocks_name[i]), 'ExchangeSymbol'].iloc[0]]],
                           columns=["ContractSymbol", "name_of_marketwatch", "ExchangeSymbol"])
        df_stocks = pd.concat([df_stocks, df1])

    df_stocks.to_csv("C://equity_application//media//UpstoxList_marketwatch.csv", index=False)
    error = ""
    return JsonResponse({"error": error})


def MarketWatch(request):
    return render(request, "first/marketwatchpage.html", {})


def VolumeRatio(request):
    return render(request, "first/volumeratio.html", {})


def screener_only_topgainer(request):
    results1screener = ""

    print("************************************************************")
    bid_ask_return = pd.read_csv(
        "C://equity_application//media//BidSize_AskSize_Return.csv")
    bid_ask_return = bid_ask_return.sort_values(by='BidAskSizeRatio', ascending=False)
    the_table_pos = """<table border="1" class="table table-striped">
                <thead>
                <tr style="text-align: right;">
                  <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">S No.</th>
                  <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Stocks</th>
                  <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Bid Size</th>              
                  <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Ask Size</th>
                  <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Volume Ratio</th>
                  <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Return</th>              

                </tr>
                </thead>
                <tbody>"""

    for k in range(0, len(bid_ask_return)):

        try:
            value1 = k + 1
            value2 = bid_ask_return['Stocks'].iloc[k]
            value3 = bid_ask_return['BidSize'].iloc[k]
            value4 = bid_ask_return['AskSize'].iloc[k]
            value5 = bid_ask_return['BidAskSizeRatio'].iloc[k]
            value6 = bid_ask_return['Return'].iloc[k]

            the_table_pos += """<tr>
                                        <td>%(value1)s</td>
                                        <td>%(value2)s</td>
                                        <td>%(value3)s</td>
                                        <td>%(value4)s</td>
                                        <td>%(value5)s</td>
                                        <td>%(value6)s</td>                                                                        


                                    </tr>""" % {'value1': value1,
                                                'value2': value2,
                                                'value3': value3,
                                                'value4': value4,
                                                'value5': value5,
                                                'value6': value6,

                                                }
        except:
            pass

    the_table_pos += """</tbody>
                            </table>"""

    results1screener += the_table_pos

    return HttpResponse(results1screener)


def screener_only(request):
    results1screener = ""
    try:
        print("************************************************************")
        df_marketwatch = pd.read_csv('C://equity_application//media//UpstoxList_marketwatch.csv')
        df_pos = pd.read_csv('C://equity_application//media//Upstox_stocklist.csv')
        df_pos = df_pos.drop_duplicates()
        df_marketwatch = df_marketwatch.drop_duplicates()
    
        if len(df_marketwatch) == 0:
            results1screener += "No Stock"
        else:
            the_table_pos = """<table border="1" class="table table-striped">
            <thead>
            <tr style="text-align: right;">
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">S No.</th>
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Contract Symbol</th>
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Exchange Symbol</th>              
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Timeframe</th>
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">No. of Lots</th>
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">Quantity</th>    
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;">sectype</th>  
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;"></th>
              <th style = "background-color : DodgerBlue; padding-top: 12px; padding-bottom: 12px; text-align: left; color: white; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;"></th>
            </tr>
            </thead>
            <tbody>"""
    
            for k in range(0, len(df_marketwatch)):
    
                try:
                    value1 = k + 1
                    value2 = df_marketwatch['ContractSymbol'].iloc[k]
                    value3 = df_pos.loc[df_pos["ContractSymbol"] == str(
                        df_marketwatch['ContractSymbol'].iloc[k]), 'ExchangeSymbol'].iloc[0]
    
                    value4 = df_pos.loc[df_pos["ContractSymbol"] == str(
                        df_marketwatch['ContractSymbol'].iloc[k]), 'Timeframe'].iloc[0]
                    value5 = int(df_pos.loc[df_pos["ContractSymbol"] == str(
                        df_marketwatch['ContractSymbol'].iloc[k]), 'no_of_lot'].iloc[0])
                    value6 = int(df_pos.loc[df_pos["ContractSymbol"] == str(
                        df_marketwatch['ContractSymbol'].iloc[k]), 'Quantity'].iloc[0])
                    value7 = df_pos.loc[df_pos["ContractSymbol"] == str(
                        df_marketwatch['ContractSymbol'].iloc[k]), 'sectype'].iloc[0]
    
                    value8 = df_marketwatch['ContractSymbol'].iloc[k]
                    value9 = df_marketwatch['ContractSymbol'].iloc[k]
    
                    the_table_pos += """<tr>
                                    <td>%(value1)s</td>
                                    <td>%(value2)s</td>
                                    <td>%(value3)s</td>
                                    <td>%(value4)s</td>
                                    <td>%(value5)s</td>
                                    <td>%(value6)s</td>  
                                    <td>%(value7)s</td>                                                                       
                                    <td id=%(value8)s onclick="mainDataBase(this.id)"><a href= "javascript:void(0)">Remove</a></td>
                                    <td id=%(value9)s onclick="updateDataBase(this.id)"><a href= "javascript:void(0)">UpdateParameter</a></td>
    
                                </tr>""" % {'value1': value1,
                                            'value2': value2,
                                            'value3': value3,
                                            'value4': value4,
                                            'value5': value5,
                                            'value6': value6,
                                            'value7': value7,
                                            'value8': value8,
                                            'value9': value9
                                            }
                except:
                    pass
    
            the_table_pos += """</tbody>
                        </table>"""
    
            results1screener += the_table_pos

    except:
        results1screener += "No Stock"
    return HttpResponse(results1screener)


def removeStock_maindatabase(request):
    url = request.get_full_path
    print(url)
    params = str(url)[:-3].split('?')[1]
    params = str(params).split('$$')[0]

    print(params)

    try:
        df_marketwatch = pd.read_csv('C://equity_application//media//UpstoxList_marketwatch.csv')
        df_frommarket = pd.read_csv(
            "C://equity_application//media//market_watchlist//" + str(
                df_marketwatch['name_of_marketwatch'].iloc[0]) + ".csv")

        df_marketwatch = df_marketwatch.drop_duplicates()
        df_marketwatch = df_marketwatch.loc[df_marketwatch['ContractSymbol'] != str(params)]
        df_marketwatch = df_marketwatch.drop_duplicates()
        df_marketwatch.to_csv('C://equity_application//media//UpstoxList_marketwatch.csv', index=False)

        string_params = params + ','

        if string_params in df_frommarket['ContractSymbol'].iloc[0]:
            df_frommarket['ContractSymbol'].iloc[0] = df_frommarket['ContractSymbol'].iloc[0].replace(string_params, '')
        else:
            string_params = ',' + params
            df_frommarket['ContractSymbol'].iloc[0] = df_frommarket['ContractSymbol'].iloc[0].replace(string_params, '')

        df_frommarket.to_csv(
            "C://equity_application//media//market_watchlist//" + str(
                df_marketwatch['name_of_marketwatch'].iloc[0]) + ".csv",
            index=False)

    except:
        print("error in Removal")

    error = ""
    return JsonResponse({"error": error})


