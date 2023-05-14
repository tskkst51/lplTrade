## lpltSlave.py is invoked by lpltMaster.py
## lpltMaster.py writes to the prices and bc files and slave reads from them
## multiple slaves are running at the same time
## Also run in offLine mode. invoked as standalone running against test data

import pyetrade
import sys
from sys import exit
import os
import io
import time
import json
import os.path
import lplTrade as lpl
import pathlib
import pickle
import simplejson
from   shutil import copyfile
from   array import array
from   optparse import OptionParser
from   time import time, sleep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def waitForPopulatedPrices(pricesPath, barChartPath):   
   
   if not offLine:
      while True:
         if not os.path.exists(pricesPath):
            sleep(0.001)
            continue
         if pathlib.Path(pricesPath).stat().st_size < 5:
            sleep(0.001)
            continue
         break
   
   barChartFD = open(barChartPath, 'r', os.O_NONBLOCK)
   lg.debug("Using " + barChartPath + " as bar chart file")

   pricesFD = open(pricesPath, 'r', os.O_NONBLOCK)
   lg.debug("Using " + pricesPath + " as process file")
      
   
   return pricesFD, barChartFD
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def isStoppedOut(positionTaken):

   if doInPosTracking:
      if a.getInPosGain():
         lg.info ("IN POS PROFIT REACHED, Gain: Bar: " + str(a.getRealizedGainLoss()) + " " + str(barCtr))
         lg.info ("PROFIT FACTOR: " + str(maxProfit))
         lg.info ("PROFIT CLOSE PRICE: " + str(last))
         lg.info ("PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         if barCtr * timeBar > 60:
            lg.info ("PROFIT TIME: " + str((barCtr * timeBar) / 60) + " hours")
         return 2

   if quitMaxProfit:            
      if a.getRealizedGainLoss() >= a.getTargetProfit() and a.getRealizedGainLoss() != 0.0:
         lg.info (" PROFIT REACHED, Gain: Bar: " + str(a.getRealizedGainLoss()) + " " + str(barCtr))
         lg.info ("PROFIT TARGET: " + str(a.getTargetProfit()))
         lg.info ("PROFIT FACTOR: " + str(maxProfit))
         lg.info ("PROFIT CLOSE PRICE: " + str(last))
         lg.info ("PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 2
         
   # We are out with our PROFIT
   if doTrailingStop and positionTaken == stoppedOut:
      lg.info ("TRAILING STOP REACHED, Gain: Bar: " + str(a.getRealizedGainLoss()) + " " + str(barCtr))
      lg.info ("PROFIT TARGET: " + str(a.getTargetProfit()))
      lg.info ("PROFIT FACTOR: " + str(maxProfit))
      lg.info ("PROFIT CLOSE PRICE: " + str(last))
      lg.info ("PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
      
      return 4
         
   if quitMaxLoss:            
      if a.getTotalLiveGain() <= a.getTargetLoss() and a.getTotalLoss() != 0.0:
      #if a.getTotalLoss() <= a.getTargetLoss() and a.getTotalLoss() != 0.0:
         lg.info ("LOSS REACHED, Gain: Bar: " + str(a.getTotalLoss()) + " " + str(barCtr))
         lg.info ("LOSS TARGET: " + str(a.getTargetLoss()))
         lg.info ("LOSS FACTOR: " + str(maxLoss))
         lg.info ("LOSS CLOSE PRICE: " + str(last))
         lg.info ("LOSS TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 2
   
   if positionTaken == stoppedOut:
      lg.info ("STOP REACHED, Gain: Bar: " + str(a.getRealizedGainLoss()) + " " + str(barCtr))
      lg.info ("PROFIT TARGET: " + str(a.getTargetProfit()))
      lg.info ("PROFIT LOSS: " + str(a.getTargetLoss()))
      lg.info ("PROFIT FACTOR: " + str(maxProfit))
      lg.info ("PROFIT CLOSE PRICE: " + str(last))
      lg.info ("PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
      
      if a.getTotalLiveGain() > 0:
         return 4
         
      return 2
      
   if maxNumLosses and a.getLosses() >= maxNumLosses:
      lg.info ("EXITING Max Number of Losses: " + str(a.getLosses()))
      return 2
   
   if positionTaken == manualQuit:
      lg.info ("MANUAL QUIT, Gain: Bar: " + str(a.getRealizedGainLoss()) + " " + str(barCtr))
      lg.info ("PROFIT TARGET: " + str(a.getTargetProfit()))
      lg.info ("LOSS   TARGET: " + str(a.getTargetLoss()))
      lg.info ("PROFIT FACTOR: " + str(maxProfit))
      lg.info ("PROFIT CLOSE PRICE: " + str(last))
      lg.info ("PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
      return 2
      
   return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

verbose = debug = quiet = offLine = slave = False

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

parser.add_option("-l", "--slave",
   action="store_true", dest="slave", help="slave")

parser.add_option("-p"  , "--profileTradeDataPath", dest="profileTradeDataPath",
   help="write report to FILE", metavar="FILE")
   
parser.add_option("-q", "--quiet",
   action="store_true", dest="quiet", default=False,
   help="don't lg.debug to stdout")
   
parser.add_option("-r", "--resume",
   action="store_true", dest="resume", help="resume")

parser.add_option("-s", "--stock", type="string",
   action="store", dest="stock", default=False,
   help="stock to bua/selly: AAPL")
   
parser.add_option("-u", "--currency", type="string",
   action="store", dest="currency", default=False,
   help="currency to buy: btc... eth... bch...")

parser.add_option("-v", "--verbose",
   action="store_true", dest="verbose", help="verbose")
   
parser.add_option("-x", "--exitMaxProfit",
   action="store_true", dest="exitMaxProfit", help="exitMaxProfit")
   
parser.add_option("-t", "--timeBar", type="string",
   action="store", dest="timeBar", default=False,
   help="time bar: 1 5 10 minute...")
   
parser.add_option("-w", "--workPath", type="string",
   action="store", dest="workPath", default=False,
   help="work directory. default lplTrade...")
   
(clOptions, args) = parser.parse_args()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load profileTradeData data

# Get trading elements

pf = lpl.Profile(clOptions.profileTradeDataPath)
d = pf.getPFValues()

cf = lpl.Profile(clOptions.profileConnectPath)
c = cf.getPFValues()

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

# Keep track of average volume based on all bars
avgVol = 0

#barChart = [[]]

resumedBarCharCtr = 0

barCtr = 0

positionTaken = 0
close = action = noAction = 0
buyAction = buy = 1
sellAction = sell = 2
executeOnOpenPosition = 1
executeOnClosePosition = 2
last = bid = ask = 0.0
vol = 0
forceClose = 1
timeBar = 0
exitMaxProfit = 0

stock = str(pf.gv("stock"))
profileName = str(pf.gv("profileName"))
currency = str(pf.gv("currency"))
alt = str(pf.gv("alt"))
timeBar = int(pf.gv("timeBar"))
service = str(pf.gv("service"))
algorithms = str(pf.gv("algorithms"))
tradingDelayBars = int(pf.gv("tradingDelayBars"))
openBuyBars = int(pf.gv("openBuyBars"))
closeBuyBars = int(pf.gv("closeBuyBars"))
openSellBars = int(pf.gv("openSellBars"))
closeSellBars = int(pf.gv("closeSellBars"))
profileTradeData = str(d)
resume = str(pf.gv("resume"))
workPath = str(pf.gv("workPath"))
doRangeTradeBars = str(pf.gv("doRangeTradeBars"))
gainTrailStop = str(pf.gv("gainTrailStop"))
quickProfitPctTrigger = float(pf.gv("quickProfitPctTrigger"))
doTrailingStop = int(pf.gv("doTrailingStop"))
maxProfit = float(pf.gv("maxProfit"))
maxLoss = float(pf.gv("maxLoss"))
quitMaxProfit = int(pf.gv("quitMaxProfit"))
quitMaxLoss = int(pf.gv("quitMaxLoss"))
marketEndTime = int(pf.gv("marketEndTime"))
doInPosTracking = int(pf.gv("doInPosTracking"))
maxNumLosses = int(pf.gv("maxNumLosses"))
doAutoStop = int(pf.gv("doAutoStop"))
useFirstMinuteAvgs = int(pf.gv("useFirstMinuteAvgs"))
useDefaultStocks = int(pf.gv("useDefaultStocks"))
numFirstBars = int(pf.gv("numFirstBars"))
doManualOveride = int(pf.gv("doManualOveride"))

sandBox = int(cf.gv("sandBox"))

symbol = currency + alt

marketDataType = "intraday"
numBars = 0

lastMinuteOfLiveTrading = 155930

stoppedOut = 4
exitMaxProfit = 2
manualQuit = 7

resume = 0
lastVol = 0

numZeroPrices = 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overide profileTradeData data with command line data

if int(clOptions.currency):
   currency = clOptions.currency
   
if clOptions.alt:
   alt = clOptions.alt
   
if clOptions.stock:
   stock = clOptions.stock
   #d["stock"] = str(stock)
   
if clOptions.debug:
   debug = int(clOptions.debug)

if clOptions.offLine:
   offLine = int(clOptions.offLine)

if clOptions.verbose:
   verbose = int(clOptions.verbose)
   
if clOptions.resume:
   resume = int(clOptions.resume)
   
if clOptions.sandBox:
   sandBox = clOptions.sandBox

if clOptions.marketDataType:
   marketDataType = clOptions.marketDataType

if clOptions.slave:
   slave = clOptions.slave

if clOptions.timeBar:
   timeBar = int(clOptions.timeBar)
   #d["timeBar"] = str(timeBar)
   
if clOptions.workPath:
   workPath = clOptions.workPath
   #d["workPath"] = str(workPath)

exitMaxProfit = clOptions.exitMaxProfit

print ("debug " + str(debug))
print ("workPath " + str(workPath))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log and debug file based on profileTradeData name and path
# Write header data to logs

tm = lpl.Time()

# Setup paths

# lpltSlave runs tests and could already be in .../test/DATE
# 
cwd = os.getcwd()
lplPath = os.getenv("LPLT")
dcPath = cwd + "/dc/" + stock + ".dc"

if cwd != lplPath:
   #dcPath = lplPath + "/dc/" + stock + ".dc"
   dcPath = cwd + "/dc/" + stock + ".dc"

if offLine:
   slave = False

if workPath:
   if os.chdir(workPath):
      print ("changed workPath " + str(workPath))
      exit (1)

print ("os.getcwd() " + os.getcwd())

logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
debugPath = clOptions.profileTradeDataPath.replace("profiles", "debug")
barChartPath = clOptions.profileTradeDataPath.replace("profiles", "bc")
pricesPath = clOptions.profileTradeDataPath.replace("profiles", "prices")
testPath = clOptions.profileTradeDataPath.replace("profiles", "test")
statsPath = clOptions.profileTradeDataPath.replace("profiles", "logs")

print ("logPath " + logPath)
print ("dcPath " + dcPath)
print ("barChartPath " + barChartPath)
print ("statsPath " + statsPath)
print ("clOptions.profileTradeDataPath " + clOptions.profileTradeDataPath)

if "_" + stock in clOptions.profileTradeDataPath:
   logPath = logPath.replace(".json_" + stock, stock + ".ls")
   debugPath = debugPath.replace(".json_" + stock, stock + ".ds")
   barChartPath = barChartPath.replace(".json_" + stock, stock + ".bc")
   statsPath = statsPath.replace(".json_" + stock, stock + ".st")
   
   print ("barChartPath1 " + barChartPath)
   
   pricesPath = pricesPath.replace(".json_" + stock, stock + ".pr")
   testPath = testPath.replace(".json_" + stock, stock + ".tt")
else:
   logPath = logPath.replace(".json", stock + ".ls")
   debugPath = debugPath.replace(".json", stock + ".ds")
   barChartPath = barChartPath.replace(".json", stock + ".bc")
   statsPath = statsPath.replace(".json", stock + ".st")
   
   print ("barChartPath " + barChartPath)

   pricesPath = pricesPath.replace(".json", stock + ".pr")
   testPath = testPath.replace(".json", stock + ".tt")

print ("barChartPath " + barChartPath)

if service == "eTrade":
   symbol = stock

lg = lpl.Log(debug, verbose, logPath, debugPath, statsPath, offLine)

#import trade_interface as ti
#ti = lpl.TradeInterface({'consumer_key': self.consumer_key, 'consumer_secret' = self.consumerSecret}) 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

stockArr = []
if service == "bitstamp":
   cn = lpl.ConnectBitStamp(service, currency, alt)
   cn.connectPublic()
elif service == "bitfinex":
   cn = lpl.ConnectBitFinex()
elif service == "eTrade":
   symbol = stock
   stockArr.append(stock)
   cn = lpl.ConnectEtrade(c, stockArr, debug, verbose, marketDataType, sandBox, offLine)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm,  barcharts objects

bc = lpl.Barchart(barChartPath, offLine, timeBar)
tr = lpl.Trends(d, lg, cn, bc, offLine)
lm = lpl.Limits(d, lg, cn, bc, pf, symbol)
pa = lpl.Pattern(d, bc, lg)
pr = lpl.Price(cn, offLine)
mo = lpl.ManualOveride(d, symbol, lplPath)

#if not offLine:
#   ac = lpl.Account(c)
#   ac.setAccount(str(cf.gv("liveAccount")))
#   cash, margin = ac.getAccountBalance()
#   print ("cash " + str(cash))
#   print ("margin " + str(margin))

dc = lpl.Dailychart()

dy = lpl.Dynamic(timeBar, dcPath, dc, offLine)

a = lpl.Algorithm(d, lg, cn, bc, tr, lm, pa, pr, dy, mo, offLine, stock)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize files

useDefaultStocks = int(pf.gv("useDefaultStocks"))

sandBox = int(cf.gv("sandBox"))

lg.debug("Using " + pricesPath + " as prices file")

with open(debugPath, "a+", encoding="utf-8") as debugFile:
   debugFile.write(lg.infoStamp(a.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
   debugFile.write(lg.header(tm.now(), stock))

lg.debug("Using " + debugPath + " as debug file")

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.infoStamp(a.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
   logFile.write(lg.header(tm.now(), stock))

lg.debug("Using " + logPath + " as log file")

pricesFD, barChartFD = waitForPopulatedPrices(pricesPath, barChartPath)

if offLine:
   # Verify files are plump
   for path in pricesPath, barChartPath:
      if not os.path.exists(path):
         lg.error("Trying to read a file that doesn't exist: " + path)
         exit(1)
      else:
         if not os.path.getsize(path):
            lg.error("Trying to read an empty file: " + path)
            exit(1)

barChart = bc.init()

# Rank stocks based on % move over 1st minute avg length
# firstMinuteAvg  avg   #days  $ movement
#                 9.95, 11,    0.9045454545454544
firstMinuteAvgs = 0.0
if useFirstMinuteAvgs and debug:
   testDir = "test/"
   if offLine:
      testDir = cwd + "/test/"
      lg.debug ("testDir " + str(testDir))
   firstMinuteAvgs = bc.getMinuteBarAvgs(stock, timeBar, testDir)
   lg.debug ("firstMinuteAvgs " + str(firstMinuteAvgs))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Display profile data

lg.debug ("Reading profileTrade data from: " + clOptions.profileTradeDataPath + "\n")
lg.debug ("Using symbol: " + symbol)
lg.debug ("Last trade: " + str(cn.getLastTrade(stock)))
lg.debug ("Minute chart: " + str(timeBar))
lg.debug ("openBuyBars: " + str(openBuyBars))
lg.debug ("closeBuyBars: " + str(closeBuyBars))
lg.debug ("openSellBars: " + str(openSellBars))
lg.debug ("closeSellBars: " + str(closeSellBars))
lg.debug ("doRangeTradeBars: " + str(doRangeTradeBars))
lg.debug ("tradingDelayBars: " + str(tradingDelayBars))
lg.debug ("sand: " + str(sandBox))
lg.debug ("slave: " + str(slave))
lg.debug ("offLine: " + str(offLine))
lg.debug ("marketDataType: " + cn.getMarketDataType())
lg.debug ("dateTimeUTC: " + cn.getDateTimeUTC())
lg.debug ("dateTime: " + cn.getDateTime())
lg.debug ("getQuoteStatus: " + cn.getQuoteStatus())
lg.debug ("workPath: " + workPath)
lg.debug (a.getAlgorithmMsg())

for dItems in d.items():
   print ("ditems: " + str(dItems))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize based on live or state 

numPrices = 0

# Fill buffers with prices
#numPrices = pr.initPriceBufferFD(pricesFD)
#if not numPrices:
#   lg.debug("Trying to read an empty prices chart: " + pricesPath)
#
##pr.skipFirstBar(numPrices, timeBar)
#
#lg.debug ("number of prices from file: " + str(numPrices))

# Set the initial price
#bid, ask, last, vol = pr.readNextPriceLine(pricesFD, pricesPath)

# Read in barChart and resume from it
#if resume:
#   bcSize = pathlib.Path(barChartPath).stat().st_size
#   
#   lg.debug ("Size of barchart file : " + str(bcSize))
#
#   # Ignore reading from barChart if it is empty
#   if bcSize:
#      numBars = bc.read(barChartPath, barChart, timeBar)
#      if not numBars:
#         lg.debug("Trying to read an empty bar chart: " + barChartPath)
#      
#      lg.debug ("Number of bars in file on disk : " + str(numBars))
#      
#      if timeBar == 1:
#         for b in range(numBars):
#            lg.debug (str(barChart[b]))
#         
#   # We're live, program halted and now resumed. Initilize a new bar and trade on
#   bc.appendBar(barChart)

if offLine:
   numPrices = pr.initPriceBuffer(pricesPath)
   if not numPrices:
      lg.error("Trying to read an empty prices chart: " + pricesPath)
      exit(1)
   lg.debug ("number of prices from file: " + str(numPrices))

   pricesFD.seek(0, io.SEEK_SET)
else:
   pricesFD.seek(0, io.SEEK_END)

lg.debug ("Start bar: " + str(barCtr))

# Start trading at the top of the minute
#if not offLine:
#   tm.waitUntilTopMinute()
#   if a.doPreMarket():
#      tm.waitUntilTopMinute()

lm.setTradingDelayBars()
bc.setTimeBarValue(timeBar)

dirtyProfit = 0

if (quitMaxProfit or doTrailingStop) and maxProfit == 0.0:
   lg.debug ("Min profit not set! ")
   exit (2)

pr.initNextBar()

#bcSize = pathlib.Path(barChartPath).stat().st_size
#lg.debug ("Size of barchart file : " + str(bcSize))
#
## Ignore reading from barChart if it is empty
#if bcSize:
#   numBars = bc.read(barChartPath, barChart, timeBar)
#   if not numBars:
#      lg.debug("Trying to read an empty bar chart: " + barChartPath)
#   
#   lg.debug ("Number of bars in file on disk : " + str(numBars))

# Init new bar

lg.debug ("bid " + str(bid))
lg.debug ("ask "+ str(ask))
lg.debug ("last " + str(last))
lg.debug ("vol " + str(vol))

bc.appendBar(barChart)

# Start trading at beginning of day
if not offLine:
   if not a.doPreMarket():
      lg.debug("Waiting till the market opens...")
      cn.waitTillMarketOpens(a.getMarketBeginTime())

bid, ask, last, vol = pr.readNextPriceLine(pricesFD, pricesPath)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever until EOD trading or end of after market 

while True:
   
   if offLine:
      try:
         bcDate = bc.getTimeStampFromBarchartFile(barCtr)
      except IndexError:
         bcDate = cn.getTimeStamp()
   else:
      bcDate = cn.getTimeStamp()
      
   #bc.loadInitBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, vol)
   bc.loadInitBar(barChart, bcDate, barCtr, bid, ask, last, vol)

   lg.debug ("barCtr  " + str(barCtr))
         
   pr.setNextBar(timeBar)
      
   dirty = doOnceOnOpen = 0
            
   a.setAllLimits(barChart, barCtr, last)

   tradeVol = 0 

   print ("barCtr333 " + str(barCtr))
   # After first bar, compare first bar movement
   #if useFirstMinuteAvgs and debug and barCtr == timeBar:
   if useFirstMinuteAvgs and debug and barCtr == numFirstBars:
      lg.trade1stBarHeader(stock, timeBar)
      avgFbl = firstMinuteAvgs[stock][2]
      fbl = bc.getFirstBarLen(barChart, 0)
      
#      if offLine:
#         fbl = bc.getMinuteBarHiLoLen(timeBar, numFirstBars, workPath)

      lg.stats("Live first bar: " + str(fbl))
      #lg.stats("Avg  first bar: " + str(round(firstMinuteAvgs[stock][2],2)))
      lg.stats("Avg  first bar: " + str(avgFbl))
      if fbl > avgFbl:
         lg.stats("Live first bar length is > than the average first bar length")
         lg.stats(str(round((100.00 - avgFbl / fbl * 100), 2)) + "\n")
      else:
         lg.stats("Live first bar length is < than the average first bar length")
         lg.stats("Use IR logic!!\n")
   
   while True:
      # Turn on to test manual overide
      if offLine and debug and doManualOveride:
         sleep(0.0004)
      
      bid, ask, last, vol = pr.readNextPriceLine(pricesFD, pricesPath)
      
      # Count the number of 0.0 bids/asks. If more than 5 quit. Stock is crap.
      #if bid == 0.0 and ask == 0.0 and last == 0.0 and vol == 0:
      if bid == 0.0 and ask == 0.0 and last == 0.0:
         lg.debug ("numZeroPrices " + str(numZeroPrices))
         numZeroPrices += 1
         
      if numZeroPrices > 15 and not positionTaken:
      #if numZeroPrices > 25:
         lg.debug ("numZeroPrices " + str(numZeroPrices) + " exiting")
         #exit (1)
         
      # Set the profit to gain and max loss
      if not dirtyProfit:
         a.setTargetProfit(last, maxProfit)
         lg.debug("Min profit set to: " + str(a.getTargetProfit()))
         a.setTargetLoss(last, maxLoss)
         lg.debug("Max loss set to: " + str(a.getTargetLoss()))
         dirtyProfit += 1
      
      # Do one time on open
      if not doOnceOnOpen:
         a.setActionOnOpenBar()
         positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
         doOnceOnOpen += 1
         a.unsetActionOnOpenBar()

      exitVal = isStoppedOut(positionTaken)
      
      if exitVal > 0:
         exit(exitVal)

      # Halt program at end of trading day or end of price file
      if offLine:
         if last == pr.getLastToken():
            if a.inPosition():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
            if a.getRealizedGainLoss() >= a.getTargetProfit():
               exit(2)
            else:
               exit(0)
      else:
         if a.isMarketExitTime():
            lg.debug ("It's beer thirty!! ")
            if not a.getAfterMarket():
               if a.inPosition():
                  a.closePosition(barCtr, barChart, bid, ask, forceClose)
                  bc.loadEndBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, tradeVol)
               lg.debug("Program exiting due to end of day trading")
               exit(0)

      tradeVol = a.getCurrentRunningVol()
      if tradeVol != 0:
         lastVol = tradeVol
         
      lg.debug ("tradeVol " + str(tradeVol))
      lg.debug ("barCtr " + str(barCtr))
      lg.debug ("last " + str(last))
      lg.debug ("stock " + str(stock))

      bc.loadBar(barChart, tradeVol, barCtr, bid, ask, last) 
        
      lg.debug ("pr.isNextBar(timeBar) " + str(pr.isNextBar(timeBar)))
      
      if pr.isNextBar(timeBar):      

         # Only do this section once
         if dirty:
            continue
            
         dirty += 1

#         if not offLine:
#            bc.displayLastNBars(barChart, 20)

         if offLine:
            bcDate = bc.getTimeStampFromBarchartFile(barCtr)
         else:
            bcDate = cn.getTimeStamp()

         bc.loadEndBar(barChart, bcDate, barCtr, bid, ask, last, lastVol)
         
         #lg.debug ("barChart after end bar" + str(barChart))
         
         # Print out the bar chart. Only print the last 20 bars
#         if not offLine:
#            bc.displayLastNBars(barChart, 20)
         
         # Do on close processing
         a.setActionOnCloseBar()
         #positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
         positionTaken = a.takePosition(bid, ask, last, barChart[barCtr][vl], barChart, barCtr)
         a.unsetActionOnCloseBar()

         exitVal = isStoppedOut(positionTaken)
         if exitVal > 0:
            exit(exitVal)
            
         #if not offLine:
         bc.appendBar(barChart)
         
         # Keep track of the bars in a position
         if a.inPosition():
            bc.setBarsInPosition()
            
         # End of bar reached. 

         lg.debug ("Stock: " + str(stock) + "\n")
         lg.debug ("Last price: " + str(last) + " Position: " + str(positionTaken))
         lg.debug ("Average Volume: " + str(bc.getAvgVol()))
         lg.debug ("Average Bar length: " + str(bc.getAvgBarLen()))

         lg.info ("\nSYM: " + str(stock))
         lg.info ("BAR: " + str(barCtr))
         lg.info ("HI: " + str(barChart[barCtr][hi]))
         lg.info ("LO: " + str(barChart[barCtr][lo]))
         lg.info ("OPEN: " + str(barChart[barCtr][op]))
         lg.info ("CLOSE: " + str(barChart[barCtr][cl]))
         lg.info ("LAST: " + str(last))
         lg.info ("BID: " + str(bid))
         lg.info ("ASK:  " + str(ask))
         
         if offLine:
            lg.debug("END TIME: " + bc.getTimeStampFromBarchartFile(barCtr))
            #lg.debug ("END TIME: " + str(barChart[barCtr][dt]))
         else:
            lg.debug ("END TIME: " + str(cn.getTimeStamp()))
            
         lg.debug ("VOL: " + str(barChart[barCtr][vl]) + "\n")
         
         barCtr += 1

         lg.debug ("\nSTART NEW BAR " + str(barCtr) + " ====================================\n")

         vol = 0
         break
         
         # End of bar Start next bar
         
      lg.debug ("positionTaken before " + str(positionTaken))

      # Take a position if conditions exist
      positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
      
      lg.debug ("positionTaken after " + str(positionTaken))
      
      exitVal = isStoppedOut(positionTaken)
      if exitVal > 0:
         exit(exitVal)
         
      # Stop trading at the end of the day
      if not offLine and not a.getAfterMarket():
         if a.isMarketExitTime():
            if a.inPosition():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
            bc.loadEndBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, tradeVol)
   
      # end bar loop. 390 bars for 1 min chart
   # end execution loop

