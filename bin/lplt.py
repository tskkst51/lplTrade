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
   action="store_true", dest="offLine", default=False,
   help="using static data")

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
dt = 5

# Keep track of average volume based on all bars
avgVol = 0.0

barChart = [[0.0,0.0,0.0,0.0,0,""]]
resumedBarCharCtr = 0

i = 0

close = action = noAction = 0
buyAction = buy = 1
sellAction = sell = 2
executeOnOpenPosition = 1
executeOnClosePosition = 2

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

offLine = int(c["profileConnectET"]["offLine"])
sandBox = int(c["profileConnectET"]["sandBox"])

symbol = currency + alt
marketDataType = "intraday"

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

logPath += "_" + stock + ".log"
debugPath += "_" + stock + ".debug"
resumePath += "_" + stock + ".bc"

lg = lpl.Log(debug, verbose, logPath, debugPath)

with open(debugPath, "a+", encoding="utf-8") as debugFile:
   debugFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))
   debugFile.write(lg.header(tm.now()))

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))
   logFile.write(lg.header(tm.now()))

with open(resumePath, "a+", encoding="utf-8") as resumeFile:
   print ("Opening bar chart file")

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
   cn.setValues(barChart, i)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm

a = lpl.Algorithm(d, lg)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Write profile data

lg.info ("Reading profileTrade data from:\n" + clOptions.profileTradeDataPath + "\n")
lg.info ("Using symbol: " + symbol)
lg.info (str(timeBar) + " minute bar chart\n")
lg.info ("openBuyBars " + str(openBuyBars))
lg.info ("closeBuyBars " + str(closeBuyBars))
lg.info ("tradingDelayBars " + str(tradingDelayBars))
lg.info ("sand: " + str(sandBox))
lg.info ("offLine: " + str(offLine))
lg.info ("marketDataType: " + marketDataType)

#lg.info ("increaseCloseBars " + str(increaseCloseBars))
#lg.info ("increaseCloseBarsMax " + str(increaseCloseBarsMax))
#lg.info ("useHiLows " + str(useHiLows))
#lg.info ("higherHighsBars " + str(higherHighsBars))
#lg.info ("higherLowsBars " + str(higherLowsBars))
#lg.info ("lowerHighsBars " + str(lowerHighsBars))
#lg.info ("lowerLowsBars " + str(lowerLowsBars))
#lg.info ("reversalPctTrigger " + str(reversalPctTrigger))
#lg.info ("closePositionFudge " + str(closePositionFudge))
#lg.info ("waitForNextBar " + str(waitForNextBar))
#lg.info ("executeOnOpen " + str(executeOnOpen))
#lg.info ("executeOnClose " + str(executeOnClose))
#lg.info ("hiLowBarMaxCounter " + str(hiLowBarMaxCounter))
#lg.info ("profitPctTrigger " + str(profitPctTrigger))
#lg.info ("trendTrigger " + str(trendTrigger))
#lg.info ("shortTrendBars " + str(shortTrendBars))
#lg.info ("midTrendBars " + str(midTrendBars))
#lg.info ("longTrendBars " + str(longTrendBars))
#lg.info ("megaTrendBars " + str(megaTrendBars))
#lg.info ("reverseLogic " + str(reverseLogic))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever. Pause trading during and after market hours 

# Wait till a couple minutes before market opens
#while cn.getTimeHrMnSecs() < 92700:
#   sleep (1)

#print (cn.getTimeHrMnSecs())
#print (cn.getDateTime())

# Read in barChart and resume from it
if resume:
   bcSize = pathlib.Path(resumePath).stat().st_size
   
   lg.verbose ("Size of barchart file : " + str(bcSize))
      
   if bcSize:
      numBars = lpl.Barchart.loadBC(barChart, resumePath)
      i = numBars - 1
      
   if offLine:
      i = 0
    
if not offLine:
   # Start trading at the top of the minute
   tm.waitUntilTopMinute()
   
while True:

   # Set the initial loop time from the minute chart time
   endBarLoopTime = cn.getTimeHrMnSecs() + (100 * timeBar)
   if offLine:
      endBarLoopTime = cn.getTimeHrMnSecs() + 3
      
   lg.verbose ("End bar time : " + str(endBarLoopTime))
   
   lg.debug ("Start time: " + str(cn.getTimeStamp()))

   
   cn.setValues(barChart, i)
      
   initialVol = cn.getVolume()
   cp = cn.getCurrentPrice()

   # Initialize the bar chart to the current price

   barChart[i][op] = barChart[i][cl] = barChart[i][hi] = barChart[i][lo] = cp
   barChart[i][dt] = cn.getTimeStamp()
      
   n = totalVol = 0
   if i > 0:
      while n < i:
         totalVol += int(barChart[n][vl])
         n += 1
      avgVol = totalVol / i
   
      lg.verbose ("initialize i: " + str(i))
      lg.verbose ("currentPrice: " + str(cp))
      lg.verbose ("Average Volume: " + str(avgVol))
   
   # Loop until each bar has ended
   while True:
   
      # Load the barChart on each iteration
      cn.setValues(barChart, i)
      
      vol = cn.getVolume()
      currentPrice = cn.getCurrentPrice()
      stamp = cn.getTimeStamp()

      lg.debug ("\nbar: " + str(i))
      lg.debug ("HI: " + str(barChart[i][hi]))
      lg.debug ("CP: " + str(currentPrice))
      lg.debug ("LO: " + str(barChart[i][lo]) + "\n")

      if currentPrice > barChart[i][hi]:
         barChart[i][hi] = currentPrice
         
      if currentPrice < barChart[i][lo]:
         barChart[i][lo] = currentPrice
               
      barChart[i][vl] = vol - initialVol
      
      # Beginning of next bar
      
      if cn.getTimeHrMnSecs() >= endBarLoopTime:
         lg.debug("time now: " + str(cn.getTimeHrMnSecs()) + " end of bar time: " + str(endBarLoopTime))

         if offLine:
            i += 1
            break

         barChart[i][cl] = currentPrice
         barChart[i][dt] = cn.getTimeStamp()

         # Set all decision points based on the end of the previous bar
         a.setAllLimits(barChart, currentPrice, i)

         # Print out the bar chart
         ctr = 0    
         lg.debug("\n")
         while ctr <= i:            
            lg.debug("BAR: " + str(ctr) + " " + str(barChart[ctr]))
            ctr += 1
         lg.debug("\n")
            
         lpl.Barchart.unLoadBC(barChart, resumePath, i)

#         with open(resumePath, 'a+') as bcChartData:
#            bcChartData.write('%s, ' % str(barChart[i][0]))
#            bcChartData.write('%s, ' % str(barChart[i][1]))
#            bcChartData.write('%s, ' % str(barChart[i][2]))
#            bcChartData.write('%s, ' % str(barChart[i][3]))
#            bcChartData.write('%s, ' % str(barChart[i][4]))
#            bcChartData.write('\'%s\'' % barChart[i][5] + "\n")
               
         lg.info ("current price: " + str(currentPrice) + " " + str(action))

         # Block taking a position if we are in a range and range trading is set
         if not a.inPosition() and a.getPriceInRange(currentPrice):
            lg.debug("NOT TRADING IN PRICE RANGE AND NOT IN A POSITION\n")         
            continue

         # Open position 
         
         action = a.takeActionOnCLose(currentPrice, barChart)

         #if not a.inPosition() and a.getExecuteOnClose():
         if not a.inPosition():
            if action == buyAction:
               if a.getReverseLogic():
                  a.openPosition(sell, currentPrice, i)
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  lg.debug("reversing the buy -> sell: " + str(action))
               else: 
                  currentPrice = cn.getCurrentAsk()
                  a.openPosition(buy, currentPrice, i)

                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               
            elif action == sellAction:               
               if a.getReverseLogic():
                  a.openPosition(buy, currentPrice, i)
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  lg.debug("reversing the sell -> buy: " + str(action))
               else: 
                  currentPrice = cn.getCurrentBid()

                  a.openPosition(sell, currentPrice, i)
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

         # Close position
         elif a.inPosition():
            if action == buyAction:
               a.closePosition(currentPrice, i)
               lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               if a.getQuickReversal():
                  a.openPosition(2, currentPrice, i)
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               
            elif action == sellAction:
               a.closePosition(currentPrice, i)
               lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               if a.getQuickReversal():
                  a.openPosition(1, currentPrice, i)
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

         barChart.append([0.0,0.0,0.0,0.0,0,""])
                  
         # Increment bar counter
         i += 1

         # Keep track of the bars in a position
         if a.inPosition():
            a.setBarInPositionCount()

         # End of bar reached. Done with on close processing
         break
               
      # Wait n number of bars when trading is within a range
      if not a.ready(i):
         continue

      # COMBINE THESE TWO AND JUST CALL ready()
      
      # Wait till next bar before trading if set
      if not a.inPosition() and a.getWaitForNextBar() and i < a.getNextBar():
         lg.debug("Waiting for next bar...")
         continue

      action = a.takeAction(currentPrice, barChart)
      
      if action:
         lg.debug ("Action set. Not on close " + str(action))
                     
      # Block trading if we are in a range and range trading is set
      if a.getPriceInRange(currentPrice) and not a.inPosition():
         continue


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

