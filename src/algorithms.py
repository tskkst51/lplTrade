'''
Algorithms module
'''
import io
import sys
import os
from bitarray import bitarray 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm():

   def __init__(self, d, lg, cn, bc, tr, lm, pa, pr, dy, mo, offLine=0, stock=""):
   
      self.d = d
      self.lg = lg
      self.cn = cn
      self.bc = bc
      self.tr = tr
      self.lm = lm
      self.pa = pa
      self.pr = pr
      self.dy = dy
      self.mo = mo
      
      self.offLine = offLine
      self.stock = stock

      # Required standard settings
      self.algorithms = str(d['algorithms'])
            
      self.timeBar = int(d['timeBar'])
      
      # Algorithms
      self.doDefault = int(d['doDefault'])
      self.doHiLo = int(d['doHiLo'])
      self.doHiLoSeq = int(d['doHiLoSeq'])
      self.doHiSeq = int(d['doHiSeq'])
      self.doHiBuyLoSellSeq = int(d['doHiBuyLoSellSeq'])
      self.doLoSeq = int(d['doLoSeq'])
      self.doOpenCloseSeq = int(d['doOpenCloseSeq'])
      self.doOpensSeq = int(d['doOpensSeq'])
      self.doClosesSeq = int(d['doClosesSeq'])
      self.doOpensCloses = int(d['doOpensCloses'])
      self.doExecuteOnClose = int(d['doExecuteOnClose'])
      self.doExecuteOnOpen = int(d['doExecuteOnOpen'])
      self.doHiLoOnClose = int(d['doHiLoOnClose'])
      self.doHiLoOnOpen = int(d['doHiLoOnOpen'])
      self.doQuickReversal = int(d['doQuickReversal'])
      self.doReversalPattern = int(d['doReversalPattern'])
      self.doReverseBuySell = int(d['doReverseBuySell'])
      self.doQuickProfit = int(d['doQuickProfit'])
      self.doTrends = int(d['doTrends'])
      self.doDynamic = int(d['doDynamic'])
      self.doOnlyBuys = int(d['doOnlyBuys'])
      self.doOnlySells = int(d['doOnlySells'])
      self.doOnlyTrends = int(d['doOnlyTrends'])
      self.doSessions = int(d['doSessions'])
      self.doSessionsHiLo = int(d['doSessionsHiLo'])
      self.sessionsHiMax = int(d['sessionsHiMax'])
      self.sessionsLoMax = int(d['sessionsLoMax'])
      self.doTrailingStop = int(d['doTrailingStop'])
      self.doAutoStop = int(d['doAutoStop'])
      self.doVolatility = int(d['doVolatility'])
      self.doInPosTracking = int(d['doInPosTracking'])
      self.doTriggers = int(d['doTriggers'])
      self.doPriceMovement = int(d['doPriceMovement'])
      self.doAllPatterns = int(d['doAllPatterns'])
      self.doHammers = int(d['doHammers'])
      self.doReversals = int(d['doReversals'])
      self.doSessionReversals = int(d['doSessionReversals'])
      self.doDoubleUp = int(d['doDoubleUp'])
      self.doubleUpMax = int(d['doubleUpMax'])
      self.doubleUpLimit = int(d['doubleUpLimit'])
      self.doHiLoHiLoSeqInHiLoOut = int(d['doHiLoHiLoSeqInHiLoOut'])
      self.doHiLoHiLoSeqInHiLoSeqOut = int(d['doHiLoHiLoSeqInHiLoSeqOut'])
      self.doManualOveride = int(d['doManualOveride'])
      self.overideModes = str(d['overideModes'])

      self.averageVolumeOpen = int(d['averageVolumeOpen'])
      self.averageVolumeClose = int(d['averageVolumeClose'])
      self.volumeLastBarOpen = int(d['volumeLastBarOpen'])
      self.volumeLastBarClose = int(d['volumeLastBarClose'])
      
      self.currentLossPct = float(d['currentLossPct'])
      self.profitGainedPct = float(d['profitGainedPct'])
      self.inPosProfitPct = float(d['inPosProfitPct'])
      self.inPosLossPct = float(d['inPosLossPct'])
      
      self.quitMaxProfit = float(d['quitMaxProfit'])
      self.quitMaxLoss = float(d['quitMaxLoss'])
      
      self.aggressiveOpen = int(d['aggressiveOpen'])
      self.aggressiveClose = int(d['aggressiveClose'])
      self.agrBuyHiOpen = int(d['agrBuyHiOpen'])
      self.agrSellLoOpen = int(d['agrSellLoOpen'])
      self.agrBuyHiClose = int(d['agrBuyHiClose'])
      self.agrSellLoClose = int(d['agrSellLoClose'])

      self.currency = str(d['currency'])
      self.alt = str(d['alt'])
      self.marketBeginTime = int(d['marketBeginTime'])
      self.marketEndTime = int(d['marketEndTime'])
      self.preMarket = int(d['preMarket'])
      self.afterMarket = int(d['afterMarket'])
      self.priceChangeMultiplier = int(d['priceChangeMultiplier'])
      self.afterMarketAnalysis = int(d['afterMarketAnalysis'])
      self.afterMarketEndTime = int(d['afterMarketEndTime'])

      # Increase the number of bars used determining close price
      self.increaseCloseBars = int(d['increaseCloseBars'])
      self.increaseCloseBarsMax = int(d['increaseCloseBarsMax'])
      self.gainTrailStop = int(d['gainTrailStop'])
      self.useAvgBarLimits = int(d['useAvgBarLimits'])

      # Additional value to add to close triggers
      self.closePositionFudge = float(d['closePositionFudge'])
            
      #self.algoBitArray = bitarray(6)
      #self.algoBitArray = bitarray.setall[0]
      
      # Wait for next bar before opening a position
      self.waitForNextBar = int(d['waitForNextBar'])

      # Yet to implement.  BELOW HERE HASN"T BEEN IMPLEMENTED yet
      
      self.endTradingTime = float(d['endTradingTime'])
      self.quickProfitPctTriggerAmt = float(d['quickProfitPctTriggerAmt'])
      
      # reverseLogic appears to be best for short term charts and
      # low liquidity
      
      self.buyNearLow = int(d['buyNearLow'])
      self.sellNearHi = int(d['sellNearHi'])
      
      self.quickProfitPctTrigger = float(d['quickProfitPctTrigger'])
      self.quickProfitPctTriggerBar = float(d['quickProfitPctTriggerBar'])
      self.reversalPctTrigger = float(d['reversalPctTrigger'])
      self.volumeRangeBars = int(d['volumeRangeBars'])
      self.inPosProfitPct = float(d['inPosProfitPct'])
      self.incPosGainPct = float(d['incPosGainPct'])
      self.incPosBars = int(d['incPosBars'])
      
      self.executeOnOpenPosition = 0
      self.executeOnClosePosition = 0

      self.hiLowBarMaxCounter = int(d['hiLowBarMaxCounter'])
      self.useSignals = int(d['useSignals'])
      self.priceLimits = str(d['priceLimits'])
      self.priceLimitDivider = float(d['priceLimitDivider'])
      self.triggerValue = float(d['triggerValue'])
      self.maxNumLosses = int(d['maxNumLosses'])
      self.autoPriceTracking = int(d['autoPriceTracking'])
      self.noLargeLosses = int(d['noLargeLosses'])
      
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
      self.stoppedOut = 4
      self.addToPosition = 5
      self.manualClose = 6
      self.manualQuit = 7
      self.overideAction = 0

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
      self.numTrades = 1
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
      
      self.previousBarSegment = self.barSegment = self.nextBarSegment = 0
      self.loReversal = self.hiReversal = 0
      self.totalGainLastPrice = 0.0
      self.totalLossLastPrice = 0.0
      self.exitWProfitVal = 0.0 
      self.inPosGain = 0

      if not self.priceChangeMultiplier:
         self.priceChangeMultiplier = 1
         
      self.numBarsInBullSessionTrend = self.numBarsInBearSessionTrend = 0
      self.lastBarsInBullSessionTrend = self.lastBarsInBearSessionTrend = 0
      
      #self.firstBarVol = 0
      self.waitingForNextBar = 0
      self.triggered = 0
      self.doubledUp = 0
      self.doubleUpOpenPrice = []
      self.currentGain = 0.0
      
      self.wins = 0
      self.losses = 0         
      
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
      self.lg.debug("self.pr.getCurrentBarNum() " + str(self.pr.getCurrentBarNum()))
      
      if bar == 0:
         return
         
      self.lm.setTradingDelayBars()
      self.lm.setMinTradingDelayBars()
    
      if self.doOnlyTrends:
         self.lm.setTradingDelayBarsDoOnlyTrends(self.timeBar)
         self.tr.setTrendLimits(bc, bar, last, last)

      if self.doPriceMovement:
         self.pr.setPriceChangeArr(bar)
      
      # Since we can't know when the last bar is we set the firstBarVol on the
      # last bar which is really the first bar.   
      #self.runningVolume = self.currentVol = self.firstBarVol
      self.runningVolume = self.currentVol = 0
         
      print ("self.lm.getTradingDelayBars() " + str(self.lm.getTradingDelayBars()))
      
#      if bar < self.lm.getTradingDelayBars():
#         return
      
      if bar < self.lm.getMinTradingDelayBars():
         return
      
      self.setNextBar(bar + 1)

      #bar -= 1
            
      self.bc.setAvgBarLen(bc, bar)

      if self.averageVolumeOpen or self.averageVolumeClose:
         self.bc.setAvgVol(bc, bar)
      
      #self.lm.setOpenCloseHiLoValues(bc, bar, self.lm.getMaxNumTradeBars())
      print ("self.stock " + self.stock)
      
      self.lm.setOpenCloseHiLoValues(bc, bar, self.lm.getMaxNumTradeBars())
      
      # Only need hi lo conditions when there are 2 or more bars
      if bar > 1:
         self.lm.setHiLoConditions()
      
      self.lm.setRangeLimits(bc, bar)


      if self.useAvgBarLimits:
         self.lm.setOpenAvgBarLenLimits(last)
         self.lm.setCloseAvgBarLenLimits(last)
      else:
         self.lm.setOpenBuySellLimits()
         if bar >= self.lm.closeBuyBars or bar >= self.lm.closeSellBars:
            self.lm.setCloseBuySellLimits()
      
      self.unsetWaitForNextBar()
      
      self.revDirty = 0
      self.priceMovement = 0
      
      self.nextBarSegment = 0
      self.reversAction = 0
      
      #self.setDynamic(bar)
            
      # Change algo's based on conditions, time slope
      if self.doDynamic:
         algo = self.dy.setOpenCloseBars(last, self.timeBar)
         print ("algoooooo " + str(algo))
         exit (1)

      if self.doTriggers:
         self.triggered = 0
         
      #   self.algorithmDynamic(bar)
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLiveProfileValues(self, d, profilePath):
   
      displayHeader = profilePath
      displayHeader += "\nProfile items: "
         
      #for key, value in d.items():
      for k, v in d.items():
         if k == "currency" or k == "alt":
            continue
         if v >= '1':
            displayHeader += v + " " + k + "\n"
   
      return displayHeader
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takePosition(self, bid, ask, last, vol, bc, bar):

      self.setTotalLiveGain(last)
      liveGainLoss = self.getTotalLiveGain()

      # Never take a large loss
      if self.noLargeLosses:
         if liveGainLoss < self.getTargetLoss():
            self.lg.debug("setting auto loss triggered")
            self.lg.debug("liveGainLoss < TargetLoss: " + str(liveGainLoss) + " " + str(self.getTargetLoss()))
            self.doAutoStop = 1
            
            #return self.stoppedOut
            
#      self.firstBarVol = 0
#      if self.doActionOnCloseBar():
#         self.firstBarVol = vol
      
      if bar == 0:
         return 0
         
      if bar < self.lm.getMinTradingDelayBars():
         return 0

      # Trading has been halted. Ignore any trading
      if bid == 0.0 or ask == 0.0 or last == 0.0:
         self.lg.debug("Trading has been halted no bids/asks: ")
         return 0

      # If in a position make sure close values are set
      if self.inPosition():
         if self.positionType == self.buy:
            if self.lm.closeBuyLimit == 0 or self.lm.closeBuyLimit == 0.0:
               return 0
         if self.positionType == self.sell:
            if self.lm.closeSellLimit == 0 or self.lm.closeSellLimit == 0.0:
               return 0

      # Determine if position should be opened/closed
      action = self.takeAction(bc, bar, bid, ask, last, vol)

      self.algorithmCalculateRunningVolume(vol)

      self.lg.debug("takeAction action: " + str(action))

      if action == self.stoppedOut:
         return self.stoppedOut
      
      if action == 0:
         return 0
      
      # Open position 
      if not self.inPosition():
         if action == self.buy:
            if self.doReverseBuySell: 
               self.lg.debug("reversing the buy -> sell. Using avgBarLen: " + str(action))
               self.useAvgBarLen += 1
               self.useAvgBarLimits += 1
               self.lm.setAvgBarLenLimits(bc, bar, last)

               self.openPosition(self.sell, bar, bc, bid, ask)               
            else: 
               self.openPosition(self.buy, bar, bc, bid, ask)
               
         elif action == self.sell:               
            if self.doReverseBuySell:
               self.lg.debug("reversing the sell -> buy Using avgBarLen: " + str(action))
               self.useAvgBarLen += 1
               self.useAvgBarLimits += 1
               self.lm.setAvgBarLenLimits(bc, bar, last)

               self.openPosition(self.buy, bar, bc, bid, ask)
            else: 
               self.openPosition(self.sell, bar, bc, bid, ask)

      # Close position or double up
      elif self.inPosition():
#         if action == self.addToPosition and self.doDoubleUp and self.doubledUp and self.doubledUp < self.doubleUpMax:               
         if action == self.addToPosition:               
            self.lg.debug("self.doubledUp: " + str(self.doubledUp))
            self.lg.debug("self.doubleUpMax: " + str(self.doubleUpMax))
            if self.positionType == self.buy:
               self.openPosition(self.buy, bar, bc, bid, ask)
            elif self.positionType == self.sell:
               self.openPosition(self.sell, bar, bc, bid, ask)
            #self.doubledUp += 1
            self.lg.debug ("doubleUp:doubleUp: " + str(self.doubledUp))

         #elif self.positionType == self.buy and action == self.buy:
         elif action == self.buy:
            self.closePosition(bar, bc, bid, ask, 0)
            if self.doQuickReversal and not self.isPriceInRange(bid, ask):
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.sell, bar, bc, bid, ask)
            
         #elif self.positionType == self.sell and action == self.sell:
         elif action == self.sell:
            self.closePosition(bar, bc, bid, ask, 0)
            if self.doQuickReversal and not self.isPriceInRange(bid, ask):
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.buy, bar, bc, bid, ask)

         # Forse a close. Manual Overide close was set
         elif action == self.manualClose:
            self.closePosition(bar, bc, bid, ask, 1)
            if self.doQuickReversal and not self.isPriceInRange(bid, ask):
               self.lg.debug("Quick reversal being used: " + str(action))
               self.openPosition(self.buy, bar, bc, bid, ask)

         # Forse a close. Manual Overide close was set
         elif action == self.manualQuit:
            self.closePosition(bar, bc, bid, ask, 1)

      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takeAction(self, bc, bar, bid, ask, last, vol):
   
      action = 0
      exitAlgo = 3

      actionOnOpen = self.doActionOnOpenBar()
      actionOnClose = self.doActionOnCloseBar()

      if self.doInPosTracking:
         action = self.algorithmPriceTracking(bid, ask, last, action)
         
         if action == self.stoppedOut:
            # We close position do to positive position turning negative
            self.closePosition(bar, bc, bid, ask, 1)
            return self.stoppedOut
            #return 0

      if self.doDoubleUp and self.inPosition():
         action = self.algorithmIncreasePosition(last, action)
         if action == self.addToPosition:
            return self.addToPosition

      if self.doDynamic:
         self.algorithmDynamic(bid, ask, last, action)
     
      if self.doVolatility:
         self.algorithmVolatility(action)
     
      if self.doQuickProfit:
         if self.algorithmQuickProfit(bc, bar, bid, ask, action) == exitAlgo:
            # We took profit exit algo's
            return 0
      
      if self.doExecuteOnOpen:
         action = self.algorithmOnOpen(bar, action)

      if self.doExecuteOnClose:
         action = self.algorithmOnClose(bar, action)

      if self.doHiLoHiLoSeqInHiLoOut:
         self.algorithmdoHL_HLSeqIN_HLOUT()
              
      if self.doHiLoHiLoSeqInHiLoSeqOut:
         self.algorithmdoHL_HLSeqIN_HLSeqOUT()

      if self.doHiLoSeq:
         action = self.algorithmHiLoSeq(bc, bar, bid, ask, last, vol, action)
      
      if self.doHiSeq:
         action = self.algorithmHiSeq(bc, bar, bid, ask, last, vol, action)
      
      if self.doHiBuyLoSellSeq:
         action = self.algorithmHiBuyLoSellSeq(bc, bar, bid, ask, last, vol, action)

      if self.doLoSeq:
         action = self.algorithmLoSeq(bc, bar, bid, ask, last, vol, action)
      
      if self.doOpenCloseSeq:
         action = self.algorithmOpensClosesSeq(bc, bar, bid, ask, last, vol, action)
         
      if self.doOpensSeq:
         action = self.algorithmOpensSeq(bc, bar, bid, ask, last, vol, action)
         
      if self.doClosesSeq:
         action = self.algorithmClosesSeq(bc, bar, bid, ask, last, vol, action)
         
      if self.doOpensCloses:
         action = self.algorithmOpensCloses(bc, bar, bid, ask, last, vol, action)
         
      if self.doSessions:
         action = self.algorithmSessions(bc, bar, bid, ask, last, vol, action)
         
      if self.doSessionsHiLo:
         action = self.algorithmSessionsHiLo(bc, bar, bid, ask, last, vol, actionOnClose, action)
         
      print (" self.doHiLo " + str(self.doHiLo))
      
      if self.doHiLo:
         action = self.algorithmHiLo(bc, bar, bid, ask, last, vol, action)
         
      if self.doReversalPattern:
         action = self.algorithmReversalPattern(bc, bar, ask, action)
      
      if self.doOnlyTrends:
         action = self.algorithmDoOnlyTrends(bc, bar, bid, ask, action)
         
      if self.lm.doRangeTradeBars:
         action = self.algorithmDoInRange(bc, bar, bid, ask, action)
         
      if self.doDefault:
         action = self.algorithmDefault(bc, bar, bid, ask, action)

      if self.doReverseBuySell:
         action = self.algorithmReverseBuySell(action)
         
      if self.doPriceMovement:
         # Don't get caught opening a position on a skewed price
         action = self.algorithmPriceMovement(bar, bid, ask, last, action)
         
         #if self.algorithmPriceMovement(bar, bid, ask, last, action) == exitAlgo:
            
      if self.doSessionReversals:
         action = self.algorithmSessionReversalsBar(bc, bar, bid, ask, actionOnOpen, actionOnClose, action)

      if self.doAllPatterns or self.doHammers or self.doReversals:
         action = self.algorithmPatterns(bc, bar, bid, ask, actionOnOpen, actionOnClose, action)

      if self.averageVolumeOpen or self.averageVolumeClose:
         action = self.algorithmAverageVolume(action)

      if self.volumeLastBarOpen or self.volumeLastBarClose:
         action = self.algorithmVolumeLastBar(bc, bar, action)

      self.lg.debug ("before doAutoStop action: " + str(action))
      
      if self.doAutoStop:
         self.algorithmAutoStop(last)
         self.lg.debug ("after doAutoStop action: " + str(action))
      
      if self.doTrailingStop:
         action = self.algorithmTrailingStop(last, action)
         
         if action == self.stoppedOut:
            self.closePosition(bar, bc, bid, ask, 1)
            if self.waitForNextBarAlgos():
               self.setWaitForNextBar()
               self.lg.debug ("STOPPED OUT a")
            return self.stoppedOut
      
      if self.doManualOveride:
         action = self.algorithmManualOveride(bar, bc, bid, ask, action)

      if action > 0:
         if self.doTriggers and not self.triggered:
            action = self.algorithmTriggers(action)
            print ("Action being taken!! Triggered " + str(action))
         else:
            print ("Action being taken!! " + str(action))
     
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmManualOveride(self, bar, bc, bid, ask, action):
      
      ## Algo to monitor over ride file and do as it's told
      
      # Read from overide file
      
      self.lg.debug ("In algorithmManualOveride: " + str(action))

      overideValue = self.mo.getOverideValue()
      self.lg.debug ("overideValue " + str(overideValue))
      
      #if len(overideValue) == 0:
      #   return action
         
      
      self.overideAction = self.mo.getOverideAction(overideValue, self.inPosition())

      if self.overideAction:
         self.lg.debug ("overideAction SET: " + str(self.overideAction))
         if self.overideAction == self.addToPosition:
            self.doDoubleUp = 1
         return self.overideAction
         
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmIncreasePosition(self, last, action):
      
      ## Increase position when in a favorable position
      
      self.lg.debug ("In algorithmIncreasePosition: " + str(action))

      self.lg.debug ("getPositionType(): " + str(self.getPositionType()))
      self.lg.debug ("openPositionPrice " + str(self.openPositionPrice))

      currentGain = self.getCurrentGain(last)
      
      self.lg.debug ("getBarsInPosition(): " + str(self.bc.getBarsInPosition()))
      self.lg.debug ("incPosBars: " + str(self.incPosBars))
      self.lg.debug ("incPosGainPct: " + str(self.incPosGainPct))
      self.lg.debug ("getCurrentGain: " + str(currentGain))
      self.lg.debug ("last: " + str(last))

      if self.getPositionType() == self.buy:
         if currentGain < 0 and self.doubledUp < self.doubleUpMax:
            if abs(currentGain) > float(self.incPosGainPct * last):
               self.lg.debug ("Adding to BUY position ")
               self.lg.debug ("CurrentGain is > : " + str(currentGain))
               self.lg.debug ("incPosGainPct * last: " + str(self.incPosGainPct * last))
               self.resetOpenPrice(last)
               #self.doubledUp += 1
               self.lg.debug ("doubledUp CTR : " + str(self.doubledUp))
               return self.addToPosition
               
      elif self.getPositionType() == self.sell:
         if currentGain > 0 and self.doubledUp < self.doubleUpMax:
            if currentGain > float(self.incPosGainPct * last):
               self.lg.debug ("Adding to SELL position ")
               self.lg.debug ("CurrentGain is > : " + str(currentGain))
               self.lg.debug ("incPosGainPct * last: " + str(self.incPosGainPct * last))
               self.resetOpenPrice(last)
               #self.doubledUp += 1
               return self.addToPosition

      # Set limits based on double up values
      if self.doubleUpLimit and self.doubledUp >= self.doubleUpLimit:
         self.lg.debug ("Setting setLimitOnDoubleUpValue ")
         self.lg.debug ("doubleUpLimit " + str(self.doubleUpLimit))
         self.lg.debug ("doubledUp >= doubleUpLimit ")
         self.lg.debug (str(self.doubledUp) + " >= " + str(self.doubleUpLimit))

         self.lm.setLimitOnDoubleUpValue(self.doubleUpOpenPrice[self.doubledUp - self.doubleUpLimit], self.getPositionType()) 
      
         if self.getPositionType() == self.buy:
            if last < self.lm.closeBuyLimit:
               self.lg.debug ("last < closeBuyLimit returning 2")
               return 2
         elif self.getPositionType() == self.sell:
            if last > self.lm.closeSellLimit:
               self.lg.debug ("last > closeBuyLimit returning 1")
               return 1
               
      if self.doubleUpLimit and self.doubledUp >= self.doubleUpMax:
         # Set trailing stop to maximize profit
         self.lg.debug ("Setting Trailing stop ")
         self.lg.debug ("doubledUp > doubleUpMax")
         self.lg.debug ("  doubleUpLimit " + str(self.doubleUpLimit))
         self.lg.debug ("  doubledUp " + str(self.doubledUp))
         self.lg.debug ("  doubleUpMax " + str(self.doubleUpMax))
         self.doTrailingStop += 1
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmTriggers(self, action=0):

      self.lg.debug ("In algorithmTriggers: " + str(action))

      # Used on opening and closing a position. Set limit lower or higher to 
      # try and get a better price
      
      if self.inPosition():
         return action
         
      self.triggered = action
      
      # Set action to 0 so position is held until new limit is breached
      #action = 0
      
      # Set new open limit. avg bar len / 2
      triggeredLimit = self.bc.getAvgBarLen() * self.triggerValue
      self.lg.debug ("triggeredLimit: " + str(triggeredLimit))

      if self.inPosition():
         if action == self.buy:
            self.lm.closeSellLimit -= triggeredLimit
            self.lg.debug ("new triggered close sell limit: " + str(self.lm.closeSellLimit))
         elif action == self.sell:
            self.lm.closeBuyLimit += triggeredLimit
            self.lg.debug ("new triggered close buy limit: " + str(self.lm.closeBuyLimit))
      else:
         if action == self.buy:
            self.lm.openBuyLimit -= triggeredLimit
            self.lg.debug ("new triggered open buy limit: " + str(self.lm.openBuyLimit))
         elif action == self.sell:
            self.lm.openSellLimit += triggeredLimit
            self.lg.debug ("new triggered open sell limit: " + str(self.lm.openSellLimit))
         
      return 0
      
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
      
      self.lg.debug ("self.pr.getCurrentBarNum(): " + str(self.pr.getCurrentBarNum()))
      self.lg.debug ("self.timeBar: " + str(self.timeBar))
      self.lg.debug ("barSegment: " + str(barSegment))
      self.lg.debug ("self.nextBarSegment: " + str(self.nextBarSegment))
      
      if self.timeBar > 1:
         if self.doActionOnCloseBar():
            pass
            
         elif barSegment == 0:               
            self.runningVolume = self.currentVol = vol
            self.nextBarSegment = 1
         else:
            if barSegment == self.nextBarSegment:
               self.runningVolume = self.currentVol
               #self.currentVol = 0
               self.nextBarSegment += 1
            else:   
               self.currentVol = vol + self.runningVolume
      else:
         self.currentVol = vol
               
      self.lg.debug ("self.runningVolume: " + str(self.runningVolume))
      self.lg.debug ("vol:                " + str(vol))
      self.lg.debug ("self.currentVol:    " + str(self.currentVol))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmVolumeLastBar(self, bc, bar, action=0):
         
      self.lg.debug ("In algorithmAverageLastBar: " + str(action))

      # Use last bar volume to verify signal

      # If no signal then return
      if not action:
         return action

      # Only check volume of last bar when opening a position
      if self.volumeLastBarOpen:
         if self.inPosition() and not self.volumeLastBarClose:
            return action
         
      # Only check volume of last bar when closing a position
      if self.volumeLastBarClose:
         if not self.inPosition() and not self.volumeLastBarOpen:
            return action
      
      # Using average volume last bar to get out of a position
      #if not self.inPosition():
      #   return action

      # using average volume last bar to get into a position
      #if self.inPosition():
      #   return action

      previousBarVol = int(bc[bar - 1][self.vl])
      
      self.lg.debug ("bar: " + str(bar))
      self.lg.debug ("barChart[bar - 1]: " + str(bc[bar - 1]))
      self.lg.debug ("barChart[bar - 2]: " + str(bc[bar - 2]))
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
      elif self.doDoubleUp and self.doubleUpLimit and self.doubledUp >= self.doubleUpLimit:
         self.lg.debug ("Ignoring currentVol being > last bar")
         self.lg.debug ("doDoubleUp is set. doubledUp >= doubleUpLimit")
         self.lg.debug (str(self.doubledUp) + " >= " + str(self.doubleUpLimit))
         return action

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmAverageVolume(self, action=0):
         
      self.lg.debug ("In algorithmAverageVolume: " + str(action))

      # Use average volume to verify signal
      # Ignore this algo if double up limit is set
      
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
      
      # Volume is 0 in the open of a bar so skip...
#      if self.doActionOnOpenBar():
#         return action
         
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
      elif self.doDoubleUp and self.doubleUpLimit and self.doubledUp >= self.doubleUpLimit:
         self.lg.debug ("Ignoring currentVol being > average volume")
         self.lg.debug ("doDoubleUp is set. doubledUp >= doubleUpLimit")
         self.lg.debug (str(self.doubledUp) + " >= " + str(self.doubleUpLimit))
         return action
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmReversalPattern(self, bc, bar, ask, action=0):
         
      self.lg.debug ("In algorithmReversalPattern: " + str(action))

      # Detect a reversal pattern in the current bar. triggerring when
      # current bar is > than previous bar
   
      if self.inPosition() and self.doReversalPattern():
         previousBarLen = float(bc[i-1][cl] - bc[i-1][op])
         #currentBarLen = bc[i][op] - self.cn.getCurrentAsk(self.stock)
         currentBarLen = bc[i][op] - ask
         
         if previousBarLen < 0.0 and currentBarLen > 0.0:
            # Bars going different directions
            return 1
         
         # Get rid of negative length bars
         if previousBarLen < 0.0:
            previousBarLen = previousBarLen * -1
         if currentBarLen < 0.0:
            currentBarLen = currentBarLen * -1
            
         currentOpen = bc[i][op]

         currentHi = 0.0
         if action == self.buy:
            currentHi = bc[i][hi]
         else:
            currentHi = bc[i][lo]
            
         self.lg.debug("barLengths; current: " + str(currentBarLen) + " prev: " + str(previousBarLen))
         
         # Add an additional percentage to currentBarLen for larger moves
         if currentBarLen > previousBarLen: 
            if self.getReversalLimit(currentHi, currentOpen):
               self.lg.debug("triggered due to reversal detected!")
               self.closePosition(bar, bc, bid, ask, 1)

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
   def algorithmQuickProfit(self, bc, bar, bid, ask, action=0):
   
      if not self.inPosition():         
         return action

      self.lg.debug ("In algorithmQuickProfit: " + str(action))
      
      # We've taken at least one profit so set the avg bar length
      #if self.quickProfitCtr:
         # Use avg bar length as the stop instead of original limits
      #   self.lm.setAvgBarLenLimits(bc, bar)
      #else:
      #   self.avgBarLenCtr = bar + 1      
      
      profitTarget = self.getProfitTarget()
      self.lg.debug ("Target profit set to: " + str(profitTarget))
      
      if self.getPositionType() == self.buy:
         if ask > profitTarget and ask != 0.0:
            self.lg.debug ( "CLOSING BUY POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(ask) + " > " + str(profitTarget))
            self.closePosition(bar, bc, bid, ask, 1)
            if self.waitForNextBar:
               self.setWaitForNextBar()
            return 3
            
      elif self.getPositionType() == self.sell:
         if bid < profitTarget and bid != 0.0:
            self.lg.debug ( "CLOSING SELL POSITION QUICK PROFIT TAKEN.")
            self.lg.debug (str(bid) + " < " + str(profitTarget))
            self.closePosition(bar, bc, bid, ask, 1)
            if self.waitForNextBar:
               self.setWaitForNextBar()
            return 3
                 
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoInRange(self, bc, bar, bid, ask, action=0):
   
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
         
         #self.lm.setAvgBarLenLimits(bc, bar)
         #self.x()
         
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoOnlyTrends(self, bc, bar, bid, ask, action=0):
   
      self.lg.debug("In algorithmDoOnlyTrends: " + str(action))

      # We set the trend limits here since the calculation is dynamic and values
      # change as the price moves
      # This algo takes much CPU time and may need rethinking
      # 23/1/8 delaying until after 30 minutes
      
      # 23/1/9 moved to setAllLimits
      #self.tr.setTrendLimits(bc, bar, bid, ask)
            
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
   # Take position if price is higher than high or lower than the low.
   # Bars have to be sequentially higher/lower on the open.
   # Close when bars are sequential opposite the open.
   
   def algorithmdoHL_HLSeqIN_HLSeqOUT(self):

      self.lg.debug("In algorithmdoHL_HLSeqIN_HLSeqOUT")

      if self.inPosition():
         self.doHiLoSeq = 1
         self.doHiLo = 0
      else:
         self.doHiLoSeq = 1
         self.doHiLo = 1
         
      self.lg.debug("doHiLoSeq " + str(self.doHiLoSeq))
      self.lg.debug("doHiLo " + str(self.doHiLo))
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high or lower than the low.
   # Bars have to be sequentially higher/lower on the open.
   # Close when price breaches hi or lo.
   
   def algorithmdoHL_HLSeqIN_HLOUT(self):

      self.lg.debug("In algorithmdoHL_HLSeqIN_HLOUT")

      if self.inPosition():
         self.doHiLoSeq = 0
         self.doHiLo = 1
      else:
         self.doHiLoSeq = 1
         self.doHiLo = 1
         
      self.lg.debug("doHiLoSeq " + str(self.doHiLoSeq))
      self.lg.debug("doHiLo " + str(self.doHiLo))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high or lower than the low Sequentially
   
   def algorithmHiLoSeq(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmHiLoSeq " + str(action))
         
      if self.inPosition():
         if self.doDoubleUp and self.doubleUpLimit and self.doubledUp > 1:

            # New limit should already be set by increasePosition() 
            if self.positionType == self.buy:
               if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
                  #self.setWaitForNextBar()
                  return self.sell
            if self.positionType == self.sell:
               if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
                  #self.setWaitForNextBar()
                  return self.buy
                  
         if self.positionType == self.buy:
            if self.lm.lowerHighsBuyClose and self.lm.lowerLowsBuyClose:
               self.lg.debug ("InPos Hi Lo Seq algo. lower hi's and lower lo's detected")
               return self.sell
         elif self.positionType == self.sell:
            if self.lm.higherHighsSellClose and self.lm.higherLowsSellClose:
               self.lg.debug ("InPos Hi Lo Seq algo. higher hi's and higher lo's detected")
               return self.buy
      else:
         if self.lm.higherHighsBuyOpen and self.lm.higherLowsBuyOpen:
            self.lg.debug ("Hi Lo Seq algo. Higher hi's and Higher lo's detected")
            return self.buy
         if self.lm.lowerHighsSellOpen and self.lm.lowerLowsSellOpen:
            self.lg.debug ("Hi Lo Seq algo. Lower hi's and Lower lo's detected")
            return self.sell

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high on a buy
   # Take position if price is lower than low on a sell
   
   def algorithmHiBuyLoSellSeq(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmHiBuyLoSellSeq " + str(action))
         
      if self.inPosition():
         if self.doDoubleUp and self.doubleUpLimit and self.doubledUp > 1:
            # New limit should already be set by increasePosition() 
            if self.positionType == self.buy:
               if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
                  #self.setWaitForNextBar()
                  return self.sell
            if self.positionType == self.sell:
               if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
                  #self.setWaitForNextBar()
                  return self.buy
         if self.positionType == self.buy:
            if self.lm.lowerLowsBuyClose:
               self.lg.debug ("InPos HiBuyLoSell. lower lo's detected")
               return self.sell
         elif self.positionType == self.sell:
            if self.lm.higherHighsSellClose:
               self.lg.debug ("InPos HiBuyLoSell. higher hi's detected")
               return self.buy
      else:
         if self.lm.higherHighsBuyOpen:
            self.lg.debug ("HiBuyLoSell algo. Higher hi's detected")
            return self.buy
         if self.lm.lowerLowsSellOpen:
            self.lg.debug ("HiBuyLoSell algo. Lower lo's detected")
            return self.sell

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high 
   # This works best when in bear trend
   
   def algorithmHiSeq(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmHiSeq " + str(action))
         
      if self.inPosition():
         if self.doDoubleUp and self.doubleUpLimit and self.doubledUp > 1:
            # New limit should already be set by increasePosition() 
            if self.positionType == self.buy:
               if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
                  #self.setWaitForNextBar()
                  return self.sell
            if self.positionType == self.sell:
               if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
                  #self.setWaitForNextBar()
                  return self.buy
         if self.positionType == self.buy:
            if self.lm.lowerHighsBuyClose:
               self.lg.debug ("InPos Hi Seq algo. lower hi's detected")
               return self.sell
         elif self.positionType == self.sell:
            if self.lm.higherHighsSellClose:
               self.lg.debug ("InPos Hi Seq algo. higher hi's detected")
               return self.buy
      else:
         if self.lm.higherHighsBuyOpen:
            self.lg.debug ("Hi Seq algo. Higher hi's detected")
            return self.buy
         if self.lm.lowerHighsSellOpen:
            self.lg.debug ("Hi Seq algo. Lower hi's  detected")
            return self.sell

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is lower than the low
   # This works best when in bull trend

   def algorithmLoSeq(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmLoSeq " + str(action))
         
      if self.inPosition():
         if self.doDoubleUp and self.doubleUpLimit and self.doubledUp > 1:
            # New limit should already be set by increasePosition() 
            if self.positionType == self.buy:
               if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
                  #self.setWaitForNextBar()
                  return self.sell
            if self.positionType == self.sell:
               if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
                  #self.setWaitForNextBar()
                  return self.buy
         if self.positionType == self.buy:
            if self.lm.lowerLowsBuyClose:
               self.lg.debug ("InPos Lo Seq algo. lower lo's detected")
               return self.sell
         elif self.positionType == self.sell:
            if self.lm.higherLowsSellClose:
               self.lg.debug ("InPos Lo Seq algo. higher lo's detected")
               return self.buy
      else:
         if self.lm.higherLowsBuyOpen:
            self.lg.debug ("Lo Seq algo. Higher lo's detected")
            return self.buy
         if self.lm.lowerLowsSellOpen:
            self.lg.debug ("Lo Seq algo. Lower lo's detected")
            return self.sell

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if price is higher than high or lower than the low

   def algorithmHiLo(self, bc, bar, bid, ask, last, vol, action=0):

      self.lg.debug("In algorithmHiLo " + str(action) + " triggered " + str(self.triggered))
      
      retCode = 0
      
      # if triggered the price limits have moved up for a sell and doen for a buy
      # reverse open/close logic

      if self.triggered:
         if not self.inPosition():
            self.lg.debug ("triggered SELL. limit: " + str(self.lm.openSellLimit) + " last "  + str(last))
            self.lg.debug ("triggered BUY. limit: " + str(self.lm.openBuyLimit) + " last "  + str(last))
            if self.triggered == self.buy:
               if last < self.lm.openBuyLimit and self.lm.openBuyLimit != 0:
                  self.lg.debug ("triggered Opening algorithmHiLo BUY. limit: " + str(self.lm.openBuyLimit) + " last "  + str(last))
                  retCode = 1
            elif self.triggered == self.sell:
               if last > self.lm.openSellLimit and self.lm.openSellLimit != 0:
                  self.lg.debug ("triggered Opening algorithmHiLo SELL. limit: " + str(self.lm.openSellLimit) + " last "  + str(last))
                  retCode = 2
         
      elif self.inPosition():
         if self.positionType == self.buy:
            self.lg.debug ("Hi Lo: in buy position " + str(self.positionType))
            self.lg.debug ("closeBuyLimit " + str(self.lm.closeBuyLimit))
            if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
               self.lg.debug ("Closing algorithmHiLo BUY. closeBuyLimit breached " + str(last))
               retCode = 2
         if self.positionType == self.sell:
            self.lg.debug ("Hi Lo: in sell position " + str(self.positionType))
            self.lg.debug ("closeSellLimit " + str(self.lm.closeSellLimit))
            if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
               self.lg.debug ("Closing algorithmHiLo SELL. closeSellLimit breached " + str(last))
               retCode = self.buy

      # Here a seq algo was triggered. Set retCode if hiLo triggered
      elif self.doHiLoSeq or self.doHiSeq or self.doLoSeq or self.doOpenCloseSeq or self.doHiBuyLoSellSeq or self.doOpensSeq or self.doClosesSeq or self.doLoSeq:
         if action == self.buy:
            if last > self.lm.openBuyLimit and self.lm.openBuyLimit != 0:
               self.lg.debug ("Setting algorithmHiLo BUY. limit: " + str(self.lm.openBuyLimit) + " last "  + str(last))
               retCode = self.buy
         if action == self.sell:
            if last < self.lm.openSellLimit and self.lm.openSellLimit != 0:
               self.lg.debug ("Setting algorithmHiLo SELL. limit: " + str(self.lm.openSellLimit) + " last "  + str(last))
               retCode = self.sell

      # No seq algo is in play. return buy or sell
      else:
         if last > self.lm.openBuyLimit and self.lm.openBuyLimit != 0:
            self.lg.debug ("Opening algorithmHiLo BUY. limit: " + str(self.lm.openBuyLimit) + " last "  + str(last))
            return self.buy
         if last < self.lm.openSellLimit and self.lm.openSellLimit != 0:
            self.lg.debug ("Opening algorithmHiLo SELL. limit: " + str(self.lm.openSellLimit) + " last "  + str(last))
            return self.sell

      self.lg.debug("self.doHiLoSeq " + str(self.doHiLoSeq))
      self.lg.debug("self.doOpenCloseSeq " + str(self.doOpenCloseSeq))
      self.lg.debug("action " + str(action))
      self.lg.debug("retCode " + str(retCode))

      if self.doHiLoSeq or self.doHiSeq or self.doLoSeq or self.doOpenCloseSeq or self.doHiBuyLoSellSeq or self.doOpensSeq or self.doClosesSeq or self.doLoSeq:
         if action > 0 and retCode == 0:
            self.lg.debug ("doHiLoSeq set. doHiLo NOT set")
            # Cancel signal if action not set here or above
            return 0
            
         if action == 0 and retCode > 0:
            self.lg.debug ("doHiLoSeq NOT set. doHiLo set")
            # Cancel signal if action not set here 
            return 0
         
         if action > 0 and retCode > 0:
            self.lg.debug ("doHiLoSeq set and doHiLo set")
            self.lg.debug ("TAKING POSITION...")
      
      return retCode

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Monitor session data
   
   def algorithmSessions(self, bc, bar, bid, ask, last, vol, action=0):
   
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
   
   def algorithmOpensCloses(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmOpensCloses " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.positionType == self.buy:
            self.lg.debug ("algorithmOpensCloses: in buy position " + str(self.positionType))
            self.lg.debug ("closeBuyLimit " + str(self.lm.closeBuyLimit))
            if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
               self.lg.debug ("Closing algorithmOpensCloses BUY " + str(last))
               self.setWaitForNextBar()
               retCode = 2
               
         if self.positionType == self.sell:
            self.lg.debug ("algorithmOpensCloses: in sell position " + str(self.positionType))
            self.lg.debug ("closeSellLimit " + str(self.lm.closeSellLimit))
            if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
               self.lg.debug ("Closing algorithmOpensCloses SELL " + str(last))
               self.setWaitForNextBar()
               retCode = 1
               
      elif not self.inPosition():
         if last > self.lm.openBuyLimit and self.lm.openBuyLimit != 0:
            self.lg.debug ("Opening algorithmOpensCloses BUY. limit: " + str(self.lm.openBuyLimit))
            retCode = 1
         if last < self.lm.openSellLimit and self.lm.openSellLimit != 0:
            self.lg.debug ("Opening algorithmOpensCloses SELL. limit: " + str(self.lm.openSellLimit))
            retCode = 2
         
      self.lg.debug ("action " + str(action))
         
      return retCode      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Take position if previous bars opens and closes are seq higher or lower
   
   def algorithmOpensClosesSeq(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmOpensClosesSeq " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         self.lg.debug("self.positionType " + str(self.positionType))
         if self.doDoubleUp and self.doubleUpLimit and self.doubledUp > 1:
            # New limit should already be set by increasePosition() 
            if self.positionType == self.buy:
               if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
                  #self.setWaitForNextBar()
                  return self.sell
            if self.positionType == self.sell:
               if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
                  #self.setWaitForNextBar()
                  return self.buy
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

      self.lg.debug ("doHiLoSeq flag: " + str(self.doHiLoSeq))
      self.lg.debug ("action " + str(action))
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if previous bars closes are sequentially higher or lower
   
   def algorithmClosesSeq(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmClosesSeq " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.doDoubleUp and self.doubleUpLimit and self.doubledUp > 1:
            # New limit should already be set by increasePosition() 
            if self.positionType == self.buy:
               if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
                  #self.setWaitForNextBar()
                  self.lg.debug ("last < closeBuyLimit returning 2")
                  return self.sell
            if self.positionType == self.sell:
               if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
                  #self.setWaitForNextBar()
                  self.lg.debug ("last > closeBuyLimit returning 1")
                  return self.buy
         if self.positionType == self.buy:
            if self.lm.lowerClosesBuyClose:
               self.lg.debug ("algorithmClosesSeq: Closing Lower closes detected")
               return 2
         elif self.positionType == self.sell:
            if self.lm.higherClosesSellClose:
               self.lg.debug ("algorithmClosesSeq: Closing Higher closes detected")
               return 1
      else:
         if self.lm.higherClosesBuyOpen:
            self.lg.debug ("algorithmClosesSeq: Higher closes detected")
            return 1
         if self.lm.lowerClosesSellOpen:
            self.lg.debug ("algorithmClosesSeq: Lower closes detected")
            return 2

      self.lg.debug ("self.doClosesSeq " + str(self.doClosesSeq))
      self.lg.debug ("action " + str(action))
      
      return 0      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Take position if previous bars opens and closes are sequentially higher or lower
   
   def algorithmOpensSeq(self, bc, bar, bid, ask, last, vol, action=0):
   
      self.lg.debug("In algorithmOpensSeq " + str(action))
      
      retCode = 0
      
      if self.inPosition():
         if self.doDoubleUp and self.doubleUpLimit and self.doubledUp > 1:

            # New limit should already be set by increasePosition() 
            if self.positionType == self.buy:
               if last < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
                  #self.setWaitForNextBar()
                  return self.sell
            if self.positionType == self.sell:
               if last > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
                  #self.setWaitForNextBar()
                  return self.buy
         if self.positionType == self.buy:
            if self.lm.lowerOpensBuyClose:
               self.lg.debug ("algorithmOpensSeq: Closing Lower opens detected")
               return 2
         elif self.positionType == self.sell:
            if self.lm.higherOpensSellClose:
               self.lg.debug ("algorithmOpensSeq: Closing Higher opens detected")
               return 1
      else:
         if self.lm.higherOpensBuyOpen:
            self.lg.debug ("algorithmOpensSeq: Higher opens detected")
            return 1
         if self.lm.lowerOpensSellOpen:
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
   def algorithmDefault(self, bc, bar, bid, ask, action=0):
      
      # Ues the right flag here or continue to use this algo as the default
   
      self.lg.debug("In algorithmDefault " + str(action))

      if self.inPosition():
         print ("close buy limit " + str(self.lm.closeBuyLimit))
         print ("close sell limit " +  str(self.lm.closeSellLimit))
         if ask < self.lm.closeBuyLimit and self.lm.closeBuyLimit != 0:
         #if self.cn.getCurrentAsk(self.stock) < self.lm.closeBuyLimit:
            return 1
         if bid > self.lm.closeSellLimit and self.lm.closeSellLimit != 0:
         #if self.cn.getCurrentBid(self.stock) > self.lm.closeSellLimit:
            return 2
      else:
         if ask >= self.lm.openBuyLimit and self.lm.openBuyLimit != 0:
         #if self.cn.getCurrentAsk(self.stock) >= self.lm.openBuyLimit and self.lm.openBuyLimit != 0.0:
            print ( "open buy limit set " + str(self.openBuyLimit))
            return 1
         if bid <= self.lm.openSellLimit and self.lm.openSellLimit != 0:
         #if self.cn.getCurrentBid(self.stock) <= self.lm.openSellLimit and self.lm.openSellLimit != 0.0:
            print ("open sell limit set " +  str(self.lm.openSellLimit))
            return 2
      
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPatterns(self, bc, bar, bid, ask, actionOnOpen, actionOnClose, action=0):
   
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

      self.lg.debug ("algorithmReversals bar -2: -1: current")
      self.lg.debug (str(bc[bar - 2]))
      self.lg.debug (str(bc[bar - 1]))
      self.lg.debug (str(bc[bar]))
         
      if self.inPosition():
         #if self.loReversal:
         if self.positionType == self.sell:
            self.lg.debug("self.loReversal " + str(self.loReversal))
            #if self.pa.isHiReversalO(bc, bar):
            if self.pa.isHiReversalO(bc, bar) and not self.pa.isEngulfing(bc, bar):
            #if self.pa.isHiReversalSessionBar(bc, bar) and \
              # not self.pa.isEngulfing(bc, bar):
               self.lg.debug("HI REVERSAL DETECTED exiting position")
               self.loReversal = 0
               #self.closePosition(bar, bc, bid, ask, 1)
               return 1
            
         #if self.hiReversal:  
         if self.positionType == self.buy:
            self.lg.debug("self.hiReversal " + str(self.hiReversal))
            #if self.pa.isLoReversalO(bc, bar):
            if self.pa.isLoReversalO(bc, bar) and not self.pa.isEngulfing(bc, bar):
            #if self.pa.isLoReversalSessionBar(bc, bar) and \
               #not self.pa.isEngulfing(bc, bar):
               self.hiReversal = 0
               self.lg.debug("LO REVERSAL DETECTED ")
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
   def algorithmSessionReversalsBar(self, bc, bar, bid, ask, actionOnOpen, actionOnClose, action=0):

      self.lg.debug("In algorithmSessionReversals " + str(action))

      if not actionOnClose:
         return action

      self.lg.debug ("algorithmSessionReversalsBar bar -2: -1: current")
      self.lg.debug (str(bc[bar - 2]))
      self.lg.debug (str(bc[bar - 1]))
      self.lg.debug (str(bc[bar]))
         
      if self.inPosition():
         if self.positionType == self.sell:
            self.lg.debug("self.loReversal " + str(self.loReversal))
            if self.pa.isHiReversalSessionBar(bc, bar) and \
                  not self.pa.isEngulfing(bc, bar):
               self.lg.debug("HI REVERSAL DETECTED exiting position")
               self.loReversal = 0
               self.closePosition(bar, bc, bid, ask, 1)
               return 1
            
         if self.positionType == self.buy:
            self.lg.debug("self.hiReversal " + str(self.hiReversal))
            if self.pa.isLoReversalSessionBar(bc, bar) and \
                  not self.pa.isEngulfing(bc, bar):
               self.hiReversal = 0
               self.lg.debug("LO REVERSAL DETECTED ")
               self.closePosition(bar, bc, bid, ask, 1)
               return 2
      else:
         if action == self.buy:
            self.lg.debug("self.hiReversal " + str(self.hiReversal))
            if self.pa.isLoReversalSessionBar(bc, bar) and \
                  not self.pa.isEngulfing(bc, bar):
               self.lg.debug("isHiReversal " + str(self.pa.isHiReversalO(bc, bar)))
               self.hiReversal += 1
               self.loReversal = 0
               self.openPosition(self.buy, bar, bc, bid, ask)
               return 1
            
         if action == self.sell:
            self.lg.debug("self.loReversal " + str(self.loReversal))
            if self.pa.isHiReversalSessionBar(bc, bar) and \
                  not self.pa.isEngulfing(bc, bar):
               self.loReversal += 1
               self.hiReversal = 0
               self.lg.debug("isLoReversal " + str(self.pa.isLoReversalO(bc, bar)))
               self.openPosition(self.sell, bar, bc, bid, ask)
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
   def algorithmSessionsHiLo(self, bc, bar, bid, ask, last, vol, actionOnClose, action=0):

      self.lg.debug("In algorithmSessionsHiLo " + str(action))
      
      if not actionOnClose:
         return action
         
      # Use open buy values
      if not self.sessionsHiMax:
         self.sessionsHiMax = self.lm.openBuyBars
      if not self.sessionsLoMax:
         self.sessionsLoMax = self.lm.openSellBars
         
      getOutLimit = self.sessionsHiMax
      maxLimit = self.sessionsHiMax
      if self.sessionsLoMax < self.sessionsHiMax:
         getOutLimit = self.sessionsLoMax
      else:
         maxLimit = self.sessionsLoMax
      
      # Take position when session hi or lo is breached.
      self.lg.debug("bar " + str(bar))
      self.lg.debug("getOutLimit " + str(getOutLimit))
      self.lg.debug("self.sessionsLoMax " + str(self.sessionsLoMax))
      self.lg.debug("self.sessionsHiMax " + str(self.sessionsHiMax))

      if bar < getOutLimit:
         return action

      seqLos = seqHis = 0
      barLo = [0] * self.sessionsLoMax
      barHi = [0] * self.sessionsHiMax
      
      for sl in range(self.sessionsLoMax):
         barLo[sl], junk = self.pa.getSessionBar(bc, bar - sl)
      
      for sh in range(self.sessionsHiMax):
         junk, barHi[sh] = self.pa.getSessionBar(bc, bar - sh)

      self.lg.debug("bars in reverse order:")
      
      for b in range(maxLimit):
         self.lg.debug("bc[bars] " + str(bc[bar - b]))
         
      self.lg.debug("barLo " + str(barLo))
      self.lg.debug("barHi " + str(barHi))

      for low in barLo:
         if low == 1:
            seqLos += 1
         
      for hi in barHi:
         if hi == 1:
            seqHis += 1
      
      if self.inPosition():
         if self.positionType == self.sell:
            if seqLos != self.sessionsLoMax: # Get out no lo's
               self.lg.debug("getting out no lo's")
               return 1
         else:
            if seqHis != self.sessionsHiMax: # Get out no hi's
               self.lg.debug("getting out no hi's")
               return 2
      else:
         if seqLos == self.sessionsLoMax:
            self.lg.debug("seqLos == self.sessionsLoMax")
            return 2
         if seqHis == self.sessionsHiMax:
            self.lg.debug("seqHis == self.sessionsHiMax")
            return 1

      return action
      
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
                  #self.sellPosition(bar, bc, bid, ask, 1)
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
               self.setWaitForNextBar()
               
#               self.lg.debug("HAMMER DETECTED! CLOSING POSITION")
#               self.openPosition(self.sell, bar, bc, bid, ask)
#               self.inHammerPosition += 1
#               self.hammerBar = bar
#               self.inInvHammerPosition = 0
               
            elif invHammer:
               self.lg.debug("INV HAMMER DETECTED! CLOSING POSITION")
               # Detect volume > previous bar by setting action
               self.closePosition(bar, bc, bid, ask, 1)
               self.setWaitForNextBar()
               
               #action = 2
               #
#               self.lg.debug("INV HAMMER DETECTED! OPENING POSITION")
#               self.openPosition(self.buy, bar, bc, bid, ask)
#               self.invHammerBar = bar
#               self.inInvHammerPosition += 1
#               self.inHammerPosition = 0

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
   def algorithmAutoLoss(self, last):
   
      self.lg.debug("In algorithmAutoLoss ")
      
      if not self.inPosition():
         return
      
      if not self.doAutoStop:
         return
         
      liveGainLoss = self.getTotalLiveGain()

      self.lg.debug("liveGainLoss " + str(liveGainLoss))

      if liveGainLoss <= self.getTargetLoss():
         self.doTrailingStop = 1
         self.doAutoStop = 1
         
      return

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmAutoStop(self, last):
   
      self.lg.debug("In algorithmAutoStop ")
      
      if not self.inPosition():
         return
      
      liveGainLoss = self.getTotalLiveGain()

      self.lg.debug("algorithmAutoStop liveGainLoss " + str(liveGainLoss))

      if self.doDoubleUp and len(self.doubleUpOpenPrice) > 1:
         liveGainLoss = self.doubleUpLiveGain(last)
         self.lg.debug("algorithmAutoStop liveGainLoss after doDoubleUp " + str(liveGainLoss))

      # Only CAP losses
      if liveGainLoss >= self.getTargetProfit():
         self.lg.debug("algorithmAutoStop setting target gain  hit trailing stop")
         self.doTrailingStop = 1
         self.doAutoStop = 1
         
      if liveGainLoss <= self.getTargetLoss():
         self.lg.debug("algorithmAutoStop target loss hit setting trailing stop!")
         self.doTrailingStop = 1
         self.doAutoStop = 1
         
      return

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmTrailingStop(self, last, action=0):
   
      # This algo takes affect when minimum profit/loss is attained.
      
      # OLD COMMENTS LEFT FOR reference...
      # Monitor gainTrailStop 
      # Move decision bars depending how long in pos
      # Take profit depending on how long in pos
      # Track how many bars price in a range. 
      # see where price is relative to session hi's/lo's
      # exit method if action > 0
      
      stoppedOut = 4
      
      self.lg.debug("In algorithmTrailingStop " + str(action))
      
      if not self.inPosition():
         return action
         
      liveGainLoss = self.getTotalLiveGain()

      if self.doDoubleUp and len(self.doubleUpOpenPrice) > 1:
         liveGainLoss = self.doubleUpLiveGain(last)

      self.lg.debug("liveGainLoss " + str(liveGainLoss))

      # If there is a signal to get out of a pos, get out. 
      # THIS ADDED AFTER ALGO WRITTEN
      if action > 0:
         return action       

      if self.stopPct > 0:         
         # Raise/Lower stop
         self.lg.debug("self.stopBuyTarget " + str(self.stopBuyTarget))
         self.lg.debug("self.stopSellTarget " + str(self.stopSellTarget))
         self.lg.debug("last " + str(last))
         self.lg.debug("self.stopPct " + str(self.stopPct))

         proposedBuyTarget = round((last - self.stopPct), 2)
         proposedSellTarget = round((last + self.stopPct), 2)
         
         if self.positionType == self.buy:
            if last < self.stopBuyTarget:
               self.lg.debug("stopped out " + str(last))
               self.lg.debug("self.stopBuyTarget " + str(self.stopBuyTarget))
               # End trading
               if self.quitMaxProfit:
                  return 4
               return 2
               
            self.lg.debug("last + self.stopPct " + str(last + self.stopPct))
            # Raise target
            #if last - self.stopPct > self.stopBuyTarget:
            if proposedBuyTarget > self.stopBuyTarget:
               self.stopBuyTarget = proposedBuyTarget
               self.lg.debug("Target raised " + str(self.stopBuyTarget))
         else:
            if last > self.stopSellTarget:
               self.lg.debug("stopped out " + str(last))
               self.lg.debug("self.stopSellTarget " + str(self.stopSellTarget))

               if self.quitMaxProfit:
                  return 4
               return 1

            self.lg.debug("stopPct: last - stopPct " + str(last - self.stopPct))
            # Lower target
            #if last + self.stopPct < self.stopSellTarget:
            if proposedSellTarget < self.stopSellTarget:
               self.stopSellTarget = proposedSellTarget
               self.lg.debug("Target lowered " + str(self.stopSellTarget))

         self.lg.debug("self.stopBuyTarget after " + str(self.stopBuyTarget))
         self.lg.debug("self.stopSellTarget after " + str(self.stopSellTarget))
            
         return 0
            
      elif self.inPosition():
         if liveGainLoss >= self.getTargetProfit():
            if self.getRealizedGainLoss() == 0.0:
               profitGained = liveGainLoss
            else:
               profitGained = self.getRealizedGainLoss()
            self.lg.debug("self.profitGainedPct " + str(self.profitGainedPct))
            self.stopPct = profitGained * self.profitGainedPct
            self.stopBuyTarget = round(last - self.stopPct, 2)
            self.stopSellTarget = round(last + self.stopPct, 2)
               
            self.lg.debug("profitGained " + str(profitGained))
            
         elif liveGainLoss <= self.getTargetLoss():
            self.lg.debug("self.currentLossPct " + str(self.currentLossPct))
            self.stopPct = abs(liveGainLoss * self.currentLossPct)
            self.stopBuyTarget = round(last + self.stopPct, 2)
            self.stopSellTarget = round(last - self.stopPct, 2)
               
            self.lg.debug("currentLoss " + str(liveGainLoss))

      self.lg.debug("self.stopBuyTarget " + str(self.stopBuyTarget))
      self.lg.debug("self.stopSellTarget " + str(self.stopSellTarget))
      
      self.lg.debug("self.getRealizedGainLoss() " + str(self.getRealizedGainLoss()))
      self.lg.debug("self.getTargetProfit() " + str(self.getTargetProfit()))

      self.lg.debug("last " + str(last))
      self.lg.debug("self.stopPct " + str(self.stopPct))
         
      return action
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPriceTracking(self, bid, ask, last, action=0):
      
      # If in a position monitor it
      # close out position if near loss/profit target.
      
      if not self.inPosition():
         return 0

      liveGainLoss = 0.0
      liveGainLoss = self.getTotalLiveGain()
      
      if liveGainLoss == 0.0:
         return 0
            
      self.lg.debug("In algorithmPriceTracking: " + str(liveGainLoss))

      if self.positionType == self.buy:
         last = ask
         self.lg.debug("Last ask price: " + str(last))
         self.lg.debug("self.openPositionPrice: " + str(self.openPositionPrice))
         self.lg.debug("IN BUY gain_loss: " + str(last - self.openPositionPrice))

         if last > self.openPositionPrice:
            self.lg.debug("Position is gaining profit: ")
            self.lg.debug("+" + str(last - self.openPositionPrice))
            if self.priceNearProfitTarget(self.getCurrentGain(last), bid, ask, last):
               return 4
               
         elif last < self.openPositionPrice:
            self.lg.debug("Position is adding to the current loss: ")
            self.lg.debug(str(liveGainLoss) + " -" + str(self.getCurrentGain(last)))

            self.lg.debug("self.maxNumLosses " + str(self.maxNumLosses))
            self.lg.debug("self.losses " + str(self.losses))

            if self.losses >= self.maxNumLosses and self.maxNumLosses != 0:
               self.lg.debug("self.losses >= self.maxNumLosses. returning 4 ")
               return 4
            
            if self.priceNearLossTarget(self.getCurrentGain(last), bid, ask, last):
               self.lg.debug("priceNearLossTarget true. returning 2 ")
               return 2

      elif self.positionType == self.sell:
         last = bid
         self.lg.debug("Last bid price: " + str(last))
         self.lg.debug("self.openPositionPrice: " + str(self.openPositionPrice))
         self.lg.debug("IN SELL gain_loss: " + str(self.getCurrentGain(last)))

         if last < self.openPositionPrice:
            self.lg.debug("Position is gaining profit: ")
            self.lg.debug("+" + str(self.getCurrentGain(last)))

            if self.priceNearProfitTarget(self.getCurrentGain(last), bid, ask, last):
               return 4
               
         else:
            self.lg.debug("Position is adding to the current loss: ")
            loss = self.getCurrentGain(last)
            self.lg.debug(str(liveGainLoss) + " -" + str(self.getCurrentGain(last)))
            
            self.lg.debug("self.maxNumLosses " + str(self.maxNumLosses))
            self.lg.debug("self.losses " + str(self.losses))

            if self.losses >= self.maxNumLosses and self.maxNumLosses != 0:
               return 4

            if self.priceNearLossTarget(loss, bid, ask, last):
               return 1
               
      return 0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDynamic(self, bid, ask, last, action=0):
      
      self.lg.debug("In algorithmDynamic: " + str(action))

      ## PUT NEW IDEAS ON TOP W DATE

      # 3/2023 If price has never gone positive after N bars reduce number of close bars
      
      # 3/2023 If in a position and in profit reduce close bars to get out w
      #  larger profit.
      #     if a new high is put in reduce close bar or turn on auto stop AS TS

      # determine OB and CB's based on daily chart data. 
      # get % gain at open compare with simlar day % gain and use that 
      # days results. e.g:
      # open 20% lower; find day(s) ~20% lower open; if day gain +
      # set OB buy bars at 1 CS bars at 3 
      
      #algo = self.dy.getInitialOpenCloseBarAlgo(last)
            
      # Too many times trends are a + gain. Don't let them turn negative
      #if self.doTrends:
      #   doInPosTracking += 1

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
         
      # If in a position and within a range sell out for profit when exiting range
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
   def priceNearLossTarget(self, loss, bid, ask, last):

      self.lg.debug("In priceNearLossTarget: " + str(loss))

      if loss == 0.0 or self.getTargetLoss() == 0:
         return 0
      
      pctNearTrgt = abs(loss / self.getTargetLoss())

      self.lg.debug("loss " + str(pctNearTrgt))
      self.lg.debug("pctNearTrgt " + str(pctNearTrgt))
      self.lg.debug("inPosLossPct " + str(self.inPosLossPct))

      # Don't let a profit turn to a loss
      if loss > 0.0:
         maxLossVal = abs(self.inPosLossPct * self.getTargetLoss())
         self.lg.debug("maxLossVal " + str(maxLossVal))
         self.lg.debug("getTargetLoss() " + str(self.getTargetLoss()))
                  
         if self.positionType == self.buy:
            diff = self.getCurrentGain(last)
            self.lg.debug("diff BUY " + str(diff))
         else:
            diff = last - self.openPositionPrice
            self.lg.debug("diff SELL " + str(diff))
         if diff > maxLossVal:
         #if maxLossVal < diff:
            return 1
         

      # If the spread (bid - ask) is greater than the loss then return 0
      if abs(bid - ask) > abs(last - self.openPositionPrice):
         self.lg.debug("The spread is greater than the loss " + str(abs(bid - ask)) + " " + str(abs(last - self.openPositionPrice)))
         return 0

      if pctNearTrgt > self.inPosLossPct: # 50%
         self.lg.info("priceNearLossTarget taking loss ")
         return 1
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def priceNearProfitTarget(self, gain, bid, ask, last):
   
      self.lg.debug("In priceNearProfitTarget: " + str(gain))

      if gain == 0.0 or self.getTargetProfit() == 0:
         return 0

      pctNearTrgt = gain / self.getTargetProfit()

      self.lg.debug("gain " + str(gain))
      self.lg.debug("pctNearTrgt " + str(pctNearTrgt))
      self.lg.debug("inPosProfitPct " + str(self.inPosProfitPct))

      # If the spread (bid - ask) is greater than the profit then return 0
      if abs(bid - ask) > abs(last - self.openPositionPrice):
         self.lg.debug("The spread is greater than the profit " + str(abs(bid - ask)) + " " + str(abs(last - self.openPositionPrice)))
         return 0
         
      if pctNearTrgt > self.inPosProfitPct: # 60%
         self.lg.info("priceNearProfitTarget taking profit ")
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
            self.lg.debug ("IN RANGE BETWEEN " + str(self.lm.rangeLo) +  " >" + str(bid) + "< " +  str(self.lm.rangeHi))

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
#         if self.getRealizedGainLoss() >= self.getTargetProfit():
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
      
#      if self.triggered:
#         self.lg.debug("BLOCKING open, waiting for new limit to be breached... ")
#         return 1

      # If manualOveride is set and got a signal, return 0
      if self.doManualOveride:
         if action == self.addToPosition or \
            action == self.manualClose or \
            action == self.manualQuit:
            return 0

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
         
      if self.getWaitForNextBar():
         self.lg.debug("wait for next bar is set. Not opening position: " + str(self.getWaitForNextBar()))
         return
         
      if self.offLine:
         try:
            time = bc[bar][self.dt]
         except IndexError:
            time = self.cn.getTimeStamp()
      else:
         time = self.cn.getTimeStamp()

      # Open a BUY position
      if action == self.buy:
         price = ask

         if self.doDoubleUp or self.doManualOveride:
            self.doubleUpOpenPrice.append(price)
            self.doubledUp += 1
            self.lg.debug ("doubleUpOpenPrice " + str(self.doubleUpOpenPrice))
            self.lg.debug ("doubledUp " + str(self.doubledUp))

         self.positionType = self.buy
         
         # Execute order here ========================
         

         self.lg.logIt(self.buy, str(price), str(self.bc.getBarsInPosition()), time, 0, 0)
         
      # Open a SELL position
      else:
         price = bid

         if self.doDoubleUp or self.doManualOveride:
            self.doubleUpOpenPrice.append(price)
            self.doubledUp += 1
            self.lg.debug ("doubleUpOpenPrice " + str(self.doubleUpOpenPrice))

         self.positionType = self.sell
         
         # Execute order here ========================
         
         self.lg.logIt(self.sell, str(price), str(self.bc.getBarsInPosition()), time, 0, 0)

      self.setOpenPositionValues(price, action, bid, ask)
      self.openPositionMsg(price, action, bar, bc)

#      if self.doDoubleUp and self.doubledUp and self.doubleUpLimit:
#         self.setWaitForNextBar()

      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def openPositionMsg(self, price, action, bar, bc):
   
      self.lg.info("\n")
      self.lg.info("POSITION OPEN " + str(self.stock))
      self.lg.info("Bar:  " + str(bar))
      actionMsg = "SELL"
      if action == 1:
         actionMsg = "BUY"
      self.lg.info("buy/sell: " + actionMsg)
      self.lg.info("Open buy limit: " + str(self.lm.openBuyLimit))
      self.lg.info("Open sell limit: " + str(self.lm.openSellLimit))
      self.lg.info("Open position Price: " + str(price))
      
      #self.lg.info("self.offLine: " + str(self.offLine))
      #self.lg.info("bc[bar][self.dt] " + str(bc[bar][self.dt]))
      
      if self.offLine:
         self.lg.info("Position Time: " + self.bc.getTimeStampFromBarchartFile(bar) + "\n")
         #self.lg.info("Position Time: " + bc[bar][self.dt] + "\n")
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()) + "\n")
               

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getInPosGain(self):
      
      return self.inPosGain
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setInPosGain(self):
      
      self.inPosGain = 1
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenPositionValues(self, price, action, bid, ask):
   
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

      if self.lm.aggressiveOpen:
         self.setWaitForNextBar()
         
      if self.lm.getSeqAlgos():
         self.setWaitForNextBar()
         
      self.overideAction = 0

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
      
      self.lg.debug("loBar sessionLo " + str(loBar) + " " + str(sessionLo))
      self.lg.debug("hiBar sessionHi " + str(hiBar) + " " + str(sessionHi))
      
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

# COMMENTING OUT 10/28/22. only trends and other specific restrict fundctions should stop a close
#      if self.getWaitForNextBar():
#         if bar < self.getNextBar():
#            self.lg.debug("Waiting for next bar... " + str(self.getNextBar()))
#            return 1

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
      else:
         price = ask
      
      self.lg.debug ("close position bid: " + str(bid))
      self.lg.debug ("close position ask: " + str(ask))
      
      if self.doDoubleUp and self.doubledUp:
         self.lg.debug ("len doubleUpOpenPrice " + str(len(self.doubleUpOpenPrice)))

         gain = self.doubleUpLiveGain(price)

      elif self.positionType == self.buy:
         gain = round(price - self.openPositionPrice, 2)
      elif self.positionType == self.sell:
         gain = round(self.openPositionPrice - price, 2)

      self.lg.debug ("gain at position close time " + str(gain))

      if gain > 0:
         self.wins += 1
      else:
         self.losses += 1

      self.closePositionPrice = price
      self.totalGain += gain
      
      # This fixes exponential values in log file
      self.totalGain = round(self.totalGain ,2)

      self.lg.debug ("total gain at position close time " + str(self.totalGain))

      self.totalLoss = self.totalGain
      self.setGainLastPrice(price)
      self.setLossLastPrice(price)

      self.closePositionMsg(bc, bar, gain, price)
      self.setClosePositionValues(bar, gain, price)

      self.lg.debug ("self.waitForNextBar" + str(self.waitForNextBar))
         
      if self.waitForNextBar:
         self.setWaitForNextBar()
         #self.setNextBar(bar + 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def closePositionMsg(self, bc, bar, gain, price):

      # Update the log
      doubleUpGain = 0
      if self.doDoubleUp and self.doubledUp and len(self.doubleUpOpenPrice):
         doubleUpGain = gain

      if self.offLine:
         try:
            time = bc[bar][self.dt]
         except IndexError:
            time = self.cn.getTimeStamp()
      else:
         time = self.cn.getTimeStamp()

      self.lg.logIt(self.close, str(price), str(self.bc.getBarsInPosition()), time, self.numTrades, doubleUpGain)

      self.lg.info ("\n")
      self.lg.info ("POSITION CLOSED " + self.stock)
      
      if self.offLine:
         try:
            self.lg.info("Position Time: " + self.bc.getTimeStampFromBarchartFile(bar) + "\n")
         except:
            self.lg.debug("bc.getTimeStampFromBarchartFile(bar) failed: bc[bar][self.dt] " + str(bar))
         #self.lg.info("Position Time: " + bc[bar][self.dt])
      else:
         self.lg.info("Position Time: " + str(self.cn.getTimeStamp()))

      self.lg.info("Bar:  " + str(bar))
      
      buySellMsg = "BUY"
      if self.positionType == 2:
         buySellMsg = "SELL"
         
      self.lg.info ("position Type: " + buySellMsg)
      
      if self.doDoubleUp and len(self.doubleUpOpenPrice):
         for p in self.doubleUpOpenPrice:
            self.lg.info ("open price: " + str(p))
      else:
         self.lg.info ("open price: " + str(self.openPositionPrice))
         
      self.lg.info ("close price: " + str(self.closePositionPrice))
      self.lg.info ("current Price: " + str(price))
      self.lg.info ("gain: " + str(gain))
      self.lg.info ("stopPrice: " + str(self.getClosePrice()))
      self.lg.info ("bar Count In Position: " + str(self.bc.getBarsInPosition()))
      self.lg.info ("Loss/Gain: " + str(gain))
      self.lg.info ("Total Gain: " + str(self.getRealizedGainLoss()) + "\n")
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

      if self.doDoubleUp:
         self.doubledUp = 0
         self.doubleUpOpenPrice = []
         self.doTrailingStop = 0
         self.doAutoStop = 0
         self.lm.setOpenBuySellLimits()
         self.lm.setCloseBuySellLimits()

         # Wait for next bar after close of doubleUp so seq conditions don't trigger
         # additional opens

         if self.lm.getSeqAlgos():
            self.setWaitForNextBar()

      if self.getRealizedGainLoss() > 0 and self.autoPriceTracking:
         # Turn on price tracking
         self.lg.debug("Turning on Price Tracking...")
         self.doInPosTracking = 1
         
      self.currentGain = 0.0
      
      self.overideAction = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doReversalPattern(self):
      if self.reversalPctTrigger > 0.0:
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def inPosition(self):
         
      print ("self.position " + str(self.position))
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
      self.lg.debug("reversing. buy is now sell...: " + str(self.buy) + " action " + str(self.sell))
      
      # Set new limits
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetRevBuySell(self):
   
      self.sell = 2
      self.buy = 1
      self.doReverseBuySell = 0
      self.lg.debug("restoring. buy is now buy...: " + str(self.buy) + " action " + str(self.sell))

      # Unset new limits
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doReverseBuySell(self):
      
      return self.doReverseBuySell
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLosses(self):

      return self.losses

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTotalLoss(self):

      return self.totalLoss

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getRealizedGainLoss(self):

      return self.totalGain

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def resetOpenPrice(self, price):
      
      self.openPositionPrice = price

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentGain(self, price):
      
      if not self.inPosition():
         return 0.0

      if self.positionType == self.buy:
         return round(price - self.openPositionPrice, 2)
      elif self.positionType == self.sell:
         return round(self.openPositionPrice - price, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLossLastPrice(self):

      return self.totalLossLastPrice

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getGainLastPrice(self):

      return self.totalGainLastPrice

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setLossLastPrice(self, price):

      self.totalLossLastPrice = price

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setGainLastPrice(self, price):

      self.totalGainLastPrice = price

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doubleUpLiveGain(self, price):
      
      gain = 0.0
      
      if len(self.doubleUpOpenPrice) == 0:
         return 0.0

      self.lg.debug ("Current price " + str(price))

      for p in self.doubleUpOpenPrice:
         self.lg.debug ("open pos double arr " + str(p))
         if self.positionType == self.buy:
            gain += round(price - p, 2)
         elif self.positionType == self.sell:
            gain += round(p - price, 2)

      return gain
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTotalLiveGain(self, last):

      # gainPrice $.50 + last $200.00 = $200.50
      # Is $200.50 > last?
      
      gainPrice = self.getGainLastPrice() 
      
      #gainPrice = self.getCurrentGain(last)
         #gainPrice = self.getCurrentGain(last)
      #gainPrice = self.getRealizedGainLoss() - (self.openPositionPrice + last)
      #getRealizedGainLoss()

      if self.inPosition():
         if self.positionType == self.buy:
            self.totalLiveGain = self.getRealizedGainLoss() + (last - gainPrice)
         else:
            self.totalLiveGain = self.getRealizedGainLoss() - (last - gainPrice)


#      if self.inPosition():
#         if self.positionType == self.buy:
#            if gainPrice < 0:
#               self.totalLiveGain = self.getRealizedGainLoss() + gainPrice
#            else:
#               self.totalLiveGain = self.getRealizedGainLoss() - gainPrice
#         else:
#            if gainPrice > 0:
#               self.totalLiveGain = self.getRealizedGainLoss() + gainPrice
#            else:
#               self.totalLiveGain = self.getRealizedGainLoss() - gainPrice

      print ("setting: self.totalLiveGain = " + str(self.totalLiveGain))

      #return self.totalLiveGain

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTotalLiveGain(self):

      print ("live gain " + str(self.totalLiveGain))
      
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
   def getTotalLiveLoss(self):

      print ("live loss " + str(self.totalLiveLoss))
      
      return self.totalLiveLoss
   
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
            self.lg.debug("Initial Min Profit pct set to " +  str(pct) + " number of prices " + str(lenPriceLimits))
            self.lg.debug("priceLimits "  + str(priceLimits))
            pct *= (lenPriceLimits - l) / self.priceLimitDivider
            self.lg.debug("lenPriceLimits " + str(lenPriceLimits) + " ctr " + str(l))
            self.lg.debug("self.priceLimitDivider " + str(self.priceLimitDivider))
            self.lg.debug("Min Profit = price * (pct * (lenPriceLimits - ctr / priceLimitDivider)) " + str(pct))
            break

      self.targetProfit = round(price * pct, 2)
      
      self.lg.debug("Min Profit set to: " +  str(self.targetProfit) + " for price " + str(price))
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTargetLoss(self, price, pct):

      # Increase profit target % for lower priced stocks

      priceLimits = self.priceLimits.split(',')
      lenPriceLimits = len(priceLimits)
      
      # "priceLimits": "5,10,20,50,100,200,500,1000,4000",

      for l in range(lenPriceLimits):
         if price <= int(priceLimits[l]):
            self.lg.debug("Initial max loss pct set to " +  str(pct) + " number of prices " + str(lenPriceLimits))
            self.lg.debug("priceLimits "  + str(priceLimits))
            pct *= (lenPriceLimits - l) / self.priceLimitDivider
            self.lg.debug("lenPriceLimits " + str(lenPriceLimits) + " ctr " + str(l))
            self.lg.debug("self.priceLimitDivider " + str(self.priceLimitDivider))
            self.lg.debug("Max loss = price * (pct * (lenPriceLimits - ctr / priceLimitDivider)) " + str(pct))
            break

      #self.targetLoss = round(price * pct, 2)*-1
      self.targetLoss = (round(price * pct, 2) * -1)
      
      self.lg.debug("Max Loss set to: " +  str(self.targetLoss) + " for price " + str(price))
   
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
      if self.doHiBuyLoSellSeq:
         self.algoMsg += "         HiBuy LoSell Sequential\n"
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
         self.algoMsg += "         Volume Last Bar on open\n"
      if self.volumeLastBarClose:
         self.algoMsg += "         Volume Last Bar on close\n"
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
      if self.doAutoStop:
         self.algoMsg += "         Auto stop\n"
      if self.quitMaxProfit:
         self.algoMsg += "         Quit max profit\n"
      if self.quitMaxLoss:
         self.algoMsg += "         Quit max loss\n"
      if self.doSessions:
         self.algoMsg += "         Sessions \n"
      if self.doSessionsHiLo:
         self.algoMsg += "         Sessions Hi Lo\n"
      if self.doAllPatterns:
         self.algoMsg += "         All Patterns: Hammers Reversals\n"
      if self.doHammers:
         self.algoMsg += "         Hammers \n"
      if self.doReversals:
         self.algoMsg += "         Reversals \n"
      if self.doSessionReversals:
         self.algoMsg += "         Session Reversals \n"
      if self.doOpensSeq:
         self.algoMsg += "         Opens sequentially \n"
      if self.doClosesSeq:
         self.algoMsg += "         Closes sequentially \n"
      if self.doInPosTracking:
         self.algoMsg += "         In position tracking \n"
      if self.doDoubleUp:
         self.algoMsg += "         Double Up " + str(self.doubleUpMax) + "\n"
      if self.doubleUpLimit:
         self.algoMsg += "         Double Up Limit " + str(self.doubleUpLimit) + "\n"
      if self.doHiLoHiLoSeqInHiLoOut:
         self.algoMsg += "         HiLo and HiLoSeq In. HiLo out \n"
      if self.doHiLoHiLoSeqInHiLoSeqOut:
         self.algoMsg += "         HiLo and HiLoSeq In. HiLoSeq out \n"
      if self.useAvgBarLimits:
         self.algoMsg += "         Using average bar lengths for limits \n"         
      if self.doTriggers:
         self.algoMsg += "         Triggers \n"
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
   
      self.waitingForNextBar = 1
      self.lg.debug("self.waitForNextBar " + str(self.waitForNextBar))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetWaitForNextBar(self):
   
      self.waitingForNextBar = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getWaitForNextBar(self):
   
      return self.waitingForNextBar
      
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
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def waitForNextBarAlgos(self):
   
      if self.doOpensCloses or self.doQuickProfit or self.doHammers \
         or self.reversAction or self.aggressiveOpen or self.aggressiveClose \
         or self.doTrends:
         return 1
      
      return 0
      
