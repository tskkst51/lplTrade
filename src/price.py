'''
price module
'''

import random
import os.path

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Price:
   def __init__(self, a, cn, usePricesFromFile=0, offLine=0):
   
      self.a = a
      self.cn = cn
      self.upff = usePricesFromFile
      self.offLine = offLine
      
      self.priceArr = [0.0]
      self.idxArr = [0]
      self.nextBar = 0
      self.priceIdx = 0
      
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
         
      i = 0
      for line in lines:
         # Skip the first and second index numbers
         line = line.replace("\n", "")
         line = line.split(",")
                     
         self.priceArr[i] = float(line[0])
         self.idxArr[i] = int(line[1])
         self.priceArr.append(0.0)
         self.idxArr.append(0)
         i += 1
      
      return i
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextPrice(self, bc, numBars, bar):
            
      price = 0
            
      # Get price from file, randomly or live
      if self.offLine:      
         
         # From file
         if self.upff:
            price = self.priceArr[self.priceIdx]
            self.priceIdx += 1
         # Randomly
         else:
            price = self.getRandomPrice(bc, numBars, bar)

      # Live      
      else:
         price = self.cn.getCurrentPrice()
         
      return float(price)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isNextBar(self, bar):
      
      if not self.offLine:
         return 0
      
      #if bar == 0:
      #   print ("self.priceArr self.priceIdx " + str(self.priceArr) + " " + str(self.priceIdx))

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
   def write(self, path, price, bar):

      with open(path, "a+", encoding="utf-8") as priceFile:
         priceFile.write ('%s' % str(price) + "," + str(bar) + "\n")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setNextBar(self):
   
      self.nextBar += 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextBar(self):
   
      return self.nextBar
            
# end price
