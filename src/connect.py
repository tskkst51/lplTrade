# Library for connection to API's

#import bitstamp.client

from time import sleep
from time import time
from datetime import datetime
import pyetrade
import traceback

#from bitfinex.client import Client

class ConnectEtrade:
   def __init__(self, d, stock="TSLA", debug=False, verbose=False, clMarketDataType="intraday", sandBox=False, offLine=False):
   
      # Set class variables
      self.sandConsumerKey = str(d["profileConnectET"]["sandConsumerKey"])
      self.sandConsumerSecret = str(d["profileConnectET"]["sandConsumerSecret"])
      self.consumerKey = str(d["profileConnectET"]["consumerKey"])
      self.consumerSecret = str(d["profileConnectET"]["consumerSecret"])
      self.oauthKeysPath = str(d["profileConnectET"]["oauthKeysPath"])
      self.marketDataType = str(d["profileConnectET"]["marketDataType"])
      self.offLine = int(d["profileConnectET"]["offLine"])
      self.sandBox = False
      self.debug = debug
      self.verbose = verbose
      
      if offLine:
         self.offLine = True
         
      if clMarketDataType != "intraday":
         self.marketDataType = clMarketDataType
      
      if sandBox:
         self.sandBox = sandBox
         self.consumerKey = self.sandConsumerKey
         self.consumerSecret = self.sandConsumerSecret
            
      with open(self.oauthKeysPath, 'r') as reader:
         lines = reader.readlines()
      
      self.oauthToken = lines[0].strip()
      self.oauthSecret = lines[1].strip()
 
      if self.debug:     
         print ("\nSandbox account: " + str(self.sandBox))
         print ("\nconsumerKey, consumer secret, auth token, auth secret\n")
         print (self.consumerKey)
         print (self.consumerSecret)
         print (self.oauthToken)
         print (self.oauthSecret)
         print ("")
   
      self.symbol = stock

   def setValues(self, barChart, i):
   
      if self.offLine:
         self.cp = 33.44
      
      # Read data from chart on the disk
      if self.offLine:
         self.ask = self.cp
         self.bid = self.cp - 1   
         self.changeClose = ""   
         self.changeClosePct = 0.0   
         self.companyName = "QQQ"   
         self.high = barChart[i][0]   
         self.low = barChart[i][1]   
         self.op = barChart[i][2]   
         self.cl = barChart[i][3]   
         self.totalVolume = barChart[i][4] 
         self.quoteStatus = "CLOSING"

      else: # Live
         mktData = pyetrade.market.ETradeMarket(self.consumerKey, 
            self.consumerSecret, self.oauthToken, self.oauthSecret, self.sandBox)
            
         sym = mktData.get_quote([self.symbol], self.marketDataType)
                    
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
            self.ask = sym['QuoteResponse']['QuoteData']['All']['ask'] 
            self.bid = sym['QuoteResponse']['QuoteData']['All']['bid'] 
            self.changeClose = sym['QuoteResponse']['QuoteData']['All']['changeClose'] 
            self.changeClosePct = sym['QuoteResponse']['QuoteData']['All']['changeClosePercentage']   
            self.companyName = sym['QuoteResponse']['QuoteData']['All']['companyName']   
            self.high = sym['QuoteResponse']['QuoteData']['All']['high']   
            self.low = sym['QuoteResponse']['QuoteData']['All']['low']   
            self.totalVolume = sym['QuoteResponse']['QuoteData']['All']['totalVolume']   
            self.dateTimeUTC = sym['QuoteResponse']['QuoteData']['dateTimeUTC']   
            self.dateTime = sym['QuoteResponse']['QuoteData']['dateTime']   
            self.quoteStatus = sym['QuoteResponse']['QuoteData']['quoteStatus']   
            
         else:
            self.ask = sym['QuoteResponse']['QuoteData']['Intraday']['ask']   
            self.bid = sym['QuoteResponse']['QuoteData']['Intraday']['bid']   
            self.changeClose = sym['QuoteResponse']['QuoteData']['Intraday']['changeClose']   
            self.changeClosePct = sym['QuoteResponse']['QuoteData']['Intraday']['changeClosePercentage']   
            self.companyName = sym['QuoteResponse']['QuoteData']['Intraday']['companyName']   
            self.high = sym['QuoteResponse']['QuoteData']['Intraday']['high']   
            self.low = sym['QuoteResponse']['QuoteData']['Intraday']['low']   
            self.totalVolume = sym['QuoteResponse']['QuoteData']['Intraday']['totalVolume'] 
            self.dateTimeUTC = sym['QuoteResponse']['QuoteData']['dateTimeUTC']   
            self.dateTime = sym['QuoteResponse']['QuoteData']['dateTime']   
            self.quoteStatus = sym['QuoteResponse']['QuoteData']['quoteStatus']
   
         if self.verbose:
            print ("\nAll Data:" )
            print (sym)
            print ("\nask: " + self.ask)
            print ("bid: " + self.bid)
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
            print ("")
  
      return

   def getCurrentPrice(self):
      return float(self.ask)
      
   def getCurrentAsk(self):
      return float(self.ask)

   def getCurrentBid(self):
      return float(self.bid)

   def getChangeClose(self):
      return float(self.changeClose)

   def getChangeClosePct(self):
      return float(self.changeClosePct)

   def getCompanyName(self):
      return self.companyName

   def getHigh(self):
      return float(self.high)

   def getLow(self):
      return float(self.low)

   def getVolume(self):
      return int(self.totalVolume)

   def getDateTimeUTC(self):
      return

   def getChangeClosePct(self):
      return self.changeClosePct
      
   def getDateTime(self):
      # Fix formatting it causes a compile error
      return datetime.strptime(self.dateTime, '%H%M%S')

   def getQuoteStatus(self):
      return self.quoteStatus

   def getTimeStamp(self): 
      ts = time()
      st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
      return (st)
      
   def getTimeHrMnSecs(self): 
      ts = time()
      st = datetime.fromtimestamp(ts).strftime('%H%M%S')
      return (int(st))
      
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
            sleep(2)
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
