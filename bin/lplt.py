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

i = 0

positionTaken = 0
close = action = noAction = 0
buyAction = buy = 1
sellAction = sell = 2
executeOnOpenPosition = 1
executeOnClosePosition = 2
currentPrice = 0.0

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

print ("Prices path: " + pricesPath)

with open(debugPath, "a+", encoding="utf-8") as debugFile:
   debugFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))
   debugFile.write(lg.header(tm.now()))

lg.info("Using " + debugPath + " as debug file")

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))
   logFile.write(lg.header(tm.now()))

lg.info("Using " + logPath + " as log file")

with open(barChartPath, "a+", encoding="utf-8") as resumeFile:
   lg.info("Using " + barChartPath + " as bar chart file")

with open(pricesPath, "a+", encoding="utf-8") as priceFile:
   lg.info("Using " + pricesPath + " as prices file")


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
# Initialize algorithm,  barchart, prices objects

a = lpl.Algorithm(d, lg, cn, offLine)
bc = lpl.Barchart()
pr = lpl.Price(a, cn, usePricesFromFile, offLine, a.getMarketBeginTime())

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
# Main loop. Loop forever. Pause trading during and after market hours 

cn.setValues(barChart, i, currentPrice)

# Fill buffers with prices
if usePricesFromFile and offLine:
   numPrices = pr.initPriceBuffer(pricesPath)
   barIdx = pr.skipFirstBar(numPrices)
   lg.debug ("number of prices from file: " + str(numPrices))

# Set the initial price
if not offLine:
   currentPrice = pr.getNextPrice(barChart, numBars, i)

# Read in barChart and resume from it
if resume:
   bcSize = pathlib.Path(barChartPath).stat().st_size
   
   lg.verbose ("Size of barchart file : " + str(bcSize))

   # Ignore reading from barChart if it is empty
   if bcSize:
      numBars = bc.read(barChartPath, barChart)
      
      lg.verbose ("Number of bars in file on disk : " + str(numBars))
      i = numBars
      
      bc.displayLastNBars(barChart, numBars)

   # If offline then iterate over the stored bar chart starting at bar 0
   if usePricesFromFile and offLine:
      i = 0
         
   # We're live, program halted and now resumed. Initilize a new bar and trade on
   else:
      bc.appendBar(barChart)
      a.setAllLimits(d, barChart, currentPrice, i)
      
lg.debug ("Start bar: " + str(i))

# Start trading at the top of the minute
if not offLine:
   tm.waitUntilTopMinute()
   if a.getPreMarket():
      tm.waitUntilTopMinute()
   if write1_5MinData:
      pr.initWrite(pricesPath)
      bc.initWrite(barChartPath)

a.setTradingDelayBars()

while True:

   # Start trading at beginning of day
   if not a.getPreMarket():
      if not offLine and not marketOpen:
         if a.getMarketBeginTime():
            lg.info("Waiting till the market opens...")
            cn.waitTillMarketOpens(a.getMarketOpenTime())
            marketOpen += 1

   if not offLine:
      sleep(0.2)
      
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
         if i >= numBars - 1:
            exit()
         
   lg.debug ("End bar time : " + str(endBarLoopTime))
   lg.debug ("Start time: " + str(cn.getTimeStamp()))
   
   # Set the prices from the current exchange (Etrade...)
   #cn.setValues(barChart, i, currentPrice)
      
   initialVol = cn.getVolume()
   
   if not offLine:
      bc.loadInit(barChart, currentPrice, cn.getTimeStamp(), cn.getVolume(), i)
         
   lg.debug ("initialize i: " + str(i))
   
   a.setCurrentBar(i)
   dirty = 0
            
   # Loop until each bar has ended
   
   while True:
      
      # Set the values from the trading service
      cn.setValues(barChart, i, currentPrice)
      
      # 
      a.unsetActionOnNewBar()
      
      currentPrice = pr.getNextPrice(barChart, numBars, i)

      lg.info ("\nbar: " + str(i))
      lg.info ("HI: " + str(barChart[i][hi]))
      lg.info ("CP: " + str(currentPrice))
      lg.info ("LO: " + str(barChart[i][lo]) + "\n")
      
      tradeVolume = cn.getVolume() - initialVol
         
      if not offLine:
         bc.loadBeginBar(barChart, currentPrice, cn.getCurrentBid(), tradeVolume, i)
   
      # Halt program at end of trading day
      if cn.getTimeHrMnSecs() > lastMinuteOfLiveTrading:
         if not offLine and not a.getAfterMarket():
            if a.inPosition():
               a.closePosition(d, currentPrice, barChart, i)
            lg.info("Program exiting due to end of day trading")
            exit()
         
      # Save off the prices so they can be later used in offLine mode
      if usePricesFromFile and not offLine:
         # Write prices and barcharts for 1-5 min charts
         pr.write(pricesPath, currentPrice, i, write1_5MinData)
         
      # Beginning of next bar
      if cn.getTimeHrMnSecs() >= endBarLoopTime or pr.isNextBar(i):      
         
         if dirty:
            continue
            
         dirty += 1
         #a.setActionOnCloseBar()
         
         lg.debug("time now: " + str(cn.getTimeHrMnSecs()) + " end of bar time: " + str(endBarLoopTime))
      
         if not offLine:
            bc.loadEndBar(barChart, currentPrice, cn.getTimeStamp(), i)
               
         # Print out the bar chart,\. Only print the last 20 bars
                  
         if not offLine:
            bc.write(barChart, barChartPath, i, write1_5MinData)
            bc.displayLastNBars(barChart, 20)
            
         bc.setAvgVol(barChart, i)
         bc.setAvgBarLen(barChart, i)
      
         lg.info ("current price: " + str(currentPrice) + " " + str(positionTaken))
         lg.info ("Average Volume: " + str(bc.getAvgVol()))
         lg.info ("Average Bar length: " + str(bc.getAvgBarLen()))

         # Set all decision points based on the end of the previous bar
         a.setAllLimits(d, barChart, currentPrice, i)

         # Take a position if conditions exist
         # Action here is really action on the open of the next bar since it comes after 
         # setAllLimits
         a.setActionOnNewBar()
         positionTaken = a.takePosition(d, currentPrice, barChart, i)

         i += 1
         
         if not offLine:
            bc.appendBar(barChart)
         
         # Keep track of the bars in a position
         if a.inPosition():
            a.setBarInPositionCount()
            
         # End of bar reached. Done with on close processing
         break
      
      # COMBINE THESE TWO AND JUST CALL ready()
      
      # Wait till next bar before trading if set
      # if not a.inPosition() and a.getWaitForNextBar() and i < a.getNextBar():

      if a.getWaitForNextBar() and i < a.getNextBar():
         lg.debug("Waiting for next bar...")
         continue
         
      if a.quickProfitCtr > a.quickProfitMax:
         lg.debug("Waiting for next bar. quickProfitCtr > max: " + str(a.quickProfitCtr) + " max: " + str(a.quickProfitMax))
         a.quickProfitCtr = 0
         a.setWaitForNextBar()
         continue

      #if a.inPosition() and i < a.getNextBar():
      #   lg.debug("In a position. Waiting for next bar...")
      #   continue

      # Take a position if conditions exist
      positionTaken = a.takePosition(d, currentPrice, barChart, i)

   # end bar loop

   # Stop trading at the end of he day
   if not offLine and not a.getAfterMarket():
      if a.inPosition():
         if a.isMarketExitTime():
            a.closePosition(d, currentPrice, barChart, i)
            # Create the 1 - 5 min profiles so they can be iterated later
            if write1_5MinData:
               copyfile(profile1m, profile2m)
               copyfile(profile1m, profile3m)
               copyfile(profile1m, profile4m)
               copyfile(profile1m, profile5m)
               testDir = testPath + "/" + str(cm.getDateMonthDayYear())
               mkdir(testDir)
               copytree(pricesPath, testDir)
               copytree(bcPath, testDir)

      # th = Thread(a.logIt(action, currentPrice, str(a.getBarsInPosition()), tm.now(), logPath))
      # Write to log file
      
   #if i == 20: break
   
# end execution loop

