# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 15:05:37 2017

@author: nextgen
"""

import datetime as dt
import pandas as pd
import numpy as np
#import talib as ta
import os
import csv
import sys
import requests
import shutil
import socket
import winsound

#os.chdir("TWS API\\source\\pythonclient")

from ibapi.client import EClient
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import *
from ibapi.tag_value import TagValue

from datetime import datetime
import pytz # $ pip install pytz

tz='Asia/Kolkata'

#time=datetime.now(pytz.timezone(tz)).strftime("%H:%M:%S")              #09:30:00

start_time = "09:15:00"  #The opening time of the market
start_time_Candel = "09:16:00"   
square_off_time = "15:25:00" #The time at which the positions will be square off,before close
rc_reckoning_close_time="15:30:00" #The closing time of the market
#signals_df=pd.DataFrame()

class TestApp(EWrapper, EClient):
    
    def __init__(self, broker=None):
        EClient.__init__(self, self)
        
        day=datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y")

        
        
# =============================================================================
#     def realtimeBar(self, reqId:TickerId, time:int, open:float, high:float,
#                          low:float, close:float, volume:int, wap:float, count:int):
#              
#         super().realtimeBar(reqId, time, open, high, low, close, volume, wap, count)
#           
#         
#         self.time=datetime.now(pytz.timezone(tz)).strftime("%H:%M:%S")
#         if self.time >= start_time and self.time < "15:31:00":
#             
# 
#      
#             print(c.symbol+"->"+str(close))
# =============================================================================
            
    def tickPrice(self, reqId: TickerId , tickType, price: float, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        c = self.contracts[reqId]
        #if tickType == 4:
        print(c.symbol+"->"+str(price))

# =============================================================================
#     def tickGeneric(self, reqId: TickerId, tickType, value: float):
#         super().tickGeneric(reqId, tickType, value)
#         
#         #if tickType == 24:
#         print(c.symbol+"->"+str(tickType)+"->"+str(value))
# =============================================================================
        
    def tickGeneric(self, reqId: TickerId, tickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        print("TickGeneric. TickerId:", reqId, "TickType:", tickType, "Value:", value)
        
    def tickOptionComputation(self, reqId: TickerId, tickType, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
        super().tickOptionComputation(reqId, tickType, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)
        
        c = self.contracts[reqId]
        
        #if tickType == 13:
            
        if c.right == 'C':
            print("Gamma for CALL----->" + str(gamma))
            
         
        if c.right == 'P':
            print("Gamma for PUT----->" + str(gamma))
            
       
        
        if c.right == 'C':
            print("IV for CALL----->" + str(impliedVol))
            
         
        if c.right == 'P':
            print("IV for PUT----->" + str(impliedVol))
            



        if c.right == 'C':
            print("Delta for CALL----->" + str(delta))
            
            
        if c.right == 'P':
            print("Delta for PUT----->" + str(delta))
                
            
            
app = TestApp()
app.connect('127.0.0.1', 9123, 1)
#app.connect(socket.gethostbyname("AOC-PC"), 8100, 20)

time=datetime.now(pytz.timezone(tz)).strftime("%H:%M:%S")
day=datetime.now(pytz.timezone(tz)).strftime("%d-%m-%y")

contracts=[]
#stocklist=pd.read_csv("C:\\MTF\\Mapping.csv")
#for stock in stocklist['IBSymbol']:
# =============================================================================
# c = Contract()
# c.symbol = 'RELIANCE'
# c.secType = 'FUT'
# c.lastTradeDateOrContractMonth='202012'
# c.exchange = 'NSE'
# c.currency = 'INR'
# contracts.append(c)
# =============================================================================

c = Contract()
c.symbol = 'BANKNIFTY'
c.secType = 'OPT'
c.lastTradeDateOrContractMonth='20201210'
c.strike = 29100
c.right = 'CE'
c.exchange = 'NSE'
c.currency = 'INR'
c.multiplier = 1
contracts.append(c)



    #c = Contract()
    #c.symbol = stock
    #c.secType = 'STK'
    #c.exchange = 'NSE'
    #c.currency = 'INR'
    #contracts.append(c)
    
app.contracts = contracts
          
for i in range(len(contracts)):
    #app.reqRealTimeBars(i, contracts[i], 5, 'TRADES', True, [])
    #app.reqMktData(i, contracts[i], "", False, False, [])
    #app.reqMktData(i, contracts[i], "233,236", False, False, []);
    
    # def tickPrice(self, reqId: TickerId , tickType, price: float, attrib): call_bid, put_bid, call_ask, put_ask (Call Back Function)
    app.reqMktData(i, contracts[i], "101", False, False, [])
        
    # def tickOptionComputation(delta, gamma, vega, theta) (Call Back Function)
    #app.reqMktData(i, contracts[i], "", False, False, [])
    
app.run()


