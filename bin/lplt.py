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

parser = OptionParser()

parser.add_option("-c"  , "--profileConnectPath", dest="profileConnectPath",
   help="write report to FILE", metavar="FILE")

parser.add_option("-p"  , "--profileTradeDataPath", dest="profileTradeDataPath",
   help="write report to FILE", metavar="FILE")
   
parser.add_option("-q", "--quiet",
   action="store_true", dest="quiet", default=False,
   help="don't print to stdout")
   
parser.add_option("-d", "--debug",
   action="store_true", dest="debug", default=False,
   help="don't print to logfile")
   
parser.add_option("-v", "--verbose",
   action="store_true", dest="verbose", default=False,
   help="verbose")
   
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

barChart = [[0.0,0.0,0.0,0.0,0.0]]

i = 0
debug = 0

close = action = 0
buyAction = buy = 1
sellAction = sell = 2

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
# Setup log and debug file based on profileTradeData name and path

logPath = clOptions.profileTradeDataPath.replace(".json", ".log")
logPath = logPath.replace("profileTradeDatas", "logs")

debugPath = clOptions.profileTradeDataPath.replace(".json", ".debug")
debugPath = logPath.replace("profileTradeDatas", "logs")

if debug:
   debugPath = clOptions.profileTradeDataPath.replace(".json", ".debug")
   debugPath = debugPath.replace("profileTradeDatas", "logs")

lg = lpl.Log()
debugLog = lpl.Log()
tm = lpl.Time()

# Delay start time to sync with top of the minute
if not debug:
   tm.waitUntilTopMinute()

#if debug:
   #with open(debugPath, "a+", encoding="utf-8") as debugFile:
      #debugFile.write(debugLog.header(tm.now()))

lg.info ("Reading profileTrade data from:\n" + clOptions.profileTradeDataPath + "\n")
lg.info ("Using symbol: " + symbol)
lg.info ("Start time: " + str(timeBar) + " Minute bar chart\n")

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

timeBar = int(d["profileTradeData"]["timeBar"])
service = str(d["profileTradeData"]["service"])
algorithm = str(d["profileTradeData"]["algorithm"])
tradingDelayBars = int(d["profileTradeData"]["tradingDelayBars"])
openBuyBars = a.openBuyBars
closeBuyBars = a.closeBuyBars
profileTradeData = str(d["profileTradeData"])

lg.info ("symbol " + str(symbol))
lg.info ("timeBar " + str(timeBar))
lg.info ("openBuyBars " + str(openBuyBars))
lg.info ("closeBuyBars " + str(closeBuyBars))

if int(a.aggressiveOpen) > 0:
   lg.info ("aggresive open " + str(a.aggressiveOpen))
if int(a.aggressiveClose) > 0:
   lg.info ("aggresive close " + str(a.aggressiveClose))
if int(a.useIntras) > 0:
   lg.info ("intraHigherHighsBars " + str(a.intraHigherHighsBars))
   lg.info ("intraLowerLowsBars " + str(a.intraLowerLowsBars))
   lg.info ("intraLowerHighsBars " + str(a.intraLowerHighsBars))
   lg.info ("intraHigherLowsBars " + str(a.intraHigherLowsBars))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever or to a.endTime

inBullTrade = inBearTrade = False

print ("\nStart time: " + cn.getTimeStamp())

while True:

   # Set the initial loop time from the profileTradeData. Default None
   
   endBarLoopTime = cn.getTimeHrMnSecs() + (100 * timeBar)
         
   cn.setValues()

   initialVol = cn.getVolume()   
   cp = cn.getCurrentPrice()

   # Initialize the bar chart to the current price
   barChart[i][op] = barChart[i][cl] = barChart[i][hi] = barChart[i][lo] = cp
   
   print ("\ninitialize i: " + str(i))
   print ("currentPrice: " + str(cp))

   # Loop until each bar has ended
   while True:
      # Load the barChart 
      vol = cn.getVolume()
      currentPrice = cn.getCurrentPrice()
      stamp = cn.getTimeStamp()
      
      print ("\nbar: " + str(i))
      print ("HI: " + str(barChart[i][hi]))
      print ("CP: " + str(currentPrice))
      print ("LO: " + str(barChart[i][lo]))
      print ("\n")

      if currentPrice > barChart[i][hi]:
         barChart[i][hi] = currentPrice
         
      if currentPrice < barChart[i][lo]:
         barChart[i][lo] = currentPrice
               
      barChart[i][vl] = vol - initialVol      
      
      if debug:
         sleep(2)
      
      # Next bar      
      if cn.getTimeHrMnSecs() >= endBarLoopTime:
         lg.info(tm.now())
         barChart[i][cl] = currentPrice
         
         # Open position on close of previous bar range
         if not a.inPosition() and a.getExecuteOnOpen() and a.ready(i):
         
            print("Executing on open...")
            print("currentPrice getOpenBuyPrice getOpenSellPrice\n" + str(currentPrice) + "     " + str(a.getOpenBuyPrice()) + "      " + str(a.getOpenSellPrice()))
            
            action = a.takeAction(currentPrice, barChart)
            if action == buyAction:
               if currentPrice >= a.getOpenBuyPrice():
                  a.openPosition(buy, currentPrice, i)
                  
                  if a.getReverseLogic():
                     lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                     lg.info("revAction: " + str(action))
                  else: 
                     lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
            elif action == sellAction:
               if currentPrice <= a.getOpenSellPrice():
                  a.openPosition(sell, currentPrice, i)
                  
                  if a.getReverseLogic():
                     lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  else: 
                     lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

         # Close position on open of previous bar range
         elif a.inPosition() and a.getExecuteOnClose() and a.ready(i):
            print("Executing on close...")
            print("currentPrice  gethighestCloseBuyPrice getLowestCloseSellPrice\n" + 
               str(currentPrice) + "        " +  str(a.getHighestCloseBuyPrice()) + "        " + 
               str(a.getLowestCloseSellPrice()))
            
            if a.getPositionType() == buyAction:
               if currentPrice <= a.getHighestCloseBuyPrice():
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  triggered = False
            elif a.getPositionType() == sellAction:
               if currentPrice >= a.getLowestCloseSellPrice():
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  triggered = False

         ctr = 0
         while ctr <= i:
            lg.info ("BAR: " + str(barChart[ctr]) + " action " + str(action))
            ctr += 1

         lg.info ("current price: " + str(currentPrice) + " " + str(action))
         a.setAllLimits(barChart, currentPrice, i)
         barChart.append([0.0,0.0,0.0,0.0,0.0])

         i += 1

         # Keep track of the bars in a position
         if a.inPosition():
            a.setBarCount()

         # End of bar reached. Get next bar
         break
         
      # Wait n number of bars when trading is within a range
      if not a.ready(i):
         continue

      # Wait till next bar before trading if set
      if not a.inPosition():
         if a.getWaitForNextBar() and i < a.getNextBar():
            print("Waiting for next bar...")
            continue

      action = a.takeAction(currentPrice, barChart)
      
      if a.getTrendTrigger():       
         if a.getBullTrend():
            if not a.inPosition():
               print ( "OPEN BUY. BULL TREND")
               a.openPosition(1, currentPrice, i)
               
               if a.getReverseLogic():
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               else: 
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
            else:
               if inBearTrade:
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  print ( "CLOSE BULL TREND POSITION.")
                  inBullTrade = False

            inBullTrade = True

         elif a.getBearTrend():
            if not a.inPosition():
               a.openPosition(2, currentPrice, i)
               if a.getReverseLogic():
                  lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               else:
                  lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
               print ( "OPEN SELL BEAR TREND")
            else:
               if inBullTrade:
                  a.closePosition(currentPrice, i)
                  lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
                  print ( "CLOSE SELL TREND POSITION.")
                  inBearTrade = False

            inBearTrade = True
         #elif a.inPosition():
            #a.closePosition(currentPrice, i)
            #lg.logIt(0, str(currentPrice), str(a.getBarsInPosition()), #tm.now(), logPath)
            #print ( "CLOSE ANY TREND POSITION")
         continue
                     
      # Block trading if we are in a range and range trading is set
      if a.getPriceInRange(currentPrice) and not a.inPosition():
         continue

      # Detect a reversal pattern in the current bar. triggerring when
      # current bar is > than previous bar
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
            
         print("barLengths; current: " + str(currentBarLen) + " prev: " + str(previousBarLen))
         
         # Add an aditional percentage to currentBarLen for larger moves
         if currentBarLen > previousBarLen: 
            if a.getReversalLimit(currentHi, currentOpen, currentPrice):
               lg.info("triggered due to reversal detected!")
               a.closePosition(currentPrice, i)
               lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

      print (str(currentPrice))

      if (action == buyAction or action == sellAction) and not a.inPosition() and not a.getExecuteOnOpen():
         #if a.getReverseLogic():
            #if action == buyAction:
               #print ("OPEN reversal logic applied buy -> sell...")
               #action = sellAction
               #a.openBuyLimit = a.openSellLimit
            #elif action == sellAction:
               #print ("OPEN reversal logic applied sell -> buy...")
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


      if a.inPosition() and not a.getExecuteOnClose():
         #if a.getReverseLogic():
            #if action == buyAction:
               #print ("CLOSE reversal logic applied buy -> sell...")
               #action = sellAction
               #a.closeBuyLimit = a.closeSellLimit
            #elif action == sellAction:
               #print ("CLOSE reversal logic applied sell -> buy...")
               #action = buyAction
               #a.closeSellLimit = a.closeBuyLimit
         # In a position and still in first bar
         #if a.getCurrentBar() == i:                        
         #  print ("In first bar...")
            #print ("InitialStopGain() " + str(a.getInitialStopGain()))
            #print ("In first bar...")
            #if a.getPositionType() == buyAction:
            #  if currentPrice > a.getInitialStopGain() or currentPrice < #a.getInitialStopLoss():
         #        triggered = True
         #  elif a.getPositionType() == sellAction:
         #     if currentPrice < a.getInitialStopGain() or currentPrice > a.getInitialStopLoss():
         #        triggered = True

         # In a position and in next bar
         #else:            
         profitTarget = a.getProfitTarget()
         if a.getPositionType() == buyAction:
            if currentPrice > profitTarget:
               lg.info("PROFIT TARGET MET: " + str(profitTarget))
               #a.setCloseBuyStop(currentPrice)
               triggered = True
            #elif currentPrice < a.getHighestCloseBuyPrice():
            elif currentPrice < a.getClosePrice():
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

