## DailyChart methods

'''
dailychart module
'''

import os
from time import time, sleep
from datetime import datetime
import urllib.request
import lplTrade as lpl


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Dailychart:
   def __init__(self):
   
      self.hi = 0
      self.lo = 1
      self.op = 2
      self.cl = 3
      self.vl = 4
      self.bl = 5
      self.sH = 6 # Session Hi
      self.sL = 7 # Session Li
      self.dt = 8

      self.bearS = 0
      self.bearM = 1
      self.bearL = 2
      self.bearE = 3
      self.bearU = 4
      self.bullS = 5
      self.bullM = 6
      self.bullL = 7
      self.bullE = 8
      self.bullU = 9
      
      self.gapAvg = 0
      self.gapHi = 1
      self.gapLo = 2
      self.gapHiDate = 3
      self.gapHiVol = 4

      self.avgBL = 0.0
      self.avgVol = 0
      self.avgVolTime = 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def init(self):
   
      #      Hi  Lo  Op  Cl  V BarL Date SH SL
      dbc = [[0.0,0.0,0.0,0.0,0,0.0,0,0,""]]
      
      return dbc

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initGap(self):
   
      #    gapAvg, gapHi, gapLo, gapHiDate, gapHiVol
      gd = [0.0,0.0,0.0,"",0]
      
      return gd

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeDailyBarChart(self, dbc, stock, path):
   
      dbcLen = len(dbc)
      path += stock + ".dc"
      
      with open(path, 'w') as gapData:
         for bar in range(dbcLen - 1):
            barLen = len(dbc[bar])
            b = 0
            for b in range(barLen - 1): 
               gapData.write ('%s' % str(dbc[bar][b]) + ",")
            gapData.write ('%s' % str(dbc[bar][b + 1]) + "\n")
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeDailyGapData(self, gapData, stock, path):
   
      gapLen = len(gapData)
      path += stock + ".gp"
      g = 0
      with open(path, 'w') as gapInfo:
         for g in range(gapLen - 1):
            gapInfo.write ('%s' % str(gapData[g]) + ",")
         gapInfo.write ('%s' % str(gapData[g + 1]) + "\n")
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def readDailyGapData(self, path):
   
      dgp = self.initGap()

      ctr = 0
      with open(path, 'r') as gapData:
         for line in gapData:
            line = line.strip("\n")
            gap = line.split(",")
               
            dgp[self.gapAvg] = float(gap[self.gapAvg])
            dgp[self.gapHi] = float(gap[self.gapHi])
            dgp[self.gapLo] = float(gap[self.gapLo])
            dgp[self.gapHiDate] = float(gap[self.gapHiDate])
            dgp[self.gapHiVol] = float(gap[self.gapHiVol])
                  
      return dgp

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDailyBarChart(self, d):

      dataItems = len(d)
      
      dbc = self.init()
      
      bar = 0
      sessionHi = 0
      sessionLo = 99999

      for bar in range(dataItems):
         for k, v in d[bar].items():
            if k == 'h':
               dbc[bar][self.hi] = v
            if k == 'l':
               dbc[bar][self.lo] = v
            if k == 'o':
               dbc[bar][self.op] = v
            if k == 'c':
               dbc[bar][self.cl] = v
            if k == 'v':
               dbc[bar][self.vl] = int(v)
            if k == 't':
               dbc[bar][self.dt] = self.getDateFromEpoch(v)
         dbc.append([0.0,0.0,0.0,0.0,0,0.0,0,0,""])
         
      bars = len(dbc)
      
      # Set the yearly hi and lo
      for bar in range(bars):
         dbc[bar][self.bl] = round(dbc[bar][self.hi] - dbc[bar][self.lo], 2)
         
         if dbc[bar][self.hi] > sessionHi:
            sessionHi = dbc[bar][self.hi]
            dbc[bar][self.sH] = 1
            
         if dbc[bar][self.lo] < sessionLo:
            sessionLo = dbc[bar][self.lo]
            dbc[bar][self.sL] = 1
      
      return dbc

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDateFromEpoch(self, time): 
      
      time = str(time)[0:10]
      
      return str(datetime.fromtimestamp(int(time)).strftime('%Y%m%d'))

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def readDailyBarChart(self, path):
   
      dbc = self.init()
      
      ctr = 0
      with open(path, 'r') as stockData:
         for line in stockData:
            line = line.strip("\n")
            bar = line.split(",")
                        
            if ctr != 0:
               dbc.append(bar)

            dbc[ctr][self.hi] = float(bar[self.hi])
            dbc[ctr][self.lo] = float(bar[self.lo])
            dbc[ctr][self.op] = float(bar[self.op])
            dbc[ctr][self.cl] = float(bar[self.cl])
            dbc[ctr][self.vl] = int(bar[self.vl])
            dbc[ctr][self.bl] = float(bar[self.bl])
            dbc[ctr][self.sH] = int(bar[self.sH])
            dbc[ctr][self.sL] = int(bar[self.sL])
            dbc[ctr][self.dt] = str(bar[self.dt])
            ctr += 1
                  
      return dbc
