'''
trends module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Limits:
   def __init__(self, d, lg, cn, ba, pf, stock=""):
      
      self.d = d
      self.lg = lg
      self.cn = cn
      self.ba = ba
      self.pf = pf

      self.hi = 0
      self.lo = 1
      self.op = 2
      self.cl = 3
      self.vl = 4
      self.bl = 5
      self.sH = 6
      self.sL = 7
      self.dt = 8
            
      self.openBuyBars = int(d['openBuyBars'])
      self.closeBuyBars = int(d['closeBuyBars'])
      self.openSellBars = int(d['openSellBars'])
      self.closeSellBars = int(d['closeSellBars'])
      self.tradingDelayBars = int(d['tradingDelayBars'])
      self.doRangeTradeBars = int(d['doRangeTradeBars'])
      self.doHiLoSeq = int(d['doHiLoSeq'])
      self.doHiSeq = int(d['doHiSeq'])
      self.doLoSeq = int(d['doLoSeq'])
      self.doOpenCloseSeq = int(d['doOpenCloseSeq'])      
      self.doOpensSeq = int(d['doOpensSeq'])      
      self.doClosesSeq = int(d['doClosesSeq'])
      self.doHiBuyLoSellSeq = int(d['doHiBuyLoSellSeq'])
      self.doHiLoHiLoSeqInHiLoOut = int(d['doHiLoHiLoSeqInHiLoOut'])
      self.doHiLoHiLoSeqInHiLoSeqOut = int(d['doHiLoHiLoSeqInHiLoSeqOut'])

      self.doOpensCloses = int(d['doOpensCloses'])      
      self.doHiLo = int(d['doHiLo'])
      self.doExecuteOnOpen = int(d['doExecuteOnOpen'])
      self.doExecuteOnClose = int(d['doExecuteOnClose'])
      self.aggressiveOpenPct = float(d['aggressiveOpenPct'])
      self.aggressiveClosePct = float(d['aggressiveClosePct'])
      self.useAvgBarLimits = int(d['useAvgBarLimits'])
      
      self.aggressiveOpen = int(d['aggressiveOpen'])
      self.aggressiveClose = int(d['aggressiveClose'])
      self.agrBuyHiOpen = int(d['agrBuyHiOpen'])
      self.agrSellLoOpen = int(d['agrSellLoOpen'])
      self.agrBuyHiClose = int(d['agrBuyHiClose'])
      self.agrSellLoClose = int(d['agrSellLoClose'])

      self.higherHighs = self.higherCloses = 0
      self.lowerHighs = self.lowerCloses = 0
      self.lowerLows = self.lowerOpens = 0
      self.higherLows = self.higherOpens = 0
      
      self.hiValues = []
      self.loValues = []
      
      self.openBuyLimit = 0.0
      self.closeBuyLimit = 0.0
      self.highestcloseBuyLimit = 0.0
      self.lowestcloseBuyLimit = 0.0
      self.highestcloseSellLimit = 0.0
      self.lowestcloseSellLimit = 99999999.999999
      self.openSellLimit = 0.0
      self.closeSellLimit = 0.0
      self.rangeHi = 0.0
      self.rangeLo = 0.0
      self.stock = stock
      self.minTradingDelayBars = 0
      self.valCtr = 0
      self.seqAlgos = 0
      
      # Must have 2 decision bars when doing hiLoSeq
      if self.doHiLoSeq or self.doHiSeq or self.doLoSeq or self.doOpenCloseSeq or \
         self.doExecuteOnOpen or self.doExecuteOnClose or self.doOpensSeq or self.doClosesSeq or self.doHiBuyLoSellSeq or self.doHiLoHiLoSeqInHiLoSeqOut or self.doHiLoHiLoSeqInHiLoOut:
         
         #or self.doOpensCloses:

         self.lg.debug ("setting decision bars to 2")

         if self.openBuyBars < 2:
            self.openBuyBars = 2
         if self.closeBuyBars < 2:
            self.closeBuyBars = 2
         if self.openSellBars < 2:
            self.openSellBars = 2
         if self.closeSellBars < 2:
            self.closeSellBars = 2

         self.seqAlgos = 1

      self.higherOpensBuyOpen = self.higherOpensSellOpen = 0
      self.higherOpensBuyClose = self.higherOpensSellClose = 0
      self.lowerOpensBuyOpen = self.lowerOpensSellOpen = 0
      self.lowerOpensBuyClose = self.lowerOpensSellClose = 0
      self.higherHighsBuyOpen = self.higherHighsSellOpen = 0
      self.higherHighsBuyClose = self.higherHighsSellClose = 0
      self.higherLowsBuyOpen = self.higherLowsSellOpen = 0
      self.higherLowsBuyClose = self.higherLowsSellClose = 0
      self.lowerHighsBuyOpen = self.lowerHighsSellOpen = 0
      self.lowerHighsBuyClose = self.lowerHighsSellClose = 0
      self.lowerLowsBuyOpen = self.lowerLowsSellOpen = 0
      self.lowerLowsBuyClose = self.lowerLowsSellClose = 0
      self.higherClosesBuyClose = self.higherClosesSellClose = 0
      self.lowerClosesBuyClose = self.lowerClosesSellClose = 0
      self.higherClosesBuyOpen = self.higherClosesSellOpen = 0
      self.lowerClosesBuyOpen = self.lowerClosesSellOpen = 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSeqAlgos(self):

      return self.seqAlgos

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setRangeLimits(self, barChart, bar):

      if self.doRangeTradeBars == 0:
         return
         
      if bar < self.doRangeTradeBars:
         return

      if bar < self.getMaxNumTradeBars():
         return

      self.lg.debug("\nRange values... " + str(bar))
      self.lg.debug("self.doRangeTradeBars... " + str(self.doRangeTradeBars))
      self.lg.debug("self.getMaxNumTradeBars()... " + str(self.getMaxNumTradeBars()))
      
      maxBars = self.doRangeTradeBars
      
      if self.doRangeTradeBars < self.getMaxNumTradeBars():
         maxBars = self.getMaxNumTradeBars()
         
      #self.setOpenCloseHiLoValues(barChart, bar, maxBars)

      #self.setHiLoConditions()
#      self.setOpenCloseHiLoConditions(self.doRangeTradeBars)

      # Use Hi and Los or open closes for determining range
      if self.doOpensCloses or self.doOpenCloseSeq:
         self.rangeHi = self.getHighestCloseOpenPrice(self.doRangeTradeBars)
         self.rangeLo = self.getLowestCloseOpenPrice(self.doRangeTradeBars)
         self.lg.debug("Range limits using Open Closes ")
      
      else:
         self.rangeHi = self.getHighestHiLoPrice(self.doRangeTradeBars)
         self.rangeLo = self.getLowestHiLoPrice(self.doRangeTradeBars)
         self.lg.debug("Range limits using Hi Los ")
                        
      self.lg.debug("\nRange limits: " + str(self.rangeHi) + " " + str(self.rangeLo)+ "\n")
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenOpenBuyLimit(self, last):

      avgBarLen = self.ba.getAvgBarLen()
      
      # Tighten up the limit when profit has been taken
      #if self.quickProfitCtr:
         #avgBarLen = avgBarLen / self.quickProfitCtr
         
      self.openBuyLimit = round(last + avgBarLen, 2)
      
      print ("AvgBarLen: setOpenBuyLimit: " + str(self.openBuyLimit))
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenOpenSellLimit(self, last):

      avgBarLen = self.ba.getAvgBarLen()

      # Tighten up the limit when profit has been taken
      #if self.quickProfitCtr:
         #avgBarLen = avgBarLen / self.quickProfitCtr

      self.openSellLimit = round(last - avgBarLen, 2)
      
      print ("AvgBarLen: setOpenSellLimit: " + str(self.openSellLimit))
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenCloseBuyLimit(self, last):

      avgBarLen = self.ba.getAvgBarLen()

      #if self.ba.getBarsInPosition() > 1:
         #avgBarLen /= 2.0
      
      print ("\navgBarLen: " + str(avgBarLen))
         
      self.closeBuyLimit = round(last - avgBarLen, 2)
      
      print ("\nAvgBarLen: setCloseBuyLimit: " + str(self.closeBuyLimit))
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenCloseSellLimit(self, last):

      avgBarLen = self.ba.getAvgBarLen()

      #if self.ba.getBarsInPosition() > 1:
         #avgBarLen /= 2.0
        
      print ("\navgBarLen: " + str(avgBarLen))
         
      self.closeSellLimit = round(last + avgBarLen, 2)
      
      print ("\nAvgBarLen: setCloseSellLimit: " + str(self.closeSellLimit))
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuyLimit(self, numBars):

      if self.doExecuteOnOpen:
         if self.aggressiveOpen:
            self.openBuyLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("aggressiveOpen: openBuyLimit lowest close ")
            
         elif self.agrBuyHiOpen:
            self.openBuyLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("agrBuyHiOpen: openBuyLimit highest open ")
            
         else:
            self.openBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("default: openBuyLimit highest close")
          
      elif self.doHiLo:
         if self.aggressiveOpen:
            self.openBuyLimit = self.getLowestHiPrice(numBars)
            self.lg.debug("aggressiveOpen: openBuyLimit lowest hi ")
         elif self.agrBuyHiOpen:
            self.openBuyLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("agrBuyHiOpen: openBuyLimit highest open ")
         else:
            self.openBuyLimit = self.getHighestHiPrice(numBars)
            self.lg.debug("default: openBuyLimit highest hi")

      elif self.doOpensSeq:
         if self.aggressiveOpen:
            self.openBuyLimit = self.getLowestOpenPrice(numBars)
            self.lg.debug("aggressiveOpen: openBuyLimit lowest open ")
         elif self.agrBuyHiOpen:
            self.openBuyLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("agrBuyHiOpen: openBuyLimit highest open ")
         else:
            self.openBuyLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("default: openBuyLimit highest open")

      elif self.doClosesSeq:
         if self.aggressiveOpen:
            self.openBuyLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("aggressiveOpen: openBuyLimit lowest close ")
         elif self.agrBuyHiOpen:
            self.openBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("agrBuyHiOpen: openBuyLimit highest close ")
         else:
            self.openBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("default: openBuyLimit highest close")
      
      elif self.doOpensCloses:
         if self.aggressiveOpen:
            self.openBuyLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("doOpensCloses aggressiveOpen: openBuyLimit lowest open/close ")
         elif self.agrBuyHiOpen:
            self.openBuyLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("agrBuyHiOpen: openBuyLimit highest open ")
         else:
            self.openBuyLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug("doOpensCloses: openBuyLimit highest open/close")

      elif self.doOpenCloseSeq:
         if self.aggressiveOpen:
            self.openBuyLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("aggressiveOpen: openBuyLimit lowest close/open ")
         elif self.agrBuyHiOpen:
            self.openBuyLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug("agrBuyHiOpen: openBuyLimit highest close/open ")
         else:
            self.openBuyLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug("default: openBuyLimit highest close/open")

      else: # Default
         if self.aggressiveOpen:
            self.openBuyLimit = self.getLowestHiPrice(numBars)
            self.lg.debug("aggressiveOpen: openBuyLimit lowest hi ")
            
         elif self.agrBuyHiOpen:
            self.openBuyLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("agrBuyHiOpen: openBuyLimit highest open ")
            
         else:
            self.openBuyLimit = self.getHighestHiPrice(numBars)
            self.lg.debug("default: openBuyLimit highest hi")
            
      self.lg.debug(str(self.openBuyLimit))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenSellLimit(self, numBars):

      if self.doExecuteOnOpen:
         if self.aggressiveOpen:
            self.openSellLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug ("aggressiveOpen: openSellLimit highest close ")
         elif self.agrSellLoOpen:
            self.openSellLimit = self.getLowestOpenPrice(numBars)
            self.lg.debug("agrSellLoOpen: openSellLimit lowest open ")
         else:
            self.openSellLimit = self.getLowestClosePrice(numBars)
            self.lg.debug ("default: openSellLimit lowest close ")
         
      elif self.doHiLo:
         if self.aggressiveOpen:
            self.openSellLimit = self.getHighestLoPrice(numBars)
            self.lg.debug ("aggressiveOpen: openSellLimit highest lo ")
         elif self.agrSellLoOpen:
            self.openSellLimit = self.getLowestOpenPrice(numBars)
            self.lg.debug("agrSellLoOpen: openSellLimit lowest open ")
         else:
            self.openSellLimit = self.getLowestLoPrice(numBars)
            self.lg.debug("default: openSellLimit Lowest lo")

      elif self.doOpensSeq:
         if self.aggressiveOpen:
            self.openSellLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("aggressiveOpen: openSellLimit highest open ")
         else:
            self.openSellLimit = self.getLowestOpenPrice(numBars)
            self.lg.debug("default: openSellLimit Lowest open ")
      
      elif self.doClosesSeq:
         if self.aggressiveOpen:
            self.openSellLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("aggressiveOpen: openSellLimit highest close ")
         else:
            self.openSellLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("default: openSellLimit Lowest close ")
            
      elif self.doOpensCloses:
         if self.aggressiveOpen:
            self.openSellLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug ("doOpensCloses aggressiveOpen: openSellLimit highest open/close ")
         else:
            self.openSellLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("doOpensCloses: openSellLimit Lowest open/close")
      
      elif self.doOpenCloseSeq:
         if self.aggressiveOpen:
            self.openSellLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug("aggressiveOpen: openSellLimit highest close/open ")
         else:
            self.openSellLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("default: openSellLimit Lowest close/open ")

      else: # Default
         if self.aggressiveOpen:
            self.openSellLimit = self.getHighestLoPrice(numBars)
            self.lg.debug ("aggressiveOpen: openSellLimit highest lo ")
         elif self.agrSellLoOpen:
            self.openSellLimit = self.getLowestOpenPrice(numBars)
            self.lg.debug("agrSellLoOpen: openSellLimit lowest open ")
         else:
            self.openSellLimit = self.getLowestLoPrice(numBars)
            self.lg.debug("default: openSellLimit Lowest lo")
         
      self.lg.debug(str(self.openSellLimit))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyLimit(self, numBars):
   
      if self.doExecuteOnOpen:
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug ("aggressiveClose: closeBuyLimit highest close")
            
         elif self.agrBuyHiClose:
            self.closeBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("agrBuyHiClose: closeBuyLimit highest close ")
            
         else: 
            self.closeBuyLimit = self.getLowestClosePrice(numBars)
            self.lg.debug ("default: closeBuyLimit lowest close")
            
      elif self.doHiLo:
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestLoPrice(numBars)
            self.lg.debug ("aggressiveClose: closeBuyLimit highest lo")
            
         elif self.agrBuyHiClose:
            self.closeBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("agrBuyHiClose: closeBuyLimit highest close ")
            
         else:
            self.closeBuyLimit = self.getLowestLoPrice(numBars)
            self.lg.debug("default closeBuyLimit Lowest lo")
            
      elif self.doOpensSeq:
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("doOpensSeq: closeBuyLimit highest open ")
         else:
            self.closeBuyLimit = self.getLowestOpenPrice(numBars)
            self.lg.debug("doOpensSeq: closeBuyLimit lowest open ")
            
      elif self.doClosesSeq:
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("doClosesSeq: closeBuyLimit highest close ")
         else:
            self.closeBuyLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("doClosesSeq: closeBuyLimit lowest close ")

      elif self.doOpensCloses:
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug("doOpensCloses: closeBuyLimit highest open/close ")
         else:
            self.closeBuyLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("doOpensCloses: closeBuyLimit lowest open/close ")
            
      elif self.doOpenCloseSeq:
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug("doClosesSeq: closeBuyLimit highest close/open ")
         else:
            self.closeBuyLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("doClosesSeq: closeBuyLimit lowest close/open ")
            
      else: # Default
         if self.aggressiveClose:
            self.closeBuyLimit = self.getHighestLoPrice(numBars)
            self.lg.debug ("aggressiveClose: closeBuyLimit highest lo")
            
         elif self.agrBuyHiClose:
            self.closeBuyLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("agrBuyHiClose: closeBuyLimit highest close ")
            
         else:
            self.closeBuyLimit = self.getLowestLoPrice(numBars)
            self.lg.debug("default closeBuyLimit Lowest lo")

      self.lg.debug (str(self.closeBuyLimit))
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellLimit(self, numBars):

      if self.doExecuteOnOpen:
         if self.aggressiveClose:
            self.closeSellLimit = self.getLowestHiPrice(numBars)
            self.lg.debug("aggressiveClose: closeSellLimit lowest hi")
            
         elif self.agrSellLoClose:
            self.closeSellLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("agrSellLoClose: closeSellLimit lowest close ")
            
         else:
            self.closeSellLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("doExecuteOnOpen: closeSellLimit highest close")

      elif self.doHiLo:
         if self.aggressiveClose:
            self.closeSellLimit = self.getLowestHiPrice(numBars)
            self.lg.debug("aggressiveClose: closeSellLimit lowest hi")
            
         elif self.agrSellLoClose:
            self.closeSellLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("agrSellLoClose: closeSellLimit lowest close ")
            
         else:
            self.closeSellLimit = self.getHighestHiPrice(numBars)
            self.lg.debug("default closeSellLimit highest hi")

      elif self.doOpensSeq:
         if self.aggressiveOpen:
            self.closeSellLimit = self.getLowestOpenPrice(numBars)
            self.lg.debug("aggressiveClose: openBuyLimit lowest open ")
         else:
            self.closeSellLimit = self.getHighestOpenPrice(numBars)
            self.lg.debug("default: openBuyLimit highest open")
            
      elif self.doClosesSeq:
         if self.aggressiveOpen:
            self.closeSellLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("aggressiveClose: openBuyLimit lowest close ")
         else:
            self.closeSellLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("default: openBuyLimit highest close")

      elif self.doOpensCloses:
         if self.aggressiveClose:
            self.closeSellLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("aggressiveClose doOpensCloses: closeSellLimit lowest open/close ")
         else:
            self.closeSellLimit = self.getHighestClosePrice(numBars)
            self.lg.debug("doOpensCloses: closeSellLimit highest open/close ")

      elif self.doOpenCloseSeq:
         if self.aggressiveOpen:
            self.closeSellLimit = self.getLowestCloseOpenPrice(numBars)
            self.lg.debug("aggressiveClose: openBuyLimit lowest close/open ")
         else:
            self.closeSellLimit = self.getHighestCloseOpenPrice(numBars)
            self.lg.debug("default: openBuyLimit highest close/open ")

      else: # Default
         if self.aggressiveClose:
            self.closeSellLimit = self.getLowestHiPrice(numBars)
            self.lg.debug("aggressiveClose: closeSellLimit lowest hi")
            
         elif self.agrSellLoClose:
            self.closeSellLimit = self.getLowestClosePrice(numBars)
            self.lg.debug("agrSellLoClose: closeSellLimit lowest close ")
            
         else:
            self.closeSellLimit = self.getHighestHiPrice(numBars)
            self.lg.debug("default closeSellLimit highest hi")

      self.lg.debug(str(self.closeSellLimit))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setLimitOnDoubleUpValue(self, stopLimit, inPosType):

      self.lg.debug ("inPosType: " + str(inPosType))
      self.lg.debug ("Original closeBuyLimit: " + str(self.closeBuyLimit))
      self.lg.debug ("Original closeSellLimit: " + str(self.closeSellLimit))
      self.lg.debug ("IN setLimitOnDoubleUpValue stopLimit: " + str(stopLimit))

      # Use the better of the current stop limit or the proposed stop limit

      if inPosType == 2:
         if self.closeSellLimit < stopLimit:
            return
         self.closeSellLimit = stopLimit
      elif inPosType == 1:
         if self.closeBuyLimit > stopLimit:
            return
         self.closeBuyLimit = stopLimit

      self.lg.debug ("OUT closeBuyLimit: " + str(self.closeBuyLimit))
      self.lg.debug ("OUT closeSellLimit: " + str(self.closeSellLimit))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuySellLimits(self):
      
      self.setOpenBuyLimit(self.openBuyBars)
      self.setOpenSellLimit(self.openSellBars)
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuySellLimits(self):
      
      self.setCloseBuyLimit(self.closeBuyBars)
      self.setCloseSellLimit(self.closeSellBars)
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def unsetCloseAvgBarLenLimits(self, barChart, bar):
   
      self.closeBuyLimit = 0.0
      self.closeSellLimit = 0.0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLenLimits(self, barChart, bar, last):
      
      self.setCloseAvgBarLenLimits(barChart, bar, last)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenAvgBarLenLimits(self, last):
      
      self.setAvgBarLenOpenBuyLimit(last)
      self.setAvgBarLenOpenSellLimit(last)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseAvgBarLenLimits(self, last):
      
      self.setAvgBarLenCloseBuyLimit(last)
      self.setAvgBarLenCloseSellLimit(last)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherOpens(self, numBars):
      
      vals = self.openValues
      valsLen = len(vals)

      highest = vals[valsLen - numBars]

      for n in range(valsLen - numBars + 1, valsLen):
         #print ("vals[n] " + str(vals[n]))
         if vals[n] <= highest:
            return 0
         highest = vals[n]
         
      return 1
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherCloses(self, numBars):

      vals = self.closeValues
      valsLen = len(vals)

      highest = vals[valsLen - numBars]

      for n in range(valsLen - numBars + 1, valsLen):
         if vals[n] <= highest:
            return 0
         highest = vals[n]
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherHighs(self, numBars):
      
      vals = self.hiValues
      valsLen = len(vals)

      highest = vals[valsLen - numBars]

      for n in range(valsLen - numBars + 1, valsLen):
         if vals[n] <= highest:
            return 0
         highest = vals[n]
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHigherLows(self, numBars): 

      vals = self.lowValues
      valsLen = len(vals)

      highest = vals[valsLen - numBars]

      for n in range(valsLen - numBars + 1, valsLen):
         if vals[n] <= highest:
            return 0
         highest = vals[n]
         
      return 1
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerHighs(self, numBars): 

      vals = self.hiValues
      valsLen = len(vals)

      lowest = vals[valsLen - numBars]
               
      for n in range(valsLen - numBars + 1, valsLen):
         if vals[n] >= lowest:
            return 0
         lowest = vals[n]
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerLows(self, numBars):

      vals = self.lowValues
      valsLen = len(vals)

      lowest = vals[valsLen - numBars]

      for n in range(valsLen - numBars + 1, valsLen):
         if vals[n] >= lowest:
            return 0
         lowest = vals[n]
         
      return 1
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerOpens(self, numBars):

      vals = self.openValues
      valsLen = len(vals)

      lowest = vals[valsLen - numBars]

      for n in range(valsLen - numBars + 1, valsLen):
         if vals[n] >= lowest:
            return 0
         lowest = vals[n]
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLowerCloses(self, numBars):

      vals = self.closeValues
      valsLen = len(vals)

      lowest = vals[valsLen - numBars]

      for n in range(valsLen - numBars + 1, valsLen):
         if vals[n] >= lowest:
            return 0
         lowest = vals[n]
         
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestHiPrice(self, numBars):

      if numBars > len(self.hiValues):
         return 0

      arrLen = len(self.hiValues)
      price = self.hiValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price < self.hiValues[n]:
            price = self.hiValues[n]
      
      return float(price)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestClosePrice(self, numBars):

      if numBars > len(self.closeValues):
         return 0

      arrLen = len(self.closeValues)
      price = self.closeValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price < self.closeValues[n]:
            price = self.closeValues[n]

      return float(price)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestOpenPrice(self, numBars):

      if numBars > len(self.openValues):
         return 0

      arrLen = len(self.openValues)
      price = self.openValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price < self.openValues[n]:
            price = self.openValues[n]

      return float(price)      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestOpenPrice(self, numBars):

      if numBars > len(self.openValues):
         return 0

      arrLen = len(self.openValues)
      price = self.openValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price > self.openValues[n]:
            price = self.openValues[n]

      return float(price)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestClosePrice(self, numBars):

      if numBars > len(self.closeValues):
         return 0

      arrLen = len(self.closeValues)
      price = self.closeValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price > self.closeValues[n]:
            price = self.closeValues[n]

      return float(price)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestLoPrice(self, numBars):

      if numBars > len(self.lowValues):
         return 0

      arrLen = len(self.lowValues)
      price = self.lowValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price > self.lowValues[n]:
            price = self.lowValues[n]

      return float(price)      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestLoPrice(self, numBars):

      if numBars > len(self.lowValues):
         return 0

      arrLen = len(self.lowValues)
      price = self.lowValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price < self.lowValues[n]:
            price = self.lowValues[n]

      print ("price " + str(price))

      return float(price)      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestHiPrice(self, numBars):

      if numBars > len(self.hiValues):
         return 0

      arrLen = len(self.hiValues)
      price = self.hiValues[arrLen - numBars]

      print ("arrayLen " + str(arrLen))
      print ("numBars " + str(numBars))
      print ("price " + str(price))
      
      for n in range(arrLen - numBars, arrLen):
         if price > self.hiValues[n]:
            price = self.hiValues[n]

      print ("price " + str(price))

      return float(price)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestHiLoPrice(self, numBars):

      loHigh = self.getLowestHiPrice(numBars)
      loLow = self.getLowestLoPrice(numBars)
      
      if loHigh < loLow:
         return loHigh
      else:
         return loLow

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestHiLoPrice(self, numBars):

      hiHigh = self.getHighestHiPrice(numBars)
      hiLow = self.getHighestLoPrice(numBars)
      
      if hiHigh > hiLow:
         return hiHigh
      else:
         return hiLow

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLowestCloseOpenPrice(self, numBars):

      loClose = self.getLowestClosePrice(numBars)
      loOpen = self.getLowestOpenPrice(numBars)
      
      if loClose < loOpen:
         return loClose
      else:
         return loOpen

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getHighestCloseOpenPrice(self, numBars):

      hiClose = self.getHighestClosePrice(numBars)
      hiOpen = self.getHighestOpenPrice(numBars)
      
      if hiClose > hiOpen:
         return hiClose
      else:
         return hiOpen

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def resetLimits(self):
   
      self.d = self.pf.getOrigValues()
      
      self.doHiLoSeq = int(self.d['doHiLoSeq'])
      self.doHiSeq = int(self.d['doHiSeq'])
      self.doLoSeq = int(self.d['doLoSeq'])
      self.doOpenCloseSeq = int(self.d['doOpenCloseSeq'])      
      self.doOpensCloses = int(self.d['doOpensCloses'])      
      self.openBuyBars = int(self.d['openBuyBars'])
      self.closeBuyBars = int(self.d['closeBuyBars'])
      self.openSellBars = int(self.d['openSellBars'])
      self.closeSellBars = int(self.d['closeSellBars'])
      self.tradingDelayBars = int(self.d['tradingDelayBars'])
      self.aggressiveOpen = int(self.d['aggressiveOpen'])
      self.aggressiveClose = int(self.d['aggressiveClose'])
      self.increaseCloseBars = int(self.d['increaseCloseBars'])
      self.increaseCloseBarsMax = int(self.d['increaseCloseBarsMax'])
      self.gainTrailStop = int(self.d['gainTrailStop'])
      self.closePositionFudge = float(self.d['closePositionFudge'])

      print ("doHiLoSeq " + str(self.doHiLoSeq))
      print ("openBuyBars " + str(self.openBuyBars))
      
      # Must have two decision bars for doHiLoSeq
      if self.doHiLoSeq or self.doHiSeq or self.doLoSeq or self.doOpenCloseSeq or \
         self.doExecuteOnOpen or self.doExecuteOnClose or self.doOpensSeq or self.doClosesSeq or self.doHiBuyLoSellSeq:
         
         self.lg.debug ("setting decision bars to 2")

         if self.openBuyBars < 2:
            self.openBuyBars = 2
         if self.openSellBars < 2:
            self.openSellBars = 2
         if self.closeBuyBars < 2:
            self.closeBuyBars = 2
         if self.closeSellBars < 2:
            self.closeSellBars = 2

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTradingDelayBarsDoOnlyTrends(self, timeBar):
      
      # Delay 30 minutes
      self.tradingDelayBars = 30 / timeBar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTradingDelayBars(self):
      
      maxNumTradeBars = self.getMaxNumTradeBars()

#      if self.tradingDelayBars < maxNumTradeBars:
#         self.tradingDelayBars = maxNumTradeBars
#      
#      print ("maxNumTradeBars " + str(maxNumTradeBars))

      if self.doRangeTradeBars > self.tradingDelayBars:
         self.tradingDelayBars = self.doRangeTradeBars
         
      self.lg.debug ("self.tradingDelayBars() " + str(self.tradingDelayBars))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMinTradingDelayBars(self):
      
      self.minTradingDelayBars = self.getMinNumTradeBars()

      self.lg.debug ("self.minTradingDelayBars() " + str(self.minTradingDelayBars))
      self.lg.debug ("self.tradingDelayBars() " + str(self.tradingDelayBars))
      self.lg.debug ("self.doRangeTradeBars() " + str(self.doRangeTradeBars))

#      if self.tradingDelayBars > self.minTradingDelayBars:
#         self.minTradingDelayBars = self.tradingDelayBars
#      
#      if self.doRangeTradeBars > self.minTradingDelayBars:
#         self.minTradingDelayBars = self.doRangeTradeBars
         
      self.lg.debug ("self.minTradingDelayBars() " + str(self.minTradingDelayBars))
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTradingDelayBars(self):
      
      return self.tradingDelayBars

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMinTradingDelayBars(self):
      
      return self.minTradingDelayBars
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMaxNumTradeBars(self):
      
      maxNumBars = self.openBuyBars
      
      if self.openSellBars > maxNumBars:
         maxNumBars = self.openSellBars

      if self.closeBuyBars > maxNumBars:
         maxNumBars = self.closeBuyBars

      if self.closeSellBars > maxNumBars:
         maxNumBars = self.closeSellBars
      
      if self.doRangeTradeBars > maxNumBars:
         maxNumBars = self.doRangeTradeBars

      print (" " + str(maxNumBars))
      
      return maxNumBars

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMinNumTradeBars(self):
      
      minNumBars = self.openBuyBars
      
      if self.openSellBars < minNumBars:
         minNumBars = self.openSellBars

#      if self.closeBuyBars < minNumBars:
#         minNumBars = self.closeBuyBars
#
#      if self.closeSellBars < minNumBars:
#         minNumBars = self.closeSellBars
      
      return minNumBars

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseHiLoValues(self, barChart, bar, tradeBars):
      
      if bar < tradeBars:
         tradeBars = bar
         
      self.openValues = [0.0] * tradeBars   
      self.closeValues = [0.0] * tradeBars  
      self.lowValues = [0.0] * tradeBars
      self.hiValues = [0.0] * tradeBars
   
      self.lg.debug("bar " + str(bar))
      self.lg.debug("tradeBars " + str(tradeBars))
      self.lg.debug("bar - tradeBars " + str(bar - tradeBars))

      try:
         i = 0
         for n in range(bar - tradeBars, bar):
            self.lg.debug("n " + str(barChart[n]))
            self.lg.debug("n and i num " + str(n) + " " + str(i))
            self.openValues[i] = barChart[n][self.op]
            self.closeValues[i] = barChart[n][self.cl]
            self.lowValues[i] = barChart[n][self.lo]
            self.hiValues[i] = barChart[n][self.hi]
            i += 1
      except IndexError as e:
         self.lg.debug ("IndexError " + str(e) + " " + str(i) + " " + str(n))

      self.lg.debug ("open's: " + str(self.openValues))  
      self.lg.debug ("close's: " + str(self.closeValues))  
      self.lg.debug ("low's: " + str(self.lowValues))  
      self.lg.debug ("hi's: " + str(self.hiValues))  

      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setHiLoConditions(self):
   
      self.higherOpensBuyOpen = self.higherOpensSellOpen = 0
      self.higherOpensBuyClose = self.higherOpensSellClose = 0
      self.lowerOpensBuyOpen = self.lowerOpensSellOpen = 0
      self.lowerOpensBuyClose = self.lowerOpensSellClose = 0
      self.higherHighsBuyOpen = self.higherHighsSellOpen = 0
      self.higherHighsBuyClose = self.higherHighsSellClose = 0
      self.higherLowsBuyOpen = self.higherLowsSellOpen = 0
      self.higherLowsBuyClose = self.higherLowsSellClose = 0
      self.lowerHighsBuyOpen = self.lowerHighsSellOpen = 0
      self.lowerHighsBuyClose = self.lowerHighsSellClose = 0
      self.lowerLowsBuyOpen = self.lowerLowsSellOpen = 0
      self.lowerLowsBuyClose = self.lowerLowsSellClose = 0
      self.higherClosesBuyClose = self.higherClosesSellClose = 0
      self.lowerClosesBuyClose = self.lowerClosesSellClose = 0
      self.higherClosesBuyOpen = self.higherClosesSellOpen = 0
      self.lowerClosesBuyOpen = self.lowerClosesSellOpen = 0

      if len(self.openValues) >= self.openBuyBars:
         self.higherOpensBuyOpen = self.isHigherOpens(self.openBuyBars)
         self.lowerOpensBuyOpen = self.isLowerOpens(self.openBuyBars)
         self.higherClosesBuyOpen = self.isHigherCloses(self.openBuyBars)
         self.lowerClosesBuyOpen = self.isLowerCloses(self.openBuyBars)
         self.higherHighsBuyOpen = self.isHigherHighs(self.openBuyBars)
         self.lowerHighsBuyOpen = self.isLowerHighs(self.openBuyBars)
         self.higherLowsBuyOpen = self.isHigherLows(self.openBuyBars)
         self.lowerLowsBuyOpen = self.isLowerLows(self.openBuyBars)

      if len(self.closeValues) >= self.openSellBars:
         self.higherOpensSellOpen = self.isHigherOpens(self.openSellBars)
         self.lowerOpensSellOpen = self.isLowerOpens(self.openSellBars)
         self.higherClosesSellOpen = self.isHigherCloses(self.openSellBars)
         self.lowerClosesSellOpen = self.isLowerCloses(self.openSellBars)
         self.higherHighsSellOpen = self.isHigherHighs(self.openSellBars)
         self.lowerHighsSellOpen = self.isLowerHighs(self.openSellBars)
         self.higherLowsSellOpen = self.isHigherLows(self.openSellBars)
         self.lowerLowsSellOpen = self.isLowerLows(self.openSellBars)

      if len(self.hiValues) >= self.closeBuyBars:
         self.higherOpensBuyClose = self.isHigherOpens(self.closeBuyBars)
         self.lowerOpensBuyClose = self.isLowerOpens(self.closeBuyBars)
         self.higherClosesBuyClose = self.isHigherCloses(self.closeBuyBars)
         self.lowerClosesBuyClose = self.isLowerCloses(self.closeBuyBars)
         self.higherHighsBuyClose = self.isHigherHighs(self.closeBuyBars)
         self.lowerHighsBuyClose = self.isLowerHighs(self.closeBuyBars)
         self.higherLowsBuyClose = self.isHigherLows(self.closeBuyBars)
         self.lowerLowsBuyClose = self.isLowerLows(self.closeBuyBars)

      if len(self.lowValues) >= self.closeSellBars:
         self.higherOpensSellClose = self.isHigherOpens(self.closeSellBars)
         self.lowerOpensSellClose = self.isLowerOpens(self.closeSellBars)
         self.higherClosesSellClose = self.isHigherCloses(self.closeSellBars)
         self.lowerClosesSellClose = self.isLowerCloses(self.closeSellBars)
         self.higherHighsSellClose = self.isHigherHighs(self.closeSellBars)
         self.lowerHighsSellClose = self.isLowerHighs(self.closeSellBars)
         self.higherLowsSellClose = self.isHigherLows(self.closeSellBars)
         self.lowerLowsSellClose = self.isLowerLows(self.closeSellBars)      

      self.lg.debug("isHigherOpens openBuyBars: " + str(self.higherOpensBuyOpen))
      self.lg.debug("isHigherOpens openSellBars: " + str(self.higherOpensSellOpen))
      self.lg.debug("isHigherOpens closeBuyBars: " + str(self.higherOpensBuyClose))
      self.lg.debug("isHigherOpens closeSellBars: " + str(self.higherOpensSellClose))

      self.lg.debug("isLowerOpens openBuyBars: " + str(self.lowerOpensBuyOpen))
      self.lg.debug("isLowerOpens openSellBars: " + str(self.lowerOpensSellOpen))
      self.lg.debug("isLowerOpens closeBuyBars: " + str(self.lowerOpensBuyClose))
      self.lg.debug("isLowerOpens closeSellBars: " + str(self.lowerOpensSellClose))
      
      self.lg.debug("isHigherCloses openBuyBars: " + str(self.higherClosesBuyOpen))
      self.lg.debug("isHigherCloses openSellBars: " + str(self.higherClosesSellOpen))
      self.lg.debug("isHigherCloses closeBuyBars: " + str(self.higherClosesBuyClose))
      self.lg.debug("isHigherCloses closeSellBars: " + str(self.higherClosesSellClose))

      self.lg.debug("isLowerCloses openBuyBars: " + str(self.lowerClosesBuyOpen))
      self.lg.debug("isLowerCloses openSellBars: " + str(self.lowerClosesSellOpen))
      self.lg.debug("isLowerCloses closeBuyBars: " + str(self.lowerClosesBuyClose))
      self.lg.debug("isLowerCloses closeSellBars: " + str(self.lowerClosesSellClose))

      self.lg.debug("isHigherHighs openBuyBars: " + str(self.higherHighsBuyOpen))
      self.lg.debug("isHigherHighs openSellBars: " + str(self.higherHighsSellOpen))
      self.lg.debug("isHigherHighs closeBuyBars: " + str(self.higherHighsBuyClose))
      self.lg.debug("isHigherHighs closeSellBars: " + str(self.higherHighsSellClose))

      self.lg.debug("isHigherLows openBuyBars: " + str(self.higherLowsBuyOpen))
      self.lg.debug("isHigherLows openSellBars: " + str(self.higherLowsSellOpen))
      self.lg.debug("isHigherLows closeBuyBars: " + str(self.higherLowsBuyClose))
      self.lg.debug("isHigherLows closeSellBars: " + str(self.higherLowsSellClose))

      self.lg.debug("isLowerHighs openBuyBars: " + str(self.lowerHighsBuyOpen))
      self.lg.debug("isLowerHighs openSellBars: " + str(self.lowerHighsSellOpen))
      self.lg.debug("isLowerHighs closeBuyBars: " + str(self.lowerHighsBuyClose))
      self.lg.debug("isLowerHighs closeSellBars: " + str(self.lowerHighsSellClose))

      self.lg.debug("isLowerLows openBuyBars: " + str(self.lowerLowsBuyOpen))
      self.lg.debug("isLowerLows openSellBars: " + str(self.lowerLowsSellOpen))
      self.lg.debug("isLowerLows closeBuyBars: " + str(self.lowerLowsBuyClose))
      self.lg.debug("isLowerLows closeSellBars: " + str(self.lowerLowsSellClose))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseHiLoConditions(self, numBars):
   
      self.higherOpens = self.isHigherOpens(numBars)
      self.higherCloses = self.isHigherCloses(numBars)
      
      self.lowerOpens = self.isLowerOpens(numBars)
      self.lowerCloses = self.isLowerCloses(numBars)

      self.higherHighs = self.isHigherHighs(numBars)
      self.higherLows = self.isHigherLows(numBars)
      
      self.lowerHighs = self.isLowerHighs(numBars)
      self.lowerLows = self.isLowerLows(numBars)

      if self.openBuyBars != self.closeBuyBars:
         self.lg.debug("NOTE: values below are not accurate since openBuyBars != closeBuyBars\n but the logic is correct")
      
      self.lg.debug("higherOpens: " + str(self.higherOpens) + " higherCloses: " + str(self.higherCloses))
      self.lg.debug("lowerOpens: " + str(self.lowerOpens) + " lowerCloses: " + str(self.lowerCloses))
      self.lg.debug("higherHighs: " + str(self.higherHighs) + " higherLows: " + str(self.higherLows))
      self.lg.debug("lowerHighs: " + str(self.lowerHighs) + " lowerLows: " + str(self.lowerLows))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setInitialClosePrices(self):

      hiLoDiff = self.openBuyLimit - self.openSellLimit
      
      #print ("Hi Lo diff: " + str(hiLoDiff) + "\n")
      
      if hiLoDiff == 0.0:
         hiLoDiff = 5.0

      if self.positionType == self.buy:
         posGain = self.cn.getCurrentAsk(self.stock) + hiLoDiff * self.profitPctTriggerBar
         posLoss = self.closeBuyLimit - self.closePositionFudge
      elif self.positionType == self.sell:
         posGain = self.cn.getCurrentBid(self.stock) - hiLoDiff * self.profitPctTriggerBar
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
         if self.cn.getCurrentAsk(self.stock) < self.openPositionPrice:
            return 0
      elif self.positionType == self.sell:
         if self.cn.getCurrentBid(self.stock) > self.openPositionPrice:
            return 0

      if not self.revDirty:
         self.topIntraBar = top
         self.revDirty = 1
         self.barCounter = 0
         return 0

      if self.positionType == self.buy:
         if self.cn.getCurrentAsk(self.stock) >= top:
            self.topIntraBar = self.cn.getCurrentAsk(self.stock)
            self.barCounter = 0
            return

         #if top >= self.topIntraBar:
         #  self.topIntraBar = top
         #  return 0

         barLen = top - op

      elif self.positionType == self.sell:
         bottom = top
         if self.cn.getCurrentBid(self.stock) <= bottom:
            self.topIntraBar = self.cn.getCurrentBid(self.stock)
            self.barCounter = 0
            return

         #if top <= self.topIntraBar:
         #  self.topIntraBar = top
         #  return 0

         barLen = op - top

         print ("top " + str(top))
         print ("open " + str(op))
         print ("self.topIntraBar " + str(self.topIntraBar))
         #print ("currentPrice " + str(self.cn.getCurrentAsk(self.stock)))
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
         if sellPrice < self.cn.getCurrentAsk(self.stock):
            return 1
      elif self.positionType == self.sell:
         if sellPrice > self.cn.getCurrentBid(self.stock):
            return 1

      return 0
      





