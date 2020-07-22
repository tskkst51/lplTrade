'''
price module
'''

import random
import os.path

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Price:
   def __init__(self, a, cn, usePricesFromFile=0, offLine=0, startTime=0):
   
      self.a = a
      self.cn = cn
      self.upff = usePricesFromFile
      self.offLine = offLine
      self.startTime = startTime
      
      # Price Array bid, ask
      self.priceArr = [0.0,0.0]
      self.idxArr = [0]
      self.nextBar = 0
      self.priceIdx = 0
      
      self.minBar2 = 2
      self.minBar3 = 3
      self.minBar4 = 4
      self.minBar5 = 5
      
      self.next2mBar = 0
      self.next3mBar = 0
      self.next4mBar = 0
      self.next5mBar = 0
      
      self.min2Ctr = 0
      self.min3Ctr = 0
      self.min4Ctr = 0
      self.min5Ctr = 0
      
      self.numLines = 0
      self.lastToken = 99999.99
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def skipFirstBar(self, numPrices):

      i = 0
      while i < numPrices:
         if self.idxArr[i] == 0:
            self.priceIdx += 1
            i += 1
         else:
            break
            
      self.nextBar = 2

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initPriceBuffer(self, path):

      with open(path, 'r') as pcData:
         lines = pcData.readlines()
         
      self.numLines = len(lines)
      
      for line in lines:
         line = line.replace("\n", "")
         line = line.split(",")

         self.priceArr.append([float(line[0]), float(line[1])])
         self.idxArr.append(int(line[2]))
                
      return self.numLines
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLastToken(self):
   
      return self.lastToken
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextPrice(self, bc, numBars, bar):
            
      last = bid = ask = 0.0
            
      # Get price from file, randomly or live
      if self.offLine:      
         
         # From file
         if self.upff:
            if self.priceIdx >= self.numLines:
               return self.getLastToken(), 0, 0
                              
            last = ask = self.priceArr[self.priceIdx][0]
            bid = self.priceArr[self.priceIdx][1]
            self.priceIdx += 1
         # Randomly
         else:
            price = self.getRandomPrice(bc, numBars, bar)
            bid = ask = last = price

      # Live      
      else:
         last = self.cn.getLastTrade()
         bid = self.cn.getCurrentBid()
         ask = self.cn.getCurrentAsk()
         
      return float(last), float(bid), float(ask)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isNextBar(self, bar):
      
      if not self.offLine:
         return 0
      
      if self.priceIdx >= self.numLines:
         return self.getLastToken()

      if self.getNextBar() == self.idxArr[self.priceIdx]:
         self.setNextBar()
         return 1
         
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getRandomPrice(self, bc, numBars, bar):

      hi = self.a.getHighestHiBarPrice(numBars, bc, bar)
      lo = self.a.getLowestLoBarPrice(numBars, bc, bar)
            
      return round(random.uniform(lo, hi), 2)      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write2m(self, ask, bid, bar):
                     
      # Start time + 2 minutes
      
      if bar == 0:
         with open(self.path2m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(bar) + "\n")
      else:
         if (bar % self.minBar2) == 0:
            if bar != self.next2mBar:
               self.min2Ctr += 1
               self.next2mBar = bar
               
         with open(self.path2m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(self.min2Ctr) + "\n")
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write3m(self, ask, bid, bar):
   
      # Start time + 3 minutes
      
      if bar == 0:
         with open(self.path3m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(bar) + "\n")
      else:
         if (bar % self.minBar3) == 0:
            if bar != self.next3mBar:
               self.min3Ctr += 1
               self.next3mBar = bar
               
         with open(self.path3m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(self.min3Ctr) + "\n")
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write4m(self, ask, bid, bar):

      # Start time + 4 minutes
      
      if bar == 0:
         with open(self.path4m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(bar) + "\n")
      else:
         if (bar % self.minBar4) == 0:
            if bar != self.next4mBar:
               self.min4Ctr += 1
               self.next4mBar = bar
               
         with open(self.path4m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(self.min4Ctr) + "\n")
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write5m(self, ask, bid, bar):

      # Start time + 5 minutes
      
      if bar == 0:
         with open(self.path5m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(bar) + "\n")
      else:
         if (bar % self.minBar5) == 0:
            if bar != self.next5mBar:
               self.min5Ctr += 1
               self.next5mBar = bar
               
         with open(self.path5m, "a+", encoding="utf-8") as priceFile:
            priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(self.min5Ctr) + "\n")
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initWrite(self, path):
                  
      self.path2m = path.replace("active", "active2m")
      self.path3m = path.replace("active", "active3m")
      self.path4m = path.replace("active", "active4m")
      self.path5m = path.replace("active", "active5m")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write(self, path, ask, bid, bar, doAllMinutes):

      with open(path, "a+", encoding="utf-8") as priceFile:
         priceFile.write ('%s' % str(ask) + "," + str(bid) + "," + str(bar) + "\n")
         
      if doAllMinutes:
         self.write2m(ask, bid, bar)
         self.write3m(ask, bid, bar)
         self.write4m(ask, bid, bar)
         self.write5m(ask, bid, bar)
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setNextBar(self):
   
      self.nextBar += 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextBar(self):
   
      return self.nextBar
            
# end price
