import pyetrade
#import order
import sys
import os
import time
import json
import os.path
import lplTrade as lpl
from array import array
from optparse import OptionParser
from time import time, sleep
import pathlib
import pickle
import simplejson
from shutil import copyfile

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

verbose = debug = quiet = False

parser = OptionParser()

parser.add_option("-a", "--alt", type="string",
   action="store", dest="alt", default=False,
   help="alternate currency to buy: usd... uer... btc... eth... bch...")

parser.add_option("-b", "--sandBox",
   action="store_true", dest="sandBox", help="Sandbox connection value")
   
parser.add_option("-c"  , "--profileConnectPath", dest="profileConnectPath",
   help="write report to FILE", metavar="FILE")

parser.add_option("-d", "--debug",
   action="store_true", dest="debug", help="don't lg.debug to logfile")
   
parser.add_option("-m", "--marketDataType", type="string",
   action="store", dest="marketDataType", default=False,
   help="currency to buy: btc... eth... bch...")
   
parser.add_option("-o", "--offLine",
   action="store_true", dest="offLine", help="offLine")

parser.add_option("-p"  , "--profileTradeDataPath", dest="profileTradeDataPath",
   help="write report to FILE", metavar="FILE")
   
parser.add_option("-q", "--quiet",
   action="store_true", dest="quiet", default=False,
   help="don't lg.debug to stdout")
   
parser.add_option("-r", "--resume",
   action="store_true", dest="resume", help="resume")

parser.add_option("-s", "--stocks", type="string",
   action="store", dest="stocks", default=False,
   help="stock to bua/selly: AAPL")
      
parser.add_option("-u", "--currency", type="string",
   action="store", dest="currency", default=False,
   help="currency to buy: btc... eth... bch...")

parser.add_option("-v", "--verbose",
   action="store_true", dest="verbose", help="verbose")
   
parser.add_option("-t", "--timeBar", type="string",
   action="store", dest="timeBar", default=False,
   help="time bar: 1 5 10 minute...")
   
parser.add_option("-w", "--workPath", type="string",
   action="store", dest="workPath", default=False,
   help="work directory. default lplTrade...")
   
(clOptions, args) = parser.parse_args()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def loadProfileData(path):

   with open(path) as jsonData:
      d = json.load(jsonData)

   return d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load profileTradeData data

# Get trading elements
with open(clOptions.profileTradeDataPath) as jsonData:
   d = json.load(jsonData)

# Get connection elements
with open(clOptions.profileConnectPath) as jsonData:
   c = json.load(jsonData)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set data variables

# Price array, hi, lo, open, close, volume, date indexes
hi = 0
lo = 1
op = 2
cl = 3
vl = 4
bl = 5
sH = 6
sL = 7
dt = 8

# Values set by the trading service
svcBid = 0
svcAsk = 1
svcLast = 2
svcVol = 3
svcDate = 4

# Keep track of average volume based on all bars
avgVol = 0

barChart = [[]]

resumedBarCharCtr = 0

barCtr = 0

close = action = noAction = 0
buyAction = buy = 1
sellAction = sell = 2
executeOnOpenPosition = 1
executeOnClosePosition = 2
#last = bid = ask = 0.0
forceClose = 1

stocks = []

stock = str(d["profileTradeData"]["stock"])
stocksStr = str(d["profileTradeData"]["stocks"])
stocks = stocksStr.split(',')
etfs = str(d["profileTradeData"]["etfs"])
profileName = str(d["profileTradeData"]["profileName"])
currency = str(d["profileTradeData"]["currency"])
alt = str(d["profileTradeData"]["alt"])
timeBar = int(d["profileTradeData"]["timeBar"])
service = str(d["profileTradeData"]["service"])
algorithms = str(d["profileTradeData"]["algorithms"])
tradingDelayBars = int(d["profileTradeData"]["tradingDelayBars"])
openBuyBars = int(d["profileTradeData"]["openBuyBars"])
closeBuyBars = int(d["profileTradeData"]["closeBuyBars"])
openSellBars = int(d["profileTradeData"]["openSellBars"])
closeSellBars = int(d["profileTradeData"]["closeSellBars"])
profileTradeData = str(d["profileTradeData"])
resume = int(d["profileTradeData"]["resume"])
workPath = str(d["profileTradeData"]["workPath"])
waitForTopMinute = int(d["profileTradeData"]["waitForTopMinute"])
halfDayEndTime = str(d["profileTradeData"]["halfDayEndTime"])
halfDays = str(d["profileTradeData"]["halfDays"])
preMarket = str(d["profileTradeData"]["preMarket"])
afterMarket = str(d["profileTradeData"]["afterMarket"])
preMarketAnalysis = int(d["profileTradeData"]["preMarketAnalysis"])
useStocksFromDailyCharts = int(d["profileTradeData"]["useStocksFromDailyCharts"])
findPreMarketMovers = int(d["profileTradeData"]["findPreMarketMovers"])
maxStocksToTrade = int(d["profileTradeData"]["maxStocksToTrade"])
doTrailingStop = int(d["profileTradeData"]["doTrailingStop"])
maxProfit = float(d["profileTradeData"]["maxProfit"])
maxLoss = float(d["profileTradeData"]["maxLoss"])
quitMaxProfit = int(d["profileTradeData"]["quitMaxProfit"])
quitMaxLoss = int(d["profileTradeData"]["quitMaxLoss"])

offLine = int(c["profileConnectET"]["offLine"])
sandBox = int(c["profileConnectET"]["sandBox"])

dailyChartPath = "dc/"
dailyChartExt = ".dc"
dailyGapExt = ".gp"
bestAlgosPath = "bestAlgos/"
bestAlgosExt = ".bs"

#symbol = currency + alt
symbol = [""]

marketDataType = "intraday"
numBars = {}

lastMinuteOfLiveTrading = 155958

#new_dict = { new_list: [] for new_list in range(4)} 

# Add ETF stocks to stocksStr
if preMarketAnalysis:
   stocksStr += "," + etfs

positionTaken = {}
stocksChart = {}
pathsChart = {}
profileData = {}
serviceValues = {}
doOnceOnOpen = {}
doOnceOnClose = {}
dirty = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def isStoppedOut(stock):

   if quitMaxProfit:          
      if a[stock].getTotalGain() >= a[stock].getTargetProfit() and a[stock].getTotalGain() != 0.0:
         lg1.info ("MAX PROFIT REACHED, Gain: Bar: " + str(a[stock].getTotalGain()) + " " + str(barCtr))
         lg1.info ("MAX PROFIT TARGET: " + str(a[stock].getTargetProfit()))
         lg1.info ("MAX PROFIT FACTOR: " + str(maxProfit))
         lg1.info ("MAX PROFIT CLOSE PRICE: " + str(last))
         lg1.info ("MAX PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 2
                  
         # We are out with our PROFIT
      if doTrailingStop and positionTaken[stock] == stoppedOut:
         lg1.info ("TRAILING STOP REACHED, Gain: Bar: " + str(a[stock].getTotalGain()) + " " + str(barCtr))
         lg1.info ("MAX PROFIT TARGET: " + str(a[stock].getTargetProfit()))
         lg1.info ("MAX PROFIT FACTOR: " + str(maxProfit))
         lg1.info ("MAX PROFIT CLOSE PRICE: " + str(last))
         lg1.info ("MAX PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 4
         
   if quitMaxLoss:            
      if a[stock].getTotalLoss() <= a[stock].getTargetLoss() and a[stock].getTotalLoss() != 0.0:
         lg1.info ("MAX LOSS REACHED, Gain: Bar: " + str(a[stock].getTotalLoss()) + " " + str(barCtr))
         lg1.info ("MAX LOSS TARGET: " + str(a[stock].getTargetLoss()))
         lg1.info ("MAX LOSS FACTOR: " + str(maxLoss))
         lg1.info ("MAX LOSS CLOSE PRICE: " + str(last))
         lg1.info ("MAX LOSS TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 3
   return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overide profileTradeData data with command line data

if int(clOptions.currency):
   currency = clOptions.currency
   
if clOptions.alt:
   alt = clOptions.alt
   
if clOptions.stocks:
   stocks.append(clOptions.stocks)
   d["profileTradeData"]["stocks"] = str(stocks)
   
if clOptions.debug:
   debug = int(clOptions.debug)

if clOptions.verbose:
   verbose = int(clOptions.verbose)
   
if clOptions.resume:
   resume = int(clOptions.resume)
   
if clOptions.sandBox:
   sandBox = clOptions.sandBox

if clOptions.marketDataType:
   marketDataType = clOptions.marketDataType

if clOptions.offLine:
   offLine = clOptions.offLine

if clOptions.timeBar:
   timeBar = clOptions.timeBar
   d["profileTradeData"]["timeBar"] = str(timeBar)
   
if clOptions.workPath:
   workPath = clOptions.workPath
   d["profileTradeData"]["workPath"] = str(workPath)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set stocks to trade based on pre market analysis

if preMarketAnalysis:

   logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
   
   # Instantiate the needed objects
   l = lpl.Log(0, 0, logPath, 0)
   pr = lpl.Premarket(dailyChartPath, dailyChartExt, dailyGapExt, bestAlgosPath, bestAlgosExt)
   tg = lpl.Target(c, d, l)
   dc = lpl.Dailychart()
   th = lpl.Thred()
   #th = lpl.Process()
   
   if useStocksFromDailyCharts:
      stocks = pr.getStockStrFromDailyCharts()
   
   print ("stocks\n" + str(stocks))

   # Candidates come from premarket movers internet site, daily charts, ETF movers
   candidates = pr.getStockCandidates(tg, dc, stocks, findPreMarketMovers, useStocksFromDailyCharts)
   
   # Suck in the yearly data charts for the candidates
   dailyStockData = pr.getDailyStockData(tg, dc, candidates)
   
   tg.setAllStocksArr(dailyStockData)
   
   # Calculate the premarket gap movement of the candidates
   dailyGapData = pr.getDailyGapData(tg, dc, candidates)
   
   # Get an ordered list of the best candidates 
   orderedStocks = pr.getDailyOrderedStocks(tg, dailyGapData, dailyStockData, candidates)

   print ("orderedStocks\n" + str(orderedStocks))

   # Pick the proper algorithm to use based on saved minute chart data
   algoData, stocks = pr.getAlgorithm(orderedStocks)
   
   # LIVE run lplt.py with the #1 stock candidate
   # If it profits out. invoke with best performing at the moment

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up stock arrays

if isinstance(stocks, str):
   stocks = stocks.split(",")
   
for stock in stocks:
   stocksChart[stock] = [[0.0,0.0,0.0,0.0,0,0.0,0,0,""]]
   pathsChart[stock] = {}
   profileData[stock] = {}
   positionTaken[stock] = 0
   doOnceOnOpen[stock] = 0
   doOnceOnClose[stock] = 0
   dirty[stock] = 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log and debug file based on profileTradeData name and path
# Write header data to logs

tm = lpl.Time()

# Create minute profile variables
#profile1m = clOptions.profileTradeDataPath
#profile2m = clOptions.profileTradeDataPath.replace("active", "active2m")
#profile3m = clOptions.profileTradeDataPath.replace("active", "active3m")
#profile4m = clOptions.profileTradeDataPath.replace("active", "active4m")
#profile5m = clOptions.profileTradeDataPath.replace("active", "active5m")

# Setup paths

if workPath:
   os.chdir(workPath)
   
lg = {}

for stock in stocks:
   logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
   debugPath = clOptions.profileTradeDataPath.replace("profiles", "debug")
   barChartPath = clOptions.profileTradeDataPath.replace("profiles", "bc")
   pricesPath = clOptions.profileTradeDataPath.replace("profiles", "prices")
   testPath = clOptions.profileTradeDataPath.replace("profiles", "test")
   
   logPath = logPath.replace(".json", "")
   debugPath = debugPath.replace(".json", "")
   barChartPath = barChartPath.replace(".json", "")
   pricesPath = pricesPath.replace(".json", "")
   testPath = testPath.replace(".json", "")
   
   # Populate the strings and log object
   lp = logPath + stock + ".log"
   db = debugPath + stock + ".debug"
   bp = barChartPath + stock + ".bc"
   pp = pricesPath + stock + ".pr"
   tp = testPath + stock + ".tt"
      
   pathsChart[stock] = {"logPath" : lp, "debugPath" : db, "barChartPath" : bp, "pricesPath" : pp, "testPath" : tp}
      
   lg[stock] = lpl.Log(debug, verbose, pathsChart[stock]['logPath'], offLine)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize trading objects

ba = {}
tr = {}
lm = {}
a = {}
pr = {}
pa = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

if service == "bitstamp":
   cn = lpl.ConnectBitStamp(service, currency, alt)
   cn.connectPublic()
elif service == "bitfinex":
   cn = lpl.ConnectBitFinex()
elif service == "eTrade":
   symbol = stock
   cn = lpl.ConnectEtrade(c, stocks, debug, verbose, marketDataType, sandBox, offLine)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm,  barcharts objects

#stocks = stocks.split(",")

# find best profile to run against list of stocks
for stock in stocks:
   if preMarketAnalysis:
      print ("algoData[stock] " + str(algoData[stock]))
      cmd = ""
      cmd = "python3 bin/profileGenerator.py -a " + algoData[stock] + " -d \"\""
      if os.system(cmd) > 0:
         print("Cannot create profile from " + str(cmd) + " " + str(algoData[stock]))
         exit(1)
      
      profileData[stock] = loadProfileData(clOptions.profileTradeDataPath)
   else:
      # Use default list
      profileData[stock] = d
   
   ba[stock] = lpl.Barchart()
   tr[stock] = lpl.Trends(profileData[stock], lg[stock], cn, ba[stock], offLine, stock)
   lm[stock] = lpl.Limits(profileData[stock], lg[stock], cn, ba[stock], offLine, stock)
   pr[stock] = lpl.Price(cn, offLine)
   pa[stock] = lpl.Pattern(profileData[stock], ba[stock])
   a[stock] = lpl.Algorithm(profileData[stock], lg[stock], cn, ba[stock], tr[stock], lm[stock], pa[stock], pr[stock], offLine, stock)

lg1 = lg[stocks[0]]
a1 = a[stocks[0]]
tr1 = tr[stocks[0]]
lm1 = lm[stocks[0]]
pr1 = pr[stocks[0]]
pa1 = pa[stocks[0]]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set end time

if str(cn.getDateMonthDayYear()) in halfDays:
   lastMinuteOfLiveTrading = int(halfDayEndTime)
   
   lg1.info ("Half day trading is set to: " + halfDayEndTime)
   lg1.info ("It must be a day after a holiday: " + halfDays)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize files

for stock in stocks:

   with open(pathsChart[stock]['debugPath'], "a+", encoding="utf-8") as debugFile:
      debugFile.write(lg[stock].infoStamp(a1.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
      debugFile.write(lg[stock].header(tm.now(), stock))
   
   lg1.info("Using " + pathsChart[stock]['debugPath'] + " as debug file")
   
   with open(pathsChart[stock]['logPath'], "a+", encoding="utf-8") as logFile:
      logFile.write(lg[stock].infoStamp(a1.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
      logFile.write(lg[stock].header(tm.now(), stock))
   
   lg1.info("Using " + pathsChart[stock]['logPath'] + " as log file")
   
   with open(pathsChart[stock]['barChartPath'], "a+", encoding="utf-8") as resumeFile:
      lg1.info("Using " + pathsChart[stock]['barChartPath'] + " as bar chart file")
   
   with open(pathsChart[stock]['pricesPath'], "a+", encoding="utf-8") as priceFile:
      lg1.info("Using " + pathsChart[stock]['pricesPath'] + " as prices file")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Display profile data

lg1.info ("Reading profileTrade data from: " + clOptions.profileTradeDataPath + "\n")
lg1.info ("Using symbol: " + symbol)
for stock in stocks:
   lg1.info ("Last trade: " + str(cn.getLastTrade(stock)))
lg1.info ("Minute bar chart: " + str(timeBar))
lg1.info ("openBuyBars: " + str(openBuyBars))
lg1.info ("closeBuyBars: " + str(closeBuyBars))
lg1.info ("openSellBars: " + str(openSellBars))
lg1.info ("closeSellBars: " + str(closeSellBars))
lg1.info ("tradingDelayBars: " + str(tradingDelayBars))
lg1.info ("sand: " + str(sandBox))
lg1.info ("offLine: " + str(offLine))
lg1.info ("marketDataType: " + cn.getMarketDataType())
lg1.info ("dateTimeUTC: " + cn.getDateTimeUTC())
lg1.info ("dateTime: " + cn.getDateTime())
lg1.info ("getQuoteStatus: " + cn.getQuoteStatus())
lg1.info ("workPath: " + workPath)
lg1.info (a1.getAlgorithmMsg())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize based on live or offLine state 

last = {}
bid = {}
ask = {}
vol = {}
tradeVol = {}
initialVol = {}
populatedStocks = []

# Start trading at the top of the minute
if not offLine:
   if waitForTopMinute and not resume:
      tm.waitUntilTopMinute()
   if preMarket and waitForTopMinute:
      tm.waitUntilTopMinute()

numPrices = {}

# Init buffers
if offLine:
   for stock in stocks:
      numPrices = pr[stock].initPriceBuffer(pathsChart[stock]['pricesPath'])
      lg[stock].debug ("number of prices from file: " + str(numPrices))
      if numPrices > 10:
         populatedStocks.append(stock)
         
   stocks = populatedStocks
   
lg1.debug ("Start bar: " + str(barCtr))
lg1.debug ("resume: " + str(resume))

# Read in barChart and resume from it
if resume:
   for stock in stocks:
      bcSize = pathlib.Path(pathsChart[stock]['barChartPath']).stat().st_size
      
      lg1.verbose ("Size of barchart file " + str(stock) + " : " + str(bcSize))
   
      # Ignore reading from barChart if it is empty
      if bcSize:
         numBars[stock] = ba[stock].read(pathsChart[stock]['barChartPath'], stocksChart[stock], timeBar)
         
         lg1.debug ("Number of bars in file on disk : " + str(numBars[stock]))
         
         barCtr = numBars[stock]
         if not offLine:
            barCtr = numBars[stock] - 1
            
      # If offline then iterate over the stored bar chart starting at bar 0
      if offLine:
         barCtr = 0
            
      # We're live, program halted and now resumed. Initilize a new bar and trade on
      else:
         ba[stock].appendBar(stocksChart[stock])
         a[stock].setAllLimits(stocksChart[stock], barCtr)
         
lg1.debug ("Start bar: " + str(barCtr))

if stock in stocks:
   lm[stock].setTradingDelayBars()
   bc[stock].setTimeBarValue(timeBar)
   
setProfit = 0

# Start trading at beginning of day
if not offLine:
   if not preMarket:
      if a1.getMarketBeginTime():
         lg1.info("Waiting till the market opens...")
         cn.waitTillMarketOpens(a1.getMarketOpenTime())

print ("stocksChart\n" + str(stocksChart))

serviceValues = cn.setStockValues(stocksChart, 0, stocks)

print ("serviceValues\n" + str(serviceValues))

#if preMarketAnalysis:
#   for stock in stocks:
#      # Launch lpltL.py
#      pass

# Set the initial price
for stock in stocks:
   #if not offLine:
   bid[stock], ask[stock], last[stock], vol[stock]  = \
      pr[stock].getNextPriceArr(serviceValues[stock])
   print ("bid[stock], ask[stock], last[stock] , vol[stock] " \
      + str(bid[stock]), str(ask[stock]), str(last[stock]), str(vol[stock]))

   if offLine:
      pr[stock].setNextBar(timeBar)

pids = {}
numLaunchedPids = 0

if preMarketAnalysis:
   pids = th.launch(algoData)
   numLaunchedPids = len(pids)

if (quitMaxProfit or doTrailingStop) and maxProfit == 0.0:
   lg1.info ("Max profit not set and it should be! ")
   exit (2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever. Pause trading during and after market hours 

while True:
   # Start trading at beginning of day
   if not a1.doPreMarket():
      if not offLine and not marketOpen:
         if a1.getMarketBeginTime():
            lg1.info("Waiting till the market opens...")
            cn.waitTillMarketOpens(a.getMarketOpenTime())
            marketOpen += 1

   #if not offLine:
      #sleep(0.02)
      
   endBarLoopTime = cn.adjustTimeToTopMinute(cn.getTimeHrMnSecs() + (100 * timeBar))

   if offLine:
      for stock in stocks:
         print ("numBars[stock] " + stock + " " + str(numBars[stock]))
         print ("numBars[stock] " + stock + " " + str(numBars[stock]))
         if barCtr >= numBars[stock] - 1 or last[stock] == pr[stock].getLastToken():
            if a[stock].inPosition():
               a[stock].closePosition(barCtr, stocksChart[stock], bid[stock], ask[stock], forceClose)
               exit()
                  
   if not offLine:
      lg1.debug ("End bar time : " + str(endBarLoopTime))
      lg1.debug ("Start time: " + str(cn.getTimeStamp()))
         
   for stock in stocks:
      initialVol[stock] = serviceValues[stock][svcVol]
   
   if not offLine:
      for stock in stocks:
         ba[stock].loadInitBar(stocksChart[stock], cn.getTimeStamp(), barCtr, bid[stock], ask[stock], last[stock], initialVol[stock])
   
   a1.setCurrentBar(barCtr)
   a1.setNextBar(barCtr + 1)

   for stock in stocks:
      doOnceOnOpen[stock] = 0
      doOnceOnClose[stock] = 0
      dirty[stock] = 0
      
   # Set all decision points at the end of the previous bar            
   for stock in stocks:
      a[stock].setAllLimits(stocksChart[stock], barCtr)

   # Manage PID's
   if preMarketAnalysis:
      for stock in stocks:
         if not isPIDRunning(p[stock]):
            print ("pop pid from running Q")
      
   # Loop until each bar has ended
   while True:
      # Set the values from the trading service
      serviceValues = cn.setStockValues(stocksChart, barCtr, stocks)

      a[stock].unsetActionOnOpenBar()
      
      for stock in stocks:
         bid[stock], ask[stock], last[stock], vol[stock] = pr[stock].getNextPriceArr(serviceValues[stock])
         vol[stock] = cn.getTotalVolume(stock) - initialVol[stock]         

      print ("vol[stock] \n" + str(vol[stock]))
       
      # Set the profit to gain
      if not setProfit:
         if quitMaxProfit > 0.0:
            setProfit += 1
            for stock in stocks:
               a[stock].setTargetProfit(last[stock], maxProfit)
               lg[stock].debug("Min profit set to: " + str(a[stock].getTargetProfit()))
               a[stock].setTargetLoss(last[stock], maxLoss)
               lg[stock].debug("Max loss set to: " + str(a[stock].getTargetLoss()))

      # Do one time on open
      if not doOnceOnOpen:
         for stock in stocks:
            a[stock].setActionOnOpenBar()
            positionTaken[stock] = a[stock].takePosition(bid, ask, last, vol, barChart, barCtr)
            doOnceOnOpen[stock] += 1
            a[stock].unsetActionOnOpenBar()

      for stock in stocks:
         exitVal = isStoppedOut(stock)
         if exitVal > 0:
            lg[stock].info ("\nSTOPPED OUT: " + stock)
            #exit(exitVal)

      for stock in stocks:
         lg[stock].info ("\nSYM : " + str(stock) + "\n")
         lg[stock].info ("BAR : " + str(barCtr))
         lg[stock].info ("HI  : " + str(stocksChart[stock][barCtr][hi]))
         lg[stock].info ("LAST: " + str(last[stock]))
         lg[stock].info ("BID : " + str(bid[stock]))
         lg[stock].info ("ASK : " + str(ask[stock]))
         lg[stock].info ("LO  : " + str(stocksChart[stock][barCtr][lo]))
         lg[stock].info ("VOL : " + str(vol[stock]) + "\n")
         #lg[stock].info ("VOL : " + str(stocksChart[stock][barCtr][vl]) + "\n")
                     
      if not offLine:
         for stock in stocks:
            ba[stock].loadBar(stocksChart[stock], vol[stock], barCtr, bid[stock], ask[stock], last[stock])
      
      print ("vol[stock] \n" + str(vol[stock]))

      # Save off the prices so they can be later used in offLine mode
      if not offLine:
         for stock in stocks:
            # Write prices and barcharts for 1-5 min charts
            pr[stock].write(pathsChart[stock]['pricesPath'], ask[stock], bid[stock], last[stock], vol[stock], barCtr)
         
      print ("vol[stock] \n" + str(vol[stock]))

      # Beginning of next bar. 2nd clause is for offline mode
      if cn.getTimeHrMnSecs() >= endBarLoopTime or pr[stock].isNextBar(timeBar):      
      
         # Only do beginning of the bar section once
         for stock in stocks:
            if dirty[stock]:
               continue
            dirty[stock] += 1
         
            if not offLine:
               ba[stock].loadEndBar(stocksChart[stock], cn.getTimeStamp(), barCtr, bid[stock], ask[stock], last[stock], vol[stock])            
            
            # Print out the bar chart. Only print the last 20 bars
            if not offLine:
               ba[stock].write(stocksChart[stock], pathsChart[stock]['barChartPath'], barCtr)
         
            lg[stock].info ("Stock: " + str(stock) + "\n")
            lg[stock].info ("Last price: " + str(last[stock]) + " Position: " + str(positionTaken[stock]))
            lg[stock].info ("Average Volume: " + str(ba[stock].getAvgVol()))
            lg[stock].info ("Average Bar length: " + str(ba[stock].getAvgBarLen()))
   
            lg1.debug ("\nNEW BAR ===========================================\n")

            # Take a position if conditions exist
            # Action here is really action on the open of the next bar since it comes after 
                        
            lg1.debug ("STOCKK " + stock + " LASTT " + str(last[stock]))
            
            a[stock].setActionOnCloseBar()
            positionTaken[stock] = a[stock].takePosition(bid[stock], ask[stock], last[stock], vol[stock], stocksChart[stock], barCtr)
            a[stock].unsetActionOnCloseBar()

            if not offLine:
               ba[stock].appendBar(stocksChart[stock])
            
            # Keep track of the bars in a position
            if a[stock].inPosition():
               ba[stock].setBarsInPosition()
   
         barCtr += 1
         break
         
      # End of bar reached. Done with on close processing
         
      # COMBINE THESE TWO AND JUST CALL ready()
      # Wait till next bar before trading if set
      # if not a.inPosition() and a.getWaitForNextBar() and barCtr < a.getNextBar():

      for stock in stocks:
         # Take a position if conditions exist
         positionTaken[stock] = a[stock].takePosition(bid[stock], ask[stock], last[stock], vol[stock], stocksChart[stock], barCtr)

      for stock in stocks:
         exitVal = isStoppedOut(stock)
         if exitVal > 0:
            lg[stock].info ("\nSTOPPED OUT: " + stock)
            #exit(exitVal)

#      for stock in stocks:
#         if a[stock].getWaitForNextBar() and barCtr < a[stock].getNextBar():
#            lg[stock].debug("Waiting for next bar...")
#            continue

      # Stop trading at the end of the day
      for stock in stocks:
         if not offLine and not a[stock].getAfterMarket():
            if a[stock].inPosition():
               if a[stock].isMarketExitTime():
                  a[stock].closePosition(barCtr, stocksChart[stock], bid, ask, forceClose)
                  bc[stock].loadEndBar(stocksChart[stock], cn.getTimeStamp(), barCtr, bid, ask, last, tradeVol)

#      # Halt program at end of trading day
#      if cn.getTimeHrMnSecs() > lastMinuteOfLiveTrading and not a1.getAfterMarket():
#         if not offLine:
#            for stock in stocks:
#               if a[stock].inPosition():
#                  a[stock].closePosition(barCtr, stocksChart[stock], bid[stock], ask[stock], forceClose)
#
#               # Write last bar
#               ba[stock].write(stocksChart[stock], pathsChart[stock]['barChartPath'], barCtr)
#               # ba[stock].fixSessionHiLo(pathsChart[stock]['barChartPath'])
#         
#            lg1.info("Program exiting due to end of day trading")
#
#         exit (3)
      # end minute loop
   # end continuous loop
# end execution loop

