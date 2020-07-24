'''
trends module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Trends:
   def __init__(self, data, lg, cn, bc, offLine):
      
      self.data = data
      self.lg = lg
      self.cn = cn
      self.bc = bc

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
      self.shortTrendBars = int(data['profileTradeData']['shortTrendBars'])
      self.midTrendBars = int(data['profileTradeData']['midTrendBars'])
      self.longTrendBars = int(data['profileTradeData']['longTrendBars'])
      self.megaTrendBars = int(data['profileTradeData']['megaTrendBars'])
      self.bullTrendValue = float(data['profileTradeData']['bullTrendValue'])
      self.bearTrendValue = float(data['profileTradeData']['bearTrendValue'])
      
      self.offLine = offLine

      self.shortTrend = self.midTrend = self.longTrend = self.megaTrend = 0.0
      
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
   
      if self.isBearMegaTrend():
         self.lg.debug("In isBearMegaTrend")
         return 1

      elif self.isBearLongTrend():
         self.lg.debug("In isBearLongTrend")
         return 1     
      
      elif self.isBearMidTrend():
         self.lg.debug("In isBearMidTrend")
         return 1      
      
      elif self.isBearShortTrend():
         self.lg.debug("In isBearShortTrend")
         return 1
              
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullTrend(self):
   
      if self.isBullMegaTrend():
         self.lg.debug("In isBullMegaTrend")
         return 1

      elif self.isBullLongTrend():
         self.lg.debug("In isBullLongTrend")
         return 1     
      
      elif self.isBullMidTrend():
         self.lg.debug("In isBullMidTrend")
         return 1      
      
      elif self.isBullShortTrend():
         self.lg.debug("In isBullShortTrend")
         return 1
              
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullShortTrend(self):
      
      if self.shortTrend > self.bullTrendValue and self.shortTrend < 3.0:
         print("IN BULL SHORT TREND " + str(self.shortTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullMidTrend(self):
      
      if self.midTrend > self.bullTrendValue and self.midTrend < 3.0:
         print("IN BULL MID TREND " + str(self.midTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullLongTrend(self):
      
      if self.longTrend > self.bullTrendValue and self.longTrend < 3.0:
         print("IN BULL LONG TREND " + str(self.longTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBullMegaTrend(self):
      
      if self.megaTrend > self.bullTrendValue and self.megaTrend < 3.0:
         print("IN BULL MEGA TREND " + str(self.megaTrend))
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearShortTrend(self):
      
      if self.shortTrend < self.bearTrendValue and self.shortTrend >= 3.0:
         print("IN BEAR SHORT TREND " + str(self.shortTrend))
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearMidTrend(self):
      
      if self.midTrend < self.bearTrendValue and self.midTrend >= 3.0:
         print("IN BEAR MID TREND " + str(self.midTrend))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearLongTrend(self):
      
      if self.longTrend < self.bearTrendValue and self.longTrend >= 3.0:
         print("IN BEAR LONG TREND " + str(self.longTrend))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearMegaTrend(self):
      
      if self.megaTrend < self.bearTrendValue and self.megaTrend >= 3.0:
         print("IN BEAR MEGA TREND " + str(self.megaTrend))
         return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBearTrend(self):
      # Bear trend means mid, long and mega trends are bearish
      
      if self.megaTrend >= 3.0 and self.midTrend >= 3.0 and self.longTrend >= 3.0:
         print("IN LONG BEAR TREND")
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendLimits(self, bc, bar):

      self.setShortTrend("short", bc, bar)
      self.setMidTrend("mid", bc, bar)
      self.setLongTrend("long", bc, bar)
      self.setMegaTrend("mega", bc, bar)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setShortTrend(self, trendType, bc, bar):

      if self.shortTrendBars == 0 or bar <= self.shortTrendBars:
         return
            
      self.shortTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, self.shortTrendBars)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMidTrend(self, trendType, bc, bar):
   
      if self.midTrendBars == 0 or bar <= self.midTrendBars:
         return
            
      self.midTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, self.midTrendBars)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setLongTrend(self, trendType, bc, bar):
   
      if self.longTrendBars == 0 or bar <= self.longTrendBars:
         return
   
      self.longTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, self.longTrendBars)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setMegaTrend(self, trendType, bc, bar):
   
      if self.megaTrendBars == 0 or bar <= self.megaTrendBars:
         return
   
      self.megaTrend = 0.0
      
      self.setTrendValues(trendType, bc, bar, self.megaTrendBars)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTrendValues(self, trendType, bc, bar, trendBarLen):
      # 0.0 - no trend; 1.[0-9] - bull; 3.[0-9] - bear
      # the fractional value is the strength 0 weak 9 strong

      lowest = 999999999.99
      highest = 0.0
      loBarPosition = hiBarPosition = i = 0
         
      b = bar - trendBarLen
      
      self.lg.debug("start bar for trend: " + str(b))
      self.lg.debug("trendBarLen: " + str(trendBarLen))
      
      while b < bar: 
         if bc[b][self.cl] < lowest:
            lowest = bc[b][self.cl]
            loBarPosition = b
         if bc[b][self.cl] > highest:
            highest = bc[b][self.cl]
            hiBarPosition = b
            
         b += 1

      self.lg.debug("currentPrice: " + str(self.cn.getCurrentAsk()))
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
      
      if self.offLine:
         date = self.bc.getTimeFromFile(bc, bar)
      
      self.lg.debug(trendType + " Trend: " + str(round(trend, 2)) + " BAR: " + str(bar) + " date: " + str(date))

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

# end trends
