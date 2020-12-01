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
testMode = 0

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
   
parser.add_option("-e", "--testMode",
   action="store_true", dest="testMode", help="testMode, used for automated testing")
   
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

barChart = [[]]

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
quitMaxProfit = float(d["profileTradeData"]["quitMaxProfit"])
workPath = str(d["profileTradeData"]["workPath"])
doRangeTradeBars = str(d["profileTradeData"]["doRangeTradeBars"])
gainTrailStop = str(d["profileTradeData"]["gainTrailStop"])
quickProfitPctTrigger = float(d["profileTradeData"]["quickProfitPctTrigger"])

offLine = int(c["profileConnectET"]["offLine"])
sandBox = int(c["profileConnectET"]["sandBox"])

symbol = currency + alt

marketDataType = "intraday"
numBars = 0

lastMinuteOfLiveTrading = 155930

marketOpen = 0

stoppedOut = 4

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

if clOptions.offLine:
   offLine = clOptions.offLine

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

logPath = logPath.replace(".json", stock + ".log")
debugPath = debugPath.replace(".json", stock + ".debug")
barChartPath = barChartPath.replace(".json", stock + ".bc")
pricesPath = pricesPath.replace(".json", stock + ".pr")
testPath = testPath.replace(".json", stock + ".tt")

if service == "eTrade":
   symbol = stock

lg = lpl.Log(debug, verbose, logPath, debugPath, offLine, testMode)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

if service == "bitstamp":
   cn = lpl.ConnectBitStamp(service, currency, alt)
   cn.connectPublic()
elif service == "bitfinex":
   cn = lpl.ConnectBitFinex()
elif service == "eTrade":
   symbol = stock
   cn = lpl.ConnectEtrade(c, stock, debug, verbose, marketDataType, sandBox, offLine)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm,  barcharts objects

bc = lpl.Barchart()
tr = lpl.Trends(d, lg, cn, bc, offLine)
lm = lpl.Limits(d, lg, cn, bc, offLine)
pa = lpl.Pattern(d, bc)
pr = lpl.Price(cn, offLine)
a = lpl.Algorithm(d, lg, cn, bc, tr, lm, pa, pr, offLine, stock)

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

with open(barChartPath, "a+", encoding="utf-8") as resumeFile:
   lg.info("Using " + barChartPath + " as bar chart file")

with open(pricesPath, "a+", encoding="utf-8") as priceFile:
   lg.info("Using " + pricesPath + " as prices file")

barChart = bc.init()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Display profile data

lg.info ("Reading profileTrade data from: " + clOptions.profileTradeDataPath + "\n")
lg.info ("Using symbol: " + symbol)
lg.info ("Last trade: " + str(cn.getLastTrade(stock)))
lg.info ("Minute bar chart: " + str(timeBar))
lg.info ("openBuyBars: " + str(openBuyBars))
lg.info ("closeBuyBars: " + str(closeBuyBars))
lg.info ("openSellBars: " + str(openSellBars))
lg.info ("closeSellBars: " + str(closeSellBars))
lg.info ("doRangeTradeBars: " + str(doRangeTradeBars))
lg.info ("tradingDelayBars: " + str(tradingDelayBars))
lg.info ("sand: " + str(sandBox))
lg.info ("offLine: " + str(offLine))
lg.info ("marketDataType: " + cn.getMarketDataType())
lg.info ("dateTimeUTC: " + cn.getDateTimeUTC())
lg.info ("dateTime: " + cn.getDateTime())
lg.info ("getQuoteStatus: " + cn.getQuoteStatus())
lg.info ("workPath: " + workPath)
lg.info (a.getAlgorithmMsg())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize based on live or offLine state 

cn.setValues(barChart, barCtr, bid, ask, last, vol)

numPrices = 0

# Fill buffers with prices
if offLine:
   numPrices = pr.initPriceBuffer(pricesPath)
   if not numPrices:
      lg.error("Trying to read an empty prices chart: " + pricesPath)
      exit(1)
   #pr.skipFirstBar(numPrices, timeBar)
   lg.debug ("number of prices from file: " + str(numPrices))

# Set the initial price
#if not offLine:
#   bid, ask, last, vol = pr.getNextPrice(barChart, numBars, barCtr)

# Read in barChart and resume from it
if resume:
   bcSize = pathlib.Path(barChartPath).stat().st_size
   
   lg.debug ("Size of barchart file : " + str(bcSize))

   # Ignore reading from barChart if it is empty
   if bcSize:
      numBars = bc.read(barChartPath, barChart, timeBar)
      if not numBars:
         lg.error("Trying to read an empty bar chart: " + barChartPath)
         exit(1)
      
      lg.debug ("Number of bars in file on disk : " + str(numBars))
      
      b = 0
      while b < numBars:
         lg.debug (str(barChart[b]))
         b += 1
         
   # We're live, program halted and now resumed. Initilize a new bar and trade on
   if not offLine:
      bc.appendBar(barChart)
      
lg.debug ("Start bar: " + str(barCtr))

# Start trading at the top of the minute
if not offLine:
   tm.waitUntilTopMinute()
   if a.doPreMarket():
      tm.waitUntilTopMinute()

lm.setTradingDelayBars(timeBar)

# This counter matches the bar number displayed in etrade
barInfoCtr = 2

if offLine:
   pr.setNextBar(timeBar)

dirtyProfit = 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever. Pause trading during and after market hours 

while True:

   # Start trading at beginning of day
   if not a.doPreMarket():
      if not offLine and not marketOpen:
         if a.getMarketBeginTime():
            lg.info("Waiting till the market opens...")
            cn.waitTillMarketOpens(a.getMarketOpenTime())
            marketOpen += 1

   if not offLine:
      sleep(0.1)

   endBarLoopTime = cn.adjustTimeToTopMinute(cn.getTimeHrMnSecs() + (100 * int(timeBar)))
   
   if offLine:
      lg.debug ("Start time: " + str(bc.getTimeFromFile(barChart, barCtr)) + "\n")
   else:
      lg.debug ("End bar time : " + str(endBarLoopTime))
      lg.debug ("Start time: " + str(cn.getTimeStamp()))
         
   initialVol = cn.getVolume()
   
   if not offLine:
         bc.loadInitBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, initialVol)

   if offLine:
      pr.setNextBar(timeBar)
      
   #a.setCurrentBar(barCtr)
      
   dirty = doOnceOnOpen = doOnceOnClose = 0
            
   if offLine:
      if barCtr == 0:
         pr.findStartPriceIdx(numPrices, timeBar)
         barCtr = 1
         
   a.setNextBar(barCtr + 1)

   a.setAllLimits(barChart, barCtr)

   while True:
               
      # Set the values from the trading service
      cn.setValues(barChart, barCtr, bid, ask, last, vol)

      bid, ask, last, vol = pr.getNextPrice(barChart, numBars, barCtr)
      
      a.setCurrentBid(bid)
      a.setCurrentAsk(ask)
      a.setCurrentLast(last)
      a.setCurrentVol(vol)

      # Do one time on open
      if not doOnceOnOpen:
         a.setActionOnOpenBar()
         positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
         doOnceOnOpen += 1
         a.unsetActionOnOpenBar()
         
      if quitMaxProfit and positionTaken == stoppedOut:
         # We are out with our PROFIT
          exit (2)
             
      if offLine:
         if barCtr > numBars or last == pr.getLastToken():
            if a.inPosition():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
            if a.getTotalGain() >= a.getTargetProfit():
               exit(2)
            else:
               exit(0)

      # Set the profit to gain
      if not dirtyProfit:
         if quitMaxProfit > 0:
            dirtyProfit += 1
            a.setTotalProfit(last, quitMaxProfit)
            lg.debug("Max profit set to: " + str(a.getTargetProfit()))
            
      tradeVol = cn.getVolume() - initialVol
      
      if not offLine:
         bc.loadBar(barChart, tradeVol, barCtr, bid, ask, last)
   
      # Halt program at end of trading day
      if not offLine and a.isMarketExitTime():
         if not a.getAfterMarket():
            if a.inPosition():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
               
            # Write last bar
            bc.write(barChart, barChartPath, barCtr)
            lg.info("Program exiting due to end of day trading")
            # bc.fixSessionHiLo(barChartPath)
            
            #if a.getTotalGain() >= a.getTargetProfit():
            #   exit(2)
            #else:
            exit(0)
         
      if quitMaxProfit > 0.0:
         if a.getTotalGain() >= a.getTargetProfit():
            lg.info ("QUITTING MAX PROFIT REACHED Gain: " + str(a.getTotalGain()) + " " + str(barCtr))
            lg.info ("MAX PROFIT TARGET: " + str(a.getTargetProfit()))
            lg.info ("MAX PROFIT PRICE: " + str(last))
            lg.info ("MAX PROFIT Bar: " + str(barCtr))
            lg.info ("MAX PROFIT    Time: " + str(cn.getTimeStamp()))
            
            if quitMaxProfit and positionTaken == stoppedOut:
               # We are out with our PROFIT
                exit (2)
            
      # Save off the prices so they can be later used in offLine mode
      if not offLine:
         # Write prices and barcharts for 1-5 min charts
         pr.write(pricesPath, ask, bid, last, vol, barCtr, write1_5MinData)
         
      # Beginning of next bar. 2nd clause is for offline mode
      if cn.getTimeHrMnSecs() >= endBarLoopTime or pr.isNextBar(timeBar):      

         # Only do this section once
         if dirty:
            continue
            
         dirty += 1
               
         if not offLine:
            bc.loadEndBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, tradeVol)
               
         # Print out the bar chart. Only print the last 20 bars
         if not offLine:
            bc.write(barChart, barChartPath, barCtr)
            bc.displayLastNBars(barChart, 20)
                           
         a.setActionOnCloseBar()
         positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)
         a.unsetActionOnCloseBar()
         
         if quitMaxProfit and positionTaken == stoppedOut:
            # We are out with our PROFIT
             exit (2)
            
         if not offLine:
            bc.appendBar(barChart)
         
         # Keep track of the bars in a position
         if a.inPosition():
            bc.setBarsInPosition()
            
         # End of bar reached. Done with on close processing

         lg.info ("Stock: " + str(stock) + "\n")
         lg.info ("Last price: " + str(last) + " Position: " + str(positionTaken))
         lg.info ("Average Volume: " + str(bc.getAvgVol()))
         lg.info ("Average Bar length: " + str(bc.getAvgBarLen()))

         lg.info ("\nSYM: " + str(stock))
         lg.info ("BAR: " + str(barInfoCtr))
         lg.info ("HI: " + str(barChart[barCtr][hi]))
         lg.info ("LO: " + str(barChart[barCtr][lo]))
         lg.info ("OPEN: " + str(barChart[barCtr][op]))
         lg.info ("CLOSE: " + str(barChart[barCtr][cl]))
         lg.info ("LAST: " + str(last))
         lg.info ("BID: " + str(bid))
         lg.info ("ASK:  " + str(ask))
         lg.info ("TIME: " + str(barChart[barCtr][dt]))
         lg.info ("VOL: " + str(barChart[barCtr][vl]) + "\n")
         #lg.info ("VOL : " + str(vol) + "\n")
                  
         barInfoCtr += 1
         
         print ("\nSTART NEW BAR " + str(barInfoCtr) + " ====================================\n")

         barCtr += 1
         
         break
      
      # COMBINE THESE TWO AND JUST CALL ready()
      
      # Wait till next bar before trading if set
      # if not a.inPosition() and a.getWaitForNextBar() and barCtr < a.getNextBar():
         
      if a.getWaitForNextBar() and barCtr < a.getNextBar():
         lg.debug("Waiting for next bar...")
         continue
         
#      if a.quickProfitMax:
#         if a.quickProfitCtr > a.quickProfitMax:
#            lg.debug("Waiting for next bar. quickProfitCtr > max: " + str(a.quickProfitCtr) + " max: " + str(a.quickProfitMax))
#            a.quickProfitCtr = 0
#            a.setWaitForNextBar()
#            continue

      #if a.inPosition() and barCtr < a.getNextBar():
      #   lg.debug("In a position. Waiting for next bar...")
      #   continue

      # Take a position if conditions exist
      positionTaken = a.takePosition(bid, ask, last, vol, barChart, barCtr)

      if quitMaxProfit and positionTaken == stoppedOut:
         # We are out with our PROFIT
          exit (2)
   # end bar loop

      # Stop trading at the end of he day
      if not offLine and not a.getAfterMarket():
         if a.inPosition():
            if a.isMarketExitTime():
               a.closePosition(barCtr, barChart, bid, ask, forceClose)
               bc.loadEndBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last, tradeVol)

      # th = Thread(a.logIt(action, str(a.getBarsInPosition()), tm.now(), logPath))
      # Write to log file
      
   #if barCtr == 20: break
   
# end execution loop

