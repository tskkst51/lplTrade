## loop reading lpltG writes

import pyetrade
import sys
import os
import io
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
def waitForPopulatedPrices(pricesPath, barChartPath):

   while True:
      if not os.path.exists(pricesPath):
         sleep(0.001)
         continue
                  
      if pathlib.Path(pricesPath).stat().st_size < 5:
         sleep(0.001)
         continue
   
      barChartFD = open(barChartPath, 'r', os.O_NONBLOCK)
      lg.info("Using " + barChartPath + " as bar chart file")
   
      pricesFD = open(pricesPath, 'r', os.O_NONBLOCK)
      lg.info("Using " + pricesPath + " as process file")
      break
      
   return pricesFD, barChartFD
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def isStoppedOut():

   if a.getTotalGain() >= a.getTargetProfit() and a.getTotalGain() != 0.0:
      if quitMaxProfit:            
         lg.info ("MAX PROFIT REACHED, Gain: Bar: " + str(a.getTotalGain()) + " " + str(barCtr))
         lg.info ("MAX PROFIT TARGET: " + str(a.getTargetProfit()))
         lg.info ("MAX PROFIT FACTOR: " + str(maxProfit))
         lg.info ("MAX PROFIT CLOSE PRICE: " + str(last))
         lg.info ("MAX PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 2
         
         # We are out with our PROFIT
      if doTrailingStop and positionTaken == stoppedOut:
         lg.info ("TRAILING STOP REACHED, Gain: Bar: " + str(a.getTotalGain()) + " " + str(barCtr))
         lg.info ("MAX PROFIT TARGET: " + str(a.getTargetProfit()))
         lg.info ("MAX PROFIT FACTOR: " + str(maxProfit))
         lg.info ("MAX PROFIT CLOSE PRICE: " + str(last))
         lg.info ("MAX PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 4
   return 0

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

offLine = 0
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

stock = str(d["profileTradeData"]["stock"])
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
resume = str(d["profileTradeData"]["resume"])
workPath = str(d["profileTradeData"]["workPath"])
doRangeTradeBars = str(d["profileTradeData"]["doRangeTradeBars"])
gainTrailStop = str(d["profileTradeData"]["gainTrailStop"])
quickProfitPctTrigger = float(d["profileTradeData"]["quickProfitPctTrigger"])
doTrailingStop = int(d["profileTradeData"]["doTrailingStop"])
maxProfit = float(d["profileTradeData"]["maxProfit"])
quitMaxProfit = int(d["profileTradeData"]["quitMaxProfit"])
marketEndTime = int(d["profileTradeData"]["marketEndTime"])

sandBox = int(c["profileConnectET"]["sandBox"])
#offLine = int(c["profileConnectET"]["offLine"])

symbol = currency + alt

marketDataType = "intraday"
numBars = 0

lastMinuteOfLiveTrading = 155930

marketOpen = 0

stoppedOut = 4
exitMaxProfit = 2

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
   d["profileTradeData"]["stock"] = str(stock)
   
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

if clOptions.slave:
   slave = clOptions.slave

if clOptions.timeBar:
   timeBar = int(clOptions.timeBar)
   d["profileTradeData"]["timeBar"] = str(timeBar)
   
if clOptions.workPath:
   workPath = clOptions.workPath
   d["profileTradeData"]["workPath"] = str(workPath)

exitMaxProfit = clOptions.exitMaxProfit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log and debug file based on profileTradeData name and path
# Write header data to logs

tm = lpl.Time()

# Setup paths

if workPath:
   os.chdir(workPath)

logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
debugPath = clOptions.profileTradeDataPath.replace("profiles", "debug")
barChartPath = clOptions.profileTradeDataPath.replace("profiles", "bc")
pricesPath = clOptions.profileTradeDataPath.replace("profiles", "prices")
testPath = clOptions.profileTradeDataPath.replace("profiles", "test")

if stock in clOptions.profileTradeDataPath:
   logPath = logPath.replace(".json_" + stock, stock + ".ls")
   debugPath = debugPath.replace(".json_" + stock, stock + ".ds")
   barChartPath = barChartPath.replace(".json_" + stock, stock + ".bc")
   pricesPath = pricesPath.replace(".json_" + stock, stock + ".pr")
   testPath = testPath.replace(".json_" + stock, stock + ".tt")
else:
   logPath = logPath.replace(".json", stock + ".ls")
   debugPath = debugPath.replace(".json", stock + ".ds")
   barChartPath = barChartPath.replace(".json", stock + ".bc")
   pricesPath = pricesPath.replace(".json", stock + ".pr")
   testPath = testPath.replace(".json", stock + ".tt")

if service == "eTrade":
   symbol = stock

lg = lpl.Log(debug, verbose, logPath, debugPath, 0)

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
   cn = lpl.ConnectEtrade(c, stockArr, debug, verbose, marketDataType, sandBox, slave)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm,  barcharts objects

bc = lpl.Barchart()
tr = lpl.Trends(d, lg, cn, bc, slave)
lm = lpl.Limits(d, lg, cn, bc, slave, symbol)
pa = lpl.Pattern(d, bc, lg)
pr = lpl.Price(cn, slave)
a = lpl.Algorithm(d, lg, cn, bc, tr, lm, pa, pr, slave, stock)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize files

lg.info("Using " + pricesPath + " as prices file")

with open(debugPath, "a+", encoding="utf-8") as debugFile:
   debugFile.write(lg.infoStamp(a.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
   debugFile.write(lg.header(tm.now(), stock))

lg.info("Using " + debugPath + " as debug file")

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.infoStamp(a.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
   logFile.write(lg.header(tm.now(), stock))

lg.info("Using " + logPath + " as log file")

pricesFD, barChartFD = waitForPopulatedPrices(pricesPath, barChartPath)

#if slave:
#   # Verify files are plump
#   for path in pricesPath, barChartPath:
#      if not os.path.exists(path):
#         lg.error("Trying to read a file that doesn't exist: " + path)
#         exit(1)
#      else:
#         if not os.path.getsize(path):
#            lg.error("Trying to read an empty file: " + path)
#            exit(1)

barChart = {}

for stock in stockArr:
   lg.debug ("stock " + str(stock))
   barChart = bc.init()
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Display profile data

lg.info ("Reading profileTrade data from: " + clOptions.profileTradeDataPath + "\n")
lg.info ("Using symbol: " + symbol)
lg.info ("Last trade: " + str(cn.getLastTrade(stock)))
lg.info ("Minute chart: " + str(timeBar))
lg.info ("openBuyBars: " + str(openBuyBars))
lg.info ("closeBuyBars: " + str(closeBuyBars))
lg.info ("openSellBars: " + str(openSellBars))
lg.info ("closeSellBars: " + str(closeSellBars))
lg.info ("doRangeTradeBars: " + str(doRangeTradeBars))
lg.info ("tradingDelayBars: " + str(tradingDelayBars))
lg.info ("sand: " + str(sandBox))
lg.info ("slave: " + str(slave))
lg.info ("marketDataType: " + cn.getMarketDataType())
lg.info ("dateTimeUTC: " + cn.getDateTimeUTC())
lg.info ("dateTime: " + cn.getDateTime())
lg.info ("getQuoteStatus: " + cn.getQuoteStatus())
lg.info ("workPath: " + workPath)
lg.info (a.getAlgorithmMsg())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize based on live or state 

#lg.debug ("profileValues\n" + str(d))
#lg.debug ("serviceValues\n" + str(serviceValues))

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

if not offLine:
   pricesFD.seek(0, io.SEEK_END)

lg.debug ("Start bar: " + str(barCtr))

# Start trading at the top of the minute
#if not slave:
#   tm.waitUntilTopMinute()
#   if a.doPreMarket():
#      tm.waitUntilTopMinute()

lm.setTradingDelayBars()
bc.setTimeBarValue(timeBar)

dirtyProfit = 0

if (quitMaxProfit or doTrailingStop) and maxProfit == 0.0:
   lg.info ("Max profit not set! ")
   exit (2)

bid, ask, last, vol = pr.readNextPriceLine(pricesFD, pricesPath)

barCtr = 0

pr.initSlaveBar()

bcSize = pathlib.Path(barChartPath).stat().st_size
lg.debug ("Size of barchart file : " + str(bcSize))

# Ignore reading from barChart if it is empty
if bcSize:
   numBars = bc.read(barChartPath, barChart, timeBar)
   if not numBars:
      lg.debug("Trying to read an empty bar chart: " + barChartPath)
   
   lg.debug ("Number of bars in file on disk : " + str(numBars))
   barCtr = numBars

# Init new bar

lg.debug ("bid " + str(bid))
lg.debug ("ask "+ str(ask))
lg.debug ("last " + str(last))
lg.debug ("vol " + str(vol))

bc.appendBar(barChart)
#bc.loadInitBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, vol)

lg.debug ("Adjusted start bar: " + str(barCtr))

# Start trading at beginning of day
if not a.doPreMarket():
   if not marketOpen:
      if a.getMarketBeginTime():
         lg.info("Waiting till the market opens...")
         cn.waitTillMarketOpens(a.getMarketOpenTime())
         marketOpen += 1

endBarLoopTime = cn.adjustTimeToTopMinute(cn.getTimeHrMnSecs() + (100 * int(timeBar)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever. Pause trading during and after market hours 

while True:
         
   #initialVol = cn.getTotalVolume(stock)
   #initialVol = cn.getVolume()
   #initialVol = 0
   
   bc.loadInitBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, vol)

   lg.debug ("barCtr  " + str(barCtr))
         
   pr.setNextBar(timeBar)
      
   dirty = doOnceOnOpen = doOnceOnClose = 0
            
   a.setAllLimits(barChart, barCtr)

   tradeVol = 0 
   
   while True:
      bid, ask, last, vol = pr.readNextPriceLine(pricesFD, pricesPath)
      
      #cn.setValues(barChart, barCtr, bid, ask, last, vol)
      
      a.setCurrentBid(bid)
      a.setCurrentAsk(ask)
      a.setCurrentLast(last)
      
      # Set the values from the trading service
      lg.debug ("bid " + str(bid))
      lg.debug ("ask "+ str(ask))
      lg.debug ("last " + str(last))
      lg.debug ("vol " + str(vol))
      lg.debug ("barCtr " + str(barCtr))
      
      # Count the number of 0.0 bids/asks. If more than 5 quit. Stock is crap.
      if bid == 0.0 and ask == 0.0 and last == 0.0 and vol == 0:
         lg.debug ("numZeroPrices " + str(numZeroPrices))
         numZeroPrices += 1
         
      if numZeroPrices > 15 and not positionTaken:
      #if numZeroPrices > 25:
         lg.debug ("numZeroPrices " + str(numZeroPrices) + " exiting")
         #exit (1)
         
      # Set the profit to gain
      if not dirtyProfit:
         a.setTargetProfit(last, maxProfit)
         lg.debug("Min profit set to: " + str(a.getTargetProfit()))
         dirtyProfit += 1

      # Do one time on open
      if not doOnceOnOpen:
         a.setActionOnOpenBar()
         positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
         doOnceOnOpen += 1
         a.unsetActionOnOpenBar()

      exitVal = isStoppedOut()
      if exitVal > 0:
         exit(exitVal)
      
      if offLine:
         if barCtr > numBars or last == pr.getLastToken():
            if a.inPosition():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
            if a.getTotalGain() >= a.getTargetProfit():
               exit(2)
            else:
               exit(0)
         
      #tradeVol = vol - initialVol
      #tradeVol = cn.getVolume() - initialVol
      #tradeVol = cn.getCurrentVolume(stock) - initialVol
      
      tradeVol = a.getCurrentRunningVol()
      if tradeVol != 0:
         lastVol = tradeVol
         
      lg.debug ("tradeVol " + str(tradeVol))
      
      #tradeVol = cn.getTotalVolume(stock) - initialVol
      
      #lg.debug ("barChart " + str(barChart))
      #lg.debug ("barChart[barCtr " + str(barChart[barCtr]))
      lg.debug ("barCtr " + str(barCtr))
      lg.debug ("last " + str(last))

      bc.loadBar(barChart, tradeVol, barCtr, bid, ask, last)   
      
      # Halt program at end of trading day
      if a.isMarketExitTime():
         lg.debug ("It's beer thirty!! ")
         if not a.getAfterMarket():
            if a.inPosition():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
            lg.info("Program exiting due to end of day trading")
            exit(0)
      
      quitBar = 0
      
      lg.debug ("cn.getTimeHrMnSecs() " + str(cn.getTimeHrMnSecs()))
      lg.debug ("endBarLoopTime " + str(endBarLoopTime))
      
      if offLine:
         lg.debug ("pr.isLastBar(timeBar) " + str(pr.isLastBar(timeBar)))
         quitBar = pr.isLastBar(timeBar)
      else:
         quitBar = pr.isLastBarSlave(timeBar)
         lg.debug ("pr.isLastBarSlave(timeBar) " + str(pr.isLastBarSlave(timeBar)))

      lg.debug ("pr.isNextBarSlave(timeBar) " + str(pr.isNextBarSlave(timeBar)))
      # Beginning of next bar. 2nd clause is for mode
      #if cn.getTimeHrMnSecs() >= endBarLoopTime or pr.isLastBarSlave(timeBar):      
      #if cn.getTimeHrMnSecs() >= endBarLoopTime or pr.isLastBar(timeBar):      
      #if cn.getTimeHrMnSecs() >= endBarLoopTime or pr.isNextBarSlave(timeBar) or quitBar:      
      if pr.isNextBarSlave(timeBar) or quitBar:      

         # Only do this section once
         if dirty:
            continue
            
         dirty += 1
               
         #lg.debug ("barChart before end bar" + str(barChart))

         bc.displayLastNBars(barChart, 20)

         bc.loadEndBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, lastVol)
         
         #lg.debug ("barChart after end bar" + str(barChart))
         
         # Print out the bar chart. Only print the last 20 bars
         bc.displayLastNBars(barChart, 20)
         
         # Do on close processing
         a.setActionOnCloseBar()
         positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
         a.unsetActionOnCloseBar()

         exitVal = isStoppedOut()
         if exitVal > 0:
            exit(exitVal)
            
         bc.appendBar(barChart)
         
         # Keep track of the bars in a position
         if a.inPosition():
            bc.setBarsInPosition()
            
         # End of bar reached. 

         lg.info ("Stock: " + str(stock) + "\n")
         lg.info ("Last price: " + str(last) + " Position: " + str(positionTaken))
         lg.info ("Average Volume: " + str(bc.getAvgVol()))
         lg.info ("Average Bar length: " + str(bc.getAvgBarLen()))

         lg.info ("\nSYM: " + str(stock))
         lg.info ("BAR: " + str(barCtr))
         lg.info ("HI: " + str(barChart[barCtr][hi]))
         lg.info ("LO: " + str(barChart[barCtr][lo]))
         lg.info ("OPEN: " + str(barChart[barCtr][op]))
         lg.info ("CLOSE: " + str(barChart[barCtr][cl]))
         lg.info ("LAST: " + str(last))
         lg.info ("BID: " + str(bid))
         lg.info ("ASK:  " + str(ask))
         #lg.info ("END TIME: " + str(barChart[barCtr][dt]))
         lg.info ("END TIME: " + str(tm.now()))
         lg.info ("VOL: " + str(barChart[barCtr][vl]) + "\n")
         
         barCtr += 1

         lg.debug ("\nSTART NEW BAR " + str(barCtr) + " ====================================\n")

         vol = 0
         break

      lg.debug ("positionTaken before " + str(positionTaken))

      # Take a position if conditions exist
      positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
      
      lg.debug ("positionTaken after " + str(positionTaken))
      
      exitVal = isStoppedOut()
      if exitVal > 0:
         exit(exitVal)
         
      # Stop trading at the end of he day
      if not a.getAfterMarket():
         if a.inPosition():
            if a.isMarketExitTime():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
               bc.loadEndBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, tradeVol)

      # th = Thread(a.logIt(action, str(a.getBarsInPosition()), tm.now(), logPath))
      # Write to log file
      
   #if barCtr == 20: break
   
# end execution loop

