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

   def __init__(self, data, lg, cn, bc, tr, lm, pa, pr, offLine=0, stock=""):
   
      self.data = data
      self.lg = lg
      self.cn = cn
      self.bc = bc
      self.tr = tr
      self.lm = lm
      self.pa = pa
      self.pr = pr
      self.offLine = offLine
      self.stock = stock

      print (str(self.bc))

      # Required standard settings
      self.algorithms = str(data['profileTradeData']['algorithms'])
            
      # Algorithms
      self.timeBar = int(data['profileTradeData']['timeBar'])
      self.doDefault = int(data['profileTradeData']['doDefault'])
      self.doHiLo = int(data['profileTradeData']['doHiLo'])
      self.doHiLoSeq = int(data['profileTradeData']['doHiLoSeq'])
      self.doOpensCloses = int(data['profileTradeData']['doOpensCloses'])
      self.doExecuteOnClose = int(data['profileTradeData']['doExecuteOnClose'])
      self.doExecuteOnOpen = int(data['profileTradeData']['doExecuteOnOpen'])
      self.doHiLoOnClose = int(data['profileTradeData']['doHiLoOnClose'])
      self.doHiLoOnOpen = int(data['profileTradeData']['doHiLoOnOpen'])
      self.doQuickReversal = int(data['profileTradeData']['doQuickReversal'])
      self.doReversalPattern = int(data['profileTradeData']['doReversalPattern'])
      self.doReverseBuySell = int(data['profileTradeData']['doReverseBuySell'])
      self.doQuickProfit = int(data['profileTradeData']['doQuickProfit'])
      self.doTrends = int(data['profileTradeData']['doTrends'])
      self.doDynamic = int(data['profileTradeData']['doDynamic'])
      self.doOnlyBuys = int(data['profileTradeData']['doOnlyBuys'])
      self.doOnlySells = int(data['profileTradeData']['doOnlySells'])
      self.doOnlyTrends = int(data['profileTradeData']['doOnlyTrends'])
      self.doSessions = int(data['profileTradeData']['doSessions'])
      self.doInPosTracking = int(data['profileTradeData']['doInPosTracking'])
      self.doPatterns = int(data['profileTradeData']['doPatterns'])
      self.doVolatility = int(data['profileTradeData']['doVolatility'])
      self.doAverageVolume = int(data['profileTradeData']['doAverageVolume'])
      self.doVolumeLastBar = int(data['profileTradeData']['doVolumeLastBar'])
      self.doPriceMovement = int(data['profileTradeData']['doPriceMovement'])

      self.currency = str(data['profileTradeData']['currency'])
      self.alt = str(data['profileTradeData']['alt'])
      self.marketBeginTime = int(data['profileTradeData']['marketBeginTime'])
      self.marketEndTime = int(data['profileTradeData']['marketEndTime'])
      self.preMarket = int(data['profileTradeData']['preMarket'])
      self.afterMarket = int(data['profileTradeData']['afterMarket'])
      self.quickProfitMax = int(data['profileTradeData']['quickProfitMax'])
      self.priceChangeMultiplier = int(data['profileTradeData']['priceChangeMultiplier'])

      # Increase the number of bars used determining close price
      self.increaseCloseBars = int(data['profileTradeData']['increaseCloseBars'])
      self.increaseCloseBarsMax = int(data['profileTradeData']['increaseCloseBarsMax'])
      self.gainTrailStop = int(data['profileTradeData']['gainTrailStop'])
      self.useAvgBarLimits = int(data['profileTradeData']['useAvgBarLimits'])

      # Additional value to add to close triggers
      self.closePositionFudge = float(data['profileTradeData']['closePositionFudge'])
            
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
      
      self.profitPctTrigger = float(data['profileTradeData']['profitPctTrigger'])
      self.profitPctTriggerBar = float(data['profileTradeData']['profitPctTriggerBar'])
      self.reversalPctTrigger = float(data['profileTradeData']['reversalPctTrigger'])
      self.volumeRangeBars = int(data['profileTradeData']['volumeRangeBars'])
      self.amountPct = float(data['profileTradeData']['amountPct'])
      
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

      self.triggerBars = 0
      self.currentBar = 0
      self.nextBar = 0
      self.rangeTradeValue = 0
      #self.rangeHi = 0.0
      #self.rangeLo = 0.0
      self.priceInRange = 0
      
      self.hiValues = [0.0] 
      self.lowValues = [0.0]
      self.openValues = [0.0] 
      self.closeValues = [0.0]

      self.topIntraBar = 0.0
      self.bcrCounter = 0
      self.revDirty = 0
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

      self.useAvgBarLen = 0
      self.avgBarLenCtr = 0

      self.totalGain = 0.0
      self.targetProfit = 0.0
      self.quickProfitCtr = 0
      self.numTrades = 1
      self.lastCloseBuyLimit = 0.0
      self.lastCloseSellLimit = 9999.99
      
      self.bid = 0.0
      self.ask = 0.0
      self.last = 0.0
      self.reversAction = 0
      self.hammer = 0
      self.priceMovement = 0
      self.profitGained = 0.0
      self.stopTarget = 0
      self.runningVolume = 0
      self.runningAvgVolume = 0
      self.currentVol = 0
      self.previousBarSegment = self.barSegment = 0
      self.stoppedOut = 4
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAllLimits(self, bc, bar):
      
      self.lg.debug("self.lm.getMaxNumWaitBars() " + str(self.lm.getMaxNumWaitBars()))
      self.lg.debug("bar " + str(bar))

      print ("setAllLimits self.runningVolume " + str(self.runningVolume))
      
      self.lg.debug("self.pr.getCurrentPriceIdx() " + str(self.pr.getCurrentPriceIdx()))
      
      if self.pr.getCurrentPriceIdx() % self.timeBar == 0:
         print ("self.pr.getCurrentPriceIdx() % self.timeBar " + str(self.pr.getCurrentPriceIdx() % self.timeBar))
         self.runningVolume = self.currentVol = 0
         self.runningAvgVolume = 0
         self.previousBarSegment = self.barSegment = 0
         
      # bar count starts at 0 sub 1
#      if bar < self.lm.getMaxNumWaitBars():
      if bar < self.lm.getMaxNumWaitBars() - 1:
         return
         
      if self.lm.doRangeTradeBars:
         if bar < self.lm.doRangeTradeBars:
         #if bar < self.lm.doRangeTradeBars - 1:
            return
            
      self.lm.setRangeLimits(bc, bar)
         
      self.bc.setAvgBarLen(bc, bar)

      self.bc.setAvgVol(bc, bar + 1)
      
      #self.bc.setAvgVolTime(bc, bar, self.timeBar, self.pr.getCurrentPriceIdx())
      
      if self.lm.setOpenCloseHiLoValues(bc, bar, self.lm.getMaxNumWaitBars()):
         self.lm.setOpenCloseHiLoConditions(self.lm.getMaxNumWaitBars())

      defaultNumBars = 0
      self.lm.setOpenBuySellLimits(defaultNumBars, bar - 1)

      if self.useAvgBarLimits:
         if not self.inPosition():
            self.lm.unsetCloseAvgBarLenLimits(bc, bar)
         self.lm.setCloseAvgBarLenLimits(bc, bar)
      else:
         self.lm.setCloseBuySellLimits(defaultNumBars, bar - 1)
         
      self.setNextBar(bar + 1)
      self.unsetWaitForNextBar()
      
      self.revDirty = 0
      self.priceMovement = 0

      #self.setDynamic(bar)
         
      self.setAlgorithmMsg()
            
      #if self.doDynamic:
      #   self.algorithmDynamic(bar)
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLiveProfileValues(self, data, profilePath):
   
      displayHeader = profilePath
      displayHeader += "\nProfile items: "
         
      for key, value in data.items():
         for k, v in value.items():
            if k == "currency" or k == "alt":
               continue
            if v >= '1':
               displayHeader += v + " " + k + "\n"
      
      return displayHeader
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takePosition(self, bid, ask, last, vol, barChart, bar):
   
      self.setCurrentBid(bid)
      self.setCurrentAsk(ask)
      self.setCurrentLast(last)
      self.setCurrentVol(vol)
      
      if bar < self.lm.getMaxNumWaitBars():
         return 0
         
      # Determine if position should be opened
      action = self.takeAction(barChart, bar, bid, ask, last, vol)
      
      if action == self.stoppedOut:
         return self.stoppedOut
      
      # Open position 
      if not self.inPosition():
         if action == self.buy:
            if self.doReverseBuySell: 
               self.lg.debug("reversing the buy -> sell. Using avgBarLen: " + str(action))
               self.useAvgBarLen += 1
               self.useAvgBarLimits += 1
               self.lm.setAvgBarLenLimits(barChart, bar)

               self.openPosition(self.sell, bar, barChart, bid, ask)
            else: 
               self.openPosition(self.buy, bar, barChart, bid, ask)
            
         elif action == self.sell:               
            if self.doReverseBuySell:
               self.lg.debug("reversing the sell -> buy Using avgBarLen: " + str(action))
               self.useAvgBarLen += 1
               self.useAvgBarLimits += 1
               self.lm.setAvgBarLenLimits(barChart, bar)

               self.openPosition(self.buy, bar, barChart, bid, ask)
            else: 
               self.openPosition(self.sell, bar, barChart, bid, ask)

      # Close position
      elif self.inPosition():
         if action == self.buy:
            self.closePosition(bar, barChart, bid, ask, 0)
            if self.doQuickReversal and not self.isPriceInRange():
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.sell, bar, barChart, bid, ask)
            
         elif action == self.sell:
            self.closePosition(bar, barChart, bid, ask, 0)
            if self.doQuickReversal and not self.isPriceInRange():
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.buy, bar, barChart, bid, ask)

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takeAction(self, barChart, bar, bid, ask, last, vol):
   
      action = 0
      exitAlgo = 3
      
      if self.doDynamic:
         self.algorithmDynamic(action)
     
      if self.doInPosTracking:
         action = self.algorithmPosTracking(last, action)
         if action == self.stoppedOut:
            return self.stoppedOut
     
      if self.doVolatility:
         self.algorithmVolatility(action)
     
      if self.doQuickProfit:
         if self.algorithmQuickProfit(barChart, bar, bid, ask, action) == exitAlgo:
            # We took profit exit algo's
            return 0
      
      if self.doExecuteOnClose:
         action = self.algorithmOnClose(barChart, bar, action)

      if self.doExecuteOnOpen:
         action = self.algorithmOnOpen(barChart, bar, action)

# Do patterns. Stay in position when hi are higher or lows are lower except when 
# close is higher than open for a sell position or a
# close is lower than an open for a buy position

      if self.doHiLo:
         action = self.algorithmHiLo(barChart, bar, bid, ask, last, vol, action)
         
      if self.doHiLoSeq:
         action = self.algorithmHiLoSeq(barChart, bar, bid, ask, last, vol, action)
         
      if self.doReversalPattern:
         action = self.algorithmReversalPattern(barChart, bar, ask, action)
      
      if self.doOnlyTrends:
         action = self.algorithmDoOnlyTrends(barChart, bar, action)
         
      if self.lm.doRangeTradeBars:
         action = self.algorithmDoInRange(barChart, bar, action)
         
      if self.doDefault:
         action = self.algorithmDefault(barChart, bar, bid, ask, action)

      if self.doReverseBuySell:
         action = self.algorithmReverseBuySell(action)
         
      if self.doAverageVolume:
         action = self.algorithmAverageVolume(barChart, bar, vol, action)

      if self.doVolumeLastBar:
         action = self.algorithmVolumeLastBar(barChart, bar, vol, action)

      if self.doPriceMovement:
         action = self.algorithmPriceMovement(bar, bid, ask, last, action)
         #if self.algorithmPriceMovement(bar, bid, ask, last, action) == exitAlgo:
            # Don't get caught opening a position on a skewed price
            
      if self.doPatterns:
         action = self.algorithmPatterns(barChart, bar, action)
     
      if action  > 0:
         print ("Action being taken!! " + str(action))
     
      return action
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPriceMovement(self, bar, bid, ask, last, action=0):
      
      # Compare previous prices (ask) and don't take a position if the price
      # moves 3x the average movement
      
      self.lg.debug ("In algorithmPriceMovement: " + str(action))
      
      if bar < 2:
         return action

      # If no signal or priceMovement not set then return
      if not action:
         if self.priceMovement == 0:
            return 0

      self.lg.debug ("self.priceMovement: " + str(self.priceMovement))

      if self.inPosition():
         return action

      avgChange = lastChange = 0.0

      if action == self.buy:
         self.lg.debug ("ask: " + str(ask))
         self.lg.debug ("self.priceMovement >= ask " + str(self.priceMovement >= ask))
         #if self.priceMovement > 0 and self.priceMovement >= self.cn.getCurrentAsk(self.stock):
         if self.priceMovement > 0 and self.priceMovement >= ask:
            return action
         elif self.priceMovement > 0:
            return 0
         lastChange = round(last - self.cn.getCurrentAsk(self.stock), 2)
         avgChange = self.pr.getAverageAskChange(bar)
      elif action == self.sell:
         self.lg.debug ("bid: " + str(bid))
         self.lg.debug ("self.priceMovement <= bid: " + str(self.priceMovement <= bid))
         #if self.priceMovement > 0 and self.priceMovement <= self.cn.getCurrentBid(self.stock):
         if self.priceMovement > 0 and self.priceMovement <= bid:
            return action
         elif self.priceMovement > 0:
            return 0
         #lastChange = round(last - self.cn.getCurrentBid(self.stock), 2)
         lastChange = bid
         avgChange = self.pr.getAverageBidChange(bar)
            
      if lastChange < 0:
         lastChange = lastChange*-1
      
      avgChange *= self.priceChangeMultiplier
      
      self.lg.debug ("lastChange: " + str(lastChange))
      self.lg.debug ("avgChange: " + str(avgChange))
      self.lg.debug ("last: " + str(last))
      self.lg.debug ("ask " + str(ask))
      self.lg.debug ("bid: " + str(bid))
#      self.lg.debug ("self.getCurrentAsk(): " + str(self.cn.getCurrentAsk(self.stock)))
#      self.lg.debug ("self.getCurrentBid: " + str(self.cn.getCurrentBid(self.stock)))
               
      if lastChange > avgChange:
         self.lg.debug ("lastChange > avgChange ")
         
         # Wait for price to come back to where it was
         if action == self.buy:
            #self.priceMovement = round(self.cn.getCurrentAsk(self.stock) - lastChange, 2)
            self.priceMovement = round(ask - lastChange, 2)
         elif action == self.sell:
            #self.priceMovement = round(self.cn.getCurrentBid(self.stock) + lastChange, 2)
            self.priceMovement = round(bid + lastChange, 2)
         self.lg.debug ("self.priceMovement " + str(self.priceMovement))
         return 0
            
      return action

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmVolumeLastBar(self, barChart, bar, vol, action=0):
         
      self.lg.debug ("In algorithmAverageLastBar: " + str(action))

      # Use last bar volume to verify signal

      self.barSegment = self.pr.getCurrentPriceIdx() % self.timeBar
      
      self.lg.debug ("self.barSegment: " + str(self.barSegment))
      self.lg.debug ("self.pr.getCurrentPriceIdx(): " + str(self.pr.getCurrentPriceIdx()))

      if self.timeBar > 1:
         if self.barSegment != self.previousBarSegment:
            self.previousBarSegment = self.barSegment
            self.runningAvgVolume += self.currentVol
         else:
            self.currentVol = self.runningAvgVolume + vol
      else:
         self.currentVol = vol
               
      # If no signal then return
      if not action:
         return action

      # using average volume to get out of a position
      if not self.inPosition():
         return action
      # using average volume to get into a position
      #if self.inPosition():
      #   return action
      
      previousBarVol = int(barChart[bar - 1][self.vl])
      
      self.lg.debug ("self.currentVol: " + str(self.currentVol))
      self.lg.debug ("self.runningVolume: " + str(self.runningVolume))
      self.lg.debug ("previousBarVol: " + str(previousBarVol))
         
      # If volume isn't > previous bar volume, cancel signal
      #if int(currentVol) > int(previousBarVol):
      # If volume isn't > average volume, cancel signal
      
      if self.runningAvgVolume > previousBarVol:
         self.lg.debug ("self.runningAvgVolume is > avgVol: " + str(self.runningAvgVolume) + " " + str(previousBarVol))
         return action
      elif self.currentVol > previousBarVol:
         self.lg.debug ("currentVol is > avgVol: " + str(self.currentVol) + " " + str(previousBarVol))
         return action
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmAverageVolume(self, barChart, bar, vol, action=0):
         
      self.lg.debug ("In algorithmAverageVolume: " + str(action))

      # Use average volume to verify signal

      # Implement volume plus price direction. high volume coming down even though trend is up
      
      self.barSegment = self.pr.getCurrentPriceIdx() % self.timeBar
      
      self.lg.debug ("self.barSegment: " + str(self.barSegment))
      self.lg.debug ("self.pr.getCurrentPriceIdx(): " + str(self.pr.getCurrentPriceIdx()))

      if self.timeBar > 1:
         if self.barSegment != self.previousBarSegment:
            self.previousBarSegment = self.barSegment
            self.runningAvgVolume += self.currentVol
         else:
            self.currentVol = self.runningAvgVolume + vol
      else:
         self.currentVol = vol
               
      self.lg.debug ("self.runningAvgVolume: " + str(self.runningAvgVolume))
      self.lg.debug ("self.currentVol: " + str(self.currentVol))
      self.lg.debug ("vol: " + str(vol))

      # If no signal then return
      if not action:
         return action

      # using average volume to get into a position
      if not self.inPosition():
         return action
      # using average volume to get out of a position
      #if self.inPosition():
      #   return action

      avgVol = self.bc.getAvgVol()

      self.lg.debug ("self.runningAvgVolume: " + str(self.runningAvgVolume))
      self.lg.debug ("avgVol: " + str(avgVol))

      if avgVol < 1:
         return 0
         
      # If volume isn't > average volume, cancel signal
      if self.runningAvgVolume > avgVol :
         self.lg.debug ("self.runningAvgVolume is > avgVol: " + str(self.runningAvgVolume) + " " + str(avgVol))
         return action
      elif self.currentVol > avgVol :
         self.lg.debug ("currentVol is > avgVol: " + str(self.currentVol) + " " + str(avgVol))
         return action

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmReversalPattern(self, barChart, bar, ask, action=0):
         
      self.lg.debug ("In algorithmReversalPattern: " + str(action))

      # Detect a reversal pattern in the current bar. triggerring when
      # current bar is > than previous bar
   
      if self.inPosition() and self.doReversalPattern():
         previousBarLen = float(barChart[i-1][cl] - barChart[i-1][op])
         #currentBarLen = barChart[i][op] - self.cn.getCurrentAsk(self.stock)
         currentBarLen = barChart[i][op] - ask
         
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
               self.closePosition(bar, barChart, bid, ask, 0)

      return 1
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmReverseBuySell(self, action):

#      self.lg.debug ("In algorithmReverseBuySell: ")
#
#      if action == self.sell:
#         self.lg.debug ("Reversing from SELL to BUY...")
#         action = self.buy
#      elif action == self.buy:
#         self.lg.debug ("Reversing from BUY to SELL...")
#         action = self.sell
          
#      if self.doReverseBuySell:
#         self.setRevBuySell()
      
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmQuickProfit(self, barChart, bar, bid, ask, action=0):
   
      if not self.inPosition():         
         return action

      self.lg.debug ("In algorithmQuickProfit: " + str(action))
      
      # We've taken at least one profit so set the avg bar length
      #if self.quickProfitCtr:
         # Use avg bar length as the stop instead of original limits
      #   self.lm.setAvgBarLenLimits(barChart, bar)
      #else:
      #   self.avgBarLenCtr = bar + 1      
      
      profitTarget = self.getProfitTarget()
      self.lg.debug ("Target profit set to: " + str(profitTarget))
      
      if self.getPositionType() == self.buy:
         if self.cn.getCurrentAsk(self.stock) > profitTarget:
            self.lg.debug ( "CLOSING BUY POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(ask) + " > " + str(profitTarget))
            #self.lg.debug (str(self.cn.getCurrentAsk(self.stock)) + " > " + str(profitTarget))
            #self.quickProfitCtr += 1
            self.closePosition(bar, barChart, bid, ask, 1)
            self.setWaitForNextBar()
            return 3
            
      elif self.getPositionType() == self.sell:
         if self.cn.getCurrentBid(self.stock) < profitTarget:
            self.lg.debug ( "CLOSING SELL POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(bid) + " < " + str(profitTarget))
            #self.lg.debug (str(self.cn.getCurrentBid(self.stock)) + " < " + str(profitTarget))
            #self.quickProfitCtr += 1
            self.closePosition(bar, barChart, bid, ask, 1)
            self.setWaitForNextBar()
            return 3
                 
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoInRange(self, barChart, bar, action=0):
   
      self.lg.debug("In algorithmDoInRange. Action: " + str(action))
      self.reversAction = 0

      if self.inPosition():
         # Take profit once limit hit
#         if self.positionType == self.sell:
#            if self.cn.getCurrentAsk(self.stock) < self.lm.closeBuyLimit:
#               return 2
#         elif self.positionType == self.buy:
#            if self.cn.getCurrentBid(self.stock) > self.lm.closeSellLimit:
#               return 1
               
         return action
         
      # Return 0 if price is within a range 

      if self.isPriceInRange():
         self.priceInRange += 1
         self.useAvgBarLen = 0
         self.lg.debug("NOT TRADING IN PRICE RANGE AND NOT IN A POSITION " + str(self.lm.doRangeTradeBars))         
         return 0
      
      # if first time out of range then reverse buys and sells and use a trailing
      # avg bar length as the stop.
      
      elif self.priceInRange > 1:
         self.lg.debug("REVERSING BUY SELL DUE TO FIRST TIME OUT OF RANGE")

         if action == self.buy:
            action = self.sell
         elif action == self.sell:
            action = self.buy
         
         self.useAvgBarLen += 1
         self.priceInRange = 0
         
         self.lm.setAvgBarLenLimits(barChart, bar)

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoOnlyTrends(self, bc, bar, action=0):
   
      self.lg.debug("In algorithmDoOnlyTrends: " + str(action))

      # We set the trend linits here since the calculation is dynamic and values
      # change as the price moves
      # This algo takes much CPU time and may need rethinking
            
      self.tr.setTrendLimits(bc, bar)
            
      self.tr.isBearTrend()
      self.tr.isBullTrend()

      self.setSessionData(bc, bar)

#      hi, hiBar = self.bc.getSessionHi(bc, bar)
#      lo, loBar = self.bc.getSessionLo(bc, bar)
#
#      sessionTrendValue = self.tr.getSessionTrendValue(hi, hiBar, lo, loBar)
#      self.tr.setSessionTrend(sessionTrendValue)

      if not self.inPosition():
         if self.tr.isBullSessionTrend() and (self.tr.isBullTrend() and not self.tr.isBearTrend()):
            action = 1
         elif self.tr.isBearSessionTrend() and self.tr.isBearTrend():
            action = 2
      else:
         if self.positionType == self.buy:
            #if self.tr.isBearShortTrend() and not self.tr.isBullTrend():
            if self.tr.isBullMegaTrend() and self.tr.isBearShortTrend():
               action = 2
         elif self.positionType == self.sell:
            if self.tr.isBullShortTrend() and not self.tr.isBearTrend():
               action = 1

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmOnClose(self, barChart, action=0):

      self.lg.debug("In algorithmOnClose: " + str(action))
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmOnOpen(self, barChart, bar, action=0):
      
      # If we are not on the beginning of a new bar, there's nothing to do, get out
      if not self.doActionOnNewBar():
         return 0

      self.lg.debug("In algorithmOnOpen: " + str(action))

      # Take position on the open if execute on open is set 
      if not self.inPosition():
         # Open a buy position on the open if closes are sequentially higher
         if self.lm.isHigherCloses(self.lm.openBuyBars) and \
            self.lm.isHigherOpens(self.lm.openBuyBars):
            self.lg.debug("TAKING POSITION HigherOpens and HigherCloses: ")
            return self.buy
   
         # Open a sell position on the open if closes are sequentially lower
         elif self.lm.isLowerCloses(self.lm.openSellBars) and \
            self.lm.isLowerOpens(self.lm.openSellBars):
            self.lg.debug("TAKING POSITION LowerOpens and LowerCloses: ")
            return self.sell
         
      else:
         # Close a buy position on the open if closes are sequentially lower
         if self.positionType == self.buy:
            if self.lm.isLowerCloses(self.lm.closeBuyBars) and \
               self.lm.isLowerOpens(self.lm.closeBuyBars):
               self.lg.debug("CLOSING POSITION LowerOpens LowerCloses: ")
               return self.buy
   
         # Close a sell position on the open if closes are sequentially higher
         elif self.positionType == self.sell:
            if self.lm.isHigherCloses(self.lm.closeSellBars) and \
               self.lm.isHigherOpens(self.lm.closeSellBars):
               self.lg.debug("CLOSING POSITION HigherOpens HigherCloses: ")
               return self.sell
            
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high or lower than the low
   
   def algorithmHiLoSeq(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmHiLoSeq " + str(action))
      
      if self.inPosition():
         if self.positionType == self.buy:
            if self.doOpensCloses:
               if self.lm.lowerCloses and self.lm.lowerOpens:
                  self.lg.debug ("algorithmHiLoSeq: Higher closes and Higher opens detected")
                  return 1
            else: # Default higher hi's and los
               if self.lm.lowerHighs and self.lm.lowerLows:
                  self.lg.debug ("algorithmHiLoSeq: Higher closes and Higher opens detected")
                  return 1
         elif self.positionType == self.sell:
            if self.doOpensCloses:
               if self.lm.higherCloses and self.lm.higherOpens:
                  self.lg.debug ("algorithmHiLoSeq: Lower hi's and Lower lo's detected")
                  return 2
            else:
               if self.lm.higherHighs and self.lm.higherLows:
                  self.lg.debug ("algorithmHiLoSeq: Lower hi's and Lower lo's detected")
                  return 2
      else:
         if self.doOpensCloses:
            if self.lm.higherCloses and self.lm.higherOpens:
               self.lg.debug ("algorithmHiLoSeq: Higher closes Higher opens detected")
               return 1
            if self.lm.lowerCloses and self.lm.lowerOpens:
               self.lg.debug ("algorithmHiLoSeq: Lower closes and Lower opens detected")
               return 2
         else: # Default higher hi's and los
            if self.lm.higherHighs and self.lm.higherLows:
               self.lg.debug ("algorithmHiLoSeq: Higher hi's and Higher lo's detected")
               return 1
            if self.lm.lowerHighs and self.lm.lowerLows:
               self.lg.debug ("algorithmHiLoSeq: Lower hi's and Lower lo's detected")
               return 2

      return action
      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high or lower than the low
   
   def algorithmHiLo(self, barChart, bar, bid, ask, last, vol, action=0):

      adjustDoToExecuteOnOpenClose = 0
      
      if action > 0 and (self.doExecuteOnOpen or self.doExecuteOnClose):
         print ("Using highs and lo's to close/open a position on execute on open/close: " + str(action))
         adjustDoToExecuteOnOpenClose = 1

      self.lg.debug("In algorithmHiLo")

      # Adjust execute on close decision based on hi's lo's
      if adjustDoToExecuteOnOpenClose:
         if self.inPosition():
            if self.positionType == self.buy:
               if self.lm.higherHighs and self.lm.higherLows:
                  self.lg.debug ("Hi Lo algo reversing action. Higher hi's and Higher lo's detected")
                  return 0
               self.lg.debug ("Hi Lo algo not affecting current action.")
               return 1
            else:
               if self.lm.lowerHighs and self.lm.lowerLows:
                  self.lg.debug ("Hi Lo algo reversing action. Lower hi's and Lower lo's detected")
                  return 0
               self.lg.debug ("Hi Lo algo not affecting current action")
               return 2
         
         else: # Not in position
            if action == self.buy:
               if self.lm.lowerHighs and self.lm.lowerLows:
                  self.lg.debug ("Hi Lo algo reversing action. Lower hi's and Lower lo's detected")
                  return 0
               print ("Hi Lo algo not affecting current action.")
               return 1
            elif action == self.sell:
               if self.lm.higherHighs and self.lm.higherLows:
                  self.lg.debug ("Hi Lo algo reversing action. Lower hi's and Lower lo's detected")
                  return 0
               print ("Hi Lo algo not affecting current action.")
               return 2

      # Hi Lo processing on close using hi's and lo's and closes to get out
      elif self.doHiLoOnOpen:
         if self.inPosition():
            if self.positionType == self.buy:
               if self.lm.lowerHighs and self.lm.lowerLows and self.lm.lowerCloses and self.lm.lowerOpens :
                  #if self.cn.getCurrentAsk(self.stock) < self.closeBuyLimit:
                  return 1
            if self.positionType == self.sell:
               if self.lm.higherHighs and self.lm.higherLows:
                  #if self.cn.getCurrentBid(self.stock) > self.closeSellLimit:
                  return 2
         elif not self.inPosition():
            if self.lm.higherHighs and self.lm.higherLows:
               return 1
            if self.lm.lowerHighs and self.lm.lowerLows:
               return 2
         
      # Make decisions when hi's or lo's are breached
      else:
         # in sequential profit taking
         if self.quickProfitCtr:
            self.lm.setAvgBarLenLimits(barChart, bar)
            self.lg.debug ("self.quickProfitCtr set: " + str(self.quickProfitCtr))

         self.lg.debug ("In Hi Lo: open limits buy " + str(self.lm.openBuyLimit) + " sell " + str(self.lm.openSellLimit))
         self.lg.debug ("In Hi Lo: close limits buy " + str(self.lm.closeBuyLimit) + " sell " + str(self.lm.closeSellLimit))
                  
#         self.lg.debug ("self.cn.getCurrentAsk(self.stock) " + str(self.cn.getCurrentAsk(self.stock)))
#         self.lg.debug ("self.cn.getCurrentBid(self.stock) " + str(self.cn.getCurrentBid(self.stock)))
#         self.lg.debug ("self.cn.getCurrentVol(self.stock) " + str(self.cn.getCurrentVol(self.stock)))
         
         self.lg.debug ("ask " + str(ask))
         self.lg.debug ("bid " + str(bid))
         self.lg.debug ("vol " + str(vol))
         
         if self.inPosition():
            if self.positionType == self.buy:
               self.lg.debug ("Hi Lo: in buy position " + str(self.positionType))
               self.lg.debug ("closeBuyLimit " + str(self.lm.closeBuyLimit))
               #if self.cn.getCurrentBid(self.stock) < self.lm.closeBuyLimit:
               if bid < self.lm.closeBuyLimit:
                  self.lg.debug ("Closing algorithmHiLo BUY")
                  return 1
            if self.positionType == self.sell:
               self.lg.debug ("Hi Lo: in sell position " + str(self.positionType))
               self.lg.debug ("closeSellLimit " + str(self.lm.closeSellLimit))
               #if self.cn.getCurrentAsk(self.stock) > self.lm.closeSellLimit:
               if ask > self.lm.closeSellLimit:
                  self.lg.debug ("Closing algorithmHiLo SELL")
                  return 2
         elif not self.inPosition():
            #if self.cn.getCurrentAsk(self.stock) > self.lm.openBuyLimit:
            if ask > self.lm.openBuyLimit:
               self.lg.debug ("Opening algorithmHiLo BUY  1")
               return 1
            #if self.cn.getCurrentBid(self.stock) < self.lm.openSellLimit:
            if bid < self.lm.openSellLimit:
               self.lg.debug ("Opening algorithmHiLo SELL 2 ")
               return 2

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDefault(self, barChart, bar, bid, ask, action=0):
      
      # Ues the right flag here or continue to use this algo as the default
   
      if self.inPosition():
         print ("close buy limit " + str(self.lm.closeBuyLimit))
         print ("close sell limit " +  str(self.lm.closeSellLimit))
         if ask < self.lm.closeBuyLimit:
         #if self.cn.getCurrentAsk(self.stock) < self.lm.closeBuyLimit:
            return 1
         if bid > self.lm.closeSellLimit:
         #if self.cn.getCurrentBid(self.stock) > self.lm.closeSellLimit:
            return 2
      else:
         if ask >= self.lm.openBuyLimit and self.lm.openBuyLimit != 0.0:
         #if self.cn.getCurrentAsk(self.stock) >= self.lm.openBuyLimit and self.lm.openBuyLimit != 0.0:
            print ( "open buy limit set " + str(self.openBuyLimit))
            return 1
         if bid <= self.lm.openSellLimit and self.lm.openSellLimit != 0.0:
         #if self.cn.getCurrentBid(self.stock) <= self.lm.openSellLimit and self.lm.openSellLimit != 0.0:
            print ("open sell limit set " +  str(self.lm.openSellLimit))
            return 2
      
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPatterns(self, bc, bar, action=0):
   
      # First should be the hammer. In sell position if hammer found close out
      # regardless of number of decision bars

      self.lg.debug("In algorithmHiLo")

      if not self.inPosition():
         return action
      
      if bar < 3:
         return action
         
      if self.positionType == self.buy:
         if self.pa.isHammer(bc, bar):
            self.lg.debug("In buy position, Hammer detected. Doing nothing")
            #self.closePosition(self, bar, bc, 1)
         elif self.pa.isInvHammer(bc, bar) and self.algorithmVolumeLastBar(bc, bar-1, 2):
            self.lg.debug("In buy position. Inverted Hammer detected! Closing buy:")
            action = 2
            self.setWaitForNextBar()
            #self.closePosition(bar, bc, 1)
      elif self.positionType == self.sell:
         if self.pa.isInvHammer(bc, bar):
            self.lg.debug("In sell position. Inverted Hammer detected! doing nothing:")
            #self.closePosition(bar, bc, 1)
         if self.pa.isHammer(bc, bar) and self.algorithmVolumeLastBar(bc, bar-1, 1):
            self.lg.debug("In sell position. Hammer detected! Closing sell:")
            self.setWaitForNextBar()
            action = 1
            #self.closePosition(bar, bc, 1)
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPosTracking(self, last, action=0):
   
      # Monitor gainTrailStop 
      # Move decision bars depending how long in pos
      # Take profit depending on how long in pos
      # Track how many bars price in a range. 
      # see where price is relative to session his/los
      # 
      
      self.lg.debug("In algorithmPosTracking")

      stopPct = 0
      
      self.lg.debug("self.stopTarget " + str(self.stopTarget))
      
      if self.stopTarget > 0:
         if last > self.profitGained:
            # Raise stop
            self.stopTarget += round((last - self.profitGained), 2)
            self.profitGained = last
            self.lg.debug("self.profitGained " + str(self.profitGained))
            self.lg.debug("self.stopTarget " + str(self.stopTarget))
            self.lg.debug("last " + str(last))
            return action
            
         # Hit our stop
         elif self.stopTarget > 0 and last < self.stopTarget:
            self.lg.debug("stopped out " + str(last))
            # End trading
            return 4

      if self.getTotalGain() >= self.getTargetProfit():
         self.profitGained = last
         stopPct = self.profitPctTrigger * 0.1
         self.stopTarget = round(last - (stopPct * last), 2)
         self.lg.debug("last " + str(last))
         self.lg.debug("stopPct " + str(stopPct))
         self.lg.debug("self.stopTarget " + str(self.stopTarget))
         
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDynamic(self, action=0):
   
      # Turn on trends after the beginning of the day to keep from trading too much
      # during the slow lunch hours for TQQQ
      
      # if in a oscilating trade get out
      # set quickProfit using avg bar length when in trade longer then the number of bars
      
      # remove range restrictions when bar length is > average. This will catch big moves.

      # If in a range for more than n number of bars, get out with small profit if possible.
      #  More risk when oscilating
       
      ## If in a range and in a trend either sell or buy opposite of normal logic with the trend
      ## if trend is sell then sell when 1st hi out of the range. : Winning ticket!!!!
      
      # After 3 quickProfit wins use avg bar length as stop when buying/selling again
      
      # When in a long trend turn quick profiit on or 
      #   reduce decision bars by 1 for each new bar. This will capture more gains in
      #.  when using decision bars > 3 BABA 8/21/20 time 12:54 5 MB 4 DB
      
      # after gains using trends turn on in range to avoid little losing trades
      #   BABA 8/21/20 time 12:54 5 MB 4 DB
      
      # After min profit hit use it as a stop and continue to bank profit
      
      self.lg.debug("In algorithmDynamic: " + str(action))
      
      # Once price goes out of range reverse buys and sells
      if self.isPriceInRange():
         self.dynPriceInRange += 1

      if not self.isPriceInRange() and self.dynPriceInRange:
         self.doReverseBuySell += 1
         self.setRevBuySell()
         self.dynPriceInRange = 0

      if self.getBarsInPosition() > self.lm.openBuyBars:
         self.lm.openBuyBars -= 1
         
      if self.getBarsInPosition() > self.lm.closeBuyBars and self.lm.closeBuyBars > 0:
         self.lm.closeBuyBars -= 1
         
      # If in a position and within a range sell out for profit as exiting range
      #if self.inPosition() and self.getBarsInPosition() > self.lm.doRangeTradeBars:
      #   self.closeSellBar = 0
      #   self.closeBuyBar = 0.0
         
      # if in a gain position set stop just above average bar length?
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def ready(self, currentNumBars):
          
      self.lg.debug("tradingDelayBars currentNumBars " + str(self.lm.getTradingDelayBars()) + " " + str(currentNumBars))
      
      if self.lm.getTradingDelayBars() <= currentNumBars:
         return 1
      else:
         return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPriceInRange(self):
   
      if not self.lm.doRangeTradeBars:
         return 0

      if self.cn.getCurrentBid(self.stock) >= self.lm.rangeLo and self.cn.getCurrentAsk(self.stock) <= self.lm.rangeHi:
         if not self.inPosition():
            self.lg.debug ("IN RANGE BETWEEN " + str(self.lm.rangeLo) +  " >" + str(self.cn.getLastTrade(self.stock)) + "< " +  str(self.lm.rangeHi))

         return 1

      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def waitingForBestPrice(self):
   
      if self.waitForBestPrice:
         return
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def openPosition(self, action, bar, bc, bid, ask):
      
      self.lg.debug("START OF OPEN POSITION: " + str(action))

      # Block taking a position if we are in a range and range trading is set or delay bars are set
      if not self.ready(bar):
         self.lg.debug("BLOCKING TRADING DUE TO DELAY BARS " + str(self.lm.getTradingDelayBars()))         
         return

      if self.isPriceInRange():
         self.priceInRange += 1
         self.lg.debug("NOT TRADING IN PRICE RANGE AND NOT IN A POSITION " + str(self.lm.doRangeTradeBars))         
         return

      if self.doSessions:
         self.setSessionData(bc, bar)
         if action == self.buy and self.tr.isBearSessionTrend():
            self.lg.debug("isBearSessionTrend... ")
            return
         elif action == self.sell and self.tr.isBullSessionTrend():
            self.lg.debug("isBullSessionTrend... ")
            return

      # Use the trend to only buy or sell if a trend exists.
      if self.doTrends:
         self.tr.setTrendLimits(bc, bar)

         if action == self.buy and self.tr.isBearTrend():
            self.lg.debug("isBearTrend... ")
            return
         elif action == self.sell and self.tr.isBullTrend():
            self.lg.debug("isBullTrend... ")
            return
            
         # Only open new position if we are in a trend after reaching profit
#         if self.getTotalGain() >= self.getTargetProfit():
#            if action == self.buy:
#               if not self.tr.isBullTrend():
#                  self.lg.debug("NOT TRADING MAX PROFIT REACHED AND NOT IN A TREND")         
#                  return
#                  
#            if action == self.sell:
#               if not self.tr.isBearTrend():
#                  self.lg.debug("NOT TRADING MAX PROFIT REACHED AND NOT IN A TREND")         
#                  return

#      if self.doTrends:
#         self.tr.setTrendLimits(bc, bar)
#         if self.tr.isShortMidBullLongMegaBear() and action == self.buy:
#            self.lg.debug("isShortMidBullLongMegaBear... ")
#            return
#         if self.tr.isShortMidBearLongMegaBull() and action == self.sell:
#            self.lg.debug("isShortMidBearLongMegaBull... ")
#            return
                        
      if self.doOnlyBuys and action == self.sell:
         return
      
      if self.doOnlySells and action == self.buy:
         return      

      # Open a BUY position
      if action == self.buy:
         #price = self.cn.getCurrentAsk(self.stock)
         price = ask
         
         # Execute order here ========================
         
         if self.offLine:
            self.lg.logIt(self.buy, str(price), str(self.bc.getBarsInPosition()), bc[bar][self.dt], "")
         else:
            self.lg.logIt(self.buy, str(price), str(self.bc.getBarsInPosition()), self.cn.getTimeStamp(), "")
         self.positionType = self.buy
         
      # Open a SELL position
      else:
         price = self.cn.getCurrentBid(self.stock)
         price = bid
         
         # Execute order here ========================
         
         if self.offLine:
            self.lg.logIt(self.sell, str(price), str(self.bc.getBarsInPosition()), bc[bar][self.dt], "")
         else:
            self.lg.logIt(self.sell, str(price), str(self.bc.getBarsInPosition()), self.cn.getTimeStamp(), "")
         self.positionType = self.sell

      # Set all values appropriate with the opening of a position

      print ("\n")
      self.lg.info("POSITION OPEN " + str(self.stock))
      self.lg.info("Bar:  " + str(bar + 1))
      self.lg.info("buy/sell: " + str(action))
      self.lg.info("Open buy limit: " + str(self.lm.openBuyLimit))
      self.lg.info("Open sell limit: " + str(self.lm.openSellLimit))
      self.lg.info("Open position Price: " + str(price))
            
      if self.offLine:
         self.lg.info("Position Time: " + bc[bar][self.dt] + "\n")
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()) + "\n")
         
      # Using avg bar length or percentage instead (setProfitTarget), Remove eventually
      #self.setInitialClosePrices()
            
      self.setProfitTarget(0)
         
      self.setExecuteOnOpenPosition(0)
      
      self.position = "open"
      self.openPositionPrice = price
      
      self.bc.setBarsInPosition()
      #self.barCountInPosition = 0

      self.lm.lowestcloseSellLimit = self.lm.closeSellLimit
      self.lm.highestcloseBuyLimit = self.lm.closeBuyLimit

      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def closePosition(self, bar, bc, bid, ask, force):

      self.lg.debug("START OF CLOSE POSITION: " + str(self.positionType))

      gain = price = 0

      # Use trends to stop start trading and to verify signal instead of holding 
      # on to a trade after we get signals
      
      if self.doTrends and not force:
         self.tr.setTrendLimits(bc, bar)    
         if self.positionType == self.buy and self.tr.isBullTrend():
         #if self.positionType == self.buy and self.tr.isBullTrend() and not self.getGain():
            self.lg.debug("Got a BUY close signal... BLOCKING isBullTrend " + str(self.positionType))
            self.setWaitForNextBar()
            return        
         if self.positionType == self.sell and self.tr.isBearTrend():
         #if self.positionType == self.sell and self.tr.isBearTrend() and not self.getGain():
            self.lg.debug("Got a SELL close signal... BLOCKING isBearTrend" + str(self.positionType))
            self.setWaitForNextBar()
            return        
            
#         if self.positionType == self.buy and (not self.tr.isBearTrend() and not self.tr.isBullTrend()):
#            self.lg.debug("Got a BUY close signal... BLOCKING no trend" + str(self.positionType))
#            self.setWaitForNextBar()
#            return        
#         if self.positionType == self.sell and (not self.tr.isBearTrend() and not self.tr.isBullTrend()):
#            self.lg.debug("Got a SELL close signal... BLOCKING no trend" + str(self.positionType))
#            self.setWaitForNextBar()
#            return        

      print (str(self.cn.getCurrentBid(self.stock)))
      
      if self.positionType == self.buy:
         #price = self.cn.getCurrentBid(self.stock)
         price = bid
      else:
         #price = self.cn.getCurrentAsk(self.stock)
         price = ask
         
      if self.positionType == self.buy:
         gain = round(price - self.openPositionPrice, 2)
      elif self.positionType == self.sell:
         gain = round(self.openPositionPrice - price, 2)
         
      self.totalGain += gain
            
      # Update the log
      if self.offLine:
         self.lg.logIt(self.close, str(price), str(self.bc.getBarsInPosition()), bc[bar][self.dt], self.numTrades)
      else:
         self.lg.logIt(self.close, str(price), str(self.bc.getBarsInPosition()), self.cn.getTimeStamp(), self.numTrades)

      self.closePositionPrice = price

      self.lg.debug ("\n")
      self.lg.info ("POSITION CLOSED " + self.stock)
      
      if self.offLine:
         self.lg.info("Position Time: " + bc[bar][self.dt])
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()))

      self.lg.info ("open price: " + str(self.openPositionPrice))
      self.lg.info ("close price: " + str(self.closePositionPrice))
      self.lg.info ("current Price: " + str(price))
      self.lg.info ("gain: " + str(gain))
      self.lg.info ("stopPrice: " + str(self.getClosePrice()))
      #self.lg.info ("bar Count In Position: " + str(self.barCountInPosition))
      self.lg.info ("bar Count In Position: " + str(self.bc.getBarsInPosition()))
      self.lg.info ("Loss/Gain: " + str(gain))
      self.lg.info ("Total Gain: " + str(self.totalGain) + "\n")
      self.lg.info ("Number of trades: " + str(self.numTrades) + "\n")
         
      self.openPositionPrice = self.closePositionPrice = 0.0
      self.topIntraBar = 0.0

      self.positionType = 0
      self.barCounter = 0
      self.highestcloseBuyLimit = 0.0
      self.lowestcloseSellLimit = 0.0
      
      #self.barCountInPosition = 0
      self.bc.resetBarsInPosition()
      
      self.position = "close"
      self.numTrades += 1
      self.lastCloseBuyLimit = 0.0
      self.lastCloseSellLimit = 999.99

      if gain < 0:
         #self.setAllLimits(bc, bar)
         self.quickProfitCtr = 0
         self.avgBarLenCtr = 0
         # self.setWaitForNextBar()

      self.lm.resetLimits()
      self.setExecuteOnClosePosition(0)
      
      #if self.doReverseBuySell:
      #   self.unsetRevBuySell()
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doReversalPattern(self):
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
   def setSessionData(self, bc, bar):
   
      hi, hiBar = self.bc.getSessionHi(bc, bar)
      lo, loBar = self.bc.getSessionLo(bc, bar)

      sessionTrendValue = self.tr.getSessionTrendValue(hi, hiBar, lo, loBar)
      self.tr.setSessionTrend(sessionTrendValue)
      
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
   def getTargetProfit(self):

      return self.targetProfit
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTotalProfit(self, price, percentage):

      self.targetProfit = round(price * percentage, 2)
   
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
   def setCurrentVol(self, vol):
      
      self.vol = vol
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentVol(self):
      
      return self.vol
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCurrentBid(self, bid):
      
      self.bid = bid
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentBid(self):
      
      return self.bid
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCurrentAsk(self, ask):
      
      self.ask = ask
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentAsk(self):
      
      return self.ask
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCurrentLast(self, last):
      
      self.last = last
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentLast(self):
      
      return self.last
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentAsk(self):
      
      return self.last
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyStop(self):
   
      self.closeBuyLimit = self.cn.getCurrentAsk(self.stock)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellStop(self):
   
      self.closeSellLimit = self.cn.getCurrentBid(self.stock)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setDynamic(self, bar):
   
      #if not self.doDynamic:
      #   self.doDynamic = 1
      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setProfitTarget(self, useBars):

      if not self.doQuickProfit:
         return
         
      self.lg.debug ("profit pct trigger: " + str(self.profitPctTrigger))

      profitAmt = 0.0
      if self.positionType == self.buy: 
         profitAmt = self.cn.getCurrentBid(self.stock) * self.profitPctTrigger
      else:
         profitAmt = self.cn.getCurrentAsk(self.stock) * self.profitPctTrigger
      
      if useBars > 0:
         profitAmt = self.bc.getAvgBarLen()
         self.lg.debug ("profit amount using avg bar length: " + str(profitAmt))
         
      if self.positionType == self.buy:
         self.profitTarget = self.cn.getCurrentAsk(self.stock) + profitAmt
      elif self.positionType == self.sell:
         self.profitTarget = self.cn.getCurrentBid(self.stock) - profitAmt

      self.lg.debug ("profit value: " + str(self.profitTarget))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCurrentBar(self, bar):

      self.currentBar = bar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setNextBar(self, nextBar):
      
      self.nextBar = nextBar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setExecuteOnOpenPosition(self, executeOnOpenPosition):

      self.executeOnOpenPosition = executeOnOpenPosition

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setExecuteOnClosePosition(self, executeOnClosePosition):

      self.executeOnClosePosition = executeOnClosePosition

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAlgorithmMsg(self):
         
      return self.algoMsg

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAlgorithmMsg(self):
         
      self.algoMsg += "Algorithms set:\n"
      
      if self.doDefault:
         self.algoMsg += "         Default\n"
      if self.doHiLo:
         self.algoMsg += "         Hi Lo's\n"
      if self.doHiLoSeq:
         self.algoMsg += "         Hi Lo's Sequential\n"
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
      if self.doOnlyTrends:
         self.algoMsg += "         Only trends\n"
      if self.doPatterns:
         self.algoMsg += "         Patterns\n"
      if self.lm.doRangeTradeBars:
         self.algoMsg += "         In Range\n"
      if self.doAverageVolume:
         self.algoMsg += "         AverageVolume\n"
      if self.doVolumeLastBar:
         self.algoMsg += "         Volume Last Bar\n"
      if self.doPriceMovement:
         self.algoMsg += "         Price Movement\n"
      if self.doPriceMovement:
         self.doPriceMovement += " Price Tracking\n"
         

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

      if self.cn.getCurrentBid(self.stock) > self.openPositionPrice:
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
         return self.lm.closeBuyLimit
      elif self.positionType == self.sell:
         return self.lm.closeSellLimit
         
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

      return self.lm.openSellLimit     
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOpenBuyPrice(self):

      return self.lm.openBuyLimit
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
      self.lg.debug("self.waitForNextBar " + str(self.waitForNextBar))
      
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
   def getProfitTarget(self):

      return self.profitTarget

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

         
