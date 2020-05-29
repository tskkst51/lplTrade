'''
Algorithms module
'''
import io
import sys
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm(object):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   def __init__(self, data, lg):
   
      # Required standard settings
      self.algorithms = str(data['profileTradeData']['algorithms'])
            
      # Algorithms
      self.default = int(data['profileTradeData']['default'])
      self.hiLows = int(data['profileTradeData']['hiLows'])
      self.executeOnClose = int(data['profileTradeData']['executeOnClose'])
      self.executeOnOpen = int(data['profileTradeData']['executeOnOpen'])

      self.currency = str(data['profileTradeData']['currency'])
      self.alt = str(data['profileTradeData']['alt'])
      self.openBuyBars = int(data['profileTradeData']['openBuyBars'])
      self.closeBuyBars = int(data['profileTradeData']['closeBuyBars'])
      self.openSellBars = int(data['profileTradeData']['openSellBars'])
      self.closeSellBars = int(data['profileTradeData']['closeSellBars'])
      self.tradingDelayBars = int(data['profileTradeData']['tradingDelayBars'])
      
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
      
      # Don't trade unless out of a range
      self.rangeTradeBars = int(data['profileTradeData']['rangeTradeBars'])
      
      # Use highs and lows for determining open/close
      self.higherHighsBars = int(data['profileTradeData']['higherHighsBars'])
      self.lowerLowsBars = int(data['profileTradeData']['lowerLowsBars'])
      self.lowerHighsBars = int(data['profileTradeData']['lowerHighsBars'])
      self.higherLowsBars = int(data['profileTradeData']['higherLowsBars'])
      
      # Wait for next bar before opening a position
      self.waitForNextBar = int(data['profileTradeData']['waitForNextBar'])

      # Yet to implement.  BELOW HERE HASN"T BEEN IMPLEMENTED yet
      
      self.endTradingTime = float(data['profileTradeData']['endTradingTime'])
      self.profitPctTriggerAmt = float(data['profileTradeData']['profitPctTriggerAmt'])
      
      # reverseLogic appears to be best for short term charts and
      # low liquidity
      self.reversalPattern = int(data['profileTradeData']['reversalPattern'])
      self.reverseLogic = int(data['profileTradeData']['reverseLogic'])
      self.buyNearLow = int(data['profileTradeData']['buyNearLow'])
      self.sellNearHi = int(data['profileTradeData']['sellNearHi'])
      self.aggressiveOpenPct = float(data['profileTradeData']['aggressiveOpenPct'])
      self.aggressiveClosePct = float(data['profileTradeData']['aggressiveClosePct'])
      
      self.takeQuickProfit = int(data['profileTradeData']['takeQuickProfit'])
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
      
      self.trendTrigger = int(data['profileTradeData']['trendTrigger'])
      
      self.executeOnOpenPosition = 0
      self.executeOnClosePosition = 0

      self.hiLowBarMaxCounter = int(data['profileTradeData']['hiLowBarMaxCounter'])

      self.dynamic = int(data['profileTradeData']['dynamic'])
      self.quickReversal = int(data['profileTradeData']['quickReversal'])
      
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
      self.open = 2
      self.close = 3
      self.volume = 4
      
      self.buy = 1
      self.sell = 2
      self.triggerBars = self.openBuyBars
      self.currentBar = 0
      self.nextBar = 0
      self.rangeTradeValue = False
      self.rangeHi = 0.0
      self.rangeLo = 0.0
      
      self.hiValues = [0.0] 
      self.lowValues = [0.0]

      self.topIntraBar = 0.0
      self.barCounter = 0
      self.revDirty = False
      self.barCount = 0
      self.barCountInPosition = 0 
      self.dirtyWaitForNextBar = False
      self.profitTarget = 0.0
      self.longMegaBars = 0.0
      
      self.shortTrend = self.midTrend = 0.0
      self.longTrend = self.megaTrend = 0.0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takeActionOnOpen(self, currentPrice, barChart):
   
      action = 0

      if self.executeOnClose:
         print ("Execute on close entered\n")
         action = self.algorithmOnClose(currentPrice, barChart)
         
      return action
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takeActionOnCLose(self, currentPrice, barChart):
   
      action = 0

      if self.executeOnClose:
         print ("Execute on close entered\n")
         action = self.algorithmOnClose(currentPrice, barChart)
         
      return action
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def takeAction(self, currentPrice, barChart):
   
      action = 0
            
      if self.reversalPattern:
         print ("Reverse logic algo\n")
         action = self.algorithmreversalPattern(currentPrice, barChart, action)
      
      if self.reverseLogic:
         print ("Reverse logic algo\n")
         action = self.algorithmReverseLogic(currentPrice, barChart, action)
      
      if self.takeQuickProfit:
         print ("Execute profit taking algo\n")
         action = self.algorithmTakeProfit(currentPrice, barChart, action)
      
      if self.hiLows:
         print ("Execute on Hi Los entered\n")
         action = self.algorithmHiLo(currentPrice, barChart, action)
         
      if self.hiLows:
         print ("Execute on Hi Los entered\n")
         action = self.algorithmHiLo(currentPrice, barChart, action)
         
      if self.trendTrigger:
         print ("Execute on trend trigger entered\n")
         action = self.algorithmDoTrends(currentPrice, barChart, action)
         
      if self.default:
         print ("Default algo entered\n")
         action = self.algorithmDefault(currentPrice, barChart, action)
     
      if action > 0:
         print ("Action being taken!! " + str(action))
     
      return action
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmreversalPattern(self, currentPrice, barChart, action=0):
   
      # Detect a reversal pattern in the current bar. triggerring when
      # current bar is > than previous bar
   
      if self.inPosition() and self.doReversal():
         previousBarLen = float(barChart[i-1][cl] - barChart[i-1][op])
         currentBarLen = barChart[i][op] - currentPrice
         
         if previousBarLen < 0.0 and currentBarLen > 0.0:
            # Bars going different directions
            return 0
         
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
            if self.getReversalLimit(currentHi, currentOpen, currentPrice):
               lg.info("triggered due to reversal detected!")
               self.closePosition(currentPrice, i)
               lg.logIt(close, str(currentPrice), str(self.getBarsInPosition()), tm.now(), logPath)

      return 0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmReverseLogic(self, currentPrice, barChart, action=0):
   
      #if self.getReverseLogic():
         #if action == buyAction:
            #lg.debug ("OPEN reversal logic applied buy -> sell...")
            #action = sellAction
            #self.openBuyLimit = self.openSellLimit
         #elif action == sellAction:
            #lg.debug ("OPEN reversal logic applied sell -> buy...")
            #action = buyAction
            #self.openSellLimit = self.openBuyLimit
   
      if self.getReverseLogic():
         revAction = buyAction
         if action == buyAction: 
             revAction = sellAction
         lg.info("revAction: " + str(revAction) + " action " + str(action))
         self.openPosition(action, currentPrice, i)
         lg.logIt(revAction, str(currentPrice), str(self.getBarsInPosition()), tm.now(), logPath)
      else:
         self.openPosition(action, currentPrice, i)
         lg.logIt(action, str(currentPrice), str(self.getBarsInPosition()), tm.now(), logPath)

      return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmTakeProfit(self, currentPrice, barChart, action=0):
   
      if self.inPosition():
      
      #if self.inPosition() and not self.getExecuteOnClose():         
         #if self.getReverseLogic():
            #if action == buyAction:
               #lg.debug ("CLOSE reversal logic applied buy -> sell...")
               #action = sellAction
               #self.closeBuyLimit = self.closeSellLimit
            #elif action == sellAction:
               #lg.debug ("CLOSE reversal logic applied sell -> buy...")
               #action = buyAction
               #self.closeSellLimit = self.closeBuyLimit
         # In a position and still in first bar
         #if self.getCurrentBar() == i:                        
         #  lg.debug ("In first bar...")
            #lg.debug ("InitialStopGain() " + str(self.getInitialStopGain()))
            #lg.debug ("In first bar...")
            #if self.getPositionType() == buyAction:
            #  if currentPrice > self.getInitialStopGain() or currentPrice < #self.getInitialStopLoss():
         #        triggered = True
         #  elif self.getPositionType() == sellAction:
         #     if currentPrice < self.getInitialStopGain() or currentPrice > self.getInitialStopLoss():
         #        triggered = True

         # In a position and in next bar
         #else:
         
         profitTarget = self.getProfitTarget()
         if self.getPositionType() == buyAction:
            if currentPrice > self.getClosePrice():
               print (str(self.getProfitPctTrigger()))
            
            if self.getProfitPctTrigger() > 0.0:
               if currentPrice > profitTarget:
                  print ("PROFIT TARGET MET: " + str(profitTarget))
                  #self.setCloseBuyStop(currentPrice)
                  
         elif self.getPositionType() == sellAction:
            if currentPrice < profitTarget:
               lg.info("PROFIT TARGET MET: " + str(profitTarget))
               # self.setCloseSellStop(currentPrice)
            #elif currentPrice > self.getLowestCloseSellPrice():
            #elif currentPrice > self.getClosePrice():
                  
      return 0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDoTrends(self, currentPrice, barChart, action=0):
   
      if self.getBullTrend():
         if not self.inPosition():
            lg.debug ( "OPEN BUY. BULL TREND")
            self.openPosition(1, currentPrice, i)
            
            if self.getReverseLogic():
               lg.logIt(sell, str(currentPrice), str(self.getBarsInPosition()), tm.now(), logPath)
            else: 
               lg.logIt(buy, str(currentPrice), str(self.getBarsInPosition()), tm.now(), logPath)
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

      return 0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmOnClose(self, currentPrice, barChart, action=0):

      #if self.getBarsInPosition() < self.getTriggerBars():
      #   print ("No action taken getBarsInPosition() " + str(self.getBarsInPosition()) + " < getTriggerBars :" + str(self.getTriggerBars()))
      #   return 0

      # Take position on the close if execute on close is set 
      if not self.inPosition():

         # Open a buy position if closes are sequentially higher
         if self.getSeqHighestClosePrice(self.triggerBars, barChart):
            return self.buy
   
         # Open a sell position if closes are sequentially lower
         elif self.getSeqLowestClosePrice(self.triggerBars, barChart):
            return self.sell
         
      else:
         # Close a buy position if closes are sequentially lower
         if self.positionType == self.buy:
            if self.getSeqLowestClosePrice(self.triggerBars, barChart):
               return self.buy
   
         # Close a sell position if closes are sequentially higher
         elif self.positionType == self.sell:
            if self.getSeqHighestClosePrice(self.triggerBars, barChart):
               return self.sell
            
      return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmHiLo(self, currentPrice, barChart, action=0):

      hiLowBuy = hiLowSell = False
      higherHighs = higherLows = lowerHighs = lowerLows = False

      # Set boolean if hi low bar conditions are true 
      if self.higherHighsBars and self.higherLowsBars:
         if self.higherHighs and self.higherLows:
            print ("HERE1")
            hiLowBuy = True

      elif self.higherHighsBars and not self.higherLowsBars:
         if self.higherHighs:
            print ("HERE2")
            hiLowBuy = True

      elif self.higherLowsBars and not self.higherHighsBars:
         if self.higherLows:
            print ("HERE3")
            hiLowBuy = True

      if self.lowerLowsBars and self.lowerHighsBars:
         if self.lowerLows and self.lowerHighs:
            print ("HERE4")
            hiLowSell = True

      elif self.lowerLowsBars and not self.lowerHighsBars:
         if self.lowerLows:
            print ("HERE5")
            hiLowSell = True

      elif self.lowerHighsBars and not self.lowerLowsBars:
         if self.lowerHighs:
            print ("HERE6")
            hiLowSell = True

      if self.inPosition():
         print ("A close buy limit " + str(self.closeBuyLimit))
         print ("A close sell limit " +   str(self.closeSellLimit))
         if currentPrice < self.closeBuyLimit:
            return 1
         if currentPrice > self.closeSellLimit:
            return 2
            
      elif not self.inPosition():
         if currentPrice > self.openBuyLimit and hiLowBuy:
            print ("A open buy limit set " + str(self.openBuyLimit))
            return 1
         if currentPrice < self.openSellLimit and hiLowSell:
            print ("A open sell limit set " +   str(self.openSellLimit))
            return 2

      return 0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmDefault(self, currentPrice, barChart, action=0):
      
      # Ues the right flag here or continue to use this algo as the default
   
      if self.inPosition():
         print ("close buy limit " + str(self.closeBuyLimit))
         print ("close sell limit " +  str(self.closeSellLimit))
         if currentPrice < self.closeBuyLimit:
            return 1
         if currentPrice > self.closeSellLimit:
            return 2
      else:
         if currentPrice >= self.openBuyLimit and self.openBuyLimit != 0.0:
            print ( "open buy limit set " + str(self.openBuyLimit))
            return 1
         if currentPrice <= self.openSellLimit and self.openSellLimit != 0.0:
            print ("open sell limit set " +  str(self.openSellLimit))
            return 2
      
      return 0
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def ready(self, currentNumBars):
   
      if self.rangeTradeBars > self.tradingDelayBars:
         self.tradingDelayBars = self.rangeTradeBars
         
      #if self.shortTrendBars > self.tradingDelayBars:
         #self.tradingDelayBars = self.shortTrendBars
         
      #if self.longTrendBars > self.tradingDelayBars:
         #self.tradingDelayBars = self.longTrendBars
      
      if self.tradingDelayBars <= currentNumBars:
         return True
      else:
         return False
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def priceInRange(self, currentPrice):
   
      if self.rangeTradeBars:
         if currentPrice <= self.rangeHi and currentPrice >= self.rangeLo:
            if not self.inPosition():
               print ("in range between " + str(self.rangeHi) +   " and " + str(self.rangeLo))

            return True

      return False
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def waitingForBestPrice(self, currentPrice):
   
      if self.waitForBestPrice:
         return
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def openPosition(self, buyOrSell, price, bar):

# DO THE COMBINGING OF ACTIONS HERE TO EXTEND OR SHORTEN TRADES E:G: BULL TRADE< REVERSAL PATTERN

      self.triggerBars = 0
      if buyOrSell == self.buy:
         self.triggerBars = self.closeBuyBars
      elif buyOrSell == self.sell:
         self.triggerBars = self.closeSellBars

      print("\n")
      print("POSITION OPEN")
      print("buy/sell: " + str(buyOrSell))
      print("Position Price: " + str(price))

      self.positionType = buyOrSell
      self.position = "open"
      self.openPositionPrice = price
      self.setInitialClosePrices(price)
      #self.barCount = 0
      self.setCurrentBar(bar)
      self.setProfitTarget(price)
      self.barCountInPosition = 0

      self.setExecuteOnOpenPosition(0)
      
      self.lowestcloseSellLimit = self.closeSellLimit
      self.highestcloseBuyLimit = self.closeBuyLimit

      print("Initial stopGain: " + str(self.getInitialStopGain()))
      print("Initial stopLoss: " + str(self.getInitialStopLoss()))
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def closePosition(self, price, bar):

      gain = 0
      self.position = "close"
            
      if self.positionType == self.buy:
         self.triggerBars = self.openBuyBars
         gain = price - self.openPositionPrice
      elif self.positionType == self.sell:
         self.triggerBars = self.openSellBars
         gain = self.openPositionPrice - price

      self.closePositionPrice = price

      print ("\n")
      print ("POSITION CLOSED")
      print ("open price: " + str(self.openPositionPrice))
      print ("close price: " + str(self.closePositionPrice))
      print ("current Price: " + str(price))
      print ("stopPrice: " + str(self.getClosePrice()) + "\n")
      print ("bar Count In Position: " + str(self.barCountInPosition) + "\n")
      print ("Total Bar Count: " + str(self.barCount) + "\n")

      self.openPositionPrice = self.closePositionPrice = 0.0
      self.topIntraBar = 0.0
      self.setNextBar(bar+1)
      self.positionType = 0
      self.barCounter = self.currentBar = 0
      self.highestcloseBuyLimit = 0.0
      self.lowestcloseSellLimit = 0.0

      self.setExecuteOnClosePosition(0)
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doReversal(self):
      if self.reversalPctTrigger > 0.0:
         return True

      return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def inPosition(self):
         
      if self.position == "open":
         return True
      else:
         return False

   # Setter definitions

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getReverseLogic(self):
   
      return self.reverseLogic
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyStop(self, currentPrice):
   
      self.closeBuyLimit = currentPrice
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellStop(self, currentPrice):
   
      self.closeSellLimit = currentPrice
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setDynamic(self, currentPrice, bar):
   
      if not self.dynamic:
         return
   
   # if in a gain position set stop just above
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBarCount(self):

      self.barCount += 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBarInPositionCount(self):

      self.barCountInPosition += 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setProfitTarget(self, currentPrice):

      if not self.profitPctTrigger:
         return
         
      print ("open position price: " + str(self.openPositionPrice))
      print ("profit pct trigger: " + str(self.profitPctTrigger))

      if self.positionType == self.buy:
         self.profitTarget = currentPrice + (self.openPositionPrice * self.profitPctTrigger)
      elif self.positionType == self.sell:
         self.profitTarget = currentPrice - (self.openPositionPrice * self.profitPctTrigger)

      print ("profit pct value: " + str(self.profitTarget))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setHiLowLimits(self, barChart):
   
      if not self.hiLows:
         return
         
      if len(barChart) < self.lowerHighsBars:
         return
      if len(barChart) <   self.higherLowsBars:
         return
      if len(barChart) < self.lowerLowsBars:
         return
      if len(barChart) <   self.higherHighsBars:
         return
      
      loopLowIterator = loopHiIterator = 0
      
      loopLowIterator = self.lowerLowsBars
      if self.higherLowsBars > self.lowerLowsBars:
         loopLowIterator = self.higherLowsBars
         
      loopHiIterator = self.higherHighsBars
      if self.lowerHighsBars > self.higherHighsBars:
         loopHiIterator = self.lowerHighsBars
         
      self.lowValues = [0.0] * loopLowIterator   
      self.hiValues = [0.0] * loopHiIterator  
   
      barChartLen = len(barChart) - 1

      for n in range(loopLowIterator):
         print ("low's: " + str(barChart[barChartLen - n][self.lo]))
         self.lowValues[n] = barChart[barChartLen - n][self.lo]
         
      for n in range(loopHiIterator):
         print ("hi's: " + str(barChart[barChartLen - n][self.hi]))
         self.hiValues[n] = barChart[barChartLen - n][self.hi]
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setHiLowValues(self):
   
      if not self.hiLows:
         return

      self.higherHighs = self.getHigherHighs()
      self.lowerLows = self.getLowerLows()
      self.lowerHighs = self.getLowerHighs()
      self.higherLows = self.getHigherLows()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setInitialClosePrices(self, currentPrice):

      hiLoDiff = self.openBuyLimit - self.openSellLimit
      
      print ("Hi Lo diff: " + str(hiLoDiff) + "\n")
      
      if hiLoDiff == 0.0:
         hiLoDiff = 5.0

      if self.positionType == self.buy:
         posGain = currentPrice + hiLoDiff * self.profitPctTriggerBar
         posLoss = self.closeBuyLimit - self.closePositionFudge
      elif self.positionType == self.sell:
         posGain = currentPrice - hiLoDiff * self.profitPctTriggerBar
         posLoss = self.closeSellLimit + self.closePositionFudge

      self.initialStopGain = posGain
      self.initialStopLoss = posLoss

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getReversalLimit(self, top, open, currentPrice):
   
      if self.reversalPctTrigger == 0.0:
         return False

      # Have to wait for the top to form so keep track of the top
      # top - open = length
      # length * reversal pct == price to sell

      # if not in a gain position get out
      if self.positionType == self.buy:
         if currentPrice < self.openPositionPrice:
            return False
      elif self.positionType == self.sell:
         if currentPrice > self.openPositionPrice:
            return False

      if not self.revDirty:
         self.topIntraBar = top
         self.revDirty = True
         self.barCounter = 0
         return False

      if self.positionType == self.buy:
         if currentPrice >= top:
            self.topIntraBar = currentPrice
            self.barCounter = 0
            return

         #if top >= self.topIntraBar:
         #  self.topIntraBar = top
         #  return False

         barLen = top - open

      elif self.positionType == self.sell:
         bottom = top
         if currentPrice <= bottom:
            self.topIntraBar = currentPrice
            self.barCounter = 0
            return

         #if top <= self.topIntraBar:
         #  self.topIntraBar = top
         #  return False

         barLen = open - top

         print ("top " + str(top))
         print ("open " + str(open))
         print ("self.topIntraBar " + str(self.topIntraBar))
         print ("currentPrice " + str(currentPrice))
         print ("self.barCounter " + str(self.barCounter))
         print ("self.hiLowBarMaxCounter " + str(self.hiLowBarMaxCounter))
         print ("self.revDirty " + str(self.revDirty))

      if self.barCounter < self.hiLowBarMaxCounter:
         # Wait 10 checks for top to be higher than previous
         print("BarCounter: " + str(self.barCounter))
         self.barCounter += 1
         return False
      
      targetPrice = (barLen * self.reversalPctTrigger)
      sellPrice = top - targetPrice

      print ("barLen " + str(barLen))
      print ("targetPrice " + str(targetPrice))
      print ("sell price " + str(sellPrice))

      if self.positionType == self.buy:
         if sellPrice < currentPrice:
            return True
      elif self.positionType == self.sell:
         if sellPrice > currentPrice:
            return True

      return False
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCurrentBar(self, bar):

      self.currentBar = bar
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setNextBar(self, nextBar):
      
      self.nextBar = nextBar
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setRangeLimits(self, barChart):

      if not self.rangeTradeBars:
         return
         
      if len(barChart) < self.rangeTradeBars:
         return
         
      if self.rangeTradeBars:
         self.rangeHi = self.getHighestCloseOpenPrice(self.rangeTradeBars, barChart)
         self.rangeLo = self.getLowestCloseOpenPrice(self.rangeTradeBars, barChart)
               
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAllLimits(self, barChart, currentPrice, bar):

      if len(barChart) < self.rangeTradeBars:
         return

      #self.triggerBars = 0
      self.barCountInPosition = 0
      self.setRangeLimits(barChart)
      self.setHiLowLimits(barChart)
      self.setHiLowValues()
      self.setTrendLimits(barChart, currentPrice)
      self.setOpenCloseLimits(barChart, currentPrice)
      
      #self.setProfitTarget(currentPrice)
      
      self.revDirty = False
      self.barCountInPosition = bar - self.currentBar
      self.barCount = bar - self.currentBar

      if self.hiLows:
         print ("higherLows higherHighs " + str(self.higherLows) + 
            " " + str(self.higherHighs)) 
         print ("lowerHighs lowerLows " + str(self.lowerHighs) + 
            " " + str(self.lowerLows))

      self.setDynamic(currentPrice, bar)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendLimits(self, barChart, currentPrice):

      self.setShortTrend("short", barChart, currentPrice)
      self.setMidTrend("mid", barChart, currentPrice)
      self.setLongTrend("long", barChart, currentPrice)
      self.setMegaTrend("mega", barChart, currentPrice)
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setShortTrend(self, trendType, barChart, currentPrice):

      if self.shortTrendBars == 0:
         return
   
      self.shortTrend = 0.0
      barChartLen = len(barChart)
      print (str(barChartLen) + " " + str(self.shortTrendBars))
      if barChartLen <= self.shortTrendBars:
         return
         
      shortTrendBarLen = barChartLen - self.shortTrendBars
      
      self.setTrendValues(trendType, barChart, barChartLen, shortTrendBarLen, currentPrice)
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMidTrend(self, trendType, barChart, currentPrice):
      if self.midTrendBars == 0:
         return
   
      self.midTrend = 0.0
      barChartLen = len(barChart)
      print (str(barChartLen) + " " + str(self.midTrendBars))
      if barChartLen <= self.midTrendBars:
         return
         
      midTrendBarLen = barChartLen - self.midTrendBars
      
      self.setTrendValues(trendType, barChart, barChartLen, midTrendBarLen, currentPrice)
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setLongTrend(self, trendType, barChart, currentPrice):
      if self.longTrendBars == 0:
         return
   
      self.longTrend = 0.0
               
      barChartLen = len(barChart)
      print (str(barChartLen) + " " + str(self.longTrendBars))
      if barChartLen <= self.longTrendBars:
         return
         
      longTrendBarLen = barChartLen - self.longTrendBars
      
      self.setTrendValues(trendType, barChart, barChartLen, longTrendBarLen, currentPrice)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMegaTrend(self, trendType, barChart, currentPrice):
      if self.megaTrendBars == 0:
         return
   
      self.megaTrend = 0.0
               
      barChartLen = len(barChart)
      print (str(barChartLen) + " " + str(self.megaTrendBars))
      if barChartLen <= self.megaTrendBars:
         return
         
      megaTrendBarLen = barChartLen - self.megaTrendBars
      
      self.setTrendValues(trendType, barChart, barChartLen, megaTrendBarLen, currentPrice)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendValues(self, trendType, barChart, barChartLen, i, currentPrice):
      # 0.0 - no trend; 1.[0-9] - bull; 3.[0-9] - bear
      # the fractional value is the strength 0 weak 9 strong

      lowest = 999999999.99
      highest = 0.0
      loBarPosition = hiBarPosition = i = 0
         
      #for i in range(barChartLen):
      while i < barChartLen:
         if barChart[i][self.lo] < lowest:
            lowest = barChart[i][self.lo]
            loBarPosition = i
         if barChart[i][self.hi] > highest:
            highest = barChart[i][self.hi]
            hiBarPosition = i
         i += 1
      
      # Comparing bar positions of the hi and lo gives us the trend
      if loBarPosition == hiBarPosition:
         return
      elif loBarPosition < hiBarPosition:
         # Bull trend
         trend = 1.0
      elif loBarPosition > hiBarPosition:
         # Bear trend
         trend = 3.0

      # Get the range of bars
      if highest > lowest:
         range = highest - lowest
      else:
         range = lowest - highest
         
      pctInTrend = pctInTrendRnd = 0.0

      # Determine where in the range the current price is
      penetration = 0.0
      if currentPrice <= lowest:
         pctInTrendRnd = 0.00
      elif currentPrice >= highest:
         pctInTrendRnd = 0.9999
      else:
         penetration = currentPrice - lowest
         pctInTrend = penetration / range
         pctInTrendRnd = round(pctInTrend, 2)

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

      print(trendType + "Trend: " + str(trend))
      
      #print("loBarPosition: " + str(loBarPosition))
      #print("hiBarPosition: " + str(hiBarPosition))
      #print("highest: " + str(highest))
      #print("lowest: " + str(lowest))
      #print("range: " + str(range))
      #print("penetration: " + str(penetration))
      #print("pctInTrend: " + str(pctInTrend))
      #print("pctInTrendRnd: " + str(pctInTrendRnd) + "\n")
      #print("current: " + str(currentPrice))
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuyLimit(self, barChart):
   
      if self.aggressiveOpen:
         self.openBuyLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
         if not self.inPosition():
            print ("aggressiveOpen openBuyLimit " + str(self.openBuyLimit))  
          
      else:
         self.openBuyLimit = self.getHighestBarPrice(self.triggerBars, barChart)
         if not self.inPosition():
            print ("openBuyLimit " + str(self.openBuyLimit))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenSellLimit(self, barChart):
   
      if self.aggressiveOpen:
         self.openSellLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
         print ("aggressiveOpen openSellLimit " + str(self.openSellLimit))
         
      else:
         self.openSellLimit = self.getLowestBarPrice(self.triggerBars, barChart)
         if not self.inPosition():
            print ("openSellLimit " + str(self.openSellLimit))
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyLimit(self, barChart, currentPrice):
   
      if self.aggressiveClose:
         # Use with execute on close otherwise the lows will knock us out
         self.closeBuyLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
         if self.inPosition():
            print ("aggressiveClose closeBuyLimit " + str(self.closeBuyLimit))
      
      else:
         self.closeBuyLimit = self.getLowestBarPrice(self.triggerBars, barChart)
         if self.inPosition():
            print ("closeBuyLimit " + str(self.closeBuyLimit))
            
      if self.inPosition():
         print ("bars in position: " + str(self.getBarsInPosition()))
         
      if self.closePositionFudge and self.closeBuyLimit != 0.0:         
         self.closeBuyLimit -= (self.closePositionFudge - float(self.getBarsInPosition()))
         print ("closeBuyLimit AFTER fudge " + str(self.closeBuyLimit))

      # Move the buy limit closer to the price if in a gain
      if self.gainTrailStop and self.getGain(currentPrice):
            if (currentPrice - self.gainTrailStop) > self.closeBuyLimit:
               self.closeBuyLimit = currentPrice - self.gainTrailStop
               print ("closeBuyLimit AFTER gainTrailStop " + str(self.closeBuyLimit))           
         
      if self.closeBuyLimit > self.highestcloseBuyLimit:
         self.highestcloseBuyLimit = self.closeBuyLimit
         print ("closeBuyhighestLimit set " + str(self.highestcloseBuyLimit))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellLimit(self, barChart, currentPrice):

     # Use with execute on close otherwise highs will knock us out
     # Or use waitForNextBar
      if self.aggressiveClose:
         self.closeSellLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
         if self.inPosition():
            print ("aggressiveClose closeSellLimit " + str(self.closeSellLimit))
            
      else:
         self.closeSellLimit = self.getHighestBarPrice(self.triggerBars, barChart)
         if self.inPosition():
            print ("closeSellLimit " + str(self.closeSellLimit))
      
      if self.inPosition():
         print ("bars in position: " + str(self.getBarsInPosition()))
         
      if self.closePositionFudge and self.closeSellLimit != 0.0:
         self.closeSellLimit += (self.closePositionFudge - float(self.getBarsInPosition()))
         print ("closeSellLimit AFTER fudge " + str(self.closeSellLimit))

      # Move the sell limit closer to the price if in a gain
      if self.gainTrailStop and self.getGain(currentPrice):
            if (currentPrice + self.gainTrailStop) < self.closeSellLimit:
               self.closeSellLimit = currentPrice + self.gainTrailStop
               print ("closeSellLimit AFTER gainTrailStop " + str(self.closeSellLimit))


      if self.closeSellLimit < self.lowestcloseSellLimit:
         self.lowestcloseSellLimit = self.closeSellLimit
         print ("closeSelllowestLimit AFTER fudge " + str(self.lowestcloseSellLimit))
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseLimits(self, barChart, currentPrice):
      
      if (self.getBullTrend() or self.getBearTrend()) and self.inPosition():
         if self.increaseCloseBars:
            if self.getBarsInPosition() < self.increaseCloseBarsMax:
               self.triggerBars += self.getBarsInPosition()
               print("in trend increasing close bars: " + str(self.getBarsInPosition()) + "triggerBars: " + str(self.triggerBars))
         
      self.setOpenBuyLimit(barChart)
      self.setOpenSellLimit(barChart)
      self.setCloseBuyLimit(barChart, currentPrice)
      self.setCloseSellLimit(barChart, currentPrice)
      
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
   def getQuickReversal(self):

      return self.quickReversal

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
   def getGain(self, currentPrice):

      if currentPrice > self.openPositionPrice:
         return True

      return False
      
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
   def getPriceInRange(self, currentPrice):

      if self.rangeTradeBars:
         return self.priceInRange(currentPrice)

      return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getWaitForNextBar(self):
   
      return self.waitForNextBar
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getProfitPctTrigger(self):
   
      return self.profitPctTrigger
      
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
   
      return self.executeOnClose
      
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

      return self.trendTrigger
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBearTrend(self):
      # Bear trend means mid, mega and long trends are bearish
      
      #if self.getShortTrend() >= 3.0 and self.getMidTrend() >= 3.0 and self.getLongTrend() >= 3.0:
      if self.getMegaTrend() >= 3.0 and self.getMidTrend() >= 3.0 and self.getLongTrend() >= 3.0:
         print("IN BEAR TREND")
         return True
      
      return False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBullTrend(self):
      # Bull trend means mid, long and mega are bullish
      
      #shortTrend = self.getShortTrend()
      midTrend = self.getMidTrend()
      longTrend = self.getLongTrend()
      megaTrend = self.getMegaTrend()
         
      #if shortTrend >= 1.0 and shortTrend <= 2.0:
      if midTrend >= 1.0 and midTrend <= 2.0:
         if longTrend >= 1.0 and longTrend <= 2.0:
            if megaTrend >= 1.0 and megaTrend <= 2.0:
               print("IN BULL TREND")
               return True
      
      return False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDynamic(self):

      return self.dynamic
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHigherHighs(self):
   
      if not self.higherHighsBars:
         return False

      if len(self.hiValues) < self.higherHighsBars:
         return False

      print ("number of hi bars: " + str(len(self.hiValues)))

      n = 1
      highest = self.hiValues[0]
      
      #while n < self.higherHighsBars:
      for n in range(self.higherHighsBars):
         hi = self.hiValues[n]
         if hi >= highest:
            return False
         highest = self.hiValues[n]
         #n += 1
         
      return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowerHighs(self): 
      if not self.lowerHighsBars:
         return False
      if len(self.hiValues) < self.lowerHighsBars:
         return False
         
      n = 1
      highest = self.hiValues[0]
      
      for n in range(self.lowerHighsBars):
         hi = self.hiValues[n]
         if hi <= highest:
            return False
         highest = self.hiValues[n]

      return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowerLows(self):  
      if not self.lowerLowsBars:
         return False
      if len(self.lowValues) < self.lowerLowsBars:
         return False
         
      n = 1
      lowest = self.lowValues[0]
      
      for n in range(self.lowerLowsBars):
         lo = self.lowValues[n]
         if lo <= lowest:
            return False
         lowest = self.lowValues[n]
         
      return True
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHigherLows(self): 
      if not self.higherLowsBars:
         return False
      if len(self.lowValues) < self.higherLowsBars:
         return False

      n = 1
      lowest = self.lowValues[0]
      
      for n in range(self.higherLowsBars):
         lo = self.lowValues[n]
         if lo >= lowest:
            return False
         lowest = self.lowValues[n]

      return True
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestCloseOpenPrice(self, numBars, barChart):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1
         
      while n < numBars:
         open = barChart[barChartLen - n][self.open]
         close = barChart[barChartLen - n][self.close]
 
         minPriceArr[n] = open
         if close < open:
            minPriceArr[n] = close
         n += 1
         
      #print ("min price arr: " + str(minPriceArr))
      
      # Compare all min prices and find the lowest price
      clean = True
      n = 0
      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = False
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestCloseOpenPrice(self, numBars, barChart):

      if len(barChart) < numBars:
         return 0.0

      n = 0
      maxPriceArr = [0.0] * numBars 
      barChartLen = len(barChart) - 1
                  
      while n < numBars:
         open = barChart[barChartLen - n][self.open]
         close = barChart[barChartLen - n][self.close]
 
         maxPriceArr[n] = open
         if close > open:
            maxPriceArr[n] = close
         n += 1
         
      #print ("max price arr: " + str(maxPriceArr))
      
      # Compare all max prices and find the highest price
      clean = True
      n = 0
      while n < numBars:
         if clean:
            maxPrice = maxPriceArr[n]
            clean = False
            continue
         
         if maxPriceArr[n] > maxPrice:
            maxPrice = maxPriceArr[n]
         
         n += 1

      return float(maxPrice)
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestClosePrice(self, numBars, barChart):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      # Fill the list
      while n < numBars:
         minPriceArr[n] = barChart[barChartLen - n][self.close]
         n += 1
         
      # Compare all the closes and find the lowest price
      clean = True
      n = 0
      
      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = False
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSeqLowestClosePrice(self, numBars, barChart):
   
      # Subtract 1 here so indexing below starts at 0 and goes to len - 1
      barChartLen = len(barChart) - 1;

      if barChartLen < numBars:
         return False

      print (str(numBars))
      print (str(barChartLen))

      # Must have two or more bars to compare
      if barChartLen < 2:
         return False

      # Initialize iterator and length of bar chart
      n = 0

      print (str(barChartLen))

      # Start at barChartLen which is the latest bar.
      # If close price is lower than previous bar return false.
      # Return true is closes are sequentialy higher
       
      print ("getSeqLowestClosePrice")
      for n in range(numBars):
         print ("Last bar: " + str(barChart[barChartLen - n][self.close]))
         print ("Last bar -1" + str(n+1) + " " + str(barChart[barChartLen - (n + 1)][self.close]))

         if barChart[barChartLen - n][self.close] >= barChart[barChartLen - (n + 1)][self.close]:
            return False

      print ("Opening a sell position")
      return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSeqHighestClosePrice(self, numBars, barChart):
   
      # Subtract 1 here so indexing below starts at 0 and goes to len - 1
      barChartLen = len(barChart) - 1;

      if barChartLen < numBars:
         return False

      print (str(numBars))
      print (str(barChartLen))

      # Must have two or more bars to compare
      if barChartLen < 2:
         return False

      # Initialize iterator and length of bar chart
      n = 0

      print (str(barChartLen))

      # Start at barChartLen which is the latest bar.
      # If close price is lower than previous bar return false.
      # Return true is closes are sequentialy higher
       
      print ("getSeqHighestClosePrice")
      for n in range(numBars):
         print ("Last bar: " + str(barChart[barChartLen - n][self.close]))
         print ("Last bar -1 " + str(n+1) + " " + str(barChart[barChartLen - (n + 1)][self.close]))

         # IF CLOSES ARE IDENTICAL COULD COMPARE HI"S AND LO"S
         # For now if closes are equal we treat that as sequential
         if barChart[barChartLen - n][self.close] <= barChart[barChartLen - (n + 1)][self.close]:
            return False

      print ("Opening a buy position")
      return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestClosePrice(self, numBars, barChart):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      maxPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      # Fill the list
      while n < numBars:
         maxPriceArr[n] = barChart[barChartLen - n][self.close]
         n += 1
         
      # Compare all the closes and find the highest price
      clean = True
      n = 0
      while n < numBars:
         if clean:
            maxPrice = maxPriceArr[n]
            clean = False
            continue
         
         if maxPriceArr[n] > maxPrice:
            maxPrice = maxPriceArr[n]
         
         n += 1
      # End while

      return float(maxPrice)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestOpenPrice(self, numBars, barChart):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      # Fill the list
      while n < numBars:
         minPriceArr[n] = barChart[barChartLen - n][self.open]
         n += 1
         
      # Compare all the closes and find the lowest price
      clean = True
      n = 0
      
      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = False
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestOpenPrice(self, numBars, barChart):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      maxPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      # Fill the list
      while n < numBars:
         maxPriceArr[n] = barChart[barChartLen - n][self.open]
         n += 1
         
      # Compare all the closes and find the highest price
      clean = True
      n = 0
      while n < numBars:
         if clean:
            maxPrice = maxPriceArr[n]
            clean = False
            continue
         
         if maxPriceArr[n] > maxPrice:
            maxPrice = maxPriceArr[n]
         
         n += 1
      # End while

      return float(maxPrice)
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestBarPrice(self, numBars, barChart):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      # Fill the list
      while n < numBars:
         minPriceArr[n] = barChart[barChartLen - n][self.lo]
         n += 1
         
      # Compare all the closes and find the lowest price
      clean = True
      n = 0
      
      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = False
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestBarPrice(self, numBars, barChart):

      if len(barChart) < numBars:
         return 0.0

      n = 0
      maxPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      # Fill the list
      while n < numBars:
         maxPriceArr[n] = barChart[barChartLen - n][self.hi]
         n += 1
         
      # Compare all the closes and find the highest price
      clean = True
      n = 0
      while n < numBars:
         if clean:
            maxPrice = maxPriceArr[n]
            clean = False
            continue
         
         if maxPriceArr[n] > maxPrice:
            maxPrice = maxPriceArr[n]
         
         n += 1
      # End while

      return float(maxPrice)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestHiLoIntraBarPrice(self, numBars, barChart):
   
      if len(barChart) < numBars:
         return 0.0

      n = 0
      minPriceArr = [0.0] * numBars
      barChartLen = len(barChart) - 1

      while n < numBars:
         hi = barChart[barChartLen - n][self.hi]
         lo = barChart[barChartLen - n][self.lo]
 
         minPriceArr[n] = hi
         if lo < hi:
            minPriceArr[n] = lo
         n += 1
         
      # Compare all min prices and find the lowest price
      clean = True
      n = 0
      while n < numBars:
         if clean:
            minPrice = minPriceArr[n]
            clean = False
            continue
         
         if minPriceArr[n] < minPrice:
            minPrice = minPriceArr[n]
         
         n += 1

      return float(minPrice)

         
         
