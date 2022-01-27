# Library for connection to API's

#import bitstamp.client

from time import sleep
from time import time
from datetime import datetime
import pyetrade
#import trade_interface
import traceback
import random
import collections
import subprocess

#from bitfinex.client import Client

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ConnectEtrade:

   def __init__(self, d, stocks="DEFAULT", debug=False, verbose=False, clMarketDataType="intraday", sandBox=False, setoffLine=False):
   
      # Set class variables
      self.sandConsumerKey = str(d["profileConnectET"]["sandConsumerKey"])
      self.sandConsumerSecret = str(d["profileConnectET"]["sandConsumerSecret"])
      self.consumerKey = str(d["profileConnectET"]["consumerKey"])
      self.consumerSecret = str(d["profileConnectET"]["consumerSecret"])
      self.oauthKeysPath = str(d["profileConnectET"]["oauthKeysPath"])
      self.marketDataType = str(d["profileConnectET"]["marketDataType"])
      self.offLine = int(d["profileConnectET"]["offLine"])
      self.usePricesFromFile = int(d["profileConnectET"]["usePricesFromFile"])
      self.sandBox = False
      self.debug = debug
      self.ask = 0.0
      self.bid = 0.0
      self.vl = 0
      self.hi = 0
      self.lo = 0
      self.verbose = verbose
      self.lastTrade = 0
      self.dateTimeUTC = "123456"   
      self.dateTime = self.getTimeHrMnSecs()
      self.quoteStatus = "CLOSING"
      self.marketEndTime = 163000
      self.d = d
      
      if setoffLine:
         self.offLine = True
         
      if clMarketDataType != "intraday":
         self.marketDataType = clMarketDataType
      
      if sandBox:
         self.sandBox = sandBox
         self.consumerKey = self.sandConsumerKey
         self.consumerSecret = self.sandConsumerSecret
            
      with open(self.oauthKeysPath, 'r') as reader:
         lines = reader.readlines()

      if not self.offLine:
         self.oauthToken = lines[0].strip()
         self.oauthSecret = lines[1].strip()
 
#      if self.debug and not self.offLine:     
#         print ("\nSandbox account: " + str(self.sandBox))
#         print ("\nconsumerKey, consumer secret, auth token, auth secret\n")
#         print (self.consumerKey)
#         print (self.consumerSecret)
#         print (self.oauthToken)
#         print (self.oauthSecret)
#         print ("")
         
      self.stocks = stocks
      
      self.serviceValues = {}
      
      for stock in self.stocks:
         self.serviceValues[stock] = [0.0,0.0,0.0,0,""]
      
      self.isStockValues = 0
      
      self.bidIdx = 0
      self.askIdx = 1
      self.lastIdx = 2
      self.totVolIdx = 3
      self.dateIdx = 4

      self.hiIdx = 0
      self.loIdx = 1
      self.opIdx = 2
      self.clIdx = 3
      self.vlIdx = 4
      self.blIdx = 5
      self.sHIdx = 6
      self.sLIdx = 7
      self.dtIdx = 8
      
      self.totalVolume = 0
      
      self.askArr = {}
      self.bidArr = {}
      self.lastTradeArr = {}
      self.totalVolumeArr = {}
      self.highArr = {}
      self.lowArr = {}
      self.opArr = {}
      self.clArr = {}
      self.barLenArr = {}
      self.hiBarValueArr = {}
      self.loBarValueArr = {}
      self.sym = {}
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setStockValues(self, stocksChart, bar, stocks):
   
      self.isStockValues += 1
      
      if self.offLine:
         for stock in stocks:
            self.askArr[stock] = stocksChart[stock][bar][self.askIdx]
            self.bidArr[stock] = stocksChart[stock][bar][self.bidIdx]
            self.lastTradeArr[stock] = stocksChart[stock][bar][self.lastIdx]
            self.totalVolumeArr[stock] = stocksChart[stock][bar][self.vlIdx] 
            self.highArr[stock] = stocksChart[stock][bar][self.hiIdx]
            self.lowArr[stock] = stocksChart[stock][bar][self.loIdx]   
            self.opArr[stock] = stocksChart[stock][bar][self.opIdx]   
            self.clArr[stock] = stocksChart[stock][bar][self.clIdx]   
            self.barLenArr[stock] = stocksChart[stock][bar][self.blIdx] 
            self.hiBarValueArr[stock] = stocksChart[stock][bar][self.sHIdx] 
            self.loBarValueArr[stock] = stocksChart[stock][bar][self.sLIdx] 
            
      else: # Live
      
         stockSegs = {}
         sSegCtr = ctr = sCtr = 0
         stocks = []
         
         if len(self.stocks) > self.d.maxNumStocksToTrade:
            # Setup a dict of stock arrays the size of self.maxEtradeStocks
            
            print ("len(self.stocks) " + str(len(self.stocks)))

            for ctr in range(len(self.stocks)):
               if ctr % self.maxEtradeStocks == 0:
                  stockSegs[sSegCtr] = self.stocks[ctr:(ctr+self.maxEtradeStocks)]
                  sSegCtr += 1
                  print ("stockSegs " + str(stockSegs))
               ctr += 1
         else:
            stockSegs[0] = self.stocks

         print ("stockSegs 0 " + str(stockSegs[0]))
         print ("len(stockSegs) " + str(len(stockSegs)))
         
         while sCtr < len(stockSegs):
            quoteData = []
            symbols = stockSegs[sCtr]
            
            #print ("stocks local " + str(symbols))
            #exit (1)
            
            symbolDetails = [0.0,0.0,0.0,0,""]

            for attempt in range(1500):
               try:
                  mktData = pyetrade.market.ETradeMarket(self.consumerKey, 
                  self.consumerSecret, self.oauthToken, self.oauthSecret, self.sandBox)
                  
                  
                  sym = mktData.get_quote(symbols, self.marketDataType)

                  symbol = ""
                  if len(symbols) > 1:
                     quoteData = sym['QuoteResponse']['QuoteData']
                  else:
                     quoteData.append(sym['QuoteResponse']['QuoteData'])
   
                  for n in quoteData:
                     for k, v in n.items():
                        if k == "dateTime":
                           dateT = v
                           
                        if k == "Product":
                           for key, value in v.items():
                              if key == 'symbol':
                                 symbol = value
                                 self.serviceValues[symbol] = (symbolDetails)
                                 #print ("symbol \n" + str(symbol))
                                 #print ("serviceValues[symbol] \n" + str(self.serviceValues[symbol]))
                                 symbolDetails = [0.0,0.0,0.0,0,""]
   
                        if k == "Intraday":
                           for key, val in v.items():
                              #print ("key " + str(key))
                              #print ("val " + str(val))
                              if key == 'bid':
                                 symbolDetails[self.bidIdx] = round(float(val), 2)
                                 #print ("bid " + str(val))
                              elif key == 'ask':
                                 symbolDetails[self.askIdx] = round(float(val), 2)
                                 #print ("ask " + str(val))
                              elif key == 'lastTrade':
                                 symbolDetails[self.lastIdx] = round(float(val), 2)
                                 #print ("lastTrade " + str(val))
                              elif key == 'totalVolume':
                                 symbolDetails[self.totVolIdx] = int(val)
                                 #print ("totalVolume " + str(val))
                              
                           symbolDetails[self.dateIdx] = dateT
                           
                  #print ("serviceValues \n" + str(self.serviceValues))
                  
               except Exception as e: 
                  print(e)
                  
                  if self.switchNetwork():
                     print ("Unable to switch to alternative network")
                  
                  print ("Etrade is crap " + str(attempt))
                  sleep(1)
                  
               else:
                  break
            else:
               print ("Etrade is really crap " + str(attempt))
               
               if self.switchNetwork():
                  print ("Unable to switch to alternative network")
               
            sCtr += 1
                  
      return self.serviceValues

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def switchNetwork(self):
      
      primaryNetworkName = self.d.primaryNetworkName
      
      connectionName = subprocess.check_output(self.d.getNetworkName | "awk '{print $4}'", shell=True)

      if connectionName == primaryNetworkName:
         primaryNetworkName = self.d.secondaryNetworkName
      
      if os.system(self.d.setNetworkName + primaryNetworkName) > 0:
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setValues(self, barChart, i, bid, ask, last, vol):
      
      # Read data from chart on the disk
      if self.offLine:
         self.ask = float(ask)
         self.bid = float(bid)
         self.lastTrade = float(last)
         self.vol = int(vol)
         self.high = barChart[i][self.hiIdx]
         self.low = barChart[i][self.loIdx]   
         self.op = barChart[i][self.opIdx]   
         self.cl = barChart[i][self.clIdx]   
         self.totalVolume = barChart[i][self.vlIdx] 
         self.barLen = barChart[i][self.blIdx] 
         self.hiBarValue = barChart[i][self.sHIdx] 
         self.loBarValue = barChart[i][self.sLIdx] 
         
         self.quoteStatus = ""
         self.dateTime = self.getTimeHrMnSecs()
         self.dateTimeUTC = "123456"   
         self.changeClose = ""   
         self.changeClosePct = 0.0   
         self.companyName = "QQQ"

      else: # New data
         if self.marketDataType == "Week52":
            self.w52Hi = float(sym['QuoteResponse']['QuoteData']['Week52']['high52']) 
            self.w52Lo = float(sym['QuoteResponse']['QuoteData']['Week52']['low52'])
            self.lastTrade = float(sym['QuoteResponse']['QuoteData']['Week52']['lastTrade'])
            self.perf12Months = float(sym['QuoteResponse']['QuoteData']['Week52']['perf12Months'])
            
            print ("\n52 week high: " + str(self.w52Hi))
            print ("52 week low: " + str(self.w52Lo))
            print ("lastTrade: " + str(self.lastTrade))
            print ("perf12Months: " + str(self.perf12Months    ) + "\n")
                  
         elif self.sandBox:
            self.ask = float(sym['QuoteResponse']['QuoteData']['All']['ask']) 
            self.bid = flost(sym['QuoteResponse']['QuoteData']['All']['bid']) 
            self.changeClose = sym['QuoteResponse']['QuoteData']['All']['changeClose'] 
            self.changeClosePct = sym['QuoteResponse']['QuoteData']['All']['changeClosePercentage']   
            self.companyName = sym['QuoteResponse']['QuoteData']['All']['companyName']   
            self.high = sym['QuoteResponse']['QuoteData']['All']['high']   
            self.low = sym['QuoteResponse']['QuoteData']['All']['low']   
            self.totalVolume = sym['QuoteResponse']['QuoteData']['All']['totalVolume']   
            self.dateTimeUTC = sym['QuoteResponse']['QuoteData']['dateTimeUTC']   
            self.dateTime = sym['QuoteResponse']['QuoteData']['dateTime']
            self.quoteStatus = sym['QuoteResponse']['QuoteData']['quoteStatus']   
            
         else: # Live
            self.ask = float(sym['QuoteResponse']['QuoteData']['Intraday']['ask'])
            self.bid = float(sym['QuoteResponse']['QuoteData']['Intraday']['bid'])
            self.lastTrade = float(sym['QuoteResponse']['QuoteData']['Intraday']['lastTrade'])
            self.changeClose = sym['QuoteResponse']['QuoteData']['Intraday']['changeClose']   
            self.changeClosePct = sym['QuoteResponse']['QuoteData']['Intraday']['changeClosePercentage']   
            self.companyName = sym['QuoteResponse']['QuoteData']['Intraday']['companyName']   
            self.high = sym['QuoteResponse']['QuoteData']['Intraday']['high']   
            self.low = sym['QuoteResponse']['QuoteData']['Intraday']['low']   
            self.totalVolume = self.vol = int(sym['QuoteResponse']['QuoteData']['Intraday']['totalVolume'])
            self.dateTimeUTC = sym['QuoteResponse']['QuoteData']['dateTimeUTC']   
            self.dateTime = sym['QuoteResponse']['QuoteData']['dateTime']   
            self.quoteStatus = sym['QuoteResponse']['QuoteData']['quoteStatus']
   
         if self.verbose:
            print ("\nAll Data:" )
            print (sym)
            print ("\nask: " + self.ask)
            print ("bid: " + self.bid)
            print ("vol: " + self.vol)
            print ("changeClose: " + self.changeClose)
            print ("changeClosePct: " + self.changeClosePct)
            print ("companyName: " + self.companyName)
            print ("high: " + self.high)
            print ("low: " + self.low)
            print ("totalVolume: " + self.totalVolume)
            print ("dateTimeUTC: " + self.dateTimeUTC)
            print ("dateTime: " + self.dateTime)
            print ("quoteStatus: " + self.quoteStatus)
            print ("marketDataType: " + self.marketDataType)
            print ("lastTrade: " + str(self.lastTrade))
            print ("")
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestHiChart(self, bc, numBars):

      if numBars < 1:
         return 0.0

      maxHi = bc[0][self.hi]
      
      n = 1
      while n < numBars:
         if bc[n][self.hi] > maxHi:
            maxHi = bc[n][self.hi]
         n += 1
      
      return maxHi   

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestLoChart(self, bc, numBars):

      if numBars < 1:
         return 0.0

      maxLo = bc[0][self.lo]
      
      n = 1
      while n < numBars:         
         if bc[n][self.lo] < maxLo:
            maxLo = bc[n][self.lo]
         n += 1
      
      return maxLo     

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMarketDataType(self):
      return self.marketDataType
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentPrice(self, stock):
      #f'rounded2    \t {var3:.2f} \n' 
      
      self.bidIdx = 0
      self.askIdx = 1
      self.lastIdx = 2
      self.totVolIdx = 3
      self.dateIdx = 4

      if self.isStockValues:
         if stock:
            return self.serviceValues[stock][self.lastIdx]
         
      return self.ask
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLastTrade(self, stock):
   
      if self.isStockValues:
         if stock:
            return self.serviceValues[stock][self.lastIdx]
            #return self.lastTradeArr[stock]

      return self.lastTrade
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentAsk(self, stock):
   
      if self.isStockValues:
         if stock:
            return self.serviceValues[stock][self.askIdx]
            #return self.askArr[stock]

      return float(self.ask)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentBid(self, stock):

      if self.isStockValues:
         if stock:
            return self.serviceValues[stock][self.bidIdx]
            #return self.bidArr[stock]

      return float(self.bid)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentVolume(self, stock):

      if self.isStockValues:
         if stock:
            return self.serviceValues[stock][self.totVolIdx]

      return self.vol

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getChangeClose(self):
      return float(self.changeClose)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getChangeClosePct(self):
      return float(self.changeClosePct)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCompanyName(self):
      return self.companyName

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHigh(self):
      return float(self.high)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLow(self):
      return float(self.low)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getVolume(self):
      return int(self.totalVolume)
      #return int(self.vol)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTotalVolume(self, symbol):
   
      return self.serviceValues[symbol][self.totVolIdx]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDateTimeUTC(self):
      return str(self.dateTimeUTC)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getChangeClosePct(self):
      return self.changeClosePct
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDateTime(self):
      return str(self.dateTime)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getQuoteStatus(self):
      return self.quoteStatus

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTimeStamp(self): 
      ts = time()
      st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
      return (st)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTimeHrMnSecs(self): 
         
      ts = time()
      st = datetime.fromtimestamp(ts).strftime('%H%M%S')
      
      return (int(st))
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDateMonthDayYear(self): 
         
      ts = time()
      st = datetime.fromtimestamp(ts).strftime('%m%d%Y')
      
      return (int(st))
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDateYearMonthDay(self): 
         
      ts = time()
      st = datetime.fromtimestamp(ts).strftime('%Y%m%d')
      
      return (int(st))
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def adjustTimeToTopMinute(self, time):
   
      timeS = str(time)
      timeLen = len(timeS)
            
      if timeS[timeLen - 2] != '0':
         time = time - int(timeS[timeLen - 2] + timeS[timeLen - 1])     
      elif timeS[timeLen - 1] != '0':
         time = time - int(timeS[timeLen - 1])
         
      return time

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def waitTillMarketOpens(self, openTime):

      while True:
         print("Time now: " + str(self.getTimeHrMnSecs()) + " Market start time: " + str(openTime))
         if self.getTimeHrMnSecs() >= openTime:
            return

         sleep(1)

      return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ConnectBitFinex:
   def __init__(self, service="bitstamp"):
      self.service = service

      #self.clientBFX = Client()

      #symbols = client.symbols()
      #print(symbols)

      symbol = 'btcusd'

      #print(self.clientBFX.ticker(symbol))
      #print(client.today(symbol))
      #print(client.stats(symbol))

      #parameters = {'limit_asks': 2, 'limit_bids': 2}

      #print(client.lendbook('btc', parameters))
      #print(client.order_book(symbol, parameters))

   def getCurrentPrice(self, currency="btc", alt="usd"):
      symbol = currency + alt
      mid = self.clientBFX.ticker(symbol)["mid"]
      return mid


# Connect to API service providers: bit stamp kraken etrade ibkr lakebtc

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ConnectBitStamp:
   def __init__(self, service="bitstamp", currency="btc", alt="usd"):
      self.service = service
      self.currency = currency
      self.alt = alt
      
   def connectPublic(self):   
      # bitstamp client
      #
      # currencies: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, 
      #      ltceur, ltcbtc, ethusd, etheur, ethbtc, bchusd, bcheur, bchbtc

      self.publicClient = bitstamp.client.Public()
      return (self.publicClient)
      # publicClient = connection.connect(service)
      
   def connectPrivate(self):  
      # TODO
      self.privateClient = ""
      return (self.privateClient)
      
   def getVolume(self): 
      vol = 0.0
      while True:
         try:
            vol = float(self.publicClient.ticker(self.currency, self.alt)['volume'])
         except:
            #print("Caught exception in getVolume for bitstamp. Retrying...")
            sleep(1)
            continue
         break
         
      return (vol)
         
   def getCurrentPrice(self):    
      cp = 0.0
      ctr = 0
      while True:
         ctr += 1
         try:
            cp = float(self.publicClient.ticker(self.currency, self.alt)['last'])
         except:
            #print("Caught exception in getCurrentPrice for bitstamp. Retrying...")
            #sleep(1)
            print(traceback.format_exc())
            continue
         break
         
      return (cp)
         
   def getTimeStamp(self): 
      stamp = 0.0
      while True:
         try:
            stamp = float(self.publicClient.ticker(self.currency, self.alt)['timestamp'])
         except:
            #print ("Caught exception in getCurrentPrice for bitstamp. Retrying...")      
            sleep(2)
            continue
         break
         
      return (stamp)
      

# pusher
# pusher = Pusher(
#   app_id='511221',
#   key='5e2e9920fc698e55daac',
#   secret='ebd723b242a9aa35e0de',
#   cluster='us2',
#  ssl=True
# )
# pusher.trigger('my-channel', 'my-event', {'message': 'hello world'})

#api = krakenex.API()
#k = KrakenAPI(api)
#ohlc, last = k.get_ohlc_data("BCHUSD")
#print(ohlc)
#tm = k.get_server_time()
#print (tm)
#ai = k.get_asset_info
#print (ai)
#print (k.get_tradable_asset_pairs(None))
#print (k.get_tradable_asset_pairs(None,"BCHUSD"))
#print (k.get_tradable_asset_pairs(None,"BTCUSD"))
