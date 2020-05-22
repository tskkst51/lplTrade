import pyetrade
#import order
import sys
import os
import time
import json
import lplTrade as lpl
from array import array
from optparse import OptionParser
from time import time, sleep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

verbose = False
debug = False

parser = OptionParser()

parser.add_option("-c"  , "--profileConnectPath", dest="profileConnectPath",
   help="write report to FILE", metavar="FILE")

parser.add_option("-p"  , "--profileTradeDataPath", dest="profileTradeDataPath",
   help="write report to FILE", metavar="FILE")
   
parser.add_option("-q", "--quiet",
   action="store_true", dest="quiet", default=False,
   help="don't lg.debug to stdout")
   
parser.add_option("-d", "--debug",
   action="store_true", dest="debug", help="don't lg.debug to logfile")
   
parser.add_option("-v", "--verbose",
   action="store_true", dest="verbose", help="verbose")
   
parser.add_option("-s", "--stock", type="string",
   action="store", dest="stock", default=False,
   help="stock to bua/selly: AAPL")
   
parser.add_option("-u", "--currency", type="string",
   action="store", dest="currency", default=False,
   help="currency to buy: btc... eth... bch...")
   
parser.add_option("-a", "--alt", type="string",
   action="store", dest="alt", default=False,
   help="alternate currency to buy: usd... uer... btc... eth... bch...")

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

# Price array hi lo open close volume indexes
hi = 0
lo = 1
op = 2
cl = 3
vl = 4
dt = 5

# Keep track of average volume based on all bars
avgVol = 0.0

#barChart = [[0.0,0.0,0.0,0.0,0.0]]
barChart = [[0.0,0.0,0.0,0.0,0.0,""]]

i = 0

close = action = 0
buyAction = buy = 1
sellAction = sell = 2
executeOnOpenPosition = 1
executeOnClosePosition = 2

stock = str(d["profileTradeData"]["stock"])
currency = str(d["profileTradeData"]["currency"])
alt = str(d["profileTradeData"]["alt"])
symbol = currency + alt
timeBar = int(d["profileTradeData"]["timeBar"])
service = str(d["profileTradeData"]["service"])
algorithm = str(d["profileTradeData"]["algorithm"])
tradingDelayBars = int(d["profileTradeData"]["tradingDelayBars"])
openBuyBars = int(d["profileTradeData"]["openBuyBars"])
closeBuyBars = int(d["profileTradeData"]["closeBuyBars"])
profileTradeData = str(d["profileTradeData"])

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log and debug file based on profileTradeData name and path

tm = lpl.Time()

logPath = clOptions.profileTradeDataPath.replace(".json", ".log")

debugPath = ""
if debug:
  stamp = "_" + stock + ".debug"
  debugPath = clOptions.profileTradeDataPath.replace(".json", stamp)

lg = lpl.Log(debug, verbose, logPath, debugPath)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

if service == "bitstamp":
   cn = lpl.ConnectBitStamp(service, currency, alt)
   cn.connectPublic()
elif service == "bitfinex":
   cn = lpl.ConnectBitFinex()
elif service == "eTrade":
   symbol = stock
   cn = lpl.ConnectEtrade(c, stock, debug)

   if debug:
      cn.setValues()
         
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm

a = lpl.Algorithm(d)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Write header data to logs

if debug:
   with open(debugPath, "a+", encoding="utf-8") as debugFile:
      debugFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))

with open(logPath, "a+", encoding="utf-8") as logFile:
   logFile.write(lg.header(tm.now()))

currency = str(d["profileTradeData"]["currency"])
alt = str(d["profileTradeData"]["alt"])
symbol = currency + alt

if service == "eTrade":
   symbol = stock

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Write data info

lg.info ("Reading profileTrade data from:\n" + clOptions.profileTradeDataPath + "\n")
lg.info ("Using symbol: " + symbol)
lg.info ("Start time: " + str(timeBar) + " Minute bar chart\n")
lg.info ("timeBar " + str(timeBar))
lg.info ("openBuyBars " + str(openBuyBars))
lg.info ("closeBuyBars " + str(closeBuyBars))
lg.info ("tradingDelayBars " + str(tradingDelayBars))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever or to a.endTime

inBullTrade = inBearTrade = False

# Wait till a couple minutes before market opens
#while cn.getTimeHrMnSecs() < 92700:
#   sleep (1)

# Delay start time to sync with top of the minute
tm.waitUntilTopMinute()

while True:
   # Set the initial loop time from the profileTradeData. Default None   
   endBarLoopTime = cn.getTimeHrMnSecs() + (100 * timeBar)

   if verbose == True:
      lg.debug ("Start time: " + cn.getTimeStamp())

   cn.setValues()
      
   initialVol = cn.getVolume()
   cp = cn.getCurrentPrice()

   # Initialize the bar chart to the current price
   barChart[i][op] = barChart[i][cl] = barChart[i][hi] = barChart[i][lo] = cp
   barChart[i][dt] = cn.getTimeStamp()
   
   totalVol = 0
   if i > 0:
      for n in range(i):
         totalVol += barChart[n][vl]
      avgVol = totalVol / i
   
   if verbose == True:
      lg.debug ("initialize i: " + str(i))
      lg.debug ("currentPrice: " + str(cp))
      lg.debug ("Average Volume: " + str(avgVol))
   
   # Loop until each bar has ended
   while True:
      # Load the barChart 
      cn.setValues()
      vol = cn.getVolume()
      currentPrice = cn.getCurrentPrice()
      stamp = cn.getTimeStamp()

      if verbose == True:
         lg.debug ("\nbar: " + str(i))
         lg.debug ("HI: " + str(barChart[i][hi]))
         lg.debug ("CP: " + str(currentPrice))
         lg.debug ("LO: " + str(barChart[i][lo]))
         lg.debug ("\n")

      if currentPrice > barChart[i][hi]:
         barChart[i][hi] = currentPrice
         
      if currentPrice < barChart[i][lo]:
         barChart[i][lo] = currentPrice
               
      barChart[i][vl] = vol - initialVol
      
      # Next bar
      if cn.getTimeHrMnSecs() >= endBarLoopTime:

         barChart[i][cl] = currentPrice
         barChart[i][dt] = cn.getTimeStamp()

         # Set all entry points based on the end of the previous bar
         a.setAllLimits(barChart, currentPrice, i)

         lg.info(tm.now())

         # lg.debug out the bar chart
         ctr = 0
         while ctr <= i:
            lg.debug("BAR: " + str(ctr) + " " + str(barChart[ctr]) + " action " + str(action))
            ctr += 1

         lg.info ("current price: " + str(currentPrice) + " " + str(action))

         # Block trading if we are in a range and range trading is set
         if a.getPriceInRange(currentPrice) and not a.inPosition():
            continue

         # Open position when closes are sequentially higher or lower
         if not a.inPosition() and a.getExecuteOnOpen() and a.ready(i):
            if verbose == True:
               lg.debug("Open a position on the open of the next bar\n")

            a.setExecuteOnOpenPosition(executeOnOpenPosition)

            action = a.takeAction(currentPrice, barChart)

            if action == buyAction:               
               lg.debug("The closes of the previous bars are sequentially higher\n")

               if a.getReverseLogic():
                  a.openPosition(sell, currentPrice, i)
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  lg.info("revAction: " + str(action))
               else: 
                  a.openPosition(buy, currentPrice, i)
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

            elif action == sellAction:
               lg.debug("The closes of the previous bars are sequentially lower\n")
               
               if a.getReverseLogic():
                  a.openPosition(buy, currentPrice, i)
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               else: 
                  a.openPosition(sell, currentPrice, i)
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

         # Close position on open of previous bar range
         elif a.inPosition() and a.getExecuteOnOpen() and a.ready(i):
            if verbose:
               lg.debug("Close a position on the open of the next bar\n")
               lg.debug("if the number of bars in the position has been exhausted\n")

            if a.getBarsInPosition() >= a.getTriggerBars():
               a.setExecuteOnOpenPosition(executeOnOpenPosition)
            
               action = a.takeAction(currentPrice, barChart)

               if action == buyAction:
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  triggered = False
               elif action == sellAction:
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  triggered = False

         barChart.append([0.0,0.0,0.0,0.0,0.0,""])
         #barChart.append([0.0,0.0,0.0,0.0,0.0])
         
         # Increment bar counter
         i += 1

         # Keep track of the bars in a position
         if a.inPosition():
            a.setBarCount()

         # End of bar reached. Get next bar
         break
         
		# REMOVE AFTER EXECUTE ON CLOSE IS TESTED
      continue

      # Wait n number of bars when trading is within a range
      if not a.ready(i):
         continue

      # Wait till next bar before trading if set
      if not a.inPosition():
         if a.getWaitForNextBar() and i < a.getNextBar():
            lg.debug("Waiting for next bar...")
            continue

      # ENABLE AFTER EXECUTE ON CLOSE IS TESTED
      if a.getExecuteOnOpen():
         continue

      action = a.takeAction(currentPrice, barChart)
      
      if a.getTrendTrigger():       
         if a.getBullTrend():
            if not a.inPosition():
               lg.debug ( "OPEN BUY. BULL TREND")
               a.openPosition(1, currentPrice, i)
               
               if a.getReverseLogic():
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               else: 
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
            else:
               if inBearTrade:
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  lg.debug ( "CLOSE BULL TREND POSITION.")
                  inBullTrade = False

            inBullTrade = True

         elif a.getBearTrend():
            if not a.inPosition():
               a.openPosition(2, currentPrice, i)
               if a.getReverseLogic():
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               else:
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               lg.debug ( "OPEN SELL BEAR TREND")
            else:
               if inBullTrade:
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  lg.debug ( "CLOSE SELL TREND POSITION.")
                  inBearTrade = False

            inBearTrade = True
         #elif a.inPosition():
            #a.closePosition(currentPrice, i)
            #lg.logIt(0, str(currentPrice), str(a.getBarsInPosition()), #tm.now(), logPath)
            #lg.debug ( "CLOSE ANY TREND POSITION")
         continue
                     
      # Block trading if we are in a range and range trading is set
      if a.getPriceInRange(currentPrice) and not a.inPosition():
         continue

      # Detect a reversal pattern in the current bar. triggerring when
      # current bar is > than previous bar

      # REVIEW THIS DO A REVERSAL IN A POSITION AND NOT IN A POSITION
            
      if a.inPosition() and a.doReversal():
         previousBarLen = float(barChart[i-1][cl] - barChart[i-1][op])
         currentBarLen = barChart[i][op] - currentPrice
         
         if previousBarLen < 0.0 and currentBarLen > 0.0:
            # Bars going different directions
            continue
         
         # Get rid of negative length bars
         if previousBarLen < 0.0:
            previousBarLen = previousBarLen * -1
         if currentBarLen < 0.0:
            currentBarLen = currentBarLen * -1
            
         currentOpen = barChart[i][op]

         currentHi = 0.0
         if action == buyAction:
            currentHi = barChart[i][hi]
         else:
            currentHi = barChart[i][lo]
            
         lg.debug("barLengths; current: " + str(currentBarLen) + " prev: " + str(previousBarLen))
         
         # Add an aditional percentage to currentBarLen for larger moves
         if currentBarLen > previousBarLen: 
            if a.getReversalLimit(currentHi, currentOpen, currentPrice):
               lg.info("triggered due to reversal detected!")
               a.closePosition(currentPrice, i)
               lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

      #lg.debug (str(currentPrice))

      if (action == buyAction or action == sellAction) and not a.inPosition() and not a.getExecuteOnOpen():
         #if a.getReverseLogic():
            #if action == buyAction:
               #lg.debug ("OPEN reversal logic applied buy -> sell...")
               #action = sellAction
               #a.openBuyLimit = a.openSellLimit
            #elif action == sellAction:
               #lg.debug ("OPEN reversal logic applied sell -> buy...")
               #action = buyAction
               #a.openSellLimit = a.openBuyLimit

         a.openPosition(action, currentPrice, i)

         if a.getReverseLogic():
            revAction = buyAction
            if action == buyAction: 
               revAction = sellAction
            lg.info("revAction: " + str(revAction) + " action " + str(action))
            lg.logIt(revAction, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
         else:
            lg.logIt(action, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                           
         triggered = False

      if a.inPosition() or (not a.getExecuteOnClose() and not a.getExecuteOnOpen()):         
         #if a.getReverseLogic():
            #if action == buyAction:
               #lg.debug ("CLOSE reversal logic applied buy -> sell...")
               #action = sellAction
               #a.closeBuyLimit = a.closeSellLimit
            #elif action == sellAction:
               #lg.debug ("CLOSE reversal logic applied sell -> buy...")
               #action = buyAction
               #a.closeSellLimit = a.closeBuyLimit
         # In a position and still in first bar
         #if a.getCurrentBar() == i:                        
         #  lg.debug ("In first bar...")
            #lg.debug ("InitialStopGain() " + str(a.getInitialStopGain()))
            #lg.debug ("In first bar...")
            #if a.getPositionType() == buyAction:
            #  if currentPrice > a.getInitialStopGain() or currentPrice < #a.getInitialStopLoss():
         #        triggered = True
         #  elif a.getPositionType() == sellAction:
         #     if currentPrice < a.getInitialStopGain() or currentPrice > a.getInitialStopLoss():
         #        triggered = True

         triggered = False

         # In a position and in next bar
         #else:
         profitTarget = a.getProfitTarget()
         if a.getPositionType() == buyAction:
            if currentPrice < a.getClosePrice():
               triggered = True
            lg.debug (str(a.getProfitPctTrigger()))
            if a.getProfitPctTrigger() > 0.0:
               if currentPrice > profitTarget:
                  lg.info("PROFIT TARGET MET: " + str(profitTarget))
                  #a.setCloseBuyStop(currentPrice)
                  triggered = True
         elif a.getPositionType() == sellAction:
            if currentPrice < profitTarget:
               lg.info("PROFIT TARGET MET: " + str(profitTarget))
               # a.setCloseSellStop(currentPrice)
               triggered = True
            #elif currentPrice > a.getLowestCloseSellPrice():
            elif currentPrice > a.getClosePrice():
               triggered = True
                     
         if triggered:           
            lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(),   logPath)
                        
            # Position is closed
            a.closePosition(currentPrice, i)
         
            triggered = False

         continue
            
      # th = Thread(a.logIt(action, currentPrice, str(a.getBarsInPosition()), tm.now(), logPath))
      # Write to log file
      
   # end bar loop
   #if i == 20: break
   
# end execution loop

lg.error("error")
lg.info("info")
lg.warning("warning")
lg.success("success")

