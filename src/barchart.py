'''
bc module
'''

import random
import os.path

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Barchart:
   def __init__(self, path, offLine, timeBar):
   
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
      self.avgVolTime = 0
      self.priceIdx = 0
      self.sessionHi = 0
      self.sessionLo = 99999
      
      self.minBar2 = 2
      self.minBar3 = 3
      self.minBar4 = 4
      self.minBar5 = 5
      
      self.barCountInPosition = 0
      self.timeBarValue = 0

      if offLine:
         self.barChart = self.init()
         ctr = self.read(path, self.barChart, timeBar)
         
         #print ("ctr: " + str(ctr))
         #print ("self.barChart: " + str(self.barChart))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def init(self):
   
      #      Hi  Lo  Op  Cl  V BarL Date SH SL
      bc = [[0.0,0.0,0.0,0.0,0,0.0,0,0,""]]
      
      return bc
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def appendBar(self, bc):
   
      bc.append([0.0,0.0,0.0,0.0,0,0.0,0,0,""])

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadFirstBar(self, bc, date, bar, bid, ask, last, vol):
   
      # We use the ask initially since etrade sets the last to be the day 
      # before close which could be a big gap away.
       
      bc[bar][self.op] = ask
      bc[bar][self.cl] = ask
      bc[bar][self.hi] = ask
      bc[bar][self.lo] = bid
      bc[bar][self.dt] = date
      bc[bar][self.vl] = vol
      
      print ("very first bar " + str(bc[bar]))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadInitBar(self, bc, date, bar, bid, ask, last, vol):
   
      bc[bar][self.op] = last      
      bc[bar][self.cl] = last
      bc[bar][self.hi] = last
      bc[bar][self.lo] = last
      bc[bar][self.dt] = date
      bc[bar][self.vl] = vol
      
      print ("b bc[bar] " + str(bc[bar]))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadBar(self, bc, vol, bar, bid, ask, last):
   
#      if ask > bc[bar][self.hi]:
#         bc[bar][self.hi] = ask
#               
#      if bid < bc[bar][self.lo]:
#         bc[bar][self.lo] = bid
         
      if last > bc[bar][self.hi]:
         bc[bar][self.hi] = last
               
      if last < bc[bar][self.lo]:
         bc[bar][self.lo] = last
               
      bc[bar][self.vl] = vol

      print ("m bc[bar] " + str(bc[bar]))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadEndBar(self, bc, date, bar, bid, ask, last, vol):
   
      bc[bar][self.cl] = last
      bc[bar][self.bl] = round(bc[bar][self.hi] - bc[bar][self.lo], 2)
      
      if last > bc[bar][self.hi]:
         bc[bar][self.hi] = last
               
      if last < bc[bar][self.lo]:
         bc[bar][self.lo] = last

      bc[bar][self.vl] = vol

      self.loadHiLoBar(bc, bar)
      print ("e bc[bar] " + str(bc[bar]))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def loadHiLoBar(self, bc, bar):
            
      if bc[bar][self.hi] > self.sessionHi:
         self.sessionHi = bc[bar][self.hi]
         bc[bar][self.sH] = 1
         
      if bc[bar][self.lo] < self.sessionLo:
         self.sessionLo = bc[bar][self.lo]
         bc[bar][self.sL] = 1
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getPreviousBarVol(self, bars, timeBar):
      
      # if timeBar = 3 bars = 14 look at bars 12, 13, 14 

      if timeBar > bars:
         return 0

      totalVol = 0
      idx = (bar - timeBar) + 1
      
      while idx <= bars:
         totalVol += self.priceArr[idx][self.vl]
         idx += 1
         print("getPreviousBarVol totalVol: " + str(totalVol))
               
      return totalVol

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgVol(self, bc, bar):
   
      if bar == 0:
         self.avgVol = bc[0][self.vl]
         print("setAvgVol bar: " + str(self.avgVol))
         return

      # Ignore first bar  since we never act on the first bar
      # and it is always the highest in vol? set n = 1
      
      n = 0
      totalVol = 0
            
      while n <= bar:
         totalVol += int(bc[n][self.vl])
         n += 1

      self.avgVol = round(totalVol / (bar + 1), 2)

      print("setAvgVol:  bar: " + str(self.avgVol) + " " + str(bar))
      print("totalVol: " + str(totalVol))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAvgVolTime(self, bc, bar, timeBar, currIdx):
   
      # if timeBar = 3 bar = 33 look at all bar divied up by the timebar 

      #if timeBar > bar:
      #   return 0
      
      print(" bar: " + str(bar)) 
      print("currIdx: " + str(currIdx)) 
         
      if bar == 0:
        self.avgVolTime = bc[0][self.vl]
        return
      
      print("avgVol: " + str(avgVol))   
      print("volCtr: " + str(volCtr))   
      print("avgVol / volCtr: " + str(avgVol / volCtr)) 
      
      self.avgVolTime =  round(avgVol / volCtr, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgVol(self):
            
      return self.avgVol  
          
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgVolTime(self):
            
      return self.avgVolTime
          
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTimeFromFile(self, bc, bar): 
         
      hi = bc[bar][self.hi]
      lo = bc[bar][self.lo]
      
      print ("bc[bar] :" + str(bc[bar])) 
      
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
   def getFirstBarLen(self, bc, bar):

      return bc[bar][self.bl]
            
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
               
            if ctr == 0:
               bid, ask, last = self.getBidAskLastLineOne(path)
               bc[ctr][self.op] = float(last)
               bc[ctr][self.hi] = float(bid)
               bc[ctr][self.lo] = float(ask)
            else:
               bc[ctr][self.op] = float(bar[self.op])
               bc[ctr][self.hi] = float(bar[self.hi])
               bc[ctr][self.lo] = float(bar[self.lo])

            #bc[ctr][self.hi] = float(bar[self.hi])
            #bc[ctr][self.lo] = float(bar[self.lo])
            #bc[ctr][self.op] = float(bar[self.op])
            
            bc[ctr][self.cl] = float(bar[self.cl])
            bc[ctr][self.vl] = int(bar[self.vl])
            bc[ctr][self.bl] = float(bar[self.bl])
            bc[ctr][self.sH] = int(bar[self.sH])
            bc[ctr][self.sL] = int(bar[self.sL])
            bc[ctr][self.dt] = str(bar[self.dt])
            ctr += 1
     
      return ctr

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

            if bcCtr == 0:
               bid, ask, last = self.getBidAskLastLineOne(path)
               bc[bcCtr][self.op] = last
               #bc[bcCtr][self.hi] = float(bid)
               #bc[bcCtr][self.lo] = float(ask)
            #else:
               #bc[bcCtr][self.op] = float(bar[self.op])

            if lineCtr % minutes == 0:
               bc.append(bar)
               
               print (str(bar[self.hi]))
               
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
                  
               print ("lineCtr: " + str(lineCtr))

               #bc[bcCtr][self.op] = round(op, 2)
               #bc[bcCtr][self.cl] = float(bar[self.cl])
               if bcCtr != 0:
                  bc[bcCtr][self.op] = float(bar[self.op])
               bc[bcCtr][self.cl] = float(cl)
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
                  
                  # Use the avg of the bid + ask for the open
                  # since Etrade uses the prev days close as today's open
                  
               #op = float(bar[self.op])
               cl = float(bar[self.cl])
               #hi = float(bar[self.hi])

               print (str(bar[self.hi]))

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
     
         print ("Min BC: ")
         for b in range(bcCtr):
            print (str(bc[b]))
            
      return bcCtr

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBidAskLastLineOne(self, path):
      
      # Change path to price path
      # get the avg of the bid and ask on line one

      firstLineVals = []
      
      sym = os.path.basename(path).strip(".bc").strip("active")      
      pPath = os.path.dirname(os.path.dirname(path)) + "/prices/active" + sym + ".pr"
      
      with open(pPath, 'r') as pp:
         firstLineVals = pp.readline().split(",")
         
#      print ("firstLineVals " + str(firstLineVals))
#
#      print (str(firstLineVals[0]))
#      print (str(firstLineVals[1]))
#
#      avg = (float(firstLineVals[0]) + float(firstLineVals[1])) / 2.0
#      print (str(avg))
      bid = float(firstLineVals[0])
      ask = float(firstLineVals[1])
      last = float(firstLineVals[2])
      
      return bid, ask, last
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTimeBarValue(self, timeBar):
      
      self.timeBarValue = timeBar
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTimeBarValue(self):
      
      return int(self.timeBarValue)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNumSessionLos(self, bc, bar):
      
      if bar == 0:
         return 0

      sessionLos = 0
      
      while bar >= 0:
         if bc[bar][self.sL] == 1:
            sessionLos += 1
         bar -= 1
      
      return sessionLos

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNumSessionHis(self, bc, bar):
      
      if bar == 0:
         return 0

      sessionHis = 0
      
      while bar >= 0:
         if bc[bar][self.sH] == 1:
            sessionHis += 1
         bar -= 1
      
      return sessionHis

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSessionHiAndBar(self, bc, bar):
      
      if bar == 0:
         return 0

      while bar >= 0:
         if bc[bar][self.sH] == 1:
            return bc[bar][self.hi], bar
         bar -= 1
      
      return 0.0, 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSessionLoAndBar(self, bc, bar):

      if bar == 0:
         return 0
         
      while bar >= 0:
         if bc[bar][self.sL] == 1:
            return bc[bar][self.lo], bar
         bar -= 1
      
      return 0.0, 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isSessionHi(self, bc, bar):
      
      if bc[bar][self.sH] == 1:
         return 1
      
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isSessionLo(self, bc, bar):

      if bc[bar][self.sL] == 1:
         return 1
      
      return 0

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
   def initWrite(self, path):
                  
      self.path2m = path.replace("active", "active2m")
      self.path3m = path.replace("active", "active3m")
      self.path4m = path.replace("active", "active4m")
      self.path5m = path.replace("active", "active5m")

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeFD(self, bc, pathFD, bar):
   
      pathFD.write('%s,' % str(bc[bar][self.hi]))
      pathFD.write('%s,' % str(bc[bar][self.lo]))
      pathFD.write('%s,' % str(bc[bar][self.op]))
      pathFD.write('%s,' % str(bc[bar][self.cl]))
      pathFD.write('%s,' % str(bc[bar][self.vl]))
      pathFD.write('%s,' % str(bc[bar][self.bl]))
      pathFD.write('%s,' % str(bc[bar][self.sH]))
      pathFD.write('%s,' % str(bc[bar][self.sL]))
      pathFD.write('%s' % bc[bar][self.dt] + "\n")
         
      return
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def write(self, bc, path, bar):
   
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
         
#      if (doAllMinutes):
#         if bar == 0:
#            return
#         if (bar % self.minBar2) == 0:
#            self.write2m(bc, bar)
#         if (bar % self.minBar3) == 0:
#            self.write3m(bc, bar)
#         if (bar % self.minBar4) == 0:
#            self.write4m(bc, bar)
#         if (bar % self.minBar5) == 0:
#            self.write5m(bc, bar)

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

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getStocksFromBCDir(path):
   
      stocks = []
   
      for rootPath, directories, paths in os.walk(path):
         for path in paths:
            if path.endswith(".bc"):
               if os.stat(rootPath + "/" + path).st_size > 10000:
                  stockName = path.replace("active","") 
                  stockName = stockName.replace(".bc","")
                  if stockName not in stocks:
                     #print ("stockName: " + str(stockName))
                     stocks.append(stockName)      
      
      return stocks
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTimeStampFromBarchartFile(self, bar):
   
      #return ("junk")
      return self.barChart[bar][self.dt]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMinuteBarHiLoLen(self, timeBar, minutes, testDir):
      
      highest = 0.0
      lowest = 99999999999.0
      
#      if timeBar > 1:
#         for bar in range(timeBar * minutes):
#            hi = self.barChart[bar][self.hi]
#            lo = self.barChart[bar][self.lo]
#            print ("hi: " + str(hi))
#            print ("lo: " + str(lo))
#            if hi > highest:
#               highest = hi;
#            if lo < lowest:
#               lowest = lo
#         barLen = round(highest - lowest, 2)
#         print ("highest: " + str(highest))
#         print ("lowest: " + str(lowest))
#      else:

      barLen = self.barChart[0][self.bl]
         
      print ("barLen: " + str(barLen))
      
      return barLen
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getMinuteBarAvgs(self, sym, minutes, testDir):
   
      assert(testDir)
      
      #print ("testDir " + testDir)
      
      allTestDays = []
      for day in os.walk(testDir):
         allTestDays = day[1]
         break
      
      #print ("allTestDays " + str(allTestDays))
      
      if isinstance(sym, str):
         syms = [sym]
            
      totBarAvg = {}
      barLens = 0.0
      for day in allTestDays:
         totBarAvg[day] = {}
         for s in syms:
            lines = []
            barLens = 0.0
            totBarAvg[s] = []
            firstBarLen = 0
            path = testDir + day + "/bc/active" + s + ".bc"
            if not os.path.exists(path):
               continue
                              
            if os.stat(path).st_size < 10:
               continue
            
            with open(path, 'r') as baFile:
               lines = baFile.readlines()
      
            hi = lo = 0.0
            # Need to subtract the lo from the hi for num minutes
            for n in range(minutes):
               hiVal = 0.0
               loVal = 0.0
               hiVal = (lines[n].split(',')[0])
               loVal = (lines[n].split(',')[1])
               
               if float(hiVal) == 0.0 or float(loVal) == 0.0:
                  continue
               
               try:
                  if n == 0:
                     hi = hiVal         
                     lo = loVal
                  else:
                     if hi < hiVal:
                        hi = hiVal
                     if lo > loVal:
                        lo = loVal
               except TypeError as e:
                  print ("TypeError bad value!!! ")
                  print ("day " + str(day))
                  print ("hiVal " + str(hiVal))
                  print ("loVal " + str(loVal))
                  print ("hi " + str(hi))
                  print ("lo " + str(lo))
                  
            totBarAvg[day][s] = float(hi) - float(lo)
            
      avgFirstMinuteValues = {}

      hi = 0
      lo = 999999999999

      # Ignore the high and lo for determining a good avg
      for key, value in totBarAvg.items():
         if len(value) == 0:
            continue
         for k, v in value.items():
            if k == s:
               if v > hi:
                  hi = v
               if v < lo:
                  lo = v

      for s in syms:
         avgFirstMinuteValues[s] = [0.0, 0, 0,0]
         for key, value in totBarAvg.items():
            if len(value) == 0:
               continue
            for k, v in value.items():
               if k == s:
                  print ("v " + str(v))
                  if v == hi or v == lo:
                     continue
                  avgFirstMinuteValues[s][0] += v
                  avgFirstMinuteValues[s][1] += 1
                  avgFirstMinuteValues[s][2] = avgFirstMinuteValues[s][0] / avgFirstMinuteValues[s][1]
                  
      
      print ("HHII " + str(hi))
      print ("LLOO " + str(lo))
      return avgFirstMinuteValues

# end bc
