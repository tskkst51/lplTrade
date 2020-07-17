'''
Algorithms module
'''
import io
import sys
import os
from bitarray import bitarray 
import lplTrade as lpl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm():

   def __init__(self, data, lg, cn, bc, offLine=0):
   
      self.cn = cn
      self.lg = lg
      self.offLine = offLine
      self.bc = bc
      
      # Required standard settings
      self.algorithms = str(data['profileTradeData']['algorithms'])
            
      # Algorithms
      self.doDefault = int(data['profileTradeData']['doDefault'])
      self.doHiLos = int(data['profileTradeData']['doHiLos'])
      self.doOpensCloses = int(data['profileTradeData']['doOpensCloses'])
      self.doExecuteOnClose = int(data['profileTradeData']['doExecuteOnClose'])
      self.doExecuteOnOpen = int(data['profileTradeData']['doExecuteOnOpen'])
      self.doHiLoOnClose = int(data['profileTradeData']['doHiLoOnClose'])
      self.doHiLoOnOpen = int(data['profileTradeData']['doHiLoOnOpen'])
      self.doQuickReversal = int(data['profileTradeData']['doQuickReversal'])
      self.doRangeTradeBars = int(data['profileTradeData']['doRangeTradeBars'])
      self.doReversalPattern = int(data['profileTradeData']['doReversalPattern'])
      self.doReverseBuySell = int(data['profileTradeData']['doReverseBuySell'])
      self.doQuickProfit = int(data['profileTradeData']['doQuickProfit'])
      self.doTrends = int(data['profileTradeData']['doTrends'])
      self.doDynamic = int(data['profileTradeData']['doDynamic'])
      self.doOnlyBuys = int(data['profileTradeData']['doOnlyBuys'])
      self.doOnlySells = int(data['profileTradeData']['doOnlySells'])

      self.currency = str(data['profileTradeData']['currency'])
      self.alt = str(data['profileTradeData']['alt'])
      self.openBuyBars = int(data['profileTradeData']['openBuyBars'])
      self.closeBuyBars = int(data['profileTradeData']['closeBuyBars'])
      self.openSellBars = int(data['profileTradeData']['openSellBars'])
      self.closeSellBars = int(data['profileTradeData']['closeSellBars'])
      self.tradingDelayBars = int(data['profileTradeData']['tradingDelayBars'])
      self.marketBeginTime = int(data['profileTradeData']['marketBeginTime'])
      self.marketEndTime = int(data['profileTradeData']['marketEndTime'])
      self.preMarket = int(data['profileTradeData']['preMarket'])
      self.afterMarket = int(data['profileTradeData']['afterMarket'])
      self.quickProfitMax = int(data['profileTradeData']['quickProfitMax'])

      # Open position using lowest close bars 
      # Close position using highest open bars 
      # Make sure their are >= 2 bars when using 
      self.aggressiveOpen = int(data['profileTradeData']['aggressiveOpen'])
      self.aggressiveClose = int(data['profileTradeData']['aggressiveClose'])

      # Increase the number of bars used determining close price
      self.increaseCloseBars = int(data['profileTradeData']['increaseCloseBars'])
      self.increaseCloseBarsMax = int(data['profileTradeData']['increaseCloseBarsMax'])
      self.gainTrailStop = int(data['profileTradeData']['gainTrailStop'])
      
      # Additional value to add to close triggers
      self.closePositionFudge = float(data['profileTradeData']['closePositionFudge'])
      
      # Use highs and lows for determining open/close
      self.higherHighsBars = int(data['profileTradeData']['higherHighsBars'])
      self.lowerLowsBars = int(data['profileTradeData']['lowerLowsBars'])
      self.lowerHighsBars = int(data['profileTradeData']['lowerHighsBars'])
      self.higherLowsBars = int(data['profileTradeData']['higherLowsBars'])
      
      self.higherHighs = self.higherCloses = 0
      self.lowerHighs = self.lowerCloses = 0
      self.lowerLows = self.lowerOpens = 0
      self.higherLows = self.higherOpens = 0

      #self.algoBitArray = bitarray(6)
      #self.algoBitArray = bitarray.setall[0]
      
      # Wait for next bar before opening a position
      self.waitForNextBar = int(data['profileTradeData']['waitForNextBar'])

      # Yet to implement.  BELOW HERE HASN"T BEEN IMPLEMENTED yet
      
      self.endTradingTime = float(data['profileTradeData']['endTradingTime'])
      self.profitPctTriggerAmt = float(data['profileTradeData']['profitPctTriggerAmt'])
      
      # reverseLogic appears to be best for short term charts and
      # low liquidity
      
      self.buyNearLow = int(data['profileTradeData']['buyNearLow'])
      self.sellNearHi = int(data['profileTradeData']['sellNearHi'])
      self.aggressiveOpenPct = float(data['profileTradeData']['aggressiveOpenPct'])
      self.aggressiveClosePct = float(data['profileTradeData']['aggressiveClosePct'])
      
      self.profitPctTrigger = float(data['profileTradeData']['profitPctTrigger'])
      self.profitPctTriggerBar = float(data['profileTradeData']['profitPctTriggerBar'])
      self.reversalPctTrigger = float(data['profileTradeData']['reversalPctTrigger'])
      self.volumeRangeBars = int(data['profileTradeData']['volumeRangeBars'])
      self.amountPct = float(data['profileTradeData']['amountPct'])

      # Use trend indicators to increase amount to trade
      self.shortTrendBars = int(data['profileTradeData']['shortTrendBars'])
      self.midTrendBars = int(data['profileTradeData']['midTrendBars'])
      self.longTrendBars = int(data['profileTradeData']['longTrendBars'])
      self.megaTrendBars = int(data['profileTradeData']['megaTrendBars'])
            
      self.executeOnOpenPosition = 0
      self.executeOnClosePosition = 0

      self.hiLowBarMaxCounter = int(data['profileTradeData']['hiLowBarMaxCounter'])
      self.useSignals = int(data['profileTradeData']['useSignals'])
      
      # Class variables
      self.position = "close"
      self.positionType = 0
      self.openPositionPrice = 0.0
      self.closePositionPrice = 0.0
      self.stopBuy = 0.0
      self.stopSell = 0.0
      self.initialStopGain = 0.0
      self.initialStopLoss = 0.0
            
      self.openBuyLimit = 0.0
      self.closeBuyLimit = 0.0
      self.highestcloseBuyLimit = 0.0
      self.lowestcloseBuyLimit = 0.0
      self.highestcloseSellLimit = 0.0
      self.lowestcloseSellLimit = 99999999.999999
      self.openSellLimit = 0.0
      self.closeSellLimit = 0.0
            
      self.hi = 0
      self.lo = 1
      self.op = 2
      self.cl = 3
      self.vl = 4
      self.bl = 5
      self.sH = 6
      self.sL = 7
      self.dt = 8
      
      self.close = 0
      self.buy = 1
      self.sell = 2

      self.triggerBars = self.openBuyBars
      self.currentBar = 0
      self.nextBar = 0
      self.rangeTradeValue = 0
      self.rangeHi = 0.0
      self.rangeLo = 0.0
      self.priceInRange = 0
      
      self.hiValues = [0.0] 
      self.lowValues = [0.0]
      self.openBuyValues = [0.0] 
      self.closeBuyValues = [0.0]
      self.openSellValues = [0.0] 
      self.closeSellValues = [0.0]

      self.topIntraBar = 0.0
      self.barCounter = 0
      self.revDirty = 0
      self.barCount = 0
      self.barCountInPosition = 0 
      self.dirtyWaitForNextBar = 0
      self.profitTarget = 0.0
      self.longMegaBars = 0.0
      
      self.shortTrend = self.midTrend = 0.0
      self.longTrend = self.megaTrend = 0.0
            
      self.algoMsg = ""
      
      self.setAlgorithmMsg()
      
      self.doOnCloseBar = 0
      self.doOnNewBar = 0
      self.dynPriceInRange = 0

      self.totalGain = 0.0
      self.totalProfit = 0.0
      self.quickProfitCtr = 0
      self.useAvgBarLen = 0
      self.avgBarLenCtr = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLiveProfileValues(self, data):
   
      displayHeader = "Profile items: "
         
      for key, value in data.items():
         for k, v in value.items():
            if k == "currency" or k == "alt":
               continue
            if v >= '1':
               displayHeader += v + " " + k + "\n"
      
      return displayHeader
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takePosition(self, d, barChart, bar):
   
      # Determine if position should be opened
      action = self.takeAction(d, barChart, bar)
      
      # Open position 
      if not self.inPosition():
         if action == self.buy:
            if self.doReverseBuySell: 
               self.openPosition(self.sell, bar, barChart)
               self.lg.debug("reversing the buy -> sell: " + str(action))
            else: 
               self.openPosition(self.buy, bar, barChart)
            
         elif action == self.sell:               
            if self.doReverseBuySell:
               self.openPosition(self.buy, bar, barChart)
               self.lg.debug("reversing the sell -> buy: " + str(action))
            else: 
               self.openPosition(self.sell, bar, barChart)

      # Close position
      elif self.inPosition():
         if action == self.buy:
            self.closePosition(d, bar, barChart)
            if self.getQuickReversal() and not self.isPriceInRange():
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.sell, bar, barChart)
            
         elif action == self.sell:
            self.closePosition(d, bar, barChart)
            if self.getQuickReversal() and not self.isPriceInRange():
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.buy, bar, barChart)

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takeAction(self, d, barChart, bar):
   
      action = 0
      
      if self.doDynamic:
         self.algorithmDynamic(action)
     
      if self.doQuickProfit:
         action = self.algorithmTakeProfit(d, barChart, bar, action)
      
      if self.doExecuteOnClose:
         action = self.algorithmOnClose(barChart, bar, action)

      if self.doExecuteOnOpen:
         action = self.algorithmOnOpen(barChart, bar, action)

# Do patterns. Stay in position when hi are higher or lows are lower except when 
# close is higher than open for a sell position or a
# close is lower than an open for a buy position

      if self.doHiLos:
         action = self.algorithmHiLo(barChart, bar, action)
         
      if self.doReversalPattern:
         action = self.algorithmReversalPattern(barChart, bar, action)
      
      if self.doTrends:
         action = self.algorithmDoTrends(barChart, bar, action)
         
      if self.doRangeTradeBars:
         action = self.algorithmDoInRange(barChart, bar, action)
         
      if self.doDefault:
         action = self.algorithmDefault(barChart, bar, action)

      if self.doReverseBuySell and action:
         action = self.algorithmReverseBuySell()
      
      if action  > 0:
         print ("Action being taken!! " + str(action))
     
      return action
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmReversalPattern(self, barChart, bar, action=0):
         
      self.lg.debug ("In algorithmReversalPattern: " + str(action))

      # Detect a reversal pattern in the current bar. triggerring when
      # current bar is > than previous bar
   
      if self.inPosition() and self.doReversal():
         previousBarLen = float(barChart[i-1][cl] - barChart[i-1][op])
         currentBarLen = barChart[i][op] - self.cn.getCurrentAsk()
         
         if previousBarLen < 0.0 and currentBarLen > 0.0:
            # Bars going different directions
            return 1
         
         # Get rid of negative length bars
         if previousBarLen < 0.0:
            previousBarLen = previousBarLen * -1
         if currentBarLen < 0.0:
            currentBarLen = currentBarLen * -1
            
         currentOpen = barChart[i][op]

         currentHi = 0.0
         if action == self.buy:
            currentHi = barChart[i][hi]
         else:
            currentHi = barChart[i][lo]
            
         self.lg.debug("barLengths; current: " + str(currentBarLen) + " prev: " + str(previousBarLen))
         
         # Add an additional percentage to currentBarLen for larger moves
         if currentBarLen > previousBarLen: 
            if self.getReversalLimit(currentHi, currentOpen):
               self.lg.info("triggered due to reversal detected!")
               self.closePosition(d, bar, barChart)

      return 1
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmReverseBuySell(self):

      self.lg.debug ("In algorithmReverseBuySell: " + str(action))

      if self.doReverseBuySell:
         self.setRevBuySell()
      
      return 1
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmTakeProfit(self, d, barChart, bar, action=0):
   
      self.lg.debug ("In algorithmTakeProfit: " + str(action))
      
      if not self.inPosition():         
         return action

      if self.quickProfitCtr:
         # Use avg bar length as the stop instead of original limits
         self.setAvgBarLenLimits(barChart, bar)
      else:
         self.avgBarLenCtr = bar + 1      
      
      profitTarget = self.getProfitTarget()
      self.lg.debug ("Target profit set to: " + str(profitTarget))
      
      if self.getPositionType() == self.buy:
         if self.cn.getCurrentAsk() > profitTarget:
            self.lg.debug ( "CLOSING BUY POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(self.cn.getCurrentAsk()) + " > " + str(profitTarget))
            self.quickProfitCtr += 1
            self.closePosition(d, bar, barChart)
            
      elif self.getPositionType() == self.sell:
         if self.cn.getCurrentBid() < profitTarget:
            self.lg.debug ( "CLOSING SELL POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(self.cn.getCurrentBid()) + " < " + str(profitTarget))
            self.quickProfitCtr += 1
            self.closePosition(d, bar, barChart)
                 
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoInRange(self, barChart, bar, action=0):
   
      self.lg.debug("In algorithmDoInRange. Action: " + str(action))

      if self.inPosition():
         return action
         
      # Return 0 if price is within a range 

      if self.isPriceInRange():
         self.priceInRange += 1
         self.useAvgBarLen = 0
         self.lg.debug("NOT TRADING IN PRICE RANGE AND NOT IN A POSITION " + str(self.doRangeTradeBars))         
         return 0
      
      # if first time out of range then reverse buys and sells and use a trailing
      # avg bar length as the stop.
      
      elif self.priceInRange > 1:
         self.lg.debug("reversing buy sell due to first time out of range")
         if action == self.buy:
            action = self.sell
         elif action == self.sell:
            action = self.buy
         
         self.useAvgBarLen += 1
         self.priceInRange = 0
         
         self.setAvgBarLenLimits(barChart, bar)

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoTrends(self, barChart, bar, action=0):
   
      self.lg.debug("In algorithmDoTrends: " + str(action))

      # We set the trend linits here since the calculation is dynamic and values
      # change as the price moves
      # This algo takes much CPU time and may need rethinking
      
      self.setTrendLimits(barChart, bar)
      
#      if self.isBullTrend():
#         if not self.inPosition():
#            self.lg.debug ( "OPEN BUY. BULL TREND")
#            if self.doReverseBuySell:
#               self.openPosition(self.sell, bar, barChart)
#            else: 
#               self.openPosition(self.buy, bar, barChart)
#         else:
#            if inBearTrade:
#               self.closePosition(bar, barChart)
#               self.lg.debug ( "CLOSE BULL TREND POSITION.")
#               inBullTrade = 0
#
#         inBullTrade = 1
#
#      elif self.isBearTrend():
#         if not self.inPosition():
#            self.doReverseBuySell
#            self.openPosition(self.sell, bar, barChart)
#            self.lg.debug ( "OPEN SELL BEAR TREND")
#         else:
#            if inBullTrade:
#               self.closePosition(bar, barChart)
#               self.lg.debug ( "CLOSE SELL TREND POSITION.")
#               inBearTrade = 0
#
#         inBearTrade = 1
         
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmOnClose(self, barChart, action=0):

      self.lg.debug("In algorithmOnClose: " + str(action))
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmOnOpen(self, barChart, bar, action=0):

      self.lg.debug("In algorithmOnOpen: " + str(action))
      
      # If we are not on the beginning of a new bar, there's nothing to do, get out
      if not self.doActionOnNewBar():
         return 0

      # Take position on the open if execute on open is set 
      if not self.inPosition():
         # Open a buy position on the open if closes are sequentially higher
         if self.isHigherCloses(self.openBuyBars, self.openBuyValues):
            self.lg.debug("TAKING POSITION isHigherCloses: ")
            return self.buy
   
         # Open a sell position on the open if closes are sequentially lower
         elif self.isLowerCloses(self.openSellBars, self.openSellValues):
            self.lg.debug("TAKING POSITION isLowerCloses: ")
            return self.sell
         
      else:
         # Close a buy position on the open if closes are sequentially lower
         if self.positionType == self.buy:
            if self.isLowerCloses(self.closeBuyBars, self.closeBuyValues):
               self.lg.debug("CLOSING POSITION isLowerCloses: ")
               return self.buy
   
         # Close a sell position on the open if closes are sequentially higher
         elif self.positionType == self.sell:
            if self.isHigherCloses(self.closeSellBars, self.closeSellValues):
               self.lg.debug("CLOSING POSITION isHigherCloses: ")
               return self.sell
            
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high or lower than the low
   
   def algorithmHiLo(self, barChart, bar, action=0):

      adjustDoToExecuteOnOpenClose = 0
      
      if action > 0 and (self.doExecuteOnOpen or self.doExecuteOnClose):
         print ("Using highs and lo's to close/open a position on execute on open/close: " + str(action))
         adjustDoToExecuteOnOpenClose = 1

      self.lg.debug("In algorithmHiLo")

      # Adjust execute on close decision based on hi's lo's
      if adjustDoToExecuteOnOpenClose:
         if self.inPosition():
            if self.positionType == self.buy:
               if self.higherHighs and self.higherLows:
                  self.lg.debug ("Hi Lo algo reversing action. Higher hi's and Higher lo's detected")
                  return 0
               self.lg.debug ("Hi Lo algo not affecting current action.")
               return 1
            else:
               if self.lowerHighs and self.lowerLows:
                  self.lg.debug ("Hi Lo algo reversing action. Lower hi's and Lower lo's detected")
                  return 0
               self.lg.debug ("Hi Lo algo not affecting current action")
               return 2
         
         else: # Not in position
            if action == self.buy:
               if self.lowerHighs and self.lowerLows:
                  self.lg.debug ("Hi Lo algo reversing action. Lower hi's and Lower lo's detected")
                  return 0
               print ("Hi Lo algo not affecting current action.")
               return 1
            elif action == self.sell:
               if self.higherHighs and self.higherLows:
                  self.lg.debug ("Hi Lo algo reversing action. Lower hi's and Lower lo's detected")
                  return 0
               print ("Hi Lo algo not affecting current action.")
               return 2

      # Hi Lo processing on close using hi's and lo's and closes to get out
      elif self.doHiLoOnOpen:
         if self.inPosition():
            if self.positionType == self.buy:
               if self.lowerHighs and self.lowerLows and self.lowerCloses and self.lowerOpens :
                  #if self.cn.getCurrentAsk() < self.closeBuyLimit:
                  return 1
            if self.positionType == self.sell:
               if self.higherHighs and self.higherLows:
                  #if self.cn.getCurrentBid() > self.closeSellLimit:
                  return 2
         elif not self.inPosition():
            if self.higherHighs and self.higherLows:
               return 1
            if self.lowerHighs and self.lowerLows:
               return 2
         
      # Make decisions when hi's or lo's are breached
      else:
         # in sequential profit taking
         if self.quickProfitCtr:
            self.setAvgBarLenLimits(barChart, bar)
            self.lg.debug ("self.quickProfitCtr set: " + str(self.quickProfitCtr))

         self.lg.debug ("In Hi Lo: open limits buy " + str(self.openBuyLimit) + " sell " + str(self.openSellLimit))
         self.lg.debug ("In Hi Lo: close limits buy " + str(self.closeBuyLimit) + " sell " + str(self.closeSellLimit))
            
         self.lg.debug ("currentPrice " + str(self.cn.getCurrentAsk()))
         
         if self.inPosition():
            if self.positionType == self.buy:
               self.lg.debug ("Hi Lo: in buy position " + str(self.positionType))
               self.lg.debug ("closeBuyLimit " + str(self.closeBuyLimit))
               if self.cn.getCurrentAsk() < self.closeBuyLimit:
                  return 1
            if self.positionType == self.sell:
               self.lg.debug ("Hi Lo: in sell position " + str(self.positionType))
               self.lg.debug ("closeSellLimit " + str(self.closeSellLimit))
               if self.cn.getCurrentBid() > self.closeSellLimit:
                  return 2
         elif not self.inPosition():
            if self.cn.getCurrentAsk() > self.openBuyLimit:
               self.lg.debug ("Opening BUY Hi Lo position")
               return 1
            if self.cn.getCurrentBid() < self.openSellLimit:
               self.lg.debug ("Opening SELL Hi Lo position")
               return 2

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDefault(self, barChart, bar, action=0):
      
      # Ues the right flag here or continue to use this algo as the default
   
      if self.inPosition():
         print ("close buy limit " + str(self.closeBuyLimit))
         print ("close sell limit " +  str(self.closeSellLimit))
         if self.cn.getCurrentAsk() < self.closeBuyLimit:
            return 1
         if self.cn.getCurrentBid() > self.closeSellLimit:
            return 2
      else:
         if self.cn.getCurrentAsk() >= self.openBuyLimit and self.openBuyLimit != 0.0:
            print ( "open buy limit set " + str(self.openBuyLimit))
            return 1
         if self.cn.getCurrentBid() <= self.openSellLimit and self.openSellLimit != 0.0:
            print ("open sell limit set " +  str(self.openSellLimit))
            return 2
      
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDynamic(self, action=0):
   
      # if in a oscilating trade get out
      # set quickProfit using avg bar length when in trade longer then the number of bars
      
      # remove range restrictins when bar length is > average. This will catch big moves.

      # If in a range for more than n number of bars, get out with small profit if possible.
      #  More risk when oscilating
       
      ## If in a range and in a trend either sell or buy opposite of normal logic with the trend
      ## if trend is sell then sell when 1st hi out of the range. : Winning ticket!!!!
      
      # After 3 quickProfit wins use avg bar length as stop when buying/selling again
      
      self.lg.debug("In algorithmDynamic: " + str(action))
      
      # Once price goes out of range reverse buys and sells
      if self.isPriceInRange():
         self.dynPriceInRange += 1

      if not self.isPriceInRange() and self.dynPriceInRange:
         self.doReverseBuySell += 1
         self.setRevBuySell()
         self.dynPriceInRange = 0

      if self.getBarsInPosition() > self.openBuyBars:
         self.openBuyBars -= 1
         
      if self.getBarsInPosition() > self.closeBuyBars and self.closeBuyBars > 0:
         self.closeBuyBars -= 1
         
      # If in a position and within a range sell out for profit as exiting range
      #if self.inPosition() and self.getBarsInPosition() > self.doRangeTradeBars:
      #   self.closeSellBar = 0
      #   self.closeBuyBar = 0.0
         
      # if in a gain position set stop just above average bar length?
   
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTradingDelayBars(self):
   
      if self.doRangeTradeBars > self.tradingDelayBars:
         self.tradingDelayBars = self.doRangeTradeBars
         
      if self.openBuyBars > self.tradingDelayBars:
         self.tradingDelayBars = self.openBuyBars
         
      if self.closeBuyBars > self.tradingDelayBars:
         self.tradingDelayBars = self.closeBuyBars
         
      if self.openSellBars > self.tradingDelayBars:
         self.tradingDelayBars = self.openSellBars
         
      if self.closeSellBars > self.tradingDelayBars:
         self.tradingDelayBars = self.closeSellBars
         
      if self.lowerHighsBars > self.tradingDelayBars:
         self.tradingDelayBars = self.lowerHighsBars
         
      if self.higherLowsBars > self.tradingDelayBars:
         self.tradingDelayBars = self.higherLowsBars
         
      if self.lowerLowsBars > self.tradingDelayBars:
         self.tradingDelayBars = self.lowerLowsBars
         
      if self.higherHighsBars > self.tradingDelayBars:
         self.tradingDelayBars = self.higherHighsBars
         
      #if self.offLine:
      #   self.tradingDelayBars += 1
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def ready(self, currentNumBars):
   
         
      #if self.shortTrendBars > self.tradingDelayBars:
         #self.tradingDelayBars = self.shortTrendBars
         
      #if self.longTrendBars > self.tradingDelayBars:
         #self.tradingDelayBars = self.longTrendBars
       
      self.lg.debug("tradingDelayBars currentNumBars " + str(self.tradingDelayBars) + " " + str(currentNumBars))
      
      if self.tradingDelayBars <= currentNumBars:
         return 1
      else:
         return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPriceInRange(self):
   
      if not self.doRangeTradeBars:
         return 0
         
      if self.cn.getCurrentBid() >= self.rangeLo and self.cn.getCurrentAsk() <= self.rangeHi:
         if not self.inPosition():
            print ("in range between " + str(self.rangeLo) +   " and " +  str(self.rangeHi))

         return 1

      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def waitingForBestPrice(self):
   
      if self.waitForBestPrice:
         return
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def openPosition(self, buyOrSell, bar, bc):

# DO THE COMBINGING OF ACTIONS HERE TO EXTEND OR SHORTEN TRADES E:G: BULL TRADE< REVERSAL PATTERN
      
      # Block taking a position if we are in a range and range trading is set or delay bars are set
      if not self.ready(bar):
         self.lg.debug("BLOCKING TRADING DUE TO DELAY BARS " + str(self.ready(bar)))         
         return

#      if self.isPriceInRange():
#         self.priceInRange += 1
#         self.lg.debug("NOT TRADING IN PRICE RANGE AND NOT IN A POSITION " + str(self.doRangeTradeBars))         
#         return
#
      if self.doTrends:      
         if self.isBullMegaTrend() and buyOrSell == self.sell:
            self.lg.debug("In isBullMegaTrend NOT BLOCKING... " + str(self.isBullMegaTrend()))
            return        
         
         elif self.isBearMegaTrend() and buyOrSell == self.buy:
            self.lg.debug("In bearMegaTrend NOT BLOCKING..." + str(self.isBearMegaTrend()))
            return        

         elif self.isBearLongTrend() and buyOrSell == self.buy:
            self.lg.debug("not buying on signal, In bearLongTrend " + str(self.isBearLongTrend()))
            return        
         
         elif self.isBullLongTrend() and buyOrSell == self.sell:
            self.lg.debug("not selling on signal, In bullLongTrend " + str(self.isBullLongTrend()))
            return        
         
         elif self.isBearMidTrend() and buyOrSell == self.buy:
            self.lg.debug("not buying on signal, In bearMidTrend " + str(self.isBearMidTrend()))
            return        
         
         elif self.isBullMidTrend() and buyOrSell == self.sell:
            self.lg.debug("not selling on signal, In bullMidTrend " + str(self.isBullMidTrend()))
            return        
         
         elif self.isBearShortTrend() and buyOrSell == self.buy:
            self.lg.debug("not buying on signal, In bearMidTrend " + str(self.isBearMidTrend()))
            return        
         
         elif self.isBullShortTrend() and buyOrSell == self.sell:
            self.lg.debug("not selling on signal, In bullMidTrend " + str(self.isBullMidTrend()))
            return        
         
         
#      if self.doRangeTradeBars:
#         if self.priceInRange > 1:
#            self.lg.debug("reversing buy sell due first time out of range")
#            if buyOrSell == self.buy:
#               buyOrSell = self.sell
#            elif buyOrSell == self.sell:
#               buyOrSell = self.buy
#            
#            setRangeBuySellLimits(bar, bc)
#            self.priceInRange = 0
         
      # Open position in oposite direction when first time out of a range
      #if self.priceInRange >= 1:
      # set quick profit based on avg bar length

      self.triggerBars = 0

      if self.doOnlyBuys and buyOrSell == self.sell:
         return
      
      if self.doOnlySells and buyOrSell == self.buy:
         return
      
      # Open a BUY position
      if buyOrSell == self.buy:
         price = round(self.cn.getCurrentAsk(), 2)
         
         # Execute order here ========================
         
         if self.offLine:
            self.lg.logIt(self.buy, str(price), str(self.getBarsInPosition()), bc[bar][self.dt])
         else:
            self.lg.logIt(self.buy, str(price), str(self.getBarsInPosition()), self.cn.getTimeStamp())
         self.positionType = self.buy
         
      # Open a SELL position
      else:
         price = round(self.cn.getCurrentBid(), 2)
         
         # Execute order here ========================
         
         if self.offLine:
            self.lg.logIt(self.sell, str(price), str(self.getBarsInPosition()), bc[bar][self.dt])
         else:
            self.lg.logIt(self.sell, str(price), str(self.getBarsInPosition()), self.cn.getTimeStamp())
         self.positionType = self.sell

      # Set all values appropriate with the opening of a position

      self.lg.info("\n")
      self.lg.info("POSITION OPEN\n")
      self.lg.info("buy/sell: " + str(buyOrSell))
      self.lg.info("Open buy limit: " + str(self.openBuyLimit))
      self.lg.info("Open position Price: " + str(price))
      self.lg.info("Open sell limit: " + str(self.openSellLimit))
            
      if self.offLine:
         self.lg.info("Position Time: " + bc[bar][self.dt])
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()))
         
      # Using avg bar length or percentage instead (setProfitTarget), Remove eventually
      #self.setInitialClosePrices()
      
      self.setCurrentBar(bar)
            
      self.setProfitTarget(0)
         
      self.setExecuteOnOpenPosition(0)
      
      self.position = "open"
      self.openPositionPrice = price
      self.barCountInPosition = 0

      self.lowestcloseSellLimit = self.closeSellLimit
      self.highestcloseBuyLimit = self.closeBuyLimit

      #print("Initial stopGain: " + str(self.getInitialStopGain()))
      #print("Initial stopLoss: " + str(self.getInitialStopLoss()))
      
      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def closePosition(self, d, bar, bc):

      gain = price = 0

      self.lg.debug ("self.isBullMidTrend() " + str(self.isBullMidTrend()))
      self.lg.debug ("self.doTrends() " + str(self.doTrends))
      self.lg.debug ("self.positionType() " + str(self.positionType))
      
      #if self.doTrends:
      #   if self.positionType == self.buy:         
      #      if (self.isBullMidTrend() or self.isBullLongTrend()) and not self.quickProfitCtr:
      #         self.lg.debug("not closing on signal, In isBullTrend " + str(self.isBullMidTrend()))
      #         return        
      #   else:
      #      if (self.isBearMidTrend() or self.isBearLongTrend()) and not self.quickProfitCtr:
      #         self.lg.debug("not closing on signal, In isBearTrend " + str(self.isBearMidTrend()))
      #         return        

      if self.positionType == self.buy:
         price = self.cn.getCurrentBid()
      else:
         price = self.cn.getCurrentAsk()
         
      if self.positionType == self.buy:
         gain = price - self.openPositionPrice
      elif self.positionType == self.sell:
         gain = self.openPositionPrice - price
         
      self.totalGain += gain
      
      # Update the log
      if self.offLine:
         self.lg.logIt(self.close, str(price), str(self.getBarsInPosition()), bc[bar][self.dt])
      else:
         self.lg.logIt(self.close, str(price), str(self.getBarsInPosition()), self.cn.getTimeStamp())

      self.closePositionPrice = price

      print ("\n")
      self.lg.info ("POSITION CLOSED")
      
      if self.offLine:
         self.lg.info("Position Time: " + bc[bar][self.dt])
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()))

      self.lg.info ("open price: " + str(self.openPositionPrice))
      self.lg.info ("close price: " + str(self.closePositionPrice))
      self.lg.info ("current Price: " + str(price))
      self.lg.info ("gain: " + str(gain))
      self.lg.info ("stopPrice: " + str(self.getClosePrice()))
      self.lg.info ("bar Count In Position: " + str(self.barCountInPosition))
      self.lg.info ("Total Bar Count: " + str(self.barCount) + "\n")
      self.lg.info ("Loss/Gain: " + str(gain) + "\n")
      self.lg.info ("Total Gain: " + str(self.totalGain) + "\n")

      if gain < 0:
         self.setAllLimits(d, bc, bar)
         self.quickProfitCtr = 0
         self.avgBarLenCtr = 0
         self.setWaitForNextBar()
         
      self.openPositionPrice = self.closePositionPrice = 0.0
      self.topIntraBar = 0.0

      self.positionType = 0
      self.barCounter = self.currentBar = 0
      self.highestcloseBuyLimit = 0.0
      self.lowestcloseSellLimit = 0.0
      self.barCountInPosition = 0
      self.position = "close"

      self.resetLimits(d)
      self.setExecuteOnClosePosition(0)
      
      if self.doReverseBuySell:
         self.unsetRevBuySell()
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def resetLimits(self, data):
   
      self.openBuyBars = int(data['profileTradeData']['openBuyBars'])
      self.closeBuyBars = int(data['profileTradeData']['closeBuyBars'])
      self.openSellBars = int(data['profileTradeData']['openSellBars'])
      self.closeSellBars = int(data['profileTradeData']['closeSellBars'])
      self.tradingDelayBars = int(data['profileTradeData']['tradingDelayBars'])
      self.aggressiveOpen = int(data['profileTradeData']['aggressiveOpen'])
      self.aggressiveClose = int(data['profileTradeData']['aggressiveClose'])
      self.increaseCloseBars = int(data['profileTradeData']['increaseCloseBars'])
      self.increaseCloseBarsMax = int(data['profileTradeData']['increaseCloseBarsMax'])
      self.gainTrailStop = int(data['profileTradeData']['gainTrailStop'])
      self.closePositionFudge = float(data['profileTradeData']['closePositionFudge'])
      self.higherHighsBars = int(data['profileTradeData']['higherHighsBars'])
      self.lowerLowsBars = int(data['profileTradeData']['lowerLowsBars'])
      self.lowerHighsBars = int(data['profileTradeData']['lowerHighsBars'])
      self.higherLowsBars = int(data['profileTradeData']['higherLowsBars'])

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doReversal(self):
      if self.reversalPctTrigger > 0.0:
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def inPosition(self):
         
      if self.position == "open":
         return 1
      else:
         return 0

   # Setter definitions

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setActionOnNewBar(self):
   
      self.doOnNewBar += 1
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetActionOnNewBar(self):
   
      self.doOnNewBar = 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doActionOnNewBar(self):
   
      return self.doOnNewBar
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setActionOnCloseBar(self):
   
      self.doOnCloseBar += 1
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetActionOnCloseBar(self):
   
      self.doOnCloseBar = 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doActionOnCloseBar(self):
   
      return self.doOnCloseBar
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setRevBuySell(self):
      
      self.sell = 1
      self.buy = 2
      self.doReverseBuySell += 1
      self.lg.info("reversing. buy is now sell...: " + str(self.buy) + " action " + str(self.sell))
      
      # Set new limits
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetRevBuySell(self):
   
      self.sell = 2
      self.buy = 1
      self.doReverseBuySell = 0
      self.lg.info("restoring. buy is now buy...: " + str(self.buy) + " action " + str(self.sell))

      # Unset new limits
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doReverseBuySell(self):
      
      return self.doReverseBuySell
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTotalGain(self):

      return round(self.totalGain, 2)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTotalProfit(self):

      return self.totalProfit
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTotalProfit(self, price, percentage):

      self.totalProfit = round(price * percentage, 2)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMarketOpenTime(self):

      return self.marketBeginTime
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAfterMarket(self):
   
      return self.afterMarket
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doPreMarket(self):
   
      return self.preMarket
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMarketBeginTime(self):
   
      return self.marketBeginTime
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyStop(self):
   
      self.closeBuyLimit = self.cn.getCurrentAsk()
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellStop(self):
   
      self.closeSellLimit = self.cn.getCurrentBid()
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setDynamic(self, bar):
   
      #if not self.doDynamic:
      #   self.doDynamic = 1
      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBarCount(self):

      self.barCount += 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBarInPositionCount(self):

      self.barCountInPosition += 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setProfitTarget(self, useBars):

      self.lg.debug ("profit pct trigger: " + str(self.profitPctTrigger))

      profitAmt = 0.0
      if self.positionType == self.buy: 
         profitAmt = self.cn.getCurrentBid() * self.profitPctTrigger
      else:
         profitAmt = self.cn.getCurrentAsk() * self.profitPctTrigger
      
      if self.quickProfitCtr:
         divisor = self.quickProfitCtr + 1
         if self.increaseCloseBarsMax < self.quickProfitCtr:
            divisor = self.increaseCloseBarsMax
         profitAmt /= divisor
         self.lg.debug ("reducing profit target by : " + str(divisor))
         self.lg.debug ("profit amount : " + str(profitAmt))
         
      # Use bar length if set
      elif useBars > 0:
         profitAmt = self.bc.getAvgBarLen()
         self.lg.debug ("profit amount using avg bar length: " + str(profitAmt))
         
      if self.positionType == self.buy:
         self.profitTarget = round((self.cn.getCurrentAsk() + profitAmt), 2)
      elif self.positionType == self.sell:
         self.profitTarget = round((self.cn.getCurrentBid() - profitAmt), 2)

      self.lg.debug ("profit value: " + str(round(self.profitTarget, 2)))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseLimits(self, barChart, bar):
   
      if bar < self.openBuyBars:
         return

      if bar < self.closeBuyBars:   
         return

      self.openBuyValues = [0.0] * self.openBuyBars   
      self.closeBuyValues = [0.0] * self.closeBuyBars  
      self.openSellValues = [0.0] * self.openSellBars   
      self.closeSellValues = [0.0] * self.closeSellBars  
   
      n = 0
      while n < self.openBuyBars:
         print ("open buy bars: " + str(barChart[bar - n][self.op]))
         self.openBuyValues[n] = barChart[bar - n][self.op]
         n += 1
      
      n = 0
      while n < self.closeBuyBars:
         print ("close buy bars: " + str(barChart[bar - n][self.cl]))
         self.closeBuyValues[n] = barChart[bar - n][self.cl]
         n += 1

      n = 0
      while n < self.openSellBars:
         print ("open sell bars: " + str(barChart[bar - n][self.op]))
         self.openSellValues[n] = barChart[bar - n][self.op]
         n += 1
      
      n = 0
      while n < self.closeSellBars:
         print ("close sell bars: " + str(barChart[bar - n][self.cl]))
         self.closeSellValues[n] = barChart[bar - n][self.cl]
         n += 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setHiLowLimits(self, barChart, bar):
                     
      if bar < self.lowerHighsBars or bar < self.higherLowsBars or bar < self.lowerLowsBars or bar < self.higherHighsBars:
         return
      
      # Find the Hi Lo bars with the max number of bars defined
      # lowerHighsBars could be 2 where lowerLowsBars could be 3
      loopLowIterator = loopHiIterator = 0
      
      loopLowIterator = self.lowerLowsBars
      if self.higherLowsBars > self.lowerLowsBars:
         loopLowIterator = self.higherLowsBars
         
      loopHiIterator = self.higherHighsBars
      if self.lowerHighsBars > self.higherHighsBars:
         loopHiIterator = self.lowerHighsBars
         
      self.lowValues = [0.0] * loopLowIterator   
      self.hiValues = [0.0] * loopHiIterator  
   
      print ("loopLowIterator for lower lo's" + str(loopLowIterator))
      print ("Bar number: " + str(bar))
      
      for n in range(loopLowIterator):
         print ("low's: " + str(barChart[bar - n][self.lo]))
         self.lowValues[n] = barChart[bar - n][self.lo]
         
      for n in range(loopHiIterator):
         print ("hi's: " + str(barChart[bar - n][self.hi]))
         self.hiValues[n] = barChart[bar - n][self.hi]
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setHiLowValues(self):
   
      #if not self.doHiLos:
      #   return

      self.higherHighs = self.isHigherHighs()
      self.lowerLows = self.isLowerLows()
      self.lowerHighs = self.isLowerHighs()
      self.higherLows = self.isHigherLows()

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseBuyValues(self):
   
      #if not self.doOpensCloses:
      #   return

      self.higherOpens = self.isHigherOpens(self.openBuyBars, self.openBuyValues)
      self.higherCloses = self.isHigherCloses(self.closeBuyBars, self.closeBuyValues)
      self.lowerOpens = self.isLowerOpens(self.openSellBars, self.openSellValues)
      self.lowerCloses = self.isLowerCloses(self.closeSellBars, self.closeSellValues)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setInitialClosePrices(self):

      hiLoDiff = self.openBuyLimit - self.openSellLimit
      
      #print ("Hi Lo diff: " + str(hiLoDiff) + "\n")
      
      if hiLoDiff == 0.0:
         hiLoDiff = 5.0

      if self.positionType == self.buy:
         posGain = self.cn.getCurrentAsk() + hiLoDiff * self.profitPctTriggerBar
         posLoss = self.closeBuyLimit - self.closePositionFudge
      elif self.positionType == self.sell:
         posGain = self.cn.getCurrentBid() - hiLoDiff * self.profitPctTriggerBar
         posLoss = self.closeSellLimit + self.closePositionFudge

      self.initialStopGain = posGain
      self.initialStopLoss = posLoss

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getReversalLimit(self, top, op):
   
      if self.reversalPctTrigger == 0.0:
         return 0

      # Have to wait for the top to form so keep track of the top
      # top - open = length
      # length * reversal pct == price to sell

      # if not in a gain position get out
      if self.positionType == self.buy:
         if self.cn.getCurrentAsk() < self.openPositionPrice:
            return 0
      elif self.positionType == self.sell:
         if self.cn.getCurrentBid() > self.openPositionPrice:
            return 0

      if not self.revDirty:
         self.topIntraBar = top
         self.revDirty = 1
         self.barCounter = 0
         return 0

      if self.positionType == self.buy:
         if self.cn.getCurrentAsk() >= top:
            self.topIntraBar = self.cn.getCurrentAsk()
            self.barCounter = 0
            return

         #if top >= self.topIntraBar:
         #  self.topIntraBar = top
         #  return 0

         barLen = top - op

      elif self.positionType == self.sell:
         bottom = top
         if self.cn.getCurrentBid() <= bottom:
            self.topIntraBar = self.cn.getCurrentBid()
            self.barCounter = 0
            return

         #if top <= self.topIntraBar:
         #  self.topIntraBar = top
         #  return 0

         barLen = op - top

         print ("top " + str(top))
         print ("open " + str(op))
         print ("self.topIntraBar " + str(self.topIntraBar))
         print ("currentPrice " + str(self.cn.getCurrentAsk()))
         print ("self.barCounter " + str(self.barCounter))
         print ("self.hiLowBarMaxCounter " + str(self.hiLowBarMaxCounter))
         print ("self.revDirty " + str(self.revDirty))

      if self.barCounter < self.hiLowBarMaxCounter:
         # Wait 10 checks for top to be higher than previous
         print("BarCounter: " + str(self.barCounter))
         self.barCounter += 1
         return 0
      
      targetPrice = (barLen * self.reversalPctTrigger)
      sellPrice = top - targetPrice

      print ("barLen " + str(barLen))
      print ("targetPrice " + str(targetPrice))
      print ("sell price " + str(sellPrice))

      if self.positionType == self.buy:
         if sellPrice < self.cn.getCurrentAsk():
            return 1
      elif self.positionType == self.sell:
         if sellPrice > self.cn.getCurrentBid():
            return 1

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCurrentBar(self, bar):

      self.currentBar = bar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setNextBar(self, nextBar):
      
      self.nextBar = nextBar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setRangeLimits(self, barChart, bar):

      if not self.doRangeTradeBars:
         return
         
      if len(barChart) < self.doRangeTradeBars:
         return
         
      # Use Hi and Los or open closes for determining range
      if self.doRangeTradeBars:
         self.rangeHi = self.getHighestCloseOpenPrice(self.doRangeTradeBars, barChart, bar)
         self.rangeLo = self.getLowestCloseOpenPrice(self.doRangeTradeBars, barChart, bar)
         self.lg.debug("Range limits using Open Closes ")
         
         if self.doHiLos:
            self.rangeHi = self.getHighestHiBarPrice(self.doRangeTradeBars, barChart, bar)
            self.rangeLo = self.getLowestLoBarPrice(self.doRangeTradeBars, barChart, bar)
            self.lg.debug("Range limits using Hi Los ")
                        
         self.lg.debug("Range limits: " + str(self.rangeHi) + " " + str(self.rangeLo))
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAllLimits(self, d, barChart, bar):

      if bar < self.doRangeTradeBars or len(barChart) < self.doRangeTradeBars:
         return
      
      self.lg.debug("Bar in chart we are on: " + str(bar))
      
      self.setRangeLimits(barChart, bar)

      self.setHiLowLimits(barChart, bar)
      self.setHiLowValues()

      self.setOpenCloseLimits(barChart, bar)
      self.setOpenCloseBuyValues()
      
      self.bc.setAvgBarLen(barChart, bar)
      
      self.setBuySellLimits(barChart, bar)
      
      if self.useAvgBarLen:
         self.setAvgBarLenLimits(barChart, bar)
      
      self.setNextBar(bar + 1)
      self.unsetWaitForNextBar()
      
      self.revDirty = 0
      self.barCount = bar - self.currentBar

      if self.doHiLos:
         print ("higherLows higherHighs " + str(self.higherLows) + 
            " " + str(self.higherHighs)) 
         print ("lowerHighs lowerLows " + str(self.lowerHighs) + 
            " " + str(self.lowerLows))

      if self.doOpensCloses or self.doExecuteOnClose or self.doExecuteOnOpen:
         print ("higherOpens higherCloses " + str(self.higherOpens) + 
            " " + str(self.higherCloses)) 
         print ("lowerOpens lowerCloses " + str(self.lowerOpens) + 
            " " + str(self.lowerCloses))

      self.setDynamic(bar)
      
      if self.inPosition():
         print ("bars in position: " + str(self.getBarsInPosition()))
         
      self.setAlgorithmMsg()
      
      if self.doDynamic:
         self.algorithmDynamic(bar)
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendLimits(self, barChart, bar):

      if self.doTrends:
         self.setShortTrend("short", barChart, bar)
         self.setMidTrend("mid", barChart, bar)
         self.setLongTrend("long", barChart, bar)
         self.setMegaTrend("mega", barChart, bar)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetShortTrend(self):

      self.shortTrend = 0.0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetMidTrend(self):

      self.midTrend = 0.0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetLongTrend(self):

      self.longTrend = 0.0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetMegaTrend(self):

      self.megaTrend = 0.0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setShortTrend(self, trendType, barChart, bar):

      if self.shortTrendBars == 0 or bar <= self.shortTrendBars:
         return
            
      self.shortTrend = 0.0
      
      self.setTrendValues(trendType, barChart, bar, self.shortTrendBars)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMidTrend(self, trendType, barChart, bar):
   
      if self.midTrendBars == 0 or bar <= self.midTrendBars:
         return
            
      self.midTrend = 0.0
      
      self.setTrendValues(trendType, barChart, bar, self.midTrendBars)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setLongTrend(self, trendType, barChart, bar):
   
      if self.longTrendBars == 0 or bar <= self.longTrendBars:
         return
   
      self.longTrend = 0.0
      
      self.setTrendValues(trendType, barChart, bar, self.longTrendBars)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMegaTrend(self, trendType, barChart, bar):
   
      if self.megaTrendBars == 0 or bar <= self.megaTrendBars:
         return
   
      self.megaTrend = 0.0
      
      self.setTrendValues(trendType, barChart, bar, self.megaTrendBars)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendValues(self, trendType, barChart, bar, trendBarLen):
      # 0.0 - no trend; 1.[0-9] - bull; 3.[0-9] - bear
      # the fractional value is the strength 0 weak 9 strong

      lowest = 999999999.99
      highest = 0.0
      loBarPosition = hiBarPosition = i = 0
         
      b = bar - trendBarLen
      
      self.lg.debug("start bar for trend: " + str(b))
      self.lg.debug("trendBarLen: " + str(trendBarLen))
      
      while b < bar: 
         if barChart[b][self.cl] < lowest:
            lowest = barChart[b][self.cl]
            loBarPosition = b
         if barChart[b][self.cl] > highest:
            highest = barChart[b][self.cl]
            hiBarPosition = b
            
         b += 1

      self.lg.debug("currentPrice: " + str(self.cn.getCurrentAsk()))
      self.lg.debug("barr " + str(bar))
      self.lg.debug("LOWEST: " + str(lowest))
      self.lg.debug("HIGHEST: " + str(highest))
      self.lg.debug("loBarPosition: " + str(loBarPosition))
      self.lg.debug("hiBarPosition: " + str(hiBarPosition))

      # Comparing bar positions of the hi and lo gives us the trend
      if loBarPosition == hiBarPosition:
         return
      elif loBarPosition < hiBarPosition:
         # Bull trend
         trend = 1.0
      elif loBarPosition > hiBarPosition:
         # Bear trend
         trend = 3.0

      pctInTrend = pctInTrendRnd = 0.0
      penetration = 0.0

      # Simple first
      if self.cn.getCurrentAsk() > highest:
         pctInTrend = 0.9999
      elif self.cn.getCurrentBid() < lowest:
         pctInTrend = 0.0000
      else:
         # Get the price range of bars
         if highest > lowest:
            priceRange = highest - lowest
            penetration = highest - self.cn.getCurrentAsk()
            pctInTrend = 1.0 - (penetration / priceRange)
         else:
            priceRange = lowest - highest
            penetration = lowest - self.cn.getCurrentBid()
            pctInTrend = 1.0 - (penetration / priceRange)
            self.lg.debug("priceRange: " + str(priceRange))
            
      pctInTrendRnd = round(pctInTrend, 2)
      
      self.lg.debug("pctInTrend: " + str(pctInTrend))
      self.lg.debug("penetration: " + str(penetration))
      self.lg.debug("pctInTrendRnd: " + str(pctInTrendRnd))

      # if pctInTrend > 1: then position is higher then the high of the range
      # and denoted with 0.9999 set above
      trend += pctInTrendRnd
      
      if trendType == "short":
         self.shortTrend = trend
      elif trendType == "mid":
         self.midTrend = trend
      elif trendType == "long":
         self.longTrend = trend
      elif trendType == "mega":
         self.megaTrend = trend

      date = self.cn.getTimeStamp()
      
      print(trendType + " Trend: " + str(round(trend, 2)) + " BAR: " + str(bar) + " date: " + str(date))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenOpenBuyLimit(self, barChart, bar):

      avgBarLen = self.bc.getAvgBarLen()
      
      # Tighten up the limit when profit has been taken
      if self.quickProfitCtr:
         avgBarLen = avgBarLen / self.quickProfitCtr
         
      self.openBuyLimit = self.cn.getCurrentAsk() + avgBarLen
      
      print ("AvgBarLen: setOpenBuyLimit: " + str(self.openBuyLimit))
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenOpenSellLimit(self, barChart, bar):

      avgBarLen = self.bc.getAvgBarLen()

      # Tighten up the limit when profit has been taken
      if self.quickProfitCtr:
         avgBarLen = avgBarLen / self.quickProfitCtr

      self.openSellLimit = self.cn.getCurrentBid() + avgBarLen
      
      print ("AvgBarLen: setOpenSellLimit: " + str(self.openSellLimit))
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenCloseBuyLimit(self, barChart, bar):

      avgBarLen = self.bc.getAvgBarLen()

      # Tighten up the limit when new bar seen. Indicates a range
      if self.positionType == self.buy:
         if self.avgBarLenCtr == bar and self.quickProfitCtr:
            print ("self.avgBarLenCtr == bar incrementing quickProfitCtr: " + str(self.avgBarLenCtr))
            self.quickProfitCtr += 1

      # Tighten up the limit when profit has been taken
      if self.quickProfitCtr:
         divisor = self.quickProfitCtr + 1
         if self.increaseCloseBarsMax < self.quickProfitCtr:
            divisor = self.increaseCloseBarsMax
         avgBarLen = avgBarLen / divisor
         print ("divisor: " + str(divisor))
         print ("avgBarLen: " + str(avgBarLen))
         print ("self.quickProfitCtr: " + str(self.quickProfitCtr))

      # only raise the limit
      if self.closeBuyLimit < self.cn.getCurrentAsk() - avgBarLen:
         self.closeBuyLimit = self.cn.getCurrentAsk() - avgBarLen
      
      print ("AvgBarLen: setCloseBuyLimit: " + str(self.closeBuyLimit))
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenCloseSellLimit(self, barChart, bar):

      avgBarLen = self.bc.getAvgBarLen()

      # Tighten up the limit when new bar seen. Indicates a range
      if self.positionType == self.sell:
         if self.avgBarLenCtr == bar and self.quickProfitCtr:
            print ("self.avgBarLenCtr == bar incrementing quickProfitCtr: " + str(self.avgBarLenCtr))
            self.quickProfitCtr += 1
         
      # Tighten up the limit when profit has been taken
      if self.quickProfitCtr:
         divisor = self.quickProfitCtr + 1
         if self.increaseCloseBarsMax < self.quickProfitCtr:
            divisor = self.increaseCloseBarsMax
         avgBarLen = avgBarLen / divisor
         print ("divisor: " + str(divisor))
         print ("avgBarLen: " + str(avgBarLen))
         print ("self.quickProfitCtr: " + str(self.quickProfitCtr))

      # only lower the limit
      if self.closeSellLimit > self.cn.getCurrentBid() + avgBarLen:
         self.closeSellLimit = self.cn.getCurrentBid() + avgBarLen
      
      print ("AvgBarLen: setCloseSellLimit: " + str(self.closeSellLimit))
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuyLimit(self, barChart, bar):

      if self.doHiLos:
         if self.aggressiveClose:
            self.openBuyLimit = self.getHighestClosePrice(self.closeBuyBars, barChart, bar)
            print ("AGR HiLo: setOpenBuyLimit to the highest close ")
         else:
            self.openBuyLimit = self.getHighestHiBarPrice(self.higherHighsBars, barChart, bar)
            print ("HiLo: setOpenBuyLimit to the highest hi " + str(self.openBuyLimit))
      

#      if self.aggressiveOpen:
#         self.openBuyLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
#         if not self.inPosition():
#            print ("aggressiveOpen openBuyLimit " + str(self.openBuyLimit))  
          
      else:
         self.openBuyLimit = self.getHighestHiBarPrice(self.higherHighsBars, barChart, bar)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenSellLimit(self, barChart, bar):

      if self.doHiLos:
         if self.aggressiveClose:
            self.openSellLimit = self.getLowestOpenPrice(self.openSellBars, barChart, bar)
            print ("AGR HiLo: openSellLimit to the lowest open " + str(self.openSellLimit))
         else:
            self.openSellLimit = self.getLowestLoBarPrice(self.lowerLowsBars, barChart, bar)
            print ("HiLo: setOpenSellLimit to the lowest lo " + str(self.openSellLimit))

#      if self.aggressiveOpen:
#         self.openSellLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
#         print ("AGR: aggressiveOpen openSellLimit " + str(self.openSellLimit))
         
      else:
         self.openSellLimit = self.getLowestLoBarPrice(self.lowerLowsBars, barChart, bar)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyLimit(self, barChart, bar):
   
      if self.doDynamic and self.isPriceInRange():
         self.closeBuyLimit = self.getHighestHiBarPrice(self.closeBuyBars, barChart, bar)
         print ("do Dynamic: setCloseBuyLimit to the getHighestHiLoBarPrice " + str(self.closeBuyLimit))
         
         self.closeSellLimit = self.getHighestLoBarPrice(self.closeSellBars, barChart, bar)
         print ("do Dynamic: closeSellLimit to the getHighestHiLoBarPrice " + str(self.closeBuyLimit))

      elif self.doHiLos:
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestClosePrice(self.closeBuyBars, barChart, bar)
            print ("AGR HiLo: setCloseBuyLimit to the highest low " + str(self.closeBuyLimit))
         else:
            self.closeBuyLimit = self.getLowestLoBarPrice(self.lowerLowsBars, barChart, bar)
            print ("HiLo: setCloseBuyLimit set to the lowest low " + str(self.closeBuyLimit))
      
      else:
         self.closeBuyLimit = self.getLowestLoBarPrice(self.lowerLowsBars, barChart, bar)
         if self.inPosition():
            print ("setCloseBuyLimit " + str(self.closeBuyLimit))
            
      if self.closePositionFudge and self.closeBuyLimit != 0.0:         
         self.closeBuyLimit -= (self.closePositionFudge - float(self.getBarsInPosition()))
         print ("setCloseBuyLimit AFTER fudge " + str(self.closeBuyLimit))

      # Move the buy limit closer to the price if in a gain
      if self.gainTrailStop and self.getGain():
            if (self.cn.getCurrentAsk() - self.gainTrailStop) > self.closeBuyLimit:
               self.closeBuyLimit = self.cn.getCurrentAsk() - self.gainTrailStop
               print ("setCloseBuyLimit AFTER gainTrailStop " + str(self.closeBuyLimit))           
         
      #if self.closeBuyLimit > self.highestcloseBuyLimit:
      #   self.highestcloseBuyLimit = self.closeBuyLimit

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellLimit(self, barChart, bar):

      if self.doHiLos:
         if self.aggressiveClose:
            self.closeSellLimit = self.getLowestOpenPrice(self.openSellBars, barChart, bar)
            print ("AGR HiLo: setCloseSellLimit to the lowest open " + str(self.closeSellLimit))
         else:
            self.closeSellLimit = self.getHighestHiBarPrice(self.higherHighsBars, barChart, bar)
            print ("HiLo: setCloseSellLimit to the highest hi " + str(self.closeSellLimit))
            
      else:
         self.closeSellLimit = self.getHighestHiBarPrice(self.higherHighsBars, barChart, bar)
         if self.inPosition():
            print ("setCloseSellLimit " + str(self.closeSellLimit))
               
      if self.closePositionFudge and self.closeSellLimit != 0.0:
         self.closeSellLimit += (self.closePositionFudge - float(self.getBarsInPosition()))
         print ("setCloseSellLimit AFTER fudge " + str(self.closeSellLimit))

      # Move the sell limit closer to the price if in a gain
      if self.gainTrailStop and self.getGain():
            if (self.cn.getCurrentBid() + self.gainTrailStop) < self.closeSellLimit:
               self.closeSellLimit = self.cn.getCurrentBid() + self.gainTrailStop
               print ("setCloseSellLimit AFTER gainTrailStop " + str(self.closeSellLimit))
         
      #if self.closeSellLimit < self.lowestcloseSellLimit:
      #   self.lowestcloseSellLimit = self.closeSellLimit
      #   print ("setCloseSellLimit AFTER fudge " + str(self.lowestcloseSellLimit))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBuySellLimits(self, barChart, bar):
      
      if (self.isBullTrend() or self.isBearTrend()) and self.inPosition():
         if self.increaseCloseBars:
            if self.getBarsInPosition() < self.increaseCloseBarsMax:
               self.triggerBars += self.getBarsInPosition()
               print("in trend increasing close bars: " + str(self.getBarsInPosition()) + "triggerBars: " + str(self.triggerBars))
         
      self.setOpenBuyLimit(barChart, bar)
      self.setOpenSellLimit(barChart, bar)
      self.setCloseBuyLimit(barChart, bar)
      self.setCloseSellLimit(barChart, bar)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenLimits(self, barChart, bar):
      
      #self.setAvgBarLenOpenBuyLimit(barChart, bar)
      #self.setAvgBarLenOpenSellLimit(barChart, bar)
      self.setAvgBarLenCloseBuyLimit(barChart, bar)
      self.setAvgBarLenCloseSellLimit(barChart, bar)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setExecuteOnOpenPosition(self, executeOnOpenPosition):

      self.executeOnOpenPosition = executeOnOpenPosition

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setExecuteOnClosePosition(self, executeOnClosePosition):

      self.executeOnClosePosition = executeOnClosePosition

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLinesInFile(self, path):

    f = open(path)                  
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAlgorithmMsg(self):
         
      return self.algoMsg

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAlgorithmMsg(self):
         
      self.algoMsg += "Algorithms set:\n"
      
      if self.doDefault:
         self.algoMsg += "         Default\n"
      if self.doHiLos:
            self.algoMsg += "         Hi Los\n"
      if self.doOpensCloses:
         self.algoMsg += "         Opens and Closes\n"
      if self.doExecuteOnOpen:
         self.algoMsg += "         Execute on Open\n"
      if self.doExecuteOnClose:
         self.algoMsg += "         Execute on Close\n"
      if self.doHiLoOnClose:
         self.algoMsg += "         Hi Lo's on execute on close\n"
      if self.doHiLoOnOpen:
         self.algoMsg += "         Hi Lo's on execute on open\n"
      if self.doReversalPattern:
         self.algoMsg += "         Reversal patterns\n"
      if self.doTrends:
         self.algoMsg += "         Trends\n"
      if self.doQuickProfit:
         self.algoMsg += "         Quick Profit\n"
      if self.doQuickReversal:
         self.algoMsg += "         Quick Reversal\n"
      if self.doReverseBuySell:
         self.algoMsg += "         Reverse Logic\n"

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getQuickReversal(self):

      return self.doQuickReversal

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getExecuteOnOpenPosition(self):

      return self.executeOnOpenPosition

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTriggerBars(self):

      return self.triggerBars

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getExecuteOnClosePosition(self):

      return self.executeOnClosePosition

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getGain(self):

      if self.cn.getCurrentBid() > self.openPositionPrice:
         return 1

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getInitialStopLoss(self):

      return self.initialStopLoss
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getInitialStopGain(self):

      return self.initialStopGain
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getClosePrice(self):

      if self.positionType == self.buy:
         return self.closeBuyLimit
      elif self .positionType == self.sell:
         return self.closeSellLimit
         
      return 0.0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestCloseBuyPrice(self):

      return self.lowestcloseBuyLimit
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestCloseBuyPrice(self):

      return self.highestcloseBuyLimit    
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestCloseSellPrice(self):

      return self.lowestcloseSellLimit
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestCloseSellPrice(self):

      return self.highestcloseSellLimit      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOpenSellPrice(self):

      return self.openSellLimit     
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOpenBuyPrice(self):

      return self.openBuyLimit
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getStopGain(self):

      return self.stopGain
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getPositionType(self):

      return self.positionType
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getRangeBars(self):
   
      if self.rangeBars >= currentBar:
         return 1
      
      return 0
               

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setWaitForNextBar(self):
   
      self.waitForNextBar += 1
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetWaitForNextBar(self):
   
      self.waitForNextBar = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getWaitForNextBar(self):
   
      return self.waitForNextBar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getProfitPctTriggerAmt(self):
   
      return self.profitPctTriggerAmt
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentBar(self):

      return self.currentBar
                  
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextBar(self):
   
      return self.nextBar

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getPositionPrice(self):
   
      return self.positionPrice     
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getExecuteOnClose(self):
   
      return self.doExecuteOnClose
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getExecuteOnOpen(self):
   
      return self.executeOnOpen
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBarsInPosition(self):
   
      return self.barCountInPosition 
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBarsCount(self):
   
      return self.barCount 
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getProfitTarget(self):

      return self.profitTarget

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getShortTrend(self):

      return self.shortTrend
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMidTrend(self):

      return self.midTrend
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLongTrend(self):

      return self.longTrend
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMegaTrend(self):

      return self.megaTrend
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTrendTrigger(self):

      return self.doTrends
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullShortTrend(self):
      
      if self.getShortTrend() >= 1.5:
         print("IN BULL SHORT TREND " + str(self.getShortTrend()))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearShortTrend(self):
      
      if self.getShortTrend() >= 3.7:
         print("IN BEAR SHORT TREND " + str(self.getShortTrend()))
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullMidTrend(self):
      
      if self.getMidTrend() >= 1.5:
         print("IN BULL MID TREND " + str(self.getMidTrend()))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearMidTrend(self):
      
      if self.getMidTrend() >= 3.6:
         print("IN BEAR MID TREND " + str(self.getMidTrend()))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullLongTrend(self):
      
      if self.getLongTrend() >= 1.5:
         print("IN BULL LONG TREND " + str(self.getLongTrend()))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearLongTrend(self):
      
      if self.getMidTrend() >= 3.6:
         print("IN BEAR LONG TREND " + str(self.getLongTrend()))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullMegaTrend(self):
      
      if self.getMegaTrend() >= 1.5:
         print("IN BULL MEGA TREND " + str(self.getMegaTrend()))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearMegaTrend(self):
      
      if self.getMidTrend() >= 3.6:
         print("IN BEAR MEGA TREND " + str(self.getMegaTrend()))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearTrend(self):
      # Bear trend means mid, long and mega trends are bearish
      
      if self.getMegaTrend() >= 3.0 and self.getMidTrend() >= 3.0 and self.getLongTrend() >= 3.0:
         print("IN LONG BEAR TREND")
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullTrend(self):
      # Bull trend means mid, long and mega are bullish
      
      shortTrend = self.getShortTrend()
      midTrend = self.getMidTrend()
      longTrend = self.getLongTrend()
      megaTrend = self.getMegaTrend()
         
      #if shortTrend >= 1.0 and shortTrend <= 2.0:
      if midTrend >= 1.0 and midTrend <= 2.0:
         if longTrend >= 1.0 and longTrend <= 2.0:
            if megaTrend >= 1.0 and megaTrend <= 2.0:
               print("IN LONG BULL TREND")
               return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getEndOfMarketTime(self): 
         
      return self.marketEndTime
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isMarketExitTime(self): 
      
      if self.cn.getTimeHrMnSecs() > self.getEndOfMarketTime():
         return 1
      
      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDynamic(self):

      return self.doDynamic
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestCloseOpenPrice(self, numBars, barChart, bar):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1
         
      while n < numBars:
         open = barChart[bar - n][self.op]
         close = barChart[bar - n][self.cl]
 
         minPriceArr[n] = open
         if close < open:
            minPriceArr[n] = close
         n += 1
         
      #print ("min price arr: " + str(minPriceArr))
      
      # Compare all min prices and find the lowest price
      clean = 1
      n = 0
      minPrice = 0.0

      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = 0
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestCloseOpenPrice(self, numBars, barChart, bar):

      if len(barChart) < numBars:
         return 0.0

      n = 0
      maxPriceArr = [0.0] * numBars 
      barChartLen = len(barChart) - 1
                  
      while n < numBars:
         open = barChart[bar - n][self.op]
         close = barChart[bar - n][self.cl]
 
         maxPriceArr[n] = open
         if close > open:
            maxPriceArr[n] = close
         n += 1
         
      #print ("max price arr: " + str(maxPriceArr))
      
      # Compare all max prices and find the highest price
      clean = 1
      n = 0
      maxPrice = 0.0

      while n < numBars:
         if clean:
            maxPrice = maxPriceArr[n]
            clean = 0
            continue
         
         if maxPriceArr[n] > maxPrice:
            maxPrice = maxPriceArr[n]
         
         n += 1

      return float(maxPrice)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestClosePrice(self, numBars, barChart, bar):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      # Fill the list
      while n < numBars:
         minPriceArr[n] = barChart[bar - n][self.cl]
         n += 1
         
      # Compare all the closes and find the lowest price
      clean = 1
      n = 0
      minPrice = 0.0

      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = 0
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherHighs(self):
   
      if not self.higherHighsBars:
         return 0

      if len(self.hiValues) < self.higherHighsBars:
         return 0

      highest = self.hiValues[0]
      
      n = 1
      while n < self.higherHighsBars:
         hi = self.hiValues[n]
         if hi >= highest:
            return 0
         highest = self.hiValues[n]
         n += 1
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherLows(self): 
   
      if not self.higherLowsBars:
         return 0
         
      if len(self.lowValues) < self.higherLowsBars:
         return 0

      lowest = self.lowValues[0]
      
      n = 1
      while n < self.higherLowsBars:
         lo = self.lowValues[n]
         if lo >= lowest:
            return 0
         lowest = self.lowValues[n]
         n += 1

      return 1
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerHighs(self): 
   
      if not self.lowerHighsBars:
         return 0
         
      if len(self.hiValues) < self.lowerHighsBars:
         return 0
         
      highest = self.hiValues[0]
      
      n = 1
      while n < self.lowerHighsBars:
         hi = self.hiValues[n]
         if hi <= highest:
            return 0
         highest = self.hiValues[n]
         n += 1

      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerLows(self):
   
      if not self.lowerLowsBars:
         return 0
         
      if len(self.lowValues) < self.lowerLowsBars:
         return 0
         
      lowest = self.lowValues[0]
      
      n = 1
      while n < self.lowerLowsBars:
         lo = self.lowValues[n]
         if lo <= lowest:
            return 0
         lowest = self.lowValues[n]
         n += 1
         
      return 1
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerOpens(self, numBars, priceArr):
    
      if len(priceArr) < numBars:
         return 0
         
      lowest = priceArr[0]
      
      n = 1
      while n < numBars:
         lo = priceArr[n]
         if lo <= lowest:
            return 0
         lowest = priceArr[n]
         n += 1

      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerCloses(self, numBars, priceArr):
   
      if len(priceArr) < numBars:
         return 0
         
      lowest = priceArr[0]
      
      n = 1
      while n < numBars:
         lo = priceArr[n]
         if lo <= lowest:
            return 0
         lowest = lo
         n += 1

      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherOpens(self, numBars, priceArr):

      if len(priceArr) < numBars:
         return 0
                  
      highest = priceArr[0]
      
      n = 1
      while n < numBars:
         hi = priceArr[n]
         if hi >= highest:
            return 0
         highest = priceArr[n]
         n += 1
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherCloses(self, numBars, priceArr):
   
      if not self.closeBuyBars:
         return 0
        
      if len(self.closeBuyValues) < self.closeBuyBars:
         return 0
         
      highest = priceArr[0]
      
      n = 1
      while n < numBars:
         hi = priceArr[n]
         if hi >= highest:
            return 0
         highest = hi
         n += 1
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestClosePrice(self):
   
      if bar < numBars:
         return 0.0
      
      priceArr = len(self.openBuyValues)
      price = self.closeBuyValues[0]
      
      n = 1
      while n < priceArr:         
         if price < self.closeBuyValues[n]:
            price = self.closeBuyValues[n]
         n += 1

      return float(price)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestOpenPrice(self, numBars, barChart, bar):
   
      if bar < numBars:
         return 0.0
      
      priceArr = len(self.openBuyValues)
      price = self.openBuyValues[0]
      
      n = 1
      while n < priceArr:         
         if price < self.openBuyValues[n]:
            price = self.openBuyValues[n]
         n += 1

      return float(price)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestOpenPrice(self, numBars, barChart, bar):
   
      if bar < numBars:
         return 0.0
      
      maxPriceArr = len(self.openBuyValues)
      maxPrice = self.op[0]
      
      n = 1
      while n < maxPriceArr:         
         if maxPrice < self.openBuyValues[n]:
            maxPrice = self.openBuyValues[n]
         n += 1

      return float(maxPrice)      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestLoBarPrice(self, numBars, barChart, bar):
   
      if bar < numBars:
         return 0.0
      
      minPriceLen = len(self.hiValues)
      minPrice = self.lowValues[0]
      
      n = 1
      while n < minPriceLen:         
         if minPrice > self.lowValues[n]:
            minPrice = self.lowValues[n]
         n += 1

      return float(minPrice)      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestLoBarPrice(self, numBars, barChart, bar):
   
      if bar < numBars:
         return 0.0
      
      maxPriceLen = len(self.hiValues)
      maxPrice = self.hiValues[0]
      
      n = 1
      while n < maxPriceLen:         
         if maxPrice > self.hiValues[n]:
            maxPrice = self.hiValues[n]
         n += 1
      
      return float(maxPrice)      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestHiBarPrice(self, numBars, barChart, bar):
      
      if bar < numBars:
         return 0.0
      
      maxPriceLen = len(self.hiValues)
      maxPrice = self.hiValues[0]
      
      n = 1
      while n < maxPriceLen:         
         if maxPrice < self.hiValues[n]:
            maxPrice = self.hiValues[n]
         n += 1
      
      return float(maxPrice)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestHiBarPrice(self, numBars, barChart, bar):

      if bar < numBars:
         return 0.0
      
      minPrice = self.hiValues[0]
      
      n = 1
      while n < numBars:         
         if minPrice > self.hiValues[bar - n]:
            minPrice = self.hiValues[bar - n]
         n += 1
      
      return float(minPrice)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestHiLoBarPrice(self, numBars, barChart, bar):
   
      if len(barChart) < numBars or bar < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      while n < numBars:
         hi = barChart[bar - n][self.hi]
         lo = barChart[bar - n][self.lo]
 
         minPriceArr[n] = hi
         if lo < hi:
            minPriceArr[n] = lo
         n += 1
         
      # Compare all min prices and find the lowest price
      clean = 1
      n = 0
      minPrice = 0.0
      
      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = 0
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestHiLoBarPrice(self, numBars, barChart, bar):
   
      if len(barChart) < numBars or bar < numBars:
         return 0.0

      n = 0
      maxPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      while n < numBars:
         hi = barChart[bar - n][self.hi]
         lo = barChart[bar - n][self.lo]
 
         maxPriceArr[n] = hi
         if lo < hi:
            maxPriceArr[n] = lo
         n += 1
         
      # Compare all max prices and find the lowest price
      clean = 1
      n = 0
      maxPrice = 0.0
      
      while n < numBars:
         if clean:
            maxPrice = maxPriceArr[n]
            clean = 0
            continue
         
         if maxPriceArr[n] > maxPrice:
            maxPrice = maxPriceArr[n]
         
         n += 1

      return float(maxPrice)

         
