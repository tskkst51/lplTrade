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
      
      self.barCountInPosition = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def init(self):
   
      #      Hi  Lo  Op  Cl  V BarL Date SH SL
      bc = [[0.0,0.0,0.0,0.0,0,0.0,0,0,""]]
      
      return bc
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadInitBar(self, bc, date, bar, bid, ask, last, vol):
      print ("loadInitBar bar : " + str(bar))
      bc[bar][self.op] = last
      bc[bar][self.cl] = last
      bc[bar][self.hi] = ask
      bc[bar][self.lo] = bid
      bc[bar][self.dt] = date
      bc[bar][self.vl] = vol

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadBar(self, bc, vol, bar, bid, ask, last):
   
      if ask > bc[bar][self.hi]:
         bc[bar][self.hi] = ask
               
      if bid < bc[bar][self.lo]:
         bc[bar][self.lo] = bid
               
      bc[bar][self.vl] = vol

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadEndBar(self, bc, date, bar, bid, ask, last, vol):
   
      bc[bar][self.cl] = last
      bc[bar][self.bl] = round(bc[bar][self.hi] - bc[bar][self.lo], 2)
      
      if last > bc[bar][self.hi]:
         bc[bar][self.hi] = last
               
      if last < bc[bar][self.lo]:
         bc[bar][self.lo] = last

      self.loadHiLoBar(bc, bar)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadHiLoBar(self, bc, bar):
            
      if bc[bar][self.hi] > self.sessionHi:
         self.sessionHi = bc[bar][self.hi]
         bc[bar][self.sH] = 1
         
      if bc[bar][self.lo] < self.sessionLo:
         self.sessionLo = bc[bar][self.lo]
         bc[bar][self.sL] = 1
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgVol(self, bc, bars):
   
      if bars < 1:
         return 0

      # Ignore 1st bar
      n = 0
      totalVol = 0
            
      while n < bars:
         totalVol += int(bc[n][self.vl])
         n += 1

      self.avgVol = round(totalVol / bars, 2)

      print("setAvgVol bar: " + str(self.avgVol) + " " + str(bars))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgVol(self):
            
      return self.avgVol  
          
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTimeFromFile(self, bc, bar): 
         
      bc[bar][self.dt]

      return (bc[bar][self.dt])

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgBarLen(self, bc, bars):
   
      if bars == 0:
         return 0

      n = 0
      totalBL = 0.0

      while n < bars:
         totalBL += bc[n][self.bl]
         n += 1
            
      self.avgBL = round(totalBL / bars, 2)
      
      print ("self.avgBL :" + str(self.avgBL)) 

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgBarLen(self):
      
      return self.avgBL
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getPriceRange(self):
   
      return self.avgBL
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextPrice(self, path):
   
      price = 0
      
      print ("self.priceIdx " + str(self.priceIdx))
      
      with open(path, 'r') as pcData:
         price = pcData[self.priceIdx].line.strip("\n")
         self.priceIdx += 1

      return price
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Create a bar chart every n minutes
   def readMin(self, path, bc, minutes):
   
      lo = 99999
      hi = op = cl = bl = 0.0
      sH = sL = vl = 0
      dt = ""
      bcCtr = dirty = 0
      lineCtr = 1

      with open(path, 'r') as bcData:
         for line in bcData:
            line = line.strip("\n")
            bar = line.split(",")
                    
            if lineCtr % minutes == 0:
               bc.append(bar)
               
               if hi < float(bar[self.hi]):
                  hi = float(bar[self.hi])
                  
               if lo > float(bar[self.lo]):
                  lo = float(bar[self.lo])
                  
               vl += int(bar[self.vl])
               
               if int(bar[self.sH]) == 1:
                  sH = int(bar[self.sH])
                  
               if int(bar[self.sL]) == 1:
                  sL = int(bar[self.sL])
               
               bc[bcCtr][self.hi] = round(hi, 2)
               bc[bcCtr][self.lo] = round(lo, 2)
               bc[bcCtr][self.op] = round(op, 2)
               bc[bcCtr][self.cl] = float(bar[self.cl])
               bc[bcCtr][self.vl] = vl
               bc[bcCtr][self.bl] = round(hi - lo, 2)
               
               bc[bcCtr][self.sH] = sH
               bc[bcCtr][self.sL] = sL
               bc[bcCtr][self.dt] = str(bar[self.dt])
               
               lo = 99999
               hi = op = cl = bl = 0.0
               sH = sL = vl = 0
               dt = ""
               dirty = 0
               bcCtr += 1
               
            else:
               if not dirty:
                  dirty += 1
                  op = float(bar[self.op])
                  
               if hi < float(bar[self.hi]):
                  hi = float(bar[self.hi])
                  
               if lo > float(bar[self.lo]):
                  lo = float(bar[self.lo])
                  
               vl += int(bar[self.vl])
               
               if int(bar[self.sH]) == 1:
                  sH = int(bar[self.sH])
                  
               if int(bar[self.sL]) == 1:
                  sL = int(bar[self.sL])
                  
            lineCtr += 1
     
      return bcCtr

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSessionHi(self, bc, barCtr):
      
      if barCtr == 0:
         return 0.0, 0

      bar = barCtr
      while bar >= 0:
         if bc[bar][self.sH] == 1:
            print("sessionHi " + str(bc[bar][self.hi]))
            return bc[bar][self.hi], bar
         bar -= 1
      
      return 0, 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSessionLo(self, bc, barCtr):

      if barCtr == 0:
         return 0, 0
         
      bar = barCtr
      while bar >= 0:
         if bc[bar][self.sL] == 1:
            print("sessionLo " + str(bc[bar][self.lo]))
            return bc[bar][self.lo], bar
         bar -= 1
      
      return 0.0, 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def fixSessionHiLo(self, path):
      
      highest = 0.0
      lowest = 99999.99
      tmpPath = path + "tmp"
      
      with open(tmpPath, 'a+') as bcDataTmp:
         with open(path, 'r') as bcData:
            for line in bcData:
               line = line.strip("\n")
               bar = line.split(",")
               
               hi = float(bar[self.hi])
               if hi > highest:
                  highest = hi
                  bar[self.sH] = 1

               lo = float(bar[self.lo])
               if lo < lowest:
                  lowest = lo
                  bar[self.sL] = 1
                  
               bcDataTmp.write('%s,' % str(bar[self.hi]))
               bcDataTmp.write('%s,' % str(bar[self.lo]))
               bcDataTmp.write('%s,' % str(bar[self.op]))
               bcDataTmp.write('%s,' % str(bar[self.cl]))
               bcDataTmp.write('%s,' % str(bar[self.vl]))
               bcDataTmp.write('%s,' % str(bar[self.bl]))
               bcDataTmp.write('%s,' % str(bar[self.sH]))
               bcDataTmp.write('%s,' % str(bar[self.sL]))
               bcDataTmp.write('%s' % bar[self.dt] + "\n")
         
         
      # Enbale this after verification of above
      #os.remove(path)      
      #os.rename(tempPath, path)
      
      return 
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def read(self, path, bc, timeBar):
            
      if timeBar > 1:
         return self.readMin(path, bc, timeBar)

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
            bc[ctr][self.sH] = int(bar[self.sH])
            bc[ctr][self.sL] = int(bar[self.sL])
            bc[ctr][self.dt] = str(bar[self.dt])
            ctr += 1
     
      return ctr

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initWrite(self, path):
                  
      self.path2m = path.replace("active", "active2m")
      self.path3m = path.replace("active", "active3m")
      self.path4m = path.replace("active", "active4m")
      self.path5m = path.replace("active", "active5m")

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
   def displayLastNBars(self, bc, bars):
   
      bcLen = len(bc)
      
      if bcLen < bars:
         ctr = 0
      else:
         ctr = bcLen - bars
      
      print ("\n")
      while ctr < bcLen:            
         print("BAR: " + str(ctr) + " " + str(bc[ctr]))
         ctr += 1
      print ("\n")
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadValues(self, bc, bars):
   
      bcLen = len(bc)
      
      if bcLen < bars:
         ctr = bcLen
      else:
         ctr = bcLen - bars
      
      print ("\n")
      while ctr < bcLen:            
         print("BAR: " + str(ctr) + " " + str(bc[ctr]))
         ctr += 1
      print ("\n")
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def resetBarsInPosition(self):

      self.barCountInPosition = 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setBarsInPosition(self):

      self.barCountInPosition += 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBarsInPosition(self):
   
      return self.barCountInPosition 
      

# end bc
