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
profileTradeData = str(d["profileTradeData"])
resume = str(d["profileTradeData"]["resume"])
usePricesFromFile = int(d["profileTradeData"]["usePricesFromFile"])

offLine = int(c["profileConnectET"]["offLine"])
sandBox = int(c["profileConnectET"]["sandBox"])

symbol = currency + alt

marketDataType = "intraday"
numBars = 0

lastMinuteOfLiveTrading = 155930

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log and debug file based on profileTradeData name and path
# Write header data to logs

tm = lpl.Time()

logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
debugPath = clOptions.profileTradeDataPath.replace("profiles", "debug")
resumePath = clOptions.profileTradeDataPath.replace("profiles", "bc")
pricesPath = clOptions.profileTradeDataPath.replace("profiles", "prices")

logPath = logPath.replace(".json", "_")
debugPath = debugPath.replace(".json", "_")
resumePath = resumePath.replace(".json", "_")
pricesPath = pricesPath.replace(".json", "_")

logPath += stock + ".log"
debugPath += stock + ".debug"
resumePath += stock + ".bc"
pricesPath += stock + ".pr"


if service == "eTrade":
   symbol = stock

lg = lpl.Log(debug, verbose, logPath, debugPath, offLine)

print ("Prices path: " + pricesPath)

with open(debugPath, "a+", encoding="utf-8") as debugFile:
   debugFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))
   debugFile.write(lg.header(tm.now()))

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))
   logFile.write(lg.header(tm.now()))

with open(resumePath, "a+", encoding="utf-8") as resumeFile:
   print ("Opening bar chart file")

with open(pricesPath, "a+", encoding="utf-8") as priceFile:
   print ("Opening price list")


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Initialize  barchart                                
#

#bc = lpl.Barchart()
#barChart = bc.init()
#
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Setup connection to the exchange service

if service == "bitstamp":
   cn = lpl.ConnectBitStamp(service, currency, alt)
   cn.connectPublic()
elif service == "bitfinex":
   cn = lpl.ConnectBitFinex()
elif service == "eTrade":
   symbol = stock
   cn = lpl.ConnectEtrade(c, lg, stock, debug, verbose, marketDataType, sandBox, offLine)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm,  barchart, connection objects

a = lpl.Algorithm(d, lg, cn, offLine)
bc = lpl.Barchart()
pr = lpl.Price(a, cn, usePricesFromFile, offLine)

barChart = bc.init()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Display profile data

lg.info ("Reading profileTrade data from:\n" + clOptions.profileTradeDataPath + "\n")
lg.info ("Using symbol: " + symbol)
lg.info ("Last trade: " + str(cn.getLastTrade()))
lg.info (str(timeBar) + " minute bar chart\n")
lg.info ("openBuyBars " + str(openBuyBars))
lg.info ("closeBuyBars " + str(closeBuyBars))
lg.info ("tradingDelayBars " + str(tradingDelayBars))
lg.info ("sand: " + str(sandBox))
lg.info ("offLine: " + str(offLine))
lg.info ("marketDataType: " + cn.getMarketDataType())
lg.info ("dateTimeUTC: " + cn.getDateTimeUTC())
lg.info ("dateTime: " + cn.getDateTime())
lg.info ("getQuoteStatus: " + cn.getQuoteStatus())
lg.info (a.getAlgorithmMsg())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever. Pause trading during and after market hours 

# Wait till a couple minutes before market opens
#while cn.getTimeHrMnSecs() < 92700:
#   sleep (1)

cn.setValues(barChart, i, currentPrice)

# Fill buffer with prices
if usePricesFromFile and offLine:
   numPrices = pr.initPriceBuffer(pricesPath)
   barIdx = pr.skipFirstBar(numPrices)
   lg.debug ("number of prices from file: " + str(numPrices))

# Set the initial price
if not offLine:
   currentPrice = pr.getNextPrice(barChart, numBars, i)

# Read in barChart and resume from it
if resume:
   bcSize = pathlib.Path(resumePath).stat().st_size
   
   lg.verbose ("Size of barchart file : " + str(bcSize))

   # Ignore reading from barChart if it is empty
   if bcSize:
      numBars = bc.read(resumePath, barChart)
      
      lg.verbose ("Number of bars in file on disk : " + str(numBars))
      i = numBars
      
      bc.displayLastNBars(barChart, numBars)

   # If offline then iterate over the stored bar chart
   if usePricesFromFile and offLine:
      i = 0
         
   # We're live, program halted and now resumed. Initilize a new bar and continue
   else:
      bc.appendBar(barChart)
      a.setAllLimits(d, barChart, currentPrice, i)
      
lg.debug ("Start bar: " + str(i))

# Start trading at the top of the minute
if not offLine:
   tm.waitUntilTopMinute()

while True:

   if not offLine:
      sleep(0.2)
      
   # Set the initial loop time from the minute chart time
   endBarLoopTime = cn.adjustTimeToTopMinute(cn.getTimeHrMnSecs() + (100 * timeBar))

   lg.debug ("time : " + str(cn.getTimeHrMnSecs()))
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
   lg.debug ("currentPrice: " + str(currentPrice))
   
   a.setCurrentBar(i)
   dirty = 0
            
   # Loop until each bar has ended
   
   while True:
      
      # Load the barChart on each iteration
      cn.setValues(barChart, i, currentPrice)
      
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
            pr.write(pricesPath, currentPrice, i)
         
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
            bc.write(barChart, resumePath, i)
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

      #if a.inPosition() and i < a.getNextBar():
      #   lg.debug("In a position. Waiting for next bar...")
      #   continue

      # Take a position if conditions exist
      positionTaken = a.takePosition(d, currentPrice, barChart, i)

#      if action:
#         lg.debug ("Action set. Not on close " + str(action))
#                     
#      # Block trading if we are in a range and range trading is set
#      if a.getPriceInRange(currentPrice) and not a.inPosition():
#         continue
#
#      #if not a.inPosition() and NOT a.getExecuteOnClose():
#      if not a.inPosition():
#         if action == buyAction:
#            if a.getReverseLogic():
#               a.openPosition(sell, currentPrice, i)
#               lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
#               lg.debug("reversing the buy -> sell: " + str(action))
#            else: 
#               currentPrice = cn.getCurrentAsk()
#               a.openPosition(buy, currentPrice, i)
#
#               lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
#            
#         elif action == sellAction:               
#            if a.getReverseLogic():
#               a.openPosition(buy, currentPrice, i)
#               lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
#               lg.debug("reversing the sell -> buy: " + str(action))
#            else: 
#               currentPrice = cn.getCurrentBid()
#
#               a.openPosition(sell, currentPrice, i)
#               lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
#
#      # Close position
#      elif a.inPosition():
#         if action == buyAction:
#            a.closePosition(currentPrice, i)
#            lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
#            if a.getQuickReversal():
#               a.openPosition(2, currentPrice, i)
#               lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
#            
#         elif action == sellAction:
#            a.closePosition(currentPrice, i)
#            lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
#            if a.getQuickReversal():
#               a.openPosition(1, currentPrice, i)
#               lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               
      # REVIEW REVERSAL LOGIC
      #if not a.inPosition() and action != noAction and not a.getExecuteOnClose():
                           
         #continue
            
      # th = Thread(a.logIt(action, currentPrice, str(a.getBarsInPosition()), tm.now(), logPath))
      # Write to log file
      
   # end bar loop
   #if i == 20: break
   
# end execution loop

lg.error("error")
lg.info("info")
lg.warning("warning")
lg.success("success")

