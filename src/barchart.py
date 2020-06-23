'''
bc module
'''

import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Barchart:
   def __init__(self):
   
      # Bar identifiers High, Low, Open, Close, Volume, Length, Date 
      
      self.hi = 0
      self.lo = 1
      self.op = 2
      self.cl = 3
      self.vl = 4
      self.bl = 5
      self.sH = 6 # Session Hi
      self.sL = 7 # Session Li
      self.dt = 8
      
      self.avgBL = 0.0
      self.avgVol = 0
      self.priceIdx = 0
      self.sessionHi = 0
      self.sessionLo = 99999
      
      self.minBar2 = 2
      self.minBar3 = 3
      self.minBar4 = 4
      self.minBar5 = 5
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def init(self):
   
      #      Hi  Lo  Op  Cl  V BarL Date SH SL
      #bc = [[0.0,0.0,0.0,0.0,0,0.0,""]]
      bc = [[0.0,0.0,0.0,0.0,0,0.0,0,0,""]]
   
      return bc
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadInit(self, bc, price, date, volume, bar):
   
      #self.appendBar(bc)

      bc[bar][self.op] = bc[bar][self.cl] = bc[bar][self.hi] = bc[bar][self.lo] = price
      bc[bar][self.dt] = date

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadBeginBar(self, bc, price, bid, volume, bar):
   
      if price > bc[bar][self.hi]:
         bc[bar][self.hi] = price
         
      if price < bc[bar][self.lo]:
         bc[bar][self.lo] = bid
               
      bc[bar][self.vl] = volume

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadEndBar(self, bc, price, date, bar):
   
      bc[bar][self.cl] = price
      bc[bar][self.dt] = date            
      bc[bar][self.bl] = round((bc[bar][self.hi] - bc[bar][self.lo]), 2)
      self.loadHiLoBar(bc, bar)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadHiLoBar(self, bc, bar):
            
      if bc[bar][self.hi] > self.sessionHi:
         self.sessionHi = bc[bar][self.hi]
         bc[bar][self.sH] = 1
         
      if bc[bar][self.lo] < self.sessionLo:
         self.sessionLo = bc[bar][self.lo]
         bc[bar][self.sL] = 1
         
#      if bc[bar][self.hi] > bc[bar - 1][self.hi]:
#         bc[bar][self.sH] = 1
#         
#      if bc[bar][self.lo] < bc[bar - 1][self.lo]:
#         bc[bar][self.sL] = 1
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgVol(self, bc, numBars):
   
      if numBars == 0:
         return 0
         
      n = avgVol = 0
      totalVol = 0
      
      while n < numBars:
         totalVol += int(bc[n][self.vl])
         n += 1

      self.avgVol = round(totalVol / numBars, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgVol(self):
            
      return self.avgVol  
          
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTimeFromFile(self, bc, bar): 
         
      bc[bar][self.dt]

      return (bc[bar][self.dt])

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLen(self, bc, numBars):
   
      if numBars == 0:
         return 0
         
      n = 0
      totalBL = 0.0

      while n < numBars:
         totalBL += bc[n][self.bl]
         n += 1
            
      self.avgBL = round(totalBL / numBars, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgBarLen(self):
   
      return self.avgBL
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getPriceRange(self):
   
      return self.avgBL
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextPrice(self, path):
   
      price = 0
      
      with open(path, 'r') as pcData:
         price = pcData[self.priceIdx].line.strip("\n")
         self.priceIdx += 1

      return price
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def read(self, path, bc):
   
      ctr = 0
      with open(path, 'r') as bcData:
         for line in bcData:
            line = line.strip("\n")
            bar = line.split(",")
                        
            if ctr != 0:
               bc.append(bar)
               
            bc[ctr][self.hi] = float(bar[self.hi])
            bc[ctr][self.lo] = float(bar[self.lo])
            bc[ctr][self.op] = float(bar[self.op])
            bc[ctr][self.cl] = float(bar[self.cl])
            bc[ctr][self.vl] = int(bar[self.vl])
            bc[ctr][self.bl] = float(bar[self.bl])
            bc[ctr][self.sH] = str(bar[self.sH])
            bc[ctr][self.sL] = str(bar[self.sL])
            bc[ctr][self.dt] = str(bar[self.dt])
            ctr += 1
     
      return ctr

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initWrite(self, path):
                  
      self.path2m = path.replace("active", "active_2m")
      self.path3m = path.replace("active", "active_3m")
      self.path4m = path.replace("active", "active_4m")
      self.path5m = path.replace("active", "active_5m")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write(self, bc, path, bar, doAllMinutes):
   
      with open(path, 'a+') as bcData:
         bcData.write('%s,' % str(bc[bar][self.hi]))
         bcData.write('%s,' % str(bc[bar][self.lo]))
         bcData.write('%s,' % str(bc[bar][self.op]))
         bcData.write('%s,' % str(bc[bar][self.cl]))
         bcData.write('%s,' % str(bc[bar][self.vl]))
         bcData.write('%s,' % str(bc[bar][self.bl]))
         bcData.write('%s,' % str(bc[bar][self.sH]))
         bcData.write('%s,' % str(bc[bar][self.sL]))
         bcData.write('%s' % bc[bar][self.dt] + "\n")
         
      if (doAllMinutes):
         if bar == 0:
            return
         if (bar % self.minBar2) == 0:
            self.write2m(bc, bar)
         if (bar % self.minBar3) == 0:
            self.write3m(bc, bar)
         if (bar % self.minBar4) == 0:
            self.write4m(bc, bar)
         if (bar % self.minBar5) == 0:
            self.write5m(bc, bar)

      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write2m(self, bc, bar):
         
      with open(self.path2m, 'a+') as bcData:
         bcData.write('%s,' % str(bc[bar][self.hi]))
         bcData.write('%s,' % str(bc[bar][self.lo]))
         bcData.write('%s,' % str(bc[bar][self.op]))
         bcData.write('%s,' % str(bc[bar][self.cl]))
         bcData.write('%s,' % str(bc[bar][self.vl]))
         bcData.write('%s,' % str(bc[bar][self.bl]))
         bcData.write('%s,' % str(bc[bar][self.sH]))
         bcData.write('%s,' % str(bc[bar][self.sL]))
         bcData.write('%s' % bc[bar][self.dt] + "\n")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write3m(self, bc, bar):
   
      with open(self.path3m, 'a+') as bcData:
         bcData.write('%s,' % str(bc[bar][self.hi]))
         bcData.write('%s,' % str(bc[bar][self.lo]))
         bcData.write('%s,' % str(bc[bar][self.op]))
         bcData.write('%s,' % str(bc[bar][self.cl]))
         bcData.write('%s,' % str(bc[bar][self.vl]))
         bcData.write('%s,' % str(bc[bar][self.bl]))
         bcData.write('%s,' % str(bc[bar][self.sH]))
         bcData.write('%s,' % str(bc[bar][self.sL]))
         bcData.write('%s' % bc[bar][self.dt] + "\n")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write4m(self, bc, bar):
   
      with open(self.path4m, 'a+') as bcData:
         bcData.write('%s,' % str(bc[bar][self.hi]))
         bcData.write('%s,' % str(bc[bar][self.lo]))
         bcData.write('%s,' % str(bc[bar][self.op]))
         bcData.write('%s,' % str(bc[bar][self.cl]))
         bcData.write('%s,' % str(bc[bar][self.vl]))
         bcData.write('%s,' % str(bc[bar][self.bl]))
         bcData.write('%s,' % str(bc[bar][self.sH]))
         bcData.write('%s,' % str(bc[bar][self.sL]))
         bcData.write('%s' % bc[bar][self.dt] + "\n")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write5m(self, bc, bar):
   
      with open(self.path5m, 'a+') as bcData:
         bcData.write('%s,' % str(bc[bar][self.hi]))
         bcData.write('%s,' % str(bc[bar][self.lo]))
         bcData.write('%s,' % str(bc[bar][self.op]))
         bcData.write('%s,' % str(bc[bar][self.cl]))
         bcData.write('%s,' % str(bc[bar][self.vl]))
         bcData.write('%s,' % str(bc[bar][self.bl]))
         bcData.write('%s,' % str(bc[bar][self.sH]))
         bcData.write('%s,' % str(bc[bar][self.sL]))
         bcData.write('%s' % bc[bar][self.dt] + "\n")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def appendBar(self, bc):
   
      bc.append([0.0,0.0,0.0,0.0,0,0.0,0,0,""])

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def displayLastNBars(self, bc, numBars):
   
      bcLen = len(bc)
      
      if bcLen < numBars:
         ctr = 0
      else:
         ctr = bcLen - numBars
      
      print ("\n")
      while ctr < bcLen:            
         print("BAR: " + str(ctr) + " " + str(bc[ctr]))
         ctr += 1
      print ("\n")
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadValues(self, bc, numBars):
   
      bcLen = len(bc)
      
      if bcLen < numBars:
         ctr = bcLen
      else:
         ctr = bcLen - numBars
      
      print ("\n")
      while ctr < bcLen:            
         print("BAR: " + str(ctr) + " " + str(bc[ctr]))
         ctr += 1
      print ("\n")
            

# end bc
