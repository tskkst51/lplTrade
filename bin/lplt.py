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

parser.add_option("-s", "--stock", type="string",
   action="store", dest="stock", default=False,
   help="stock to bua/selly: AAPL")
   
parser.add_option("-u", "--currency", type="string",
   action="store", dest="currency", default=False,
   help="currency to buy: btc... eth... bch...")

parser.add_option("-v", "--verbose",
   action="store_true", dest="verbose", help="verbose")
   
parser.add_option("-t", "--timeBar", type="string",
   action="store", dest="timeBar", default=False,
   help="time bar: 1 5 10 minute...")
   
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
forceClose = 1

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
usePricesFromFile = int(d["profileTradeData"]["usePricesFromFile"])
write1_5MinData = int(d["profileTradeData"]["write1_5MinData"])
quitMaxProfit = float(d["profileTradeData"]["quitMaxProfit"])

offLine = int(c["profileConnectET"]["offLine"])
sandBox = int(c["profileConnectET"]["sandBox"])

symbol = currency + alt

marketDataType = "intraday"
numBars = 0

lastMinuteOfLiveTrading = 155930

marketOpen = 0

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
   timeBar = clOptions.timeBar
   d["profileTradeData"]["timeBar"] = str(timeBar)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log and debug file based on profileTradeData name and path
# Write header data to logs

tm = lpl.Time()

# Create minute profile variables
profile1m = clOptions.profileTradeDataPath
profile2m = clOptions.profileTradeDataPath.replace("active", "active2m")
profile3m = clOptions.profileTradeDataPath.replace("active", "active3m")
profile4m = clOptions.profileTradeDataPath.replace("active", "active4m")
profile5m = clOptions.profileTradeDataPath.replace("active", "active5m")

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

logPath += stock + ".log"
debugPath += stock + ".debug"
barChartPath += stock + ".bc"
pricesPath += stock + ".pr"

if service == "eTrade":
   symbol = stock

lg = lpl.Log(debug, verbose, logPath, debugPath, offLine)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

if service == "bitstamp":
   cn = lpl.ConnectBitStamp(service, currency, alt)
   cn.connectPublic()
elif service == "bitfinex":
   cn = lpl.ConnectBitFinex()
elif service == "eTrade":
   symbol = stock
   cn = lpl.ConnectEtrade(c, lg, stock, debug, verbose, marketDataType, sandBox, offLine)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm,  barcharts objects

bc = lpl.Barchart()
a = lpl.Algorithm(d, lg, cn, bc, offLine)
pr = lpl.Price(a, cn, usePricesFromFile, offLine, a.getMarketBeginTime())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize files

#date = cn.getDateMonthDayYear()

#logPath += stock + "_" + str(date) + ".log"
#debugPath += stock + "_" + str(date) + ".debug"
#barChartPath += stock + "_" + str(date) + ".bc"
#pricesPath += stock + "_" + str(date) + ".pr"

print ("Prices path: " + pricesPath)

with open(debugPath, "a+", encoding="utf-8") as debugFile:
   debugFile.write(lg.infoStamp(a.getLiveProfileValues(d)))
   debugFile.write(lg.header(tm.now()))

lg.info("Using " + debugPath + " as debug file")

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.infoStamp(a.getLiveProfileValues(d)))
   logFile.write(lg.header(tm.now()))

lg.info("Using " + logPath + " as log file")

with open(barChartPath, "a+", encoding="utf-8") as resumeFile:
   lg.info("Using " + barChartPath + " as bar chart file")

with open(pricesPath, "a+", encoding="utf-8") as priceFile:
   lg.info("Using " + pricesPath + " as prices file")

barChart = bc.init()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Display profile data

lg.info ("Reading profileTrade data from:\n" + clOptions.profileTradeDataPath + "\n")
lg.info ("Using symbol: " + symbol)
lg.info ("Last trade: " + str(cn.getLastTrade()))
lg.info ("Minute bar chart: " + str(timeBar))
lg.info ("openBuyBars: " + str(openBuyBars))
lg.info ("closeBuyBars: " + str(closeBuyBars))
lg.info ("openSellBars: " + str(openSellBars))
lg.info ("closeSellBars: " + str(closeSellBars))
lg.info ("tradingDelayBars: " + str(tradingDelayBars))
lg.info ("sand: " + str(sandBox))
lg.info ("offLine: " + str(offLine))
lg.info ("marketDataType: " + cn.getMarketDataType())
lg.info ("dateTimeUTC: " + cn.getDateTimeUTC())
lg.info ("dateTime: " + cn.getDateTime())
lg.info ("getQuoteStatus: " + cn.getQuoteStatus())
lg.info (a.getAlgorithmMsg())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize based on live or offLine state 

cn.setValues(barChart, barCtr, ask, bid)

# Fill buffers with prices
if usePricesFromFile and offLine:
   numPrices = pr.initPriceBuffer(pricesPath)
   barIdx = pr.skipFirstBar(numPrices)
   lg.debug ("number of prices from file: " + str(numPrices))

# Set the initial price
if not offLine:
   last, bid, ask = pr.getNextPrice(barChart, numBars, barCtr)

# Read in barChart and resume from it
if resume:
   bcSize = pathlib.Path(barChartPath).stat().st_size
   
   lg.verbose ("Size of barchart file : " + str(bcSize))

   # Ignore reading from barChart if it is empty
   if bcSize:
      numBars = bc.read(barChartPath, barChart)
      
      lg.verbose ("Number of bars in file on disk : " + str(numBars))
      barCtr = numBars
      
      bc.displayLastNBars(barChart, numBars)

   # If offline then iterate over the stored bar chart starting at bar 0
   if usePricesFromFile and offLine:
      barCtr = 0
         
   # We're live, program halted and now resumed. Initilize a new bar and trade on
   else:
      bc.appendBar(barChart)
      a.setAllLimits(barChart, barCtr)
      
lg.debug ("Start bar: " + str(barCtr))

# Start trading at the top of the minute
if not offLine:
   tm.waitUntilTopMinute()
   if a.doPreMarket():
      tm.waitUntilTopMinute()
   if write1_5MinData:
      pr.initWrite(pricesPath)
      bc.initWrite(barChartPath)

a.setTradingDelayBars()

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
      
   # Set the initial loop time from the profile
   if write1_5MinData:
      # Use the 1 min chart and save data for 1-5 min charts
      timeBar = 1
      endBarLoopTime = cn.adjustTimeToTopMinute(cn.getTimeHrMnSecs() + (100 * timeBar))
   else:
      endBarLoopTime = cn.adjustTimeToTopMinute(cn.getTimeHrMnSecs() + (100 * timeBar))

   lg.debug ("Time : " + str(cn.getTimeHrMnSecs()))
   lg.debug ("End bar time : " + str(endBarLoopTime))
      
   if offLine:
      if usePricesFromFile:
         if barCtr >= numBars - 1:
            if a.inPosition():
               a.closePosition(barCtr, barChart, forceClose)
            exit()
         
   lg.debug ("End bar time : " + str(endBarLoopTime))
   lg.debug ("Start time: " + str(cn.getTimeStamp()))
         
   initialVol = cn.getVolume()
   
   if not offLine:
         bc.loadInitBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last)
   
   a.setCurrentBar(barCtr)
   a.setNextBar(barCtr + 1)
   dirty = 0
            
   # Loop until each bar has ended
   
   while True:
      
      # Set the values from the trading service
      cn.setValues(barChart, barCtr, ask, bid)
      
      a.unsetActionOnNewBar()
      
      last, bid, ask = pr.getNextPrice(barChart, numBars, barCtr)

      # Set the profit to gain
      if not dirtyProfit:
         if quitMaxProfit > 0.0:
            dirtyProfit += 1
            a.setTotalProfit(last, quitMaxProfit)
            lg.debug("Max profit set to: " + str(a.getTotalProfit()))

      lg.info ("\nBAR : " + str(barCtr))
      lg.info ("HI  : " + str(barChart[barCtr][hi]))
      lg.info ("LAST: " + str(last))
      lg.info ("BID : " + str(bid))
      lg.info ("ASK:  " + str(ask))
      lg.info ("LO  : " + str(barChart[barCtr][lo]) + "\n")
      
      tradeVolume = cn.getVolume() - initialVol
         
      if not offLine:
         bc.loadBar(barChart, tradeVolume, barCtr, bid, ask, last)
   
      # Halt program at end of trading day
      if cn.getTimeHrMnSecs() > lastMinuteOfLiveTrading:
         if not offLine and not a.getAfterMarket():
            if a.inPosition():
               a.closePosition(barCtr, barChart, forceClose)
            lg.info("Program exiting due to end of day trading")
            exit()
         
      if quitMaxProfit > 0.0:
         if a.getTotalGain() >= a.getTotalProfit():
            lg.info ("QUITTING MAX PROFIT REACHED Gain: " + str(a.getTotalGain()))
            lg.info ("Bar: " + str(barCtr))
            lg.info ("Time: " + str(cn.getTimeStamp()))
            # Instead of exiting set a trailing stop a few points below target to 
            # capture more gain
            # exit()
            
      # Save off the prices so they can be later used in offLine mode
      if usePricesFromFile and not offLine:
      
         # Write prices and barcharts for 1-5 min charts
         pr.write(pricesPath, ask, bid, barCtr, write1_5MinData)
         
      # Beginning of next bar. 2nd clause is for offline mode
      if cn.getTimeHrMnSecs() >= endBarLoopTime or pr.isNextBar(barCtr):      
               
         # Only do this section once
         if dirty:
            continue
            
         dirty += 1
         
         # Not implemented yet
         a.setActionOnCloseBar()
         
         lg.debug("time now: " + str(cn.getTimeHrMnSecs()) + " end of bar time: " + str(endBarLoopTime))
      
         if not offLine:
            bc.loadEndBar(barChart, cn.getTimeStamp(), barCtr, bid, ask, last)
               
         # Print out the bar chart. Only print the last 20 bars
         if not offLine:
            bc.write(barChart, barChartPath, barCtr, write1_5MinData)
            bc.displayLastNBars(barChart, 20)
            
         bc.setAvgVol(barChart, barCtr)
         bc.setAvgBarLen(barChart, barCtr)
      
         lg.info ("Last price: " + str(last) + " Position: " + str(positionTaken))
         lg.info ("Average Volume: " + str(bc.getAvgVol()))
         lg.info ("Average Bar length: " + str(bc.getAvgBarLen()))

         # Set all decision points at the end of the previous bar
         a.setAllLimits(barChart, barCtr)

         print ("\nNEW BAR ===========================================\n")
         
         # Take a position if conditions exist
         # Action here is really action on the open of the next bar since it comes after 
         # setAllLimits
         a.setActionOnNewBar()
         positionTaken = a.takePosition(d, barChart, barCtr)

         barCtr += 1
         
         if not offLine:
            bc.appendBar(barChart)
         
         # Keep track of the bars in a position
         if a.inPosition():
            a.setBarInPositionCount()
            
         # End of bar reached. Done with on close processing
         break
      
      # COMBINE THESE TWO AND JUST CALL ready()
      
      # Wait till next bar before trading if set
      # if not a.inPosition() and a.getWaitForNextBar() and barCtr < a.getNextBar():

      if a.getWaitForNextBar() and barCtr < a.getNextBar():
         lg.debug("Waiting for next bar...")
         continue
         
      if a.quickProfitMax:
         if a.quickProfitCtr > a.quickProfitMax:
            lg.debug("Waiting for next bar. quickProfitCtr > max: " + str(a.quickProfitCtr) + " max: " + str(a.quickProfitMax))
            a.quickProfitCtr = 0
            a.setWaitForNextBar()
            continue

      #if a.inPosition() and barCtr < a.getNextBar():
      #   lg.debug("In a position. Waiting for next bar...")
      #   continue

      # Take a position if conditions exist
      positionTaken = a.takePosition(d, barChart, barCtr)

   # end bar loop

      # Stop trading at the end of he day
      if not offLine and not a.getAfterMarket():
         if a.inPosition():
            if a.isMarketExitTime():
               a.closePosition(barChart, barCtr, forceClose)

      # th = Thread(a.logIt(action, str(a.getBarsInPosition()), tm.now(), logPath))
      # Write to log file
      
   #if barCtr == 20: break
   
# end execution loop

