'''
trends module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Trends:
   def __init__(self, data, lg, cn, ba, offLine, stock=""):
      
      self.data = data
      self.lg = lg
      self.cn = cn
      self.ba = ba

      self.hi = 0
      self.lo = 1
      self.op = 2
      self.cl = 3
      self.vl = 4
      self.bl = 5
      self.sH = 6
      self.sL = 7
      self.dt = 8

      # Use trend indicators to increase amount to trade
      self.timeBar = int(data['profileTradeData']['timeBar'])
      self.shortTrendBars = int(data['profileTradeData']['shortTrendBars'])
      self.midTrendBars = int(data['profileTradeData']['midTrendBars'])
      self.longTrendBars = int(data['profileTradeData']['longTrendBars'])
      self.megaTrendBars = int(data['profileTradeData']['megaTrendBars'])
      self.superTrendBars = int(data['profileTradeData']['superTrendBars'])
      self.bullTrendValue = float(data['profileTradeData']['bullTrendValue'])
      self.bearTrendValue = float(data['profileTradeData']['bearTrendValue'])
      self.bullSessionValue = float(data['profileTradeData']['bullSessionValue'])
      self.bearSessionValue = float(data['profileTradeData']['bearSessionValue'])
      
      self.offLine = offLine

      self.shortTrend = self.midTrend = self.longTrend = self.megaTrend = self.superTrend = 0.0
      
      self.stock = stock
      
      if self.timeBar > 1:
         self.setTrendBars(self.timeBar)
         
      self.sessionBullTrend = 0
      self.sessionBearTrend = 0

      self.sessionHiPrice = 0.0
      self.sessionLiPrice = 0.0

      self.setBullSessionValue(self.bullSessionValue)
      self.setBearSessionValue(self.bearSessionValue)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendBars(self, timeBar):
   
      if self.timeBar == 5:
         self.shortTrendBars = 4
         self.midTrendBars = 8
         self.longTrendBars = 16
         self.megaTrendBars = 32
         self.superTrendBars = 64
      elif self.timeBar == 4:
         self.shortTrendBars = 5
         self.midTrendBars = 10
         self.longTrendBars = 20
         self.megaTrendBars = 40
         self.superTrendBars = 80
      elif self.timeBar == 3:
         self.shortTrendBars = 6
         self.midTrendBars = 12
         self.longTrendBars = 24
         self.megaTrendBars = 48
         self.superTrendBars = 96
      elif self.timeBar == 2:
         self.shortTrendBars = 7
         self.midTrendBars = 14
         self.longTrendBars = 28
         self.megaTrendBars = 56
         self.superTrendBars = 112

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isShortMidBullLongMegaBear(self):
   
      if self.isBullShortTrend():
         if self.isBullMidTrend():
            if self.isBearLongTrend():
               if self.isBearMegaTrend():
                  self.lg.debug("In isShortMidBullLongMegaBear")
                  return 1
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isShortMidBearLongMegaBull(self):
   
      if self.isBearShortTrend():
         if self.isBearMidTrend():
            if self.isBullLongTrend():
               if self.isBullMegaTrend():
                  self.lg.debug("In isShortMidBearLongMegaBull")
                  return 1
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isShortBullMidLongMegaBear(self):
   
      if self.isBullShortTrend():
         if self.isBearMidTrend():
            if self.isBearLongTrend():
               if self.isBearMegaTrend():
                  self.lg.debug("In isShortBullMidLongMegaBear")
                  return 1
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isShortBearMidLongMegaBull(self):
   
      if self.isBearShortTrend():
         if self.isBullMidTrend():
            if self.isBullLongTrend():
               if self.isBullMegaTrend():
                  self.lg.debug("In isShortBearMidLongMegaBull")
                  return 1
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearTrend(self):
         
      retCode = 0

#      if self.isBearSuperTrend():
#         self.lg.debug("In isBearSuperTrend")
#         retCode += 1

      if self.isBearMegaTrend():
         self.lg.debug("In isBearTrend")
         retCode += 2

      if self.isBearLongTrend():
         self.lg.debug("In isBearLongTrend")
         retCode += 3
      
      if self.isBearMidTrend():
         self.lg.debug("In isBearMidTrend")
         retCode += 4
      
      if self.isBearShortTrend():
         self.lg.debug("In isBearShortTrend")
         retCode += 5
              
      return retCode

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullTrend(self):
   
      retCode = 0

#      if self.isBearSuperTrend():
#         self.lg.debug("In isBearSuperTrend")
#         retCode += 1

      if self.isBullMegaTrend():
         self.lg.debug("In isBullMegaTrend")
         retCode += 2

      if self.isBullLongTrend():
         self.lg.debug("In isBullLongTrend")
         retCode += 3
      
      if self.isBullMidTrend():
         self.lg.debug("In isBullMidTrend")
         retCode += 4
      
      if self.isBullShortTrend():
         self.lg.debug("In isBullShortTrend")
         retCode += 5
              
      return retCode

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullTrendClose(self):
   
      retCode = 0

#      if self.isBullSuperTrend():
#         self.lg.debug("In isBullSuperTrend")
#         retCode += 1

      if self.isBullMegaTrend():
         self.lg.debug("In isBullMegaTrend")
         retCode += 1

      if self.isBullLongTrend():
         self.lg.debug("In isBullLongTrend")
         retCode += 1
      
      if self.isBullMidTrend():
         self.lg.debug("In isBullMidTrend")
         retCode += 1
      
      if self.isBullShortTrend():
         self.lg.debug("In isBullShortTrend")
         retCode += 1
              
      return retCode

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearTrendClose(self):
         
      retCode = 0

#      if self.isBearSuperTrend():
#         self.lg.debug("In isBearSuperTrend")
#         retCode += 1

      if self.isBearMegaTrend():
         self.lg.debug("In isBearMegaTrend")
         retCode += 1

      if self.isBearLongTrend():
         self.lg.debug("In isBearLongTrend")
         retCode += 1
      
      if self.isBearMidTrend():
         self.lg.debug("In isBearMidTrend")
         retCode += 1
      
      if self.isBearShortTrend():
         self.lg.debug("In isBearShortTrend")
         retCode += 1
              
      return retCode

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullShortTrend(self):
      
      if self.shortTrend >= self.bullTrendValue and self.shortTrend <= 2.0:
         self.lg.debug("IN BULL SHORT TREND " + str(self.shortTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullMidTrend(self):
      
      if self.midTrend >= self.bullTrendValue and self.midTrend <= 2.0:
         self.lg.debug("IN BULL MID TREND " + str(self.midTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullLongTrend(self):
      
      if self.longTrend >= self.bullTrendValue and self.longTrend <= 2.0:
         self.lg.debug("IN BULL LONG TREND " + str(self.longTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullMegaTrend(self):
      
      if self.megaTrend >= self.bullTrendValue and self.megaTrend <= 2.0:
         self.lg.debug("IN BULL MEGA TREND " + str(self.megaTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullSuperTrend(self):
      
      if self.superTrend >= self.bullTrendValue and self.superTrend <= 2.0:
         self.lg.debug("IN BULL SUPER TREND " + str(self.superTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearShortTrend(self):
      
      if self.shortTrend < self.bearTrendValue and self.shortTrend >= 3.0:
         self.lg.debug("IN BEAR SHORT TREND " + str(self.shortTrend))
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearMidTrend(self):
      
      self.lg.debug("self.midTrend: " + str(self.midTrend))
      self.lg.debug("self.bearTrendValue: " + str(self.bearTrendValue))
      
      if self.midTrend <= self.bearTrendValue and self.midTrend >= 3.0:
         self.lg.debug("IN BEAR MID TREND " + str(self.midTrend))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearLongTrend(self):
      
      if self.longTrend < self.bearTrendValue and self.longTrend >= 3.0:
         self.lg.debug("IN BEAR LONG TREND " + str(self.longTrend))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearMegaTrend(self):
      
      if self.megaTrend < self.bearTrendValue and self.megaTrend >= 3.0:
         self.lg.debug("IN BEAR MEGA TREND " + str(self.megaTrend))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearSuperTrend(self):
      
      if self.superTrend < self.bearTrendValue and self.superTrend >= 3.0:
         self.lg.debug("IN BEAR SUPER TREND " + str(self.superTrend))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendLimits(self, bc, bar, bid, ask):
            
      self.setShortTrend("short", bc, bar, bid, ask)
      self.setMidTrend("mid", bc, bar, bid, ask)
      self.setLongTrend("long", bc, bar, bid, ask)
      self.setMegaTrend("mega", bc, bar, bid, ask)
      self.setSuperTrend("super", bc, bar, bid, ask)
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullSessionTrend(self):
   
      if self.sessionBullTrend == 1:
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearSessionTrend(self):
   
      if self.sessionBearTrend == 1:
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setSessionInPositionTrend(self, trendValue):

      self.inPosSessionBullTrend = self.inPosSessionBearTrend = 0.0
      # FINISH!!      
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBullSessionValue(self, trendValue):
   
      self.bullSessionValue = trendValue

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBearSessionValue(self, trendValue):
   
      self.bearSessionValue = trendValue

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBullSessionValue(self):
   
      return float(self.bullSessionValue)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBearSessionValue(self):
   
      return float(self.bearSessionValue)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setSessionTrend(self, trendValue):

      self.sessionBullTrend = self.sessionBearTrend = 0

      self.lg.debug("bullSessionValue: " + str(self.bullSessionValue))
      self.lg.debug("bearSessionValue: " + str(self.bearSessionValue))

      if trendValue > self.bullSessionValue and trendValue <= 2.0:
         self.lg.debug("IN BULL SESSION TREND " + str(trendValue))
         #self.sessionBullTrend = trendValue
         self.sessionBullTrend = 1
      elif trendValue < self.bearSessionValue and trendValue >= 3.0:
         self.lg.debug("IN BEAR SESSION TREND " + str(trendValue))
         #self.sessionBearTrend = trendValue
         self.sessionBearTrend = 1
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSessionTrendValue(self, sH, sHbar, sL, sLbar, price):

      priceRange = pctInTrend = pctInTrendRnd = trend = 0.0
      
      if sH == sL:
         return 0.5
      elif sLbar < sHbar:
         # Bull trend
         trend = 1.00
      elif sLbar > sHbar:
         # Bear trend
         trend = 3.00

      #price = self.cn.getCurrentAsk(self.stock)
      
      pctInTrend = pctInTrendRnd = 0.0
      penetration = 0.0

      # Simple first
      if price > sH:
         pctInTrend = 0.99
      elif price < sL:
         pctInTrend = 0.00
      else:
         # Get the price range of bars
         if sH > sL:
            priceRange = sH - sL
            penetration = sH - price
         else:
            priceRange = sL - sH
            penetration = sL - price
            
         pctInTrend = 1.0 - (penetration / priceRange)
            
            
      pctInTrendRnd = round(pctInTrend, 2)
      
      self.lg.debug("session priceRange: " + str(priceRange))
      self.lg.debug("session pctInTrend: " + str(pctInTrend))
      self.lg.debug("session penetration: " + str(penetration))
      self.lg.debug("session pctInTrendRnd: " + str(pctInTrendRnd))
      self.lg.debug("trend + pctInTrendRnd: " + str(trend + pctInTrendRnd))

      return trend + pctInTrendRnd
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setShortTrend(self, trendType, bc, bar, bid, ask):
      
      trendValue = 0

      if self.shortTrendBars == 0 or bar < self.shortTrendBars:
         return
            
      if bar <= self.shortTrendBars:
         trendValue = bar
      else:
         trendValue = self.shortTrendBars

      self.shortTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, trendValue, bid, ask)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMidTrend(self, trendType, bc, bar, bid, ask):
   
      trendValue = 0

      if self.midTrendBars == 0 or bar < self.shortTrendBars:
         return
            
      if bar <= self.midTrendBars:
         trendValue = bar
      else:
         trendValue = self.midTrendBars

      self.midTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, trendValue, bid, ask)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setLongTrend(self, trendType, bc, bar, bid, ask):
      
      trendValue = 0
      
      if self.longTrendBars == 0 or bar < self.midTrendBars:
         return
            
      self.lg.debug("bar: " + str(bar))
      self.lg.debug("self.longTrendBars: " + str(self.longTrendBars))

      if bar <= self.longTrendBars:
         trendValue = bar
      else:
         trendValue = self.longTrendBars

      self.longTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, trendValue, bid, ask)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMegaTrend(self, trendType, bc, bar, bid, ask):
      
      trendValue = 0
      
      if self.megaTrendBars == 0 or bar < self.longTrendBars:
         return
            
      if bar <= self.megaTrendBars:
         trendValue = bar
      else:
         trendValue = self.megaTrendBars

      self.megaTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, trendValue, bid, ask)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setSuperTrend(self, trendType, bc, bar, bid, ask):
      
      trendValue = 0
      
      if self.superTrendBars == 0 or bar < self.megaTrendBars:
         return
            
      if bar <= self.superTrendBars:
         trendValue = bar
      else:
         trendValue = self.superTrendBars

      self.superTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, trendValue, bid, ask)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTrendValues(self):

      return self.shortTrend, self.midTrend , self.longTrend , self.megaTrend, self.superTrend 
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendValues(self, trendType, bc, bar, trendBarLen, bid, ask):
      # 0.0 - no trend; 1.[0-9] - bull; 3.[0-9] - bear
      # the fractional value is the strength 0 weak 9 strong

      # Unitl we get to a superTrend continue to use the start bar from bar 1
      
      lowest = 999999999.99
      highest = 0.0
      loBarPosition = hiBarPosition = i = b = 0
      loBartime = hiBarTime = ""
      
      #ask = self.cn.getCurrentAsk(self.stock)
      #bid = self.cn.getCurrentBid(self.stock)

      if trendType == "short":
         if bar <= self.shortTrendBars:
            b = 0
         else:
            b = bar - trendBarLen
      elif trendType == "mid":
         if bar <= self.midTrendBars:
            b = 0
         else:
            b = bar - trendBarLen
      elif trendType == "long":
         if bar <= self.longTrendBars:
            b = 0
         else:
            b = bar - trendBarLen
      elif trendType == "mega":
         if bar <= self.megaTrendBars:
            b = 0
         else:
            b = bar - trendBarLen
      elif trendType == "super":
         if bar <= self.superTrendBars:
            b = 0
         else:
            b = bar - trendBarLen
      
      self.lg.debug("start bar for trend: " + str(b))
      self.lg.debug("trendBarLen: " + str(trendBarLen))
      
      while b < bar: 
         if bc[b][self.lo] < lowest:
            lowest = bc[b][self.lo]
            loBarPosition = b
            loBartime = bc[b][self.dt]
         if bc[b][self.hi] > highest:
            highest = bc[b][self.hi]
            hiBarPosition = b
            hiBartime = bc[b][self.dt]
            
         b += 1

      self.lg.debug("currentPrice: " + str(ask))
      self.lg.debug("LOWEST: " + str(lowest))
      self.lg.debug("HIGHEST: " + str(highest))
      self.lg.debug("loBarPosition: " + str(loBarPosition) + " " + loBartime)
      self.lg.debug("hiBarPosition: " + str(hiBarPosition) + " " + hiBartime)

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
      if ask > highest:
         pctInTrend = 0.9999
      elif bid < lowest:
         pctInTrend = 0.0000
      else:
         # Get the price range of bars
         if highest > lowest:
            priceRange = highest - lowest
            penetration = highest - ask
         else:
            priceRange = lowest - highest
            penetration = lowest - bid
            self.lg.debug("priceRange: " + str(priceRange))
         
         pctInTrend = 1.0 - (penetration / priceRange)

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
      elif trendType == "super":
         self.superTrend = trend

      date = self.cn.getTimeStamp()
      
      if self.offLine:
         date = self.ba.getTimeFromFile(bc, bar)
      
      self.lg.debug(trendType + " Trend: " + str(round(trend, 2)) + " BAR: " + str(bar) + " date: " + str(date) + "\n")

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
   def unsetSuperTrend(self):

      self.superTrend = 0.0

# end trends
