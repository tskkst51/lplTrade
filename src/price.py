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
      
      self.priceIdx = 0
      self.idxFromFile = 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getIdxFromFile(self):

      return self.idxFromFile

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextPrice(self, bc, numBars, path, bar):
            
      price = 0
      
      with open(path, 'r') as bcData:
         for line in bcData:
            line = line.strip("\n")
            bar = line.split(",")


      # Randomly
      if self.offLine:         
         # From file
         if self.upff:
            if os.path.getsize(path) == 0:
               return 0.0
               
            with open(path, 'r') as pcData:
               lines = pcData.readlines()
               
               ctr = 0
               for line in lines:
                  if ctr == self.priceIdx:
                     line = line.split(",")
                     price = line[0]
                     self.idxFromFile = int(line[1])
                     break
                  ctr += 1
                  
               self.priceIdx += 1

               #price = int(line[0])
               #self.idxFromFile = int(line[1])

               #price = float(priceLines[self.priceIdx])
               #priceIdx = float(priceLines[self.priceIdx])
         else:
            price = self.getRandomPrice(bc, numBars, bar)

      # Live      
      else:
         price = self.cn.getCurrentPrice()
         
      return float(price)

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
   def getPriceIdx(self):

      return self.priceIdx

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getIdxFromFile(self):

      return self.idxFromFile
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doNextBar(self, offLine):
   
      if not offLine:
         return 0
         
      if not self.upff:
         return 0

      value = self.priceIdx % self.upff
      
      print ("self.priceIdx " + str(self.priceIdx)  + " self.upff " + str(self.upff))
      print ("self.priceIdx mod self.upff " + str(value) )
      if self.priceIdx % self.upff == 0:
         return 1
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def doNextBarFromFile(self, offLine, bar):
   
      if not offLine:
         return 0
         
      if not self.upff:
         return 0
      
      if self.getIdxFromFile() > bar:
         return 1

      return 0
      
# end price
