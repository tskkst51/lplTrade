'''
price module
'''

import random
import os.path
import os
import io
from time import sleep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Price:
   def __init__(self, cn, offLine=0):
   
      self.cn = cn
      self.offLine = offLine
      
      self.priceArr = []
      self.idxArr = [0]
      self.priceChangeArr = []
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
      
      self.ask = 0
      self.bid = 1
      self.last = 2
      self.vl = 3
      self.bar = 4
      self.startIdx = 0
      self.lastPriceInfo = 0
      self.dirty = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setStartPriceIdx(self, idx):

      print ("startIdx " + str(self.startIdx))
      self.startIdx = idx

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getStartPriceIdx(self):
      
      return self.startIdx

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentPriceIdx(self):
      
      return self.priceIdx - 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentBarNum(self):
      
      return self.idxArr[self.priceIdx]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getVolPriceTimeIdx(self, idx, timeBar):
      
      totalVol = 0
      bar = 1
      
      while bar <= timeBar:
         idx -= bar
         totalVol += self.priceArr[idx][self.vl]
         
      return totalVol

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getVolPriceIdx(self, idx):
      
      return self.priceArr[idx][self.vl]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLastPriceIdx(self, idx):
      
      return self.priceArr[idx][self.last]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAskPriceIdx(self, idx):
      
      return self.priceArr[idx][self.ask]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBidPriceIdx(self, idx):
      
      return self.priceArr[idx][self.bid]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def findStartPriceIdx(self, numPrices, timeBar):

      i = 0
      while i < numPrices:
      
         print ("self.priceArr[self.priceIdx] " + str(self.priceArr[i]))
         print ("self.idxArr[i] " + str(self.idxArr[i]))
         print ("timeBar " + str(timeBar))

         if self.idxArr[i] < timeBar:
            self.priceIdx += 1
            i += 1
         else:
            self.setStartPriceIdx(self.priceIdx)
            break
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initPriceBufferFD(self, pathFD):

      # path is already open if slave mode
      
      if pathFD.closed:
         return 0
         
      lines = pathFD.readlines()
         
      self.numLines = len(lines)

      for line in lines:
         line = line.replace("\n", "")
         line = line.split(",")

         self.priceArr.append([float(line[self.bid]), float(line[self.ask]), float(line[self.last]), int(line[self.vl])])
         self.idxArr.append(int(line[self.bar]))
         
#      print ("priceArr LLL " + str(self.priceArr))
#      print ("idxArr LLL " + str(self.idxArr))
#      print ("priceIdx LLL " + str(self.priceIdx))
      
      return self.numLines
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initPriceBuffer(self, path):

      with open(path, 'r') as pcData:
         lines = pcData.readlines()
         
      self.numLines = len(lines)

      for line in lines:
         line = line.replace("\n", "")
         line = line.split(",")

         self.priceArr.append([float(line[self.bid]), float(line[self.ask]), float(line[self.last]), int(line[self.vl])])
         self.idxArr.append(int(line[self.bar]))
         
      return self.numLines
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLastToken(self):
   
      return self.lastToken
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getVolTime(self):
   
      # Get the volume at the time in bar
      # Use for trigger confirmation
      pass
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgVolTime(self, minChart, bc, bar):
   
      # Get the average volume at the time in bar
      # Use for trigger confirmation
      pass      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAvgVol(self, bar):
   
      # Get the average volume at the index
      
      if bar < 1:
         return 0
      
      totalVol = volIdx = b = 0
      
      idx = self.getStartPriceIdx()
      curIdx = self.getCurrentPriceIdx()

      print ("idx " + str(idx))
      print ("curIdx " + str(curIdx))
      
      #for b in range(1, bar):
      while b <= bar:
         volIdx = curIdx - (b * idx)
         if volIdx < 0:
            break
         print ("volIdx " + str(volIdx))
         print ("b " + str(b))
         print ("bar " + str(bar))
         totalVol += self.getVolPriceIdx(volIdx) 
         print ("getVolPriceIdx(volIdx) " + str(self.getVolPriceIdx(volIdx)))
         print ("totalVol " + str(totalVol))
         b += 1
      
      print ("totalVol / bar " + str(totalVol / bar))
      
      return int(round(totalVol,2) / bar)
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAverageAskChange(self, bar):
   
      if bar < 2:
         return 0
      
      previousPrice = totalChange = 0.0
      numPrices = 1
      
      idx = self.getStartPriceIdx()
      curIdx = self.getCurrentPriceIdx()
            
      previousPrice = self.priceArr[idx][0]
      idx += 1
      
      while idx < curIdx:
         priceChange = round(previousPrice - self.priceArr[idx][self.ask], 2)
         previousPrice = round(self.priceArr[idx][0], 2)
         if priceChange < 0:
            priceChange = priceChange*-1
         totalChange = round(totalChange + priceChange, 2)
         numPrices += 1
         idx += 1
            
      print ("total Ask Change / numPrices " + str(totalChange / numPrices))
      
      return round(totalChange / numPrices, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAverageLastChangeArr(self, bar):
   
      if bar < 1:
         return 0
      
      idx = 0
      totalChange = 0.0
         
      print ("barr " + str(bar))
      
      while idx < bar:
         totalChange += self.priceChangeArr[idx]
         idx += 1
      
      print ("totalChange / idx " + str(totalChange / idx))
      
      return round(totalChange / idx, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAverageLastChange(self, bar):
   
      if bar < 2:
         return 0
      
      previousPrice = totalChange = 0.0
      numPrices = 1
      
      idx = self.getStartPriceIdx()
      curIdx = self.getCurrentPriceIdx()
            
      previousPrice = self.priceArr[idx][0]
      idx += 1
      
      while idx < curIdx:
         priceChange = previousPrice - self.priceArr[idx][self.last]
         previousPrice = self.priceArr[idx][self.last]
         if priceChange < 0:
            priceChange = priceChange*-1
         totalChange = totalChange + priceChange
         numPrices += 1
         idx += 1
            
      print ("total Last Change / numPrices " + str(totalChange / numPrices))
      
      return round(totalChange / numPrices, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAverageBidChange(self, bar):
   
      if bar < 2:
         return 0
      
      previousPrice = totalChange = 0.0
      numPrices = 1
      
      idx = self.getStartPriceIdx()
      curIdx = self.getCurrentPriceIdx()
            
      previousPrice = self.priceArr[idx][1]
      idx += 1
      
      print ("idx " + str(idx))
      print ("curIdx " + str(curIdx))
      print ("previousPrice " + str(previousPrice))
      
      while idx < curIdx:
         priceChange = round(previousPrice - self.priceArr[idx][self.bid], 2)
         previousPrice = round(self.priceArr[idx][0], 2)
         if priceChange < 0:
            priceChange = priceChange*-1
         totalChange = round(totalChange + priceChange, 2)
         numPrices += 1
         idx += 1
         
      print ("total Bid Change / numPrices " + str(totalChange / numPrices))
      
      return round(totalChange / numPrices, 2)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setPriceChangeArr(self, bar):
   
      previousPrice = totalChange = 0.0
      numPrices = 1
      priceIdx = bar - 1
      
      if bar == 1:
         idx = 0
      else:
         idx = self.getStartPriceIdx()
         
      curIdx = self.getCurrentPriceIdx()
            
      previousPrice = self.priceArr[idx][1]
      idx += 1
      
      print ("idx " + str(idx))
      print ("curIdx " + str(curIdx))
      print ("previousPrice " + str(previousPrice))      
      
      self.priceChangeArr.append([])
      
      while idx < curIdx:
         # Add up the prices, fill array
         
         priceChange = previousPrice - self.priceArr[idx][self.last]
         previousPrice = self.priceArr[idx][0]
         if priceChange < 0:
            priceChange = priceChange*-1
         totalChange = totalChange + priceChange
         numPrices += 1
         idx += 1
         
      print ("total Bid Change / numPrices " + str(totalChange / numPrices))
      
      self.priceChangeArr[priceIdx] = round(totalChange / numPrices, 2)

      print ("self.priceChangeArr[priceIdx] " + str(self.priceChangeArr[priceIdx]))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextPriceArr(self, serviceValues):
   
      if self.offLine:
#         print ("self.priceIdx " + str(self.priceIdx))
#         print ("self.priceArr[self.priceIdx] " + str(self.priceArr[self.priceIdx]))
#         print ("numLines] " + str(self.numLines))
                           
         ask = last = self.priceArr[self.priceIdx][self.ask]
         bid = self.priceArr[self.priceIdx][self.bid]
         last = self.priceArr[self.priceIdx][self.last]
         vl = self.priceArr[self.priceIdx][self.vl]
         self.priceIdx += 1
         
         if self.priceIdx >= self.numLines - 10:
            last = self.getLastToken()
      else:
      
         bid = serviceValues[self.bid]
         ask = serviceValues[self.ask]
         last = serviceValues[self.last]
         vl = serviceValues[self.vl]
         
      return float(bid), float(ask), float(last), int(vl) 
          
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextPrice(self, bc, numBars, bar, stock):
            
      last = bid = ask = 0.0
      vl = 0 
      
      # Get price from file, randomly or live
      if self.offLine:      
         
         print ("self.priceIdx " + str(self.priceIdx)	)
         print ("self.priceArr[self.priceIdx] " + str(self.priceArr[self.priceIdx]))
                           
         ask = self.priceArr[self.priceIdx][self.ask]
         bid = self.priceArr[self.priceIdx][self.bid]
         last = self.priceArr[self.priceIdx][self.last]
         vl = self.priceArr[self.priceIdx][self.vl]
         self.priceIdx += 1
         
         if self.priceIdx >= self.numLines - 10:
            last = self.getLastToken()
      # Live      
      else:
         last = self.cn.getLastTrade(stock)
         bid = self.cn.getCurrentBid(stock)
         ask = self.cn.getCurrentAsk(stock)
         vl = self.cn.getCurrentVolume(stock)
         
      return float(bid), float(ask), float(last), int(vl)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def readNextPriceLine(self, fd, path):

      line = ""
      
      priceInfo = 0
      
      priceInfo = os.stat(path)
      #print ("size " + str(priceInfo.st_size))
      #print ("self.lastPriceInfo " + str(self.lastPriceInfo))

      while True:
         if priceInfo.st_size == 0:
            sleep(0.01)
         else:
            break

      if not self.dirty:
         self.lastPriceInfo = priceInfo.st_size
         self.dirty += 1
         
      while priceInfo.st_size > 0:
         priceInfo = os.stat(path)
         if priceInfo.st_size > self.lastPriceInfo:
            self.lastPriceInfo = priceInfo.st_size
         
            line = fd.readline()
            break
                     
      line = line.replace("\n", "")
      line = line.split(",")

      self.priceArr.append([float(line[self.bid]), float(line[self.ask]), float(line[self.last]), int(line[self.vl])])
      self.idxArr.append(int(line[self.bar]))
         
      ask = float(self.priceArr[self.priceIdx][self.ask])
      bid = float(self.priceArr[self.priceIdx][self.bid])
      last = float(self.priceArr[self.priceIdx][self.last])
      vl = int(self.priceArr[self.priceIdx][self.vl])
      self.priceIdx += 1

      return bid, ask, last, vl

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLastBar(self, timeBar):

      print ("isLastBar offline: " + str(self.offLine))

      if self.offLine:
         if self.priceIdx >= self.numLines:
            return self.getLastToken()
   
         print ("self.getNextBar() " + str(self.getNextBar()))
         print ("self.idxArr[self.priceIdx] " +  str(self.idxArr[self.priceIdx]))
         
         if self.getNextBar() == self.idxArr[self.priceIdx]:
            return 1
      
      else: # Live
         print ("self.getNextBar() " + str(self.getNextBar()))
         print ("self.idxArr[self.priceIdx] " +  str(self.idxArr[self.priceIdx]))
         
         if self.getNextBar() == self.idxArr[self.priceIdx]:
            return 1

      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   def isLastBarSlave(self, timeBar):
#      
#      if not self.offLine:
#         return 0
#      
#      print ("self.getNextBar() " + str(self.getNextBar()))
#      print ("self.idxArr[self.priceIdx] " +  str(self.idxArr[self.priceIdx]))
#      
#      if self.getNextBar() == self.idxArr[self.priceIdx]:
#         return 1
#         
#      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isNextBar(self, timeBar):
      
      print ("offline: " + str(self.offLine))
      
      if self.offLine:
         if self.priceIdx >= self.numLines:
            return self.getLastToken()
   
         print ("self.getNextBar() " + str(self.getNextBar()))
         print ("self.idxArr[self.priceIdx] " +  str(self.idxArr[self.priceIdx]))
         
         if self.getNextBar() == self.idxArr[self.priceIdx]:
         #if self.getNextBar() == self.idxArr[self.priceIdx] + 1:
            #self.setNextBar(timeBar)
            return 1
            
      else:
         print ("self.getNextBar() " + str(self.getNextBar()))
         print ("self.idxArr[self.priceIdx] " +  str(self.idxArr[self.priceIdx]))
         
         if self.getNextBar() == self.idxArr[self.priceIdx] + 1:
         #if self.getNextBar() == self.idxArr[self.priceIdx] + 1:
            #self.setNextBar(timeBar)
            return 1
            
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   def isNextBarSlave(self, timeBar):
#      
#      if not self.offLine:
#         return 0
#      
#      print ("self.getNextBar() " + str(self.getNextBar()))
#      print ("self.idxArr[self.priceIdx] " +  str(self.idxArr[self.priceIdx]))
#      
#      if self.getNextBar() == self.idxArr[self.priceIdx]:
#      #if self.getNextBar() == self.idxArr[self.priceIdx] + 1:
#         #self.setNextBar(timeBar)
#         return 1
#         
#      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setNextBar(self, timeBar):
   
      self.nextBar += timeBar

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initNextBar(self):
   
      self.nextBar = self.idxArr[self.priceIdx]
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNextBar(self):
   
      return self.nextBar

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
   def write(self, path, ask, bid, last, vl, bar):

      with open(path, "a+", encoding="utf-8") as priceFile:
         priceFile.write ('%s' % str(ask) + "," + str(bid) + ","  + str(last) + "," + str(vl) + "," + str(bar) + "\n")
         priceFile.flush()
         
#      if doAllMinutes:
#         self.write2m(ask, bid, bar)
#         self.write3m(ask, bid, bar)
#         self.write4m(ask, bid, bar)
#         self.write5m(ask, bid, bar)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeFD(self, pathFD, ask, bid, last, vl, bar):

      if pathFD.closed:
         print ("FILE IS NOT OPEN ")
         return 0

      pathFD.write ('%s' % str(ask) + "," + str(bid) + ","  + str(last) + "," + str(vl) + "," + str(bar) + "\n")
      pathFD.flush()
                     
# end price

