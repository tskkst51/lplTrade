'''
Algorithms module
'''
import io
import sys
import os
from bitarray import bitarray 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm():

   def __init__(self, data, lg, cn, bc, tr, lm, pa, pr, dy, offLine=0, stock=""):
   
      self.data = data
      self.lg = lg
      self.cn = cn
      self.bc = bc
      self.tr = tr
      self.lm = lm
      self.pa = pa
      self.pr = pr
      self.dy = dy
      self.offLine = offLine
      self.stock = stock

      # Required standard settings
      self.algorithms = str(data['profileTradeData']['algorithms'])
            
      # Algorithms
      self.timeBar = int(data['profileTradeData']['timeBar'])
      self.doDefault = int(data['profileTradeData']['doDefault'])
      self.doHiLo = int(data['profileTradeData']['doHiLo'])
      self.doHiLoSeq = int(data['profileTradeData']['doHiLoSeq'])
      self.doHiSeq = int(data['profileTradeData']['doHiSeq'])
      self.doLoSeq = int(data['profileTradeData']['doLoSeq'])
      self.doOpenCloseSeq = int(data['profileTradeData']['doOpenCloseSeq'])
      self.doOpensSeq = int(data['profileTradeData']['doOpensSeq'])
      self.doClosesSeq = int(data['profileTradeData']['doClosesSeq'])
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
      self.doTrailingStop = int(data['profileTradeData']['doTrailingStop'])
      self.doVolatility = int(data['profileTradeData']['doVolatility'])
      self.doInPosTracking = int(data['profileTradeData']['doInPosTracking'])
      self.averageVolumeOpen = int(data['profileTradeData']['averageVolumeOpen'])
      self.averageVolumeClose = int(data['profileTradeData']['averageVolumeClose'])
      self.volumeLastBarOpen = int(data['profileTradeData']['volumeLastBarOpen'])
      self.volumeLastBarClose = int(data['profileTradeData']['volumeLastBarClose'])
      
      self.doPriceMovement = int(data['profileTradeData']['doPriceMovement'])
      self.doAllPatterns = int(data['profileTradeData']['doAllPatterns'])
      self.doHammers = int(data['profileTradeData']['doHammers'])
      self.doReversals = int(data['profileTradeData']['doReversals'])
      self.profitGainedPct = float(data['profileTradeData']['profitGainedPct'])
      self.inPosProfitPct = float(data['profileTradeData']['inPosProfitPct'])
      self.inPosLossPct = float(data['profileTradeData']['inPosLossPct'])
      
      self.quitMaxProfit = float(data['profileTradeData']['quitMaxProfit'])
      self.quitMaxLoss = float(data['profileTradeData']['quitMaxLoss'])
      
      self.aggressiveOpen = int(data['profileTradeData']['aggressiveOpen'])
      self.aggressiveClose = int(data['profileTradeData']['aggressiveClose'])
      self.agrBuyHiOpen = int(data['profileTradeData']['agrBuyHiOpen'])
      self.agrSellLoOpen = int(data['profileTradeData']['agrSellLoOpen'])
      self.agrBuyHiClose = int(data['profileTradeData']['agrBuyHiClose'])
      self.agrSellLoClose = int(data['profileTradeData']['agrSellLoClose'])

      self.currency = str(data['profileTradeData']['currency'])
      self.alt = str(data['profileTradeData']['alt'])
      self.marketBeginTime = int(data['profileTradeData']['marketBeginTime'])
      self.marketEndTime = int(data['profileTradeData']['marketEndTime'])
      self.preMarket = int(data['profileTradeData']['preMarket'])
      self.afterMarket = int(data['profileTradeData']['afterMarket'])
      self.priceChangeMultiplier = int(data['profileTradeData']['priceChangeMultiplier'])
      self.afterMarketAnalysis = int(data['profileTradeData']['afterMarketAnalysis'])
      self.afterMarketEndTime = int(data['profileTradeData']['afterMarketEndTime'])

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
      self.quickProfitPctTriggerAmt = float(data['profileTradeData']['quickProfitPctTriggerAmt'])
      
      # reverseLogic appears to be best for short term charts and
      # low liquidity
      
      self.buyNearLow = int(data['profileTradeData']['buyNearLow'])
      self.sellNearHi = int(data['profileTradeData']['sellNearHi'])
      
      self.quickProfitPctTrigger = float(data['profileTradeData']['quickProfitPctTrigger'])
      self.quickProfitPctTriggerBar = float(data['profileTradeData']['quickProfitPctTriggerBar'])
      self.reversalPctTrigger = float(data['profileTradeData']['reversalPctTrigger'])
      self.volumeRangeBars = int(data['profileTradeData']['volumeRangeBars'])
      self.inPosProfitPct = float(data['profileTradeData']['inPosProfitPct'])
      
      self.executeOnOpenPosition = 0
      self.executeOnClosePosition = 0

      self.hiLowBarMaxCounter = int(data['profileTradeData']['hiLowBarMaxCounter'])
      self.useSignals = int(data['profileTradeData']['useSignals'])
      self.priceLimits = str(data['profileTradeData']['priceLimits'])
      self.priceLimitDivider = float(data['profileTradeData']['priceLimitDivider'])

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
      self.priceInRange = 0
      
      self.hiValues = [0.0] 
      self.lowValues = [0.0]
      self.openValues = [0.0] 
      self.closeValues = [0.0]

      self.topIntraBar = 0.0
      self.bcrCounter = 0
      self.revDirty = 0
      self.profitTarget = 0.0
      self.longMegaBars = 0.0
      
      self.shortTrend = self.midTrend = 0.0
      self.longTrend = self.megaTrend = 0.0
      self.shT = self.miT = self.loT = self.meT = self.suT = 0.0
      
      self.algoMsg = ""
      
      self.setAlgorithmMsg()
      
      self.doOnCloseBar = 0
      self.doOnOpenBar = 0
      self.dynPriceInRange = 0

      self.useAvgBarLen = 0
      self.avgBarLenCtr = 0

      self.totalGain = 0.0
      self.totalLoss = 0.0
      self.totalLiveGain = 0.0
      self.totalLiveLoss = 0.0
      self.targetProfit = 0.0
      self.targetLoss = 0.0
      self.quickProfitCtr = 0
      self.numTrades = 0
      self.lastCloseBuyLimit = 0.0
      self.lastCloseSellLimit = 9999.99
      
      self.bid = 0.0
      self.ask = 0.0
      self.last = 0.0
      self.reversAction = 0
      self.inHammerPosition = self.inInvHammerPosition = 0
      self.hammerBar = self.invHammerBar = 0
      self.priceMovement = 0
      self.stopBuyTarget = 0.0
      self.stopSellTarget = 0.0
      self.stopPct = 0
      self.runningVolume = 0
      self.currentVol = 0
      self.onCloseBarVolume = 0
      
      self.previousBarSegment = self.barSegment = self.nextBarSegment = 0
      self.stoppedOut = 4
      self.loReversal = self.hiReversal = 0
      self.totalGainLastPrice = 0.0
      self.totalLossLastPrice = 0.0
      self.exitWProfitVal = 0.0 
      self.inPosGain = 0

      if not self.priceChangeMultiplier:
         self.priceChangeMultiplier = 1
         
      self.numBarsInBullSessionTrend = self.numBarsInBearSessionTrend = 0
      self.lastBarsInBullSessionTrend = self.lastBarsInBearSessionTrend = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def resetAlgoLimits(self):
      
      pass
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAlgoLimits(self):
      
      pass
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAllLimits(self, bc, bar, last):
      
      self.lg.debug("actual bar number passed in to setAllLimits..." + str(bar))
      self.lg.debug("lm.getMaxNumTradeBars() " + str(self.lm.getMaxNumTradeBars()))
      self.lg.debug("setAllLimits self.runningVolume " + str(self.runningVolume))
      self.lg.debug("pr.getCurrentPriceIdx() " + str(self.pr.getCurrentPriceIdx()))
      
      if bar == 0:
         return
         
      self.lm.setTradingDelayBars()
      
      if self.doPriceMovement:
         self.pr.setPriceChangeArr(bar)
      
      if self.pr.getCurrentPriceIdx() % self.timeBar == 0:
         print ("self.pr.getCurrentPriceIdx() % self.timeBar " + str(self.pr.getCurrentPriceIdx() % self.timeBar))
         self.runningVolume = self.currentVol = self.onCloseBarVolume = 0
         
      print ("self.lm.getTradingDelayBars() " + str(self.lm.getTradingDelayBars()))
      
      if bar < self.lm.getTradingDelayBars():
         return
      
      # The above doesn't work on it's own in master mode FIX.
      if bar < self.lm.getMaxNumTradeBars():
         return

      self.setNextBar(bar + 1)

      print ("HHEERREE")

      bar -= 1
                     
      self.bc.setAvgBarLen(bc, bar)

      if self.averageVolumeOpen or self.averageVolumeClose:
         self.bc.setAvgVol(bc, bar)
         
      print ("bar is subtracted by 1" + str(bar))
      print ("getMaxNumTradeBars() " + str(self.lm.getMaxNumTradeBars()))
      print ("getTradingDelayBars() " + str(self.lm.getTradingDelayBars()))
      
#      if self.lm.setOpenCloseHiLoValues(bc, bar, self.lm.getTradingDelayBars()):
#         self.lm.setOpenCloseHiLoConditions(self.lm.getTradingDelayBars())

      self.lm.setRangeLimits(bc, bar)
      #self.lm.setRangeLimits(bc, self.lm.getTradingDelayBars())

      self.lm.setOpenCloseHiLoValues(bc, bar, self.lm.getMaxNumTradeBars())
      #self.lm.setOpenCloseHiLoConditions(self.lm.getMaxNumTradeBars())
      
      self.lm.setHiLoConditions()
      
      #self.lm.setOpenCloseHiLoValues(bc, bar, self.lm.getTradingDelayBars())
      #self.lm.setOpenCloseHiLoConditions(self.lm.getTradingDelayBars())

      self.lm.setOpenBuySellLimits()

      if self.useAvgBarLimits:
         if not self.inPosition():
            self.lm.unsetCloseAvgBarLenLimits(bc, bar)
         self.lm.setCloseAvgBarLenLimits(bc, bar)
      else:
         self.lm.setCloseBuySellLimits()
      
      #if not self.waitForNextBar:
      self.unsetWaitForNextBar()
      
      self.revDirty = 0
      self.priceMovement = 0
      
      self.nextBarSegment = 1
      self.reversAction = 0
      
      #self.setDynamic(bar)
            
      # Change algo's based on conditions, time slope
      if self.doDynamic:
         algo = self.dy.setOpenCloseBars(last, self.timeBar)
         
         
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

      self.algorithmCalculateRunningVolume(vol)

      if bar < self.lm.getTradingDelayBars():
         return
         
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
            if self.doQuickReversal and not self.isPriceInRange(bid, ask):
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.sell, bar, barChart, bid, ask)
            
         elif action == self.sell:
            self.closePosition(bar, barChart, bid, ask, 0)
            if self.doQuickReversal and not self.isPriceInRange(bid, ask):
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.buy, bar, barChart, bid, ask)

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takeAction(self, barChart, bar, bid, ask, last, vol):
   
      action = 0
      exitAlgo = 3
      
      if self.doInPosTracking:
         if self.algorithmPriceTracking(bid, ask, last, action):
            # We close position do to positive position turning negative
            self.closePosition(bar, barChart, bid, ask, 1)
            #return 4
            return 0
     
      if self.doDynamic:
         self.algorithmDynamic(bid, ask, last, action)
     
      if self.doVolatility:
         self.algorithmVolatility(action)
     
      if self.doQuickProfit:
         if self.algorithmQuickProfit(barChart, bar, bid, ask, action) == exitAlgo:
            # We took profit exit algo's
            return 0
      
      if self.doExecuteOnOpen:
         action = self.algorithmOnOpen(bar, action)

      if self.doExecuteOnClose:
         action = self.algorithmOnClose(bar, action)

      if self.doHiLoSeq:
         action = self.algorithmHiLoSeq(barChart, bar, bid, ask, last, vol, action)
      
      # In at hi seq out on close ?
      #if self.doHiSeq and self.inPosition():
      if self.doHiSeq:
         action = self.algorithmHiSeq(barChart, bar, bid, ask, last, vol, action)
      
      if self.doLoSeq:
         action = self.algorithmLoSeq(barChart, bar, bid, ask, last, vol, action)
      
      if self.doOpenCloseSeq:
         action = self.algorithmOpensClosesSeq(barChart, bar, bid, ask, last, vol, action)
         
      if self.doOpensSeq:
         action = self.algorithmOpensSeq(barChart, bar, bid, ask, last, vol, action)
         
      if self.doClosesSeq:
         action = self.algorithmClosesSeq(barChart, bar, bid, ask, last, vol, action)
         
      if self.doOpensCloses:
         action = self.algorithmOpensCloses(barChart, bar, bid, ask, last, vol, action)
         
      if self.doSessions:
         action = self.algorithmSessions(barChart, bar, bid, ask, last, vol, action)
         
      if self.doHiLo:
         action = self.algorithmHiLo(barChart, bar, bid, ask, last, vol, action)
         
      if self.doReversalPattern:
         action = self.algorithmReversalPattern(barChart, bar, ask, action)
      
      if self.doOnlyTrends:
         action = self.algorithmDoOnlyTrends(barChart, bar, bid, ask, action)
         
      if self.lm.doRangeTradeBars:
         action = self.algorithmDoInRange(barChart, bar, bid, ask, action)
         
      if self.doDefault:
         action = self.algorithmDefault(barChart, bar, bid, ask, action)

      if self.doReverseBuySell:
         action = self.algorithmReverseBuySell(action)
         
      if self.doPriceMovement:
         # Don't get caught opening a position on a skewed price
         action = self.algorithmPriceMovement(bar, bid, ask, last, action)
         
         #if self.algorithmPriceMovement(bar, bid, ask, last, action) == exitAlgo:
            
      if self.doAllPatterns or self.doHammers or self.doReversals:
         action = self.algorithmPatterns(barChart, bar, bid, ask, action)

      if self.averageVolumeOpen or self.averageVolumeClose:
         action = self.algorithmAverageVolume(action)

      if self.volumeLastBarOpen or self.volumeLastBarClose:
         action = self.algorithmVolumeLastBar(barChart, bar, action)

      if self.doTrailingStop:
         action = self.algorithmTrailingStop(last, action)
         
         if action == self.stoppedOut:
            self.closePosition(bar, barChart, bid, ask, 1)
            return self.stoppedOut
     
      if action > 0:
         print ("Action being taken!! " + str(action))
     
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPriceMovement(self, bar, bid, ask, last, action=0):
      
      # Compare previous prices (last) and don't take a position if the price
      # moves priceChangeMultiplier x the average movement
      
      self.lg.debug ("In algorithmPriceMovement: " + str(action))
      
      # If no signal or priceMovement not set then return
      if not action and self.priceMovement == 0:
            return 0

      self.lg.debug ("self.priceMovement: " + str(self.priceMovement))

      if self.inPosition():
         return action

      lastChange = prevLast = 0.0

      curIdx = self.pr.getCurrentPriceIdx()
      prevLast = self.pr.getLastPriceIdx(curIdx - 1)
      
      lastChange = round(last - prevLast, 2)

      if lastChange < 0:
         lastChange = lastChange*-1

      avgChange = self.pr.getAverageLastChangeArr(bar) * self.priceChangeMultiplier
      
      self.lg.debug ("last: " + str(last))
      self.lg.debug ("prevLast: " + str(prevLast))
      self.lg.debug ("lastChange: " + str(lastChange))
      self.lg.debug ("avgChange: " + str(avgChange))
      self.lg.debug ("curIdx: " + str(curIdx))

      if lastChange > avgChange:
         self.lg.debug ("lastChange > avgChange set price target")
         
         # if priceMovement already set don't set it again
         if self.priceMovement > 0:
            return 0
         
         # Wait for price to come back to where it was
         if action == self.buy:
            self.priceMovement = round(last - lastChange, 2)
         elif action == self.sell:
            self.priceMovement = round(last + lastChange, 2)
            
         self.lg.debug ("self.priceMovement " + str(self.priceMovement))
         
         return 0
      
      elif lastChange <= avgChange:
         if self.priceMovement > 0:
            if action == self.buy:
               if last <= self.priceMovement:
                  self.lg.debug ("PRICE MOVED BACK TO WHERE IT WAS " + str(self.priceMovement))
                  return action
            if action == self.sell:
               if last >= self.priceMovement:
                  self.lg.debug ("PRICE MOVED BACK TO WHERE IT WAS " + str(self.priceMovement))
                  return action

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmCalculateRunningVolume(self, vol):
         
      self.lg.debug ("In algorithmCalculateRunningVloume: ")
      
      barSegment = self.pr.getCurrentBarNum() % self.timeBar
      
      self.lg.debug ("barSegment: " + str(barSegment))
      self.lg.debug ("self.nextBarSegment: " + str(self.nextBarSegment))
      
      if self.timeBar > 1:
         if barSegment == 0:               
            self.onCloseBarVolume = self.currentVol
            self.runningVolume = self.currentVol = vol
         else:
            if barSegment == self.nextBarSegment:
               self.runningVolume = self.currentVol
               self.currentVol = 0
               self.nextBarSegment += 1
            else:   
               self.currentVol = vol + self.runningVolume
      else:
         self.currentVol = vol
               
      self.lg.debug ("self.runningVolume: " + str(self.runningVolume))
      self.lg.debug ("self.currentVol: " + str(self.currentVol))
      self.lg.debug ("vol: " + str(vol))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmVolumeLastBar(self, barChart, bar, action=0):
         
      self.lg.debug ("In algorithmAverageLastBar: " + str(action))

      # Use last bar volume to verify signal

      # If no signal then return
      if not action:
         return action

      if self.volumeLastBarOpen:
         if self.inPosition() and not self.volumeLastBarClose:
            return action
         
      if self.volumeLastBarClose:
         if not self.inPosition() and not self.volumeLastBarOpen:
            return action
      
      # Using average volume last bar to get out of a position
      #if not self.inPosition():
      #   return action

      # using average volume last bar to get into a position
      #if self.inPosition():
      #   return action

      previousBarVol = int(barChart[bar - 1][self.vl])
      
      self.lg.debug ("bar: " + str(bar))
      self.lg.debug ("barChart[bar - 1]: " + str(barChart[bar - 1]))
      self.lg.debug ("barChart[bar - 2]: " + str(barChart[bar - 2]))
      self.lg.debug ("self.currentVol: " + str(self.currentVol))
      self.lg.debug ("self.runningVolume: " + str(self.runningVolume))
      self.lg.debug ("previousBarVol: " + str(previousBarVol))
         
      # If volume isn't > previous bar volume, cancel signal
      
      if self.runningVolume > previousBarVol:
         self.lg.debug ("runningVolume is > last bar avg vol: " + str(self.runningVolume) + " " + str(previousBarVol))
         return action
      elif self.currentVol > previousBarVol:
         self.lg.debug ("currentVol is > last bar vol: " + str(self.currentVol) + " " + str(previousBarVol))
         return action
      elif self.onCloseBarVolume > previousBarVol:
         self.lg.debug ("onCloseBarVolume is > last bar avg vol: " + str(self.currentVol) + " " + str(previousBarVol))
         return action
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmAverageVolume(self, action=0):
         
      self.lg.debug ("In algorithmAverageVolume: " + str(action))

      # Use average volume to verify signal

      # Implement volume plus price direction. high volume coming down even though trend is up
      
      # If no signal then return
      if not action:
         return action

      if self.averageVolumeOpen:
         if self.inPosition() and not self.averageVolumeClose:
            return action
         
      if self.averageVolumeClose:
         if not self.inPosition() and not self.averageVolumeOpen:
            return action
         
      # using average volume to get out of a position
      #if not self.inPosition():
      #   return action

      # using average volume to get into a position
      #if self.inPosition():
      #   return action

      avgVol = self.bc.getAvgVol()

      self.lg.debug ("avgVol: " + str(avgVol))
      self.lg.debug ("runningVolume: " + str(self.runningVolume))
      self.lg.debug ("currentVol: " + str(self.currentVol))

      if avgVol < 1:
         return action
         
      # If volume isn't > average volume, cancel signal
      if self.runningVolume > avgVol :
         self.lg.debug ("runningVolume is > avgVol: " + str(self.runningVolume) + " " + str(avgVol))
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
               self.closePosition(bar, barChart, bid, ask, 1)

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
         if ask > profitTarget and ask != 0.0:
            self.lg.debug ( "CLOSING BUY POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(ask) + " > " + str(profitTarget))
            self.closePosition(bar, barChart, bid, ask, 1)
            if self.waitForNextBar:
               self.setWaitForNextBar()
            return 3
            
      elif self.getPositionType() == self.sell:
         if bid < profitTarget and bid != 0.0:
            self.lg.debug ( "CLOSING SELL POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(bid) + " < " + str(profitTarget))
            self.closePosition(bar, barChart, bid, ask, 1)
            if self.waitForNextBar:
               self.setWaitForNextBar()
            return 3
                 
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoInRange(self, barChart, bar, bid, ask, action=0):
   
      self.lg.debug("In algorithmDoInRange. Action: " + str(action))
      self.reversAction = 0

      if self.inPosition():
         # Take profit once limit hit
#         if self.positionType == self.sell:
#            if self.cn.getCurrentAsk(self.stock) < self.lm.algorithmDoInRange:
#               return 2
#         elif self.positionType == self.buy:
#            if self.cn.getCurrentBid(self.stock) > self.lm.closeSellLimit:
#               return 1
               
         return action
         
      # Return 0 if price is within a range 

      if self.isPriceInRange(bid, ask):
         self.priceInRange += 1
         self.useAvgBarLen = 0
         self.lg.debug("NOT TRADING IN PRICE RANGE AND NOT IN A POSITION " + str(self.lm.doRangeTradeBars))         
         return 0
      
      # if first time out of range then reverse buys and sells and use a trailing
      # avg bar length as the stop.
      # DISBALED 4/13/21 NOT ENOUGH EVIDENCE TO ENABLE AT THIS POINT 
      
      elif self.priceInRange > 1:
         self.lg.debug("REVERSING BUY SELL DUE TO FIRST TIME OUT OF RANGE")
         
         self.reversAction = 1
         
         if action == self.buy:
            action = self.sell
         elif action == self.sell:
            action = self.buy
         
         self.useAvgBarLen += 1
         self.priceInRange = 0
         
         #self.lm.setAvgBarLenLimits(barChart, bar)
         #self.x()
         
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoOnlyTrends(self, bc, bar, bid, ask, action=0):
   
      self.lg.debug("In algorithmDoOnlyTrends: " + str(action))

      # We set the trend limits here since the calculation is dynamic and values
      # change as the price moves
      # This algo takes much CPU time and may need rethinking
            
      self.tr.setTrendLimits(bc, bar, bid, ask)
            
      self.tr.isBearTrend()
      self.tr.isBullTrend()

      loPrice, loBar, hiPrice, hiBar = self.setSessionData(bc, bar)
      
      sessionTrendValue = self.tr.getSessionTrendValue(hiPrice, hiBar, loPrice, loBar, ask)
      self.tr.setSessionTrend(sessionTrendValue)

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
   # Take position if price is higher than high or lower than the low
   
   def algorithmHiLoSeq(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmHiLoSeq " + str(action))
         
      if self.inPosition():
         if self.positionType == self.buy:
            if self.lm.lowerHighsBuyClose and self.lm.lowerLowsBuyClose:
#            if self.lm.isLowerHighs(self.lm.closeBuyBars) and \
#               self.lm.isLowerLows(self.lm.closeBuyBars):
               self.lg.debug ("InPos Hi Lo Seq algo. lower hi's and lower lo's detected")
               return self.sell
         elif self.positionType == self.sell:
            if self.lm.higherHighsSellClose and self.lm.higherLowsSellClose:
#            if self.lm.isHigherHighs(self.lm.closeSellBars) and \
#               self.lm.isHigherLows(self.lm.closeSellBars):
               self.lg.debug ("InPos Hi Lo Seq algo. higher hi's and higher lo's detected")
               return self.buy
      else:
         if self.lm.higherHighsBuyOpen and self.lm.higherLowsBuyOpen:
#         if self.lm.isHigherHighs(self.lm.openBuyBars) and \
#            self.lm.isHigherLows(self.lm.openBuyBars):
            self.lg.debug ("Hi Lo Seq algo. Higher hi's and Higher lo's detected")
            return self.buy
         if self.lm.lowerHighsSellOpen and self.lm.lowerLowsSellOpen:
#         if self.lm.isLowerHighs(self.lm.openSellBars) and \
#            self.lm.isLowerLows(self.lm.openSellBars):
            self.lg.debug ("Hi Lo Seq algo. Lower hi's and Lower lo's detected")
            return self.sell

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high 
   # This works best when in bear trend
   
   def algorithmHiSeq(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmHiSeq " + str(action))
         
      if self.inPosition():
         if self.positionType == self.buy:
            if self.lm.lowerHighsBuyClose:
#            if self.lm.isLowerHighs(self.lm.closeBuyBars):
               self.lg.debug ("InPos Hi Seq algo. lower hi's detected")
               return self.sell
         elif self.positionType == self.sell:
            if self.lm.higherHighsSellClose:
#            if self.lm.isHigherHighs(self.lm.closeSellBars):
               self.lg.debug ("InPos Hi Seq algo. higher hi's detected")
               return self.buy
      else:
         if self.lm.higherHighsBuyOpen:
#         if self.lm.isHigherHighs(self.lm.openBuyBars):
            self.lg.debug ("Hi Seq algo. Higher hi's detected")
            return self.buy
         if self.lm.lowerHighsSellOpen:
#         if self.lm.isLowerHighs(self.lm.openSellBars):
            self.lg.debug ("Hi Seq algo. Lower hi's  detected")
            return self.sell

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is lower than the low
   # This works best when in bull trend

   def algorithmLoSeq(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmLoSeq " + str(action))
         
      if self.inPosition():
         if self.positionType == self.buy:
            if self.lm.lowerLowsBuyClose:
#            if self.lm.isLowerLows(self.lm.closeBuyBars):
               self.lg.debug ("InPos Lo Seq algo. lower lo's detected")
               return self.sell
         elif self.positionType == self.sell:
            if self.lm.higherLowsSellClose:
#            if self.lm.isHigherLows(self.lm.closeSellBars):
               self.lg.debug ("InPos Lo Seq algo. higher lo's detected")
               return self.buy
      else:
         if self.lm.higherLowsBuyOpen:
#         if self.lm.isHigherLows(self.lm.openBuyBars):
            self.lg.debug ("Lo Seq algo. Higher lo's detected")
            return self.buy
         if self.lm.lowerLowsSellOpen:
#         if self.lm.isLowerLows(self.lm.openSellBars):
            self.lg.debug ("Lo Seq algo. Lower lo's detected")
            return self.sell

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high or lower than the low
   # This works best in general

   def algorithmHiLo(self, barChart, bar, bid, ask, last, vol, action=0):

      self.lg.debug("In algorithmHiLo " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.positionType == self.buy:
            self.lg.debug ("Hi Lo: in buy position " + str(self.positionType))
            self.lg.debug ("closeBuyLimit " + str(self.lm.closeBuyLimit))
            if last < self.lm.closeBuyLimit:
               self.lg.debug ("Closing algorithmHiLo BUY. closeBuyLimit breached " + str(last))
               retCode = 2
         if self.positionType == self.sell:
            self.lg.debug ("Hi Lo: in sell position " + str(self.positionType))
            self.lg.debug ("closeSellLimit " + str(self.lm.closeSellLimit))
            if last > self.lm.closeSellLimit:
               self.lg.debug ("Closing algorithmHiLo SELL. closeSellLimit breached " + str(last))
               retCode = 1
      else:
         if last > self.lm.openBuyLimit:
            self.lg.debug ("Opening algorithmHiLo BUY. limit: " + str(self.lm.openBuyLimit) + " last "  + str(last))
            retCode = 1
         if last < self.lm.openSellLimit:
            self.lg.debug ("Opening algorithmHiLo SELL. limit: " + str(self.lm.openSellLimit) + " last "  + str(last))
            retCode = 2

      self.lg.debug("self.doHiLoSeq " + str(self.doHiLoSeq))
      self.lg.debug("self.doOpenCloseSeq " + str(self.doOpenCloseSeq))
      self.lg.debug("action " + str(action))
      self.lg.debug("retCode " + str(retCode))

      if self.doHiLoSeq or self.doHiSeq or self.doLoSeq or self.doOpenCloseSeq:
         if action > 0 and retCode == 0:
            self.lg.debug ("doHiLoSeq set. doHiLo not set")
            # Cancel signal if action not set here or above
            return 0
            
         if action == 0 and retCode > 0:
            self.lg.debug ("doHiLoSeq not set. doHiLo set")
            # Cancel signal if action not set here 
            return 0
         
         if action > 0 and retCode > 0:
            self.lg.debug ("doHiLoSeq set and doHiLo set")
            self.lg.debug ("Taking position...")
      
      return retCode
      


   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Monitor session data
   
   def algorithmSessions(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmSessions " + str(action))
      
      # Count number of session hi's and lows on the open.
      
      if not self.doActionOnOpenBar():
         return action
         
      # Count number of bars in session trends
      
      self.numBarsInBullSessionTrend += self.tr.isBullSessionTrend()
      self.numBarsInBearSessionTrend += self.tr.isBearSessionTrend()
      
      # Decrease trend limit by timeBar
      
      tbf = self.bc.getTimeBarValue() * 0.01
      
      self.lg.debug("Increment session trend value: " + str(tbf))
      
      if self.numBarsInBullSessionTrend > self.lastBarsInBullSessionTrend:
         self.lastBarsInBullSessionTrend = self.numBarsInBullSessionTrend
         self.tr.setBullSessionValue(self.tr.getBullSessionValue() + tbf)
         self.lg.debug("numBarsInBullSessionTrend: " + str(self.numBarsInBullSessionTrend))
         self.lg.debug("New bull session trend value: " + str(self.tr.getBullSessionValue()))
      
      if self.numBarsInBearSessionTrend > self.lastBarsInBearSessionTrend:
         self.lastBarsInBearSessionTrend = self.numBarsInBearSessionTrend
         self.tr.setBearSessionValue(self.tr.getBearSessionValue() - tbf)
         self.lg.debug("numBarsInBearSessionTrend: " + str(self.numBarsInBearSessionTrend))
         self.lg.debug("New bear session trend value: " + str(self.tr.getBearSessionValue()))
      
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher or lower than the opens or closes
   
   def algorithmOpensCloses(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmOpensCloses " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.positionType == self.buy:
            self.lg.debug ("algorithmOpensCloses: in buy position " + str(self.positionType))
            self.lg.debug ("closeBuyLimit " + str(self.lm.closeBuyLimit))
            if last < self.lm.closeBuyLimit:
               self.lg.debug ("Closing algorithmOpensCloses BUY " + str(last))
               retCode = 2
         if self.positionType == self.sell:
            self.lg.debug ("algorithmOpensCloses: in sell position " + str(self.positionType))
            self.lg.debug ("closeSellLimit " + str(self.lm.closeSellLimit))
            if last > self.lm.closeSellLimit:
               self.lg.debug ("Closing algorithmOpensCloses SELL " + str(last))
               retCode = 1
               
      elif not self.inPosition():
         if last > self.lm.openBuyLimit:
            self.lg.debug ("Opening algorithmOpensCloses BUY. limit: " + str(self.lm.openBuyLimit))
            retCode = 1
         if last < self.lm.openSellLimit:
            self.lg.debug ("Opening algorithmOpensCloses SELL. limit: " + str(self.lm.openSellLimit))
            retCode = 2
         
      self.lg.debug ("action " + str(action))
         
      return retCode      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if previous bars opens and closes are sequentially higher or lower
   
   def algorithmOpensClosesSeq(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmOpensClosesSeq " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.positionType == self.buy:
            if self.lm.lowerOpensBuyClose and self.lm.lowerClosesBuyClose:
#            if self.lm.isLowerOpens(self.lm.closeBuyBars) and \
#               self.lm.isLowerCloses(self.lm.closeBuyBars):
               self.lg.debug ("algorithmOpensClosesSeq: Closing Lower opens and Lower closes detected")
               return 2
         elif self.positionType == self.sell:
            if self.lm.higherOpensSellClose and self.lm.higherClosesSellClose:
#            if self.lm.isHigherOpens(self.lm.closeSellBars) and \
#               self.lm.isHigherCloses(self.lm.closeSellBars):
               self.lg.debug ("algorithmOpensClosesSeq: Closing Higher opens and Higher closes detected")
               return 1
      else:
         if self.lm.higherOpensBuyOpen and self.lm.higherClosesBuyOpen:
#         if self.lm.isHigherOpens(self.lm.openBuyBars) and \
#            self.lm.isHigherCloses(self.lm.openBuyBars):
            self.lg.debug ("algorithmOpensClosesSeq: Higher opens and Higher closes detected")
            return 1
         if self.lm.lowerOpensSellOpen and self.lm.lowerClosesSellOpen:
#         if self.lm.isLowerOpens(self.lm.openSellBars) and \
#            self.lm.isLowerCloses(self.lm.openSellBars):
            self.lg.debug ("algorithmOpensClosesSeq: Lower opens and Lower closes detected")
            return 2

      self.lg.debug ("self.doHiLoSeq " + str(self.doHiLoSeq))
      self.lg.debug ("action " + str(action))
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if previous bars closes are sequentially higher or lower
   
   def algorithmClosesSeq(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmClosesSeq " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.positionType == self.buy:
            if self.lm.lowerClosesBuyClose:
#            if self.lm.isLowerCloses(self.lm.closeBuyBars):
               self.lg.debug ("algorithmClosesSeq: Closing Lower closes detected")
               return 2
         elif self.positionType == self.sell:
            if self.lm.higherClosesSellClose:
#            if self.lm.isHigherCloses(self.lm.closeSellBars):
               self.lg.debug ("algorithmClosesSeq: Closing Higher closes detected")
               return 1
      else:
         if self.lm.higherClosesBuyOpen:
            self.lg.debug ("algorithmClosesSeq: Higher closes detected")
            return 1
         if self.lm.lowerClosesSellOpen:
#         if self.lm.isLowerCloses(self.lm.openSellBars):
            self.lg.debug ("algorithmClosesSeq: Lower closes detected")
            return 2

      self.lg.debug ("self.doClosesSeq " + str(self.doClosesSeq))
      self.lg.debug ("action " + str(action))
      
      return 0      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if previous bars opens and closes are sequentially higher or lower
   
   def algorithmOpensSeq(self, barChart, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmOpensSeq " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.positionType == self.buy:
            if self.lm.lowerOpensBuyClose:
#            if self.lm.isLowerOpens(self.lm.closeBuyBars):
               self.lg.debug ("algorithmOpensSeq: Closing Lower opens detected")
               return 2
         elif self.positionType == self.sell:
            if self.lm.higherOpensSellClose:
#            if self.lm.isHigherOpens(self.lm.closeSellBars):
               self.lg.debug ("algorithmOpensSeq: Closing Higher opens detected")
               return 1
      else:
         if self.lm.higherOpensBuyOpen:
#         if self.lm.isHigherOpens(self.lm.openBuyBars):
            self.lg.debug ("algorithmOpensSeq: Higher opens detected")
            return 1
         if self.lm.lowerOpensSellOpen:
#         if self.lm.isLowerOpens(self.lm.openSellBars):
            self.lg.debug ("algorithmOpensSeq: Lower opens detected")
            return 2

      self.lg.debug ("self.doOpensSeq " + str(self.doOpensSeq))
      self.lg.debug ("action " + str(action))
      
      return 0      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmOnClose(self, bar,  action=0):

      self.lg.debug("In algorithmOnClose: " + str(action))

      # If we are not at the end of a new bar, there's nothing to do, get out
      if not self.doActionOnCloseBar():
         return action

      if bar == self.hammerBar or bar == self.invHammerBar:
         self.lg.debug("In algorithmOnClose bar == invHammerBar or hammerBar returning ")
         return action
         
      self.lg.debug("doActionOnCloseBar: " + str(self.doActionOnCloseBar()))         

      # Take position on the close if execute on close is set 
      # Use hi's and lo's for opening a position
      
      if not self.inPosition():
         if self.lm.higherHighsBuyOpen and self.lm.higherLowsBuyOpen:
#         if self.lm.isHigherHighs(self.lm.openBuyBars) and \
#            self.lm.isHigherLows(self.lm.openBuyBars):
            self.lg.debug("TAKING POSITION HigherHighs HigherLows: ")
            return self.buy
         elif self.lm.lowerLowsSellOpen and self.lm.lowerHighsSellOpen:
#         elif self.lm.isLowerLows(self.lm.openSellBars) and \
#            self.lm.isLowerHighs(self.lm.openSellBars):
            self.lg.debug("TAKING POSITION LowerLows LowerHighs: ")
            return self.sell
      
      # Use lo's or hi's on close to get out  
      else:
         if self.positionType == self.buy:
            if self.lm.lowerLowsBuyClose and self.lm.lowerHighsBuyClose:
#            if self.lm.isLowerLows(self.lm.closeBuyBars) and \
#               self.lm.isLowerHighs(self.lm.closeBuyBars):
               self.lg.debug("CLOSING POSITION LowerLows LowerHighs: ")
               return self.buy
         elif self.positionType == self.sell:
            if self.lm.higherHighsSellClose and self.lm.higherLowsSellClose:
#            if self.lm.isHigherHighs(self.lm.closeSellBars) and \
#               self.lm.isHigherLows(self.lm.closeSellBars):
               self.lg.debug("CLOSING POSITION HigherHighs HigherLows: ")
               return self.sell
            
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmOnOpen(self, bar, action=0):
      
      self.lg.debug("In algorithmOnOpen: " + str(action))

      # If we are not on the beginning of a new bar, there's nothing to do, get out
      if not self.doActionOnOpenBar():
         return action

#      if bar == self.hammerBar or bar == self.invHammerBar:
#         self.lg.debug("In algorithmOnOpen bar == invHammerBar or hammerBar returning")
#         return action

      self.lg.debug("doActionOnOpenBar: " + str(self.doActionOnOpenBar()))

      # Use hi's and lo's for opening a position
      if not self.inPosition():
         if self.lm.higherHighsBuyOpen and self.lm.higherLowsBuyOpen:
#         if self.lm.isHigherHighs(self.lm.openBuyBars) and \
#            self.lm.isHigherLows(self.lm.openBuyBars):
            self.lg.debug("TAKING POSITION HigherHighs HigherLows: ")
            return self.buy
         elif self.lm.lowerLowsSellOpen and self.lm.lowerHighsSellOpen:
#         elif self.lm.isLowerLows(self.lm.openSellBars) and \
#            self.lm.isLowerHighs(self.lm.openSellBars):
            self.lg.debug("TAKING POSITION LowerLows LowerHighs: ")
            return self.sell
      
      # Use lo's or hi's on open to get out  
      else:
         if self.positionType == self.buy:
            if self.lm.lowerLowsBuyClose and self.lm.lowerHighsBuyClose:
#            if self.lm.isLowerLows(self.lm.closeBuyBars) and \
#               self.lm.isLowerHighs(self.lm.closeBuyBars):
               self.lg.debug("CLOSING POSITION LowerLows LowerHighs: ")
               return self.buy
         elif self.positionType == self.sell:
            if self.lm.higherHighsSellClose and self.lm.higherLowsSellClose:
#            if self.lm.isHigherHighs(self.lm.closeSellBars) and \
#               self.lm.isHigherLows(self.lm.closeSellBars):
               self.lg.debug("CLOSING POSITION HigherHighs HigherLows: ")
               return self.sell
            
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDefault(self, barChart, bar, bid, ask, action=0):
      
      # Ues the right flag here or continue to use this algo as the default
   
      self.lg.debug("In algorithmDefault " + str(action))

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
   def algorithmPatterns(self, bc, bar, bid, ask, action=0):
   
      # First should be the hammer. In sell position if hammer found close out
      # regardless of number of decision bars

      self.lg.debug("In algorithmPatterns " + str(action))

      #if not self.inPosition():
      #   return action
      
      # bar starts at 0. Need 3 bars
      if bar < 2:
         return action
      
      #if not action:
      #   return action
         
      actionOnOpen = self.doActionOnOpenBar()
      actionOnClose = self.doActionOnCloseBar()
      
      if not actionOnOpen and not actionOnClose:
         return action
      
      self.lg.debug("actionOnOpen " + str(actionOnOpen))
      self.lg.debug("actionOnClose " + str(actionOnClose))
      self.lg.debug("bar in pattern " + str(bar))

      if self.doHammers or self.doAllPatterns:
         action = self.algorithmHammers(bc, bar, bid, ask, actionOnOpen, actionOnClose, action)
         
      if self.doReversals or self.doAllPatterns:
         action = self.algorithmReversals(bc, bar, bid, ask, actionOnOpen, actionOnClose, action)

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmReversals(self, bc, bar, bid, ask, actionOnOpen, actionOnClose, action=0):

      self.lg.debug("In algorithmReversals " + str(action))

      if not actionOnClose:
         return action
         
      if self.inPosition():
         #if self.loReversal:
         if self.positionType == self.sell:
            self.lg.debug("self.loReversal " + str(self.loReversal))
            #if self.pa.isHiReversalO(bc, bar):
            if self.pa.isHiReversalO(bc, bar) and not self.pa.isEngulfing(bc, bar):
               self.lg.debug("isHiReversal exiting " + str(self.pa.isHiReversalO(bc, bar)))
               self.loReversal = 0
               #self.closePosition(bar, bc, bid, ask, 1)
               return 1
            
         #if self.hiReversal:  
         if self.positionType == self.buy:
            self.lg.debug("self.hiReversal " + str(self.hiReversal))
            #if self.pa.isLoReversalO(bc, bar):
            if self.pa.isLoReversalO(bc, bar) and not self.pa.isEngulfing(bc, bar):
               self.hiReversal = 0
               self.lg.debug("isLoReversal exiting " + str(self.pa.isLoReversalO(bc, bar)))
               #self.closePosition(bar, bc, bid, ask, 1)
               return 2
      else:
         #if self.pa.isHiReversalO(bc, bar):
         if self.pa.isHiReversalO(bc, bar) and not self.pa.isEngulfing(bc, bar):
            self.lg.debug("isHiReversal " + str(self.pa.isHiReversalO(bc, bar)))
            self.hiReversal += 1
            self.loReversal = 0
            #self.openPosition(self.buy, bar, bc, bid, ask)
            return 1
            
         #if self.pa.isLoReversalO(bc, bar):
         if self.pa.isLoReversalO(bc, bar) and not self.pa.isEngulfing(bc, bar):
            self.loReversal += 1
            self.hiReversal = 0
            self.lg.debug("isLoReversal " + str(self.pa.isLoReversalO(bc, bar)))
            #self.openPosition(self.sell, bar, bc, bid, ask)
            return 2

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmEncompassing(self, bc, bar, action=0):

      self.lg.debug("In algorithmEncompassing " + str(action))

      if self.pa.isHiEncompassing(bc, bar, action):
         self.lg.debug("isHiEncompassing " + str(self.pa.isHiEncompassing(bc, bar)))
         return 1
         
      if self.pa.isLoEncompassing(bc, bar, action):
         self.lg.debug("isLoEncompassing " + str(self.pa.isLoEncompassing(bc, bar)))
         return 1

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmHammers(self, bc, bar, bid, ask, actionOnOpen, actionOnClose, action=0):

      self.lg.debug("In algorithmHammers " + str(action))

      hammer = invHammer = hiEncompassing = loEncompassing = 0
      barAfterHammerHigher = barAfterHammerLower = invHammerInner = 0
      
      if self.pa.isHammer(bc, bar):
         hammer = 1
         self.lg.debug("HAMMER " + str(hammer))
         
      elif self.pa.isInvHammer(bc, bar):
         invHammer = 1
         self.lg.debug("INV HAMMER " + str(invHammer))
         
      elif self.pa.isHammerInner(bc, bar):
         hammerInner = 1
         self.lg.debug("HAMMER INNER " + str(hammerInner))
         
      elif self.pa.isInvHammerInner(bc, bar):
         invHammerInner = 1
         self.lg.debug("INV HAMMER INNER " + str(invHammerInner))
                     
      # Logic: Take position if hammer or invHammer on open of next bar
      # hammer = session hi; invHammer = sessionlo
      # Get out of position on hammer not at session hi or lo
            
      # Get out if really not a hammer. Do once on after bar close.
      if self.inPosition():
         # Get out if really not a hammer
         if self.inHammerPosition:
            if actionOnClose:
               if bar == self.hammerBar:
                  if self.pa.isPreviousBarLower(bc, bar - 1, bar):
                     self.closePosition(bar, bc, bid, ask, 1)
                     self.inHammerPosition = 0
                     
                  
            # Close out of Hammer. Open invHammer if at session hi
            elif actionOnOpen:
               if invHammer:
                  self.closePosition(bar, bc, bid, ask, 1)
                  self.openPosition(self.buy, bar, bc, bid, ask)
                  self.inInvHammerPosition += 1
                  self.inHammerPosition = 0
                  
            # Ignore action set by upstrean algorithm if in bar after hammer bar
            if self.hammerBar + 1 == bar and action > 0:
               self.lg.debug("Ignoring previous signal... ")
               action = 0

         # Get out if really not an invHammer
         elif self.inInvHammerPosition:
            if actionOnClose:
               if bar == self.invHammerBar:
                  if self.pa.isPreviousBarHigher(bc, bar - 1, bar):
                     self.closePosition(bar, bc, bid, ask, 1)
                     self.inInvHammerPosition = 0
                                 
            # Close out of InvHammer. Open Hammer if at session lo
            elif actionOnOpen:
               if hammer:
                  self.closePosition(bar, bc, bid, ask, 1)
                  self.openPosition(self.sell, bar, bc, bid, ask)
                  self.inHammerPosition += 1
                  self.hammerBar = bar
                  self.inInvHammerPosition = 0
            
            # Ignore action set by upstrean algorithm if in bar after invHammer bar
            if self.invHammerBar + 1 == bar and action > 0:
               self.lg.debug("Ignoring previous signal... ")
               action = 0
                  
         # In a position NOT initiated from a hammer or invHammer
         else:
            if hammer:
               self.lg.debug("HAMMER DETECTED! CLOSING POSITION")
               # Detect volume > previous bar by setting action             
               # THIS WAS JUST CHANGED TESTTTTTTTTTTTTT
               #action = 1
               
               self.closePosition(bar, bc, bid, ask, 1)
               
               
#               self.lg.debug("HAMMER DETECTED! CLOSING POSITION")
#               self.openPosition(self.sell, bar, bc, bid, ask)
#               self.inHammerPosition += 1
#               self.hammerBar = bar
#               self.inInvHammerPosition = 0
               
            elif invHammer:
               self.lg.debug("INV HAMMER DETECTED! CLOSING POSITION")
               # Detect volume > previous bar by setting action
               self.closePosition(bar, bc, bid, ask, 1)
               
               #action = 2
               #
#               self.lg.debug("INV HAMMER DETECTED! OPENING POSITION")
#               self.openPosition(self.buy, bar, bc, bid, ask)
#               self.invHammerBar = bar
#               self.inInvHammerPosition += 1
#               self.inHammerPosition = 0
#               self.setWaitForNextBar()

      else:
         if hammer:
            action = 2
            self.lg.debug("Hammer detected! setting action " + str(action))
            self.inHammerPosition += 1
            self.hammerBar = bar
         elif invHammer:
            action = 1
            self.lg.debug("invHammer detected! setting action " + str(action))
            self.inInvHammerPosition += 1
            self.invHammerBar = bar
         else:
            self.inInvHammerPosition = self.inHammerPosition = 0
            self.hammerBar = self.invHammerBar = 0
               
      return action

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmTrailingStop(self, last, action=0):
   
      # Monitor gainTrailStop 
      # Move decision bars depending how long in pos
      # Take profit depending on how long in pos
      # Track how many bars price in a range. 
      # see where price is relative to session hi's/lo's
      # exit method if action > 0
      
      stoppedOut = 4
      
      self.lg.debug("In algorithmTrailingStop " + str(action))
        
      liveGain = self.setTotalLiveGain(last)
      self.lg.debug("liveGain " + str(liveGain))
      
      # If there is a signal to get out of a pos, get out. THIS ADDED AFTER ALGO WRITTEN
      if action > 0:
         return action       

      if self.stopPct > 0:         
         # Raise/Lower stop
         self.lg.debug("self.stopBuyTarget " + str(self.stopBuyTarget))
         self.lg.debug("self.stopSellTarget " + str(self.stopSellTarget))
         self.lg.debug("last " + str(last))
         self.lg.debug("self.stopPct " + str(self.stopPct))
         
         if self.positionType == self.buy:
            if last < self.stopBuyTarget:
               self.lg.debug("stopped out " + str(last))
               self.lg.debug("self.stopBuyTarget " + str(self.stopBuyTarget))
               # End trading
               return 4
               
            self.lg.debug("last + self.stopPct " + str(last + self.stopPct))
            # Raise target
            if last - self.stopPct > self.stopBuyTarget:
               self.stopBuyTarget = round((last - self.stopPct), 2)
         else:
            if last > self.stopSellTarget:
               self.lg.debug("stopped out " + str(last))
               self.lg.debug("self.stopSellTarget " + str(self.stopSellTarget))
               # End trading
               return 4

            self.lg.debug("last - self.stopPct " + str(last - self.stopPct))
            # Lower target
            if last + self.stopPct < self.stopSellTarget:
               self.stopSellTarget = round((last + self.stopPct), 2)
               
         self.lg.debug("self.stopBuyTarget after " + str(self.stopBuyTarget))
         self.lg.debug("self.stopSellTarget after " + str(self.stopSellTarget))
            
         return 0
            
      elif self.inPosition():
         #if self.getTotalGain() >= self.getTargetProfit():
         if liveGain >= self.getTargetProfit():
            # self.getTotalGain() will be 0 when in the first position
            if self.getTotalGain() == 0.0:
               profitGained = liveGain
            else:
               profitGained = self.getTotalGain()
            self.lg.debug("self.profitGainedPct " + str(self.profitGainedPct))
            self.stopPct = profitGained * self.profitGainedPct
            self.stopBuyTarget = round(last - self.stopPct, 2)
            self.stopSellTarget = round(last + self.stopPct, 2)
               
            self.lg.debug("profitGained " + str(profitGained))

      self.lg.debug("self.getTotalGain() " + str(self.getTotalGain()))
      self.lg.debug("self.getTargetProfit() " + str(self.getTargetProfit()))

      self.lg.debug("last " + str(last))
      self.lg.debug("self.stopPct " + str(self.stopPct))
         
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPriceTracking(self, bid, ask, last, action=0):
      
      self.lg.debug("In algorithmPriceTracking: " + str(action))

      # If in a position monitor it
      # close out position if near loss/profit target.
      
      if not self.inPosition():
         return 0
      
      tGain = last - self.openPositionPrice

      if self.ask:
         if tGain < 0:
            tGain = tGain*-1

      print ("tGain last - self.openPositionPrice " + str(tGain))
            
      if tGain == 0.0:
         return 0
      
      if self.positionType == self.buy:
         last = ask
         self.lg.debug("Last ask price: " + str(last))
         self.lg.debug("self.openPositionPrice: " + str(self.openPositionPrice))
         self.lg.debug("diff: " + str(last - self.openPositionPrice))

         if last > self.openPositionPrice:
            self.lg.debug("Position is gaining profit: ")
            self.lg.debug("+" + str(last - self.openPositionPrice))
#            if self.exitWProfit(tGain):
#               self.lg.debug("Exiting with inPos profit: ")
#               self.setInPosGain()
#               return 1
            
            if self.priceNearProfitTarget(tGain):
               return 1
               
         else:
            self.lg.debug("Position is adding to the current loss: ")
            self.lg.debug(str(tGain) + " -" + str(self.openPositionPrice - last))
            #if self.exitWLoss(tGain):
#            if self.exitWLoss(tGain):
#               self.lg.debug("Exiting with inPos loss: ")
#               #self.setInPosGain()
#               return 1
            
            if self.priceNearLossTarget(tGain):
               return 1

      elif self.positionType == self.sell:
         last = bid
         self.lg.debug("Last bid price: " + str(last))
         self.lg.debug("self.openPositionPrice: " + str(self.openPositionPrice))
         self.lg.debug("diff: " + str(self.openPositionPrice - last))

         if last < self.openPositionPrice:
            self.lg.debug("Position is gaining profit: ")
            self.lg.debug("+" + str(self.openPositionPrice - last))
#            if self.exitWProfit(tGain):
#               self.lg.debug("Exiting with inPos profit: ")
#               self.setInPosGain()
#               return 1
            if self.priceNearProfitTarget(tGain):
               return 1
               
         else:
            self.lg.debug("Position is adding to the current loss: ")
            self.lg.debug(str(tGain) + " -" + str(self.openPositionPrice - last))
#            if self.exitWLoss(tGain):
#               self.lg.debug("Exiting with inPos loss: ")
#               #self.setInPosGain()
#               return 1

            if self.priceNearLossTarget(tGain):
               return 1
               
      return 0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDynamic(self, bid, ask, last, action=0):
      
      self.lg.debug("In algorithmDynamic: " + str(action))

      # determine OB and CB's based on daily chart data. 
      # get % gain at open compare with simlar day % gain and use that 
      # days results. e.g:
      # open 20% lower; find day(s) ~20% lower open; if day gain +
      # set OB buy bars at 1 CS bars at 3 
      
      # Too many times trends are a + gain. Don't let them turn negative
      if self.doTrends:
         doInPosTracking += 1

      # Turn on quick loss 
      
      
      # Detect range bound condition and get out or turn on IR
      
      inRangeBars = self.dy.getRangeBars()
      
      # Turn QP on during first ~30 min of trading
      
      # Turn QP or IT on for stock price > $20 or when CS/CB's > 2
      #  many positive positions turn negative when using CS/CB's > 2
      
      # If in bull trend use HI algo? LO for bear?
      
      # Use live tracking. If in profit over $1 set limit to $1 and get out
      
      # if in trend for a while (after MEGA is set )set quick profit, HM, RV to get 
      # out with healthy profit don't let the trend turn around for minimum profit...

      # Use trends to turn on more or less decision bars.
      # e.g: if short and mid bull, turn on 4 or 5 close buy bars
      # if bear trend turn on 4 or 5 close sell bars
      
      #                                     |   | |
      # do hammer detection. once detected | |   |  turn on sells, buys and/or trends
      
      # Turn on trends after the beginning of the day to keep from trading too much
      # during the slow lunch hours for TQQQ
      
      # if in an oscilating trade get out
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
            
      # Once price goes out of range reverse buys and sells
      if self.isPriceInRange(bid, ask):
         self.dynPriceInRange += 1

      if not self.isPriceInRange(bid, ask) and self.dynPriceInRange:
         self.doReverseBuySell += 1
         self.setRevBuySell()
         self.dynPriceInRange = 0

      if self.bc.getBarsInPosition() > self.lm.openBuyBars:
         self.lm.openBuyBars -= 1
         
      if self.bc.getBarsInPosition() > self.lm.closeBuyBars and self.lm.closeBuyBars > 0:
         self.lm.closeBuyBars -= 1
         
      # If in a position and within a range sell out for profit as exiting range
      #if self.inPosition() and self.getBarsInPosition() > self.lm.doRangeTradeBars:
      #   self.closeSellBar = 0
      #   self.closeBuyBar = 0.0
         
      # if in a gain position set stop just above average bar length?
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def exitWProfit(self, lastGain):
      
      # Calculate if we should exit with profit
      # How close is the price to the min profit amount?
      
      #profitAmt = lastGain * self.quickProfitPctTrigger

      if lastGain < 0:
         return 0
                  
      pctNearTrgt = lastGain / self.getTargetProfit()

      self.lg.debug("exitWProfit: pctNearTrgt " + str(pctNearTrgt))
      self.lg.debug("exitWProfit: inPosProfitPct " + str(self.inPosProfitPct))

      if pctNearTrgt > self.inPosProfitPct: # 60%
         return 1
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def exitWLoss(self, lastLoss):
      
      # Calculate if we should exit with profit
      # How close is the price to the min profit amount?
      
      #profitAmt = lastLoss * self.quickProfitPctTrigger

      if lastLoss > 0:
         return 0
                  
      pctNearTrgt = lastLoss / self.getTargetProfit()

      self.lg.debug("exitWProfit: pctNearTrgt " + str(pctNearTrgt))
      self.lg.debug("exitWProfit: inPosProfitPct " + str(self.inPosProfitPct))

      if pctNearTrgt > self.inPosLossPct: # 50%
         return 1
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def priceNearLossTarget(self, loss):
   
      pctNearTrgt = loss / self.getTargetProfit()

      self.lg.debug("priceNearLossTarget: pctNearTrgt " + str(pctNearTrgt))
      self.lg.debug("priceNearLossTarget: inPosProfitPct " + str(self.inPosProfitPct))

      if pctNearTrgt > self.inPosLossPct: # 60%
         return 
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def priceNearProfitTarget(self, gain):
   
      pctNearTrgt = gain / self.getTargetProfit()

      self.lg.debug("priceNearProfitTarget: pctNearTrgt " + str(pctNearTrgt))
      self.lg.debug("priceNearProfitTarget: inPosProfitPct " + str(self.inPosProfitPct))

      if pctNearTrgt > self.inPosProfitPct: # 50%
         return 1
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def ready(self, currentNumBars):
          
      self.lg.debug("tradingDelayBars currentNumBars " + str(self.lm.getTradingDelayBars()) + " " + str(currentNumBars))
      
      if self.lm.getTradingDelayBars() <= currentNumBars:
         return 1
      else:
         return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPriceInRange(self, bid, ask):
   
      if not self.lm.doRangeTradeBars:
         return 0

      self.lg.debug("In isPriceInRange")
      self.lg.debug("self.lm.rangeHi " + str(self.lm.rangeHi))
      self.lg.debug("self.lm.rangeLo " + str(self.lm.rangeLo))

      #if self.cn.getCurrentBid(self.stock) >= self.lm.rangeLo and self.cn.getCurrentAsk(self.stock) <= self.lm.rangeHi:
      if bid >= self.lm.rangeLo and ask <= self.lm.rangeHi:
         if not self.inPosition():
            self.lg.debug ("IN RANGE BETWEEN " + str(self.lm.rangeLo) +  " >" + str(self.cn.getLastTrade(self.stock)) + "< " +  str(self.lm.rangeHi))

         return 1

      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def waitingForBestPrice(self):
   
      if self.waitForBestPrice:
         return
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doTrendsRestrictOpen(self, action, bar, bc, bid, ask):

      if self.numTrades > 0:
      
         self.tr.setTrendLimits(bc, bar, bid, ask)

         if action == self.buy and not self.tr.isBullTrend():
            self.lg.debug("got buy with no bull trend BLOCKING... ")
            return 1
         elif action == self.sell and not self.tr.isBearTrend():
            self.lg.debug("got sell with no bear trend BLOCKING... ")
            return 1
         
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
#         self.tr.setTrendLimits(bc, bar, bid, ask)
#         if self.tr.isShortMidBullLongMegaBear() and action == self.buy:
#            self.lg.debug("isShortMidBullLongMegaBear... ")
#            return
#         if self.tr.isShortMidBearLongMegaBull() and action == self.sell:
#            self.lg.debug("isShortMidBearLongMegaBull... ")
#            return

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doSessionsRestrictOpen(self, action, bar, bc, bid, ask):
   
      # Don't take position the opposite way of the lo
      
      loPrice, loBar, hiPrice, hiBar = self.setSessionData(bc, bar)
      
      self.lg.debug("session loPrice, loBar " + str(loPrice) + " " + str(loBar))
      self.lg.debug("session hiPrice, hiBar " + str(hiPrice) + " " + str(hiBar))

      sessionTrendValue = self.tr.getSessionTrendValue(hiPrice, hiBar, loPrice, loBar, ask)
      self.tr.setSessionTrend(sessionTrendValue)

      if self.lm.doRangeTradeBars:
         # Block if we are in a bull trend and trade is reversed
         if self.reversAction:
            self.lg.debug("reversAction set " )
            if action == self.buy and self.tr.isBearSessionTrend():
               self.lg.debug("blocking  isBearSessionTrend and buy" )
               return 1
            if action == self.sell and self.tr.isBullSessionTrend():
               self.lg.debug("blocking  isBullSessionTrend and sell " )
               return 1
#      else:     
         # NOT SURE WHAT THIS ACCOMPLISHES TEST
#            if action == self.buy and bid > hiPrice and hiBar == 1:
#               self.lg.debug("blocking buy bid > hiPrice and hiBar == 1" )
#               return 1
#            if action == self.sell and ask < loPrice and loBar == 1:
#               self.lg.debug("blocking sell ask < loPrice and loBar == 1" )
#               return 1
         
      if action == self.buy and self.tr.isBearSessionTrend():
         self.lg.debug("session buy isBearSessionTrend not opening position... ")
         return 1
      elif action == self.sell and self.tr.isBullSessionTrend():
         self.lg.debug("session sell isBullSessionTrend not opening position... ")
         return 1

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def restrictOpen(self, action, bar, bc, bid, ask):
      
      self.lg.debug("In restrictOpen")
      
      # Bastards halt trading, bid and ask are 0 sometimes
      if bid == 0.0 or ask == 0.0:
         self.lg.debug("bid or ask are 0: bid: " + str(bid) + " ask: " + str(ask))
         return 1

      if self.getWaitForNextBar():
         self.lg.debug("getWaitForNextBar is set... bar;self.getNextBar() " + str(bar) + " " + str(self.getNextBar()))
         if bar < self.getNextBar():
            self.lg.debug("Waiting for next bar... " + str(self.getNextBar()))
            return 1

      # Block taking a position if we are in a range and 
      # range trading is set or delay bars are set
      if not self.ready(bar):
         self.lg.debug("BLOCKING TRADING DUE TO DELAY BARS " + \
            str(self.lm.getTradingDelayBars()))         
         return 1

      if self.isPriceInRange(bid, ask):
         self.priceInRange += 1
         self.lg.debug("NOT TRADING IN PRICE RANGE AND NOT IN A POSITION " + \
            str(self.lm.doRangeTradeBars))         
         return 1

      if self.doSessions:
         if self.doSessionsRestrictOpen(action, bar, bc, bid, ask):
            return 1
            
      # Use the trend to only buy or sell if a trend exists.
      
      if self.doTrends:
         if self.doTrendsRestrictOpen(action, bar, bc, bid, ask):
            return 1

      if self.doOnlyBuys and action == self.sell:
         return 1
      
      if self.doOnlySells and action == self.buy:
         return 1
         
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def openPosition(self, action, bar, bc, bid, ask):
      
      self.lg.debug("START OF OPEN POSITION: " + str(action))

      if self.restrictOpen(action, bar, bc, bid, ask):
         return
         
      # Open a BUY position
      if action == self.buy:
         price = ask
         self.positionType = self.buy
         
         # Execute order here ========================
         
         if self.offLine:
            self.lg.logIt(self.buy, str(price), str(self.bc.getBarsInPosition()), bc[bar][self.dt], "")
         else:
            self.lg.logIt(self.buy, str(price), str(self.bc.getBarsInPosition()), self.cn.getTimeStamp(), "")
         
      # Open a SELL position
      else:
         price = bid
         self.positionType = self.sell
         
         # Execute order here ========================
         
         if self.offLine:
            self.lg.logIt(self.sell, str(price), str(self.bc.getBarsInPosition()), bc[bar][self.dt], "")
         else:
            self.lg.logIt(self.sell, str(price), str(self.bc.getBarsInPosition()), self.cn.getTimeStamp(), "")

      self.setOpenPositionValues(price, bid, ask)
      self.openPositionMsg(price, action, bar, bc)
         
      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def openPositionMsg(self, price, action, bar, bc):
   
      self.lg.info("\n")
      self.lg.info("POSITION OPEN " + str(self.stock))
      self.lg.info("Bar:  " + str(bar + 1))
      self.lg.info("buy/sell: " + str(action))
      self.lg.info("Open buy limit: " + str(self.lm.openBuyLimit))
      self.lg.info("Open sell limit: " + str(self.lm.openSellLimit))
      self.lg.info("Open position Price: " + str(price))
      
      
      #self.lg.info("self.offLine: " + str(self.offLine))
      #self.lg.info("bc[bar][self.dt] " + str(bc[bar][self.dt]))
      
      if self.offLine:
         self.lg.info("Position Time: " + bc[bar][self.dt] + "\n")
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()) + "\n")
               

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getInPosGain(self):
      
      return self.inPosGain
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setInPosGain(self):
      
      self.inPosGain = 1
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenPositionValues(self, price, bid, ask):
   
      self.setGainLastPrice(price)
      self.setLossLastPrice(price)
      self.setQuickProfitTarget(bid, ask, 0)
      self.setExecuteOnOpenPosition(0)
      
      self.position = "open"
      self.openPositionPrice = price
      
      self.exitWProfitVal = self.openPositionPrice * self.quickProfitPctTrigger

      self.bc.setBarsInPosition()

      self.lm.lowestcloseSellLimit = self.lm.closeSellLimit
      self.lm.highestcloseBuyLimit = self.lm.closeBuyLimit
      
      if self.reversAction:
         self.setWaitForNextBar()

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doTrendsRestrictClose(self, bar, bc, bid, ask):

      self.tr.setTrendLimits(bc, bar, bid, ask)  
      
      # Decrement the trend value so we get out of long positions earlier at
      # possibly a better price
      
      
      if self.positionType == self.buy and self.tr.isBullTrendClose():
#      #if self.positionType == self.buy and self.tr.isBullTrend():
#      #if self.positionType == self.buy and self.tr.isBullTrend() and not self.getGain():
#      
#         if self.doActionOnOpenBar():
#            self.shortTrend = self.shT
#            self.midTrend = self.miT
#            self.longTrend = self.loT
#            self.megaTrend = self.meT
#     
#         # KEEP TRACK OF THE TREND VALUES IF THEY ARE NOT INCREASING DON'T BLOCK
#         self.shT, self.miT, self.loT, self.meT, self.suT =  self.tr.getTrendValues()
#
#         self.lg.debug("self.shT " + str(self.shT))
#         self.lg.debug("self.shortTrend" + str(self.shortTrend))
#         
#         self.lg.debug("self.miT " + str(self.miT))
#         self.lg.debug("self.midTrend" + str(self.midTrend))
#         
#         self.lg.debug("self.loT " + str(self.loT))
#         self.lg.debug("self.longTrend" + str(self.longTrend))
#         
#         self.lg.debug("self.meT " + str(self.meT))
#         self.lg.debug("self.megaTrend" + str(self.megaTrend))
#         
#         if self.shortTrend > self.shT or self.midTrend > self.miT \
#            or self.longTrend > self.loT or self.megaTrend > self.meT:
#            self.lg.debug("trend bar values are shrinking. Getting out")
#            return 0
#
         self.lg.debug("Got a BUY close signal... BLOCKING isBullTrend " + str(self.positionType))
         self.lg.debug("barsInposition < 1 setting bar delay ")

         self.setWaitForNextBar()
         return 1
         
      if self.positionType == self.sell and self.tr.isBearTrendClose():
      #if self.positionType == self.sell and self.tr.isBearTrend():
      #if self.positionType == self.sell and self.tr.isBearTrend() and not self.getGain():
         self.lg.debug("Got a SELL close signal... BLOCKING isBearTrend " + str(self.positionType))
         if self.bc.getBarsInPosition() < 2:
            self.lg.debug("barsInposition < 1 setting bar delay ")
            self.setWaitForNextBar()
         return 1
         
#         if self.positionType == self.buy and (not self.tr.isBearTrend() and not self.tr.isBullTrend()):
#            self.lg.debug("Got a BUY close signal... BLOCKING no trend" + str(self.positionType))
#            self.setWaitForNextBar()
#            return 1
#         if self.positionType == self.sell and (not self.tr.isBearTrend() and not self.tr.isBullTrend()):
#            self.lg.debug("Got a SELL close signal... BLOCKING no trend" + str(self.positionType))
#            self.setWaitForNextBar()
#            return 1    

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doSessionsRestrictClose(self, bar, bc, bid, ask):

      # Don't close position the opposite way of the lo
      sessionLo, loBar, sessionHi, hiBar = self.setSessionData(bc, bar)

      loPrice, loBar, hiPrice, hiBar = self.setSessionData(bc, bar)
      
      sessionTrendValue = self.tr.getSessionTrendValue(hiPrice, hiBar, loPrice, loBar, ask)
      self.tr.setSessionTrend(sessionTrendValue)

      self.lg.debug("session loPrice, loBar " + str(sessionLo) + " " + str(loBar))
      self.lg.debug("session hiPrice, hiBar " + str(sessionHi) + " " + str(hiBar))
      
      self.lg.info ("loBar sessionLo " + str(loBar) + " " + str(sessionLo))
      self.lg.info ("hiBar sessionHi " + str(hiBar) + " " + str(sessionHi))
      
      # NEED in position session trend tracker : 
      # bar 10 sTrend = 1.9 bar 15 strend == 1.7...
       
#         if self.positionType == self.buy and bid > sessionLo and loBar == 0:
#            self.lg.info ("positionType == buy and bid > sessionLo and loBar == 0 " + str(sessionLo > bid) + " " + str(loBar))
#            return 1
#            
#         if self.positionType == self.sell and ask < sessionHi and hiBar == 0:
#            self.lg.info ("positionType == sell and ask < sessionHi and hiBar == 0 " + str(sessionHi > ask) + " " + str(hiBar))
#            return 1

      self.lg.debug("session: getBullSessionValue " + str(self.tr.getBullSessionValue()))
      self.lg.debug("session: getBearSessionValue " + str(self.tr.getBearSessionValue()))

      if self.positionType == self.buy and self.tr.isBullSessionTrend():
         self.lg.debug("session: in a buy and isBullSessionTrend not closing position... ")
         return 1
      elif self.positionType == self.sell and self.tr.isBearSessionTrend():
         self.lg.debug("session in a sell and isBearSessionTrend not closing position... ")
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def restrictClose(self, bar, bc, bid, ask):

      self.lg.debug ("bar " + str(bar))
      self.lg.debug ("getNextBar() " + str(self.getNextBar()))

      # Bastards halt trading and bid and ask are 0 sometimes
      if bid == 0.0 or ask == 0.0:
         self.lg.debug("bid or ask are 0: bid: " + str(bid) + " ask: " + str(ask))
         return 1
   
      if self.reversAction:
         if bar < self.getNextBar():
            return 1

      if self.getWaitForNextBar():
         if bar < self.getNextBar():
            self.lg.debug("Waiting for next bar... " + str(self.getNextBar()))
            return 1

      # Use trends to stop start trading and to verify signal instead of holding 
      # on to a trade after we get signals
      
      if self.doTrends:
      #if self.doTrends and not self.doReversals:
         if self.doTrendsRestrictClose(bar, bc, bid, ask):
            return 1

      if self.doSessions:
      #if self.doSessions and not self.doReversals:
         if self.doSessionsRestrictClose(bar, bc, bid, ask):
            return 1

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def closePosition(self, bar, bc, bid, ask, force):

      self.lg.debug("START OF CLOSE POSITION: " + str(self.positionType))

      if not force:
         if self.restrictClose(bar, bc, bid, ask):
            return
      
      gain = price = 0

      if self.positionType == self.buy:
         price = bid
         print ("close position bid: " + str(bid))
      else:
         price = ask
         print ("close position ask: " + str(ask))
         
      if self.positionType == self.buy:
         gain = round(price - self.openPositionPrice, 2)
      elif self.positionType == self.sell:
         gain = round(self.openPositionPrice - price, 2)

      self.lg.debug ("gain at position close time " + str(gain))

      self.closePositionPrice = price
      self.totalGain += gain
      
      # This fixes exponential values in log file
      self.totalGain = round(self.totalGain ,2)

      self.lg.debug ("total gain at position close time" + str(self.totalGain))

      self.totalLoss = self.totalGain
      self.setGainLastPrice(price)
      self.setLossLastPrice(price)

      self.closePositionMsg(bc, bar, gain, price)
      self.setClosePositionValues(bar, gain, price)
      
      if self.waitForNextBar:
         self.setNextBar(bar + 1)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def closePositionMsg(self, bc, bar, gain, price):

      # Update the log
      if self.offLine:
         self.lg.logIt(self.close, str(price), str(self.bc.getBarsInPosition()), bc[bar][self.dt], self.numTrades)
      else:
         self.lg.logIt(self.close, str(price), str(self.bc.getBarsInPosition()), self.cn.getTimeStamp(), self.numTrades)

      self.lg.debug ("\n")
      self.lg.info ("POSITION CLOSED " + self.stock)
      
      if self.offLine:
         self.lg.info("Position Time: " + bc[bar][self.dt])
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()))

      self.lg.info ("position Type: " + str(self.positionType))
      self.lg.info ("open price: " + str(self.openPositionPrice))
      self.lg.info ("close price: " + str(self.closePositionPrice))
      self.lg.info ("current Price: " + str(price))
      self.lg.info ("gain: " + str(gain))
      self.lg.info ("stopPrice: " + str(self.getClosePrice()))
      self.lg.info ("bar Count In Position: " + str(self.bc.getBarsInPosition()))
      self.lg.info ("Loss/Gain: " + str(gain))
      self.lg.info ("Total Gain: " + str(self.totalGain) + "\n")
      self.lg.info ("Number of trades: " + str(self.numTrades) + "\n")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setClosePositionValues(self, bar, gain, price):

      self.numTrades += 1
      
      #gain = price = 0

      self.openPositionPrice = self.closePositionPrice = 0.0
      self.topIntraBar = 0.0

      self.positionType = 0
      self.barCounter = 0
      self.highestcloseBuyLimit = 0.0
      self.lowestcloseSellLimit = 0.0
      self.stopPct = 0
      
      self.bc.resetBarsInPosition()
      
      self.position = "close"
      self.lastCloseBuyLimit = 0.0
      self.lastCloseSellLimit = 999.99

      if gain < 0:
         self.quickProfitCtr = 0
         self.avgBarLenCtr = 0
         # self.setWaitForNextBar()
      
      #self.lm.resetLimits()
      self.setExecuteOnClosePosition(0)

      #if self.doReverseBuySell:
      #   self.unsetRevBuySell()
      
      # Reset session values
      if self.doSessions:
         self.tr.setBullSessionValue(self.timeBar)
         self.tr.setBearSessionValue(self.timeBar)

      if self.doTrends:
         self.shT = self.miT = self.loT = self.meT = self.suT = 0.0
         self.shortTrend = self.midTrend = 0.0
         self.longTrend = self.megaTrend = 0.0

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

   # Setter/Getter definitions

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setSessionData(self, bc, bar):
   
      loPrice, loBar = self.bc.getSessionLoAndBar(bc, bar)
      hiPrice, hiBar = self.bc.getSessionHiAndBar(bc, bar)
      
      return loPrice, loBar, hiPrice, hiBar

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setActionOnOpenBar(self):
   
      self.doOnOpenBar += 1
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetActionOnOpenBar(self):
   
      self.doOnOpenBar = 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doActionOnOpenBar(self):
   
      return self.doOnOpenBar
            
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
   def getTotalLoss(self):

      return self.totalLoss

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTotalGain(self):

      return self.totalGain

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getGainLastPrice(self):

      return self.totalGainLastPrice

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setGainLastPrice(self, price):

      self.totalGainLastPrice = price

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLossLastPrice(self):

      return self.totalLossLastPrice

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setLossLastPrice(self, price):

      self.totalLossLastPrice = price

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTotalLiveGain(self, last):

      # gainPrice $.50 + last $200.00 = $200.50
      # Is $200.50 > last?
               
      gainPrice = self.getGainLastPrice() 
      
      if self.inPosition():
         if self.positionType == self.buy:
            self.totalLiveGain = self.getTotalGain() + (last - gainPrice)
         else:
            self.totalLiveGain = self.getTotalGain() - (last - gainPrice)
         
      return self.totalLiveGain
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTotalLiveLoss(self, last):

      # gainPrice $.50 - last $200.00 = $199.50
      # Is $199.50 < last?
               
      lossPrice = self.getLossLastPrice() 
      
      if self.inPosition():
         if self.positionType == self.buy:
            self.totalLiveLoss = self.getTotalLoss() - (last - lossPrice)
         else:
            self.totalLiveLoss = self.getTotalLoss() + (last - lossPrice)
         
      return self.totalLiveLoss
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTotalLiveGain(self):

      print ("live gain " + str(self.totalLiveGain))
      
      return self.totalLiveGain
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTargetProfit(self):

      return self.targetProfit
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTargetLoss(self):

      return self.targetLoss
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTargetProfit(self, price, pct):

      # Increase profit target % for lower priced stocks

      priceLimits = self.priceLimits.split(',')
      lenPriceLimits = len(priceLimits)
      
      # "priceLimits": "5,10,20,50,100,200,500,1000,4000",

      for l in range(lenPriceLimits):
         if price <= int(priceLimits[l]):
            self.lg.info("Initial Min Profit pct set to " +  str(pct) + " number of prices " + str(lenPriceLimits))
            self.lg.info("priceLimits "  + str(priceLimits))
            pct *= (lenPriceLimits - l) / self.priceLimitDivider
            self.lg.info("lenPriceLimits " + str(lenPriceLimits) + " ctr " + str(l))
            self.lg.info("self.priceLimitDivider " + str(self.priceLimitDivider))
            self.lg.info("Min Profit = price * (pct * (lenPriceLimits - ctr / priceLimitDivider)) " + str(pct))
            break

      self.targetProfit = round(price * pct, 2)
      
      self.lg.info("Min Profit set to: " +  str(self.targetProfit) + " for price " + str(price))
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTargetLoss(self, price, pct):

      # Increase profit target % for lower priced stocks

      priceLimits = self.priceLimits.split(',')
      lenPriceLimits = len(priceLimits)
      
      # "priceLimits": "5,10,20,50,100,200,500,1000,4000",

      for l in range(lenPriceLimits):
         if price <= int(priceLimits[l]):
            self.lg.info("Initial max loss pct set to " +  str(pct) + " number of prices " + str(lenPriceLimits))
            self.lg.info("priceLimits "  + str(priceLimits))
            pct *= (lenPriceLimits - l) / self.priceLimitDivider
            self.lg.info("lenPriceLimits " + str(lenPriceLimits) + " ctr " + str(l))
            self.lg.info("self.priceLimitDivider " + str(self.priceLimitDivider))
            self.lg.info("Max loss = price * (pct * (lenPriceLimits - ctr / priceLimitDivider)) " + str(pct))
            break

      self.targetLoss = round(price * pct, 2)*-1
      
      self.lg.info("Max Loss set to: " +  str(self.targetLoss) + " for price " + str(price))
   
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
   def getCurrentRunningVol(self):
      
      return self.currentVol
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setDynamic(self, bar):
   
      #if not self.doDynamic:
      #   self.doDynamic = 1
      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setQuickProfitTarget(self, bid, ask, useBars):

      if not self.doQuickProfit:
         return
         
      self.lg.debug("profit pct trigger: " + str(self.quickProfitPctTrigger))

      profitAmt = 0.0
      if self.positionType == self.buy: 
         profitAmt = bid * self.quickProfitPctTrigger
      else:
         profitAmt = ask * self.quickProfitPctTrigger
      
      if useBars > 0:
         profitAmt = self.bc.getAvgBarLen()
         self.lg.debug ("profit amount using avg bar length: " + str(profitAmt))
         
      if self.positionType == self.buy:
         self.profitTarget = ask + profitAmt
      elif self.positionType == self.sell:
         self.profitTarget = bid - profitAmt

      self.lg.debug ("profit value: " + str(self.profitTarget))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCurrentBar(self, bar):

      self.currentBar = bar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setNextBar(self, nextBar):
      
      self.lg.debug ("next bar set to: " + str(nextBar))
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
      delayBars = self.lm.getTradingDelayBars()
      
      if self.doDefault:
         self.algoMsg += "         Default\n"
      if self.doHiLo:
         self.algoMsg += "         HiLo\n"
      if self.doHiLoSeq:
         self.algoMsg += "         HiLo Sequential\n"
      if self.doHiSeq:
         self.algoMsg += "         Hi Sequential\n"
      if self.doLoSeq:
         self.algoMsg += "         Lo Sequential\n"
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
      if self.lm.doRangeTradeBars:
         self.algoMsg += "         In Range\n"
      if self.averageVolumeOpen:
         self.algoMsg += "         Average Volume on open\n"
      if self.averageVolumeClose:
         self.algoMsg += "         Average Volume on close\n"
      if self.volumeLastBarOpen:
         self.algoMsg += "         Volume Last Bar open\n"
      if self.volumeLastBarClose:
         self.algoMsg += "         Volume Last Bar close\n"
      if self.doPriceMovement:
         self.algoMsg += "         Price Movement\n"
      if self.doOpenCloseSeq:
         self.algoMsg += "         Opens closes Sequential\n"
      if self.aggressiveOpen:
         self.algoMsg += "         Aggressive Open\n"
      if self.aggressiveClose:
         self.algoMsg += "         Aggressive Close\n"
      if self.agrBuyHiOpen:
         self.algoMsg += "         Aggressive Buy Hi Open\n"
      if self.agrSellLoOpen:
         self.algoMsg += "         Aggressive Sell Lo Open\n"
      if self.agrBuyHiClose:
         self.algoMsg += "         Aggressive Buy Hi Open\n"
      if self.agrSellLoClose:
         self.algoMsg += "         Aggressive Sell Lo Close\n"
      if self.waitForNextBar:
         self.algoMsg += "         Wait for next bar after close\n"
      if self.doTrailingStop:
         self.algoMsg += "         Trailing stop\n"
      if self.quitMaxProfit:
         self.algoMsg += "         Quit max profit\n"
      if self.quitMaxLoss:
         self.algoMsg += "         Quit max loss\n"
      if self.doSessions:
         self.algoMsg += "         Sessions \n"
      if self.doAllPatterns:
         self.algoMsg += "         All Patterns: Hammers Reversals\n"
      if self.doHammers:
         self.algoMsg += "         Hammers \n"
      if self.doReversals:
         self.algoMsg += "         Reversals \n"
      if self.doOpensSeq:
         self.algoMsg += "         Opens sequentially \n"
      if self.doClosesSeq:
         self.algoMsg += "         Closes sequentially \n"
      if self.doInPosTracking:
         self.algoMsg += "         In position tracking \n"
      if delayBars > 0:
         self.algoMsg += "         " + str(delayBars) + " Delay bars\n"
         
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
#   def getGain(self):
#
#      if self.cn.getCurrentBid(self.stock) > self.openPositionPrice:
#         return 1
#
#      return 0
      
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
   
      self.waitForNextBar = 1
      self.lg.debug("self.waitForNextBar " + str(self.waitForNextBar))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetWaitForNextBar(self):
   
      self.waitForNextBar = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getWaitForNextBar(self):
   
      return self.waitForNextBar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getQuickProfitPctTriggerAmt(self):
   
      return self.quickProfitPctTriggerAmt
      
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
