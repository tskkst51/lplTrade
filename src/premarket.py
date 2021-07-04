## PreMarket methods

'''
premarket module
'''

import os
from time import time, sleep
#import time
from datetime import datetime
import urllib.request
import json
import lplTrade as lpl
import pathlib
import traceback

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Premarket:
   def __init__(self, minuteChartPath, minuteChartExt, dailyChartPath, dailyChartExt, dailyGapExt, bestAlgosPath, bestAlgosExt):
   
      self.bc = lpl.Barchart()
      
      self.dailyChartPath = dailyChartPath
      self.dailyChartExt = dailyChartExt
      
      self.minuteChartPath = minuteChartPath
      self.minuteChartExt = minuteChartExt
      
      self.dailyGapExt = dailyGapExt
      
      self.bestAlgosPath = bestAlgosPath
      self.bestAlgosExt = bestAlgosExt
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAlgorithm(self, stocks, useDefaultAlgo, useStocksWithNoTestData):
   
      print ("getAlgorithm\n" + str(stocks))

      bestAlgoD = {}
      defaultStocks = ["BABA","BIDU","TSLA","SNAP"]
      
      defaultAlgo = "TB1_HL_QM_OB3_OS3_CB2_CS2"
      #defaultAlgo = "TB1_OC_QM_OB5_OS5_CB2_CS2_TR_IR5"
      #defaultAlgo = "TB3_OC_QM_OB2_OS2_CB3_CS3_TR"
      #defaultAlgo = "TB3_HI_QM_OB2_OS2_CB4_CS4_TR"
      #defaultAlgo = "TB2_HL_HS_AL_QM_OB2_OS2_CB3_CS3_QP"
      stocksBeingUsed = []
      
      if useDefaultAlgo:
         for s in defaultStocks:
            bestAlgoD[s] = defaultAlgo 
            stocksBeingUsed.append(s)
      else:
         for s in stocks:
            bestAlgoFile = self.bestAlgosPath + s + self.bestAlgosExt
               
            if not os.path.exists(bestAlgoFile):
               if useStocksWithNoTestData:
                  bestAlgoD[s] = defaultAlgo 
                  stocksBeingUsed.append(s)
               continue
               
            with open(bestAlgoFile, 'r') as baFile:
               lines = baFile.readlines()
   
            lastLineItems = lines[len(lines) - 1].split()
            bestAlgoD[s] = lastLineItems[len(lastLineItems) - 1] 
            stocksBeingUsed.append(s)   
   
         if len(bestAlgoD) == 0:
            for s in defaultStocks:
               print ("Using Default stocks\n" + str(defaultStocks))
      
               bestAlgoFile = self.bestAlgosPath + s + self.bestAlgosExt
               
               if not os.path.exists(bestAlgoFile):
                  continue
                  
               with open(bestAlgoFile, 'r') as baFile:
                  lines = baFile.readlines()
      
               lastLineItems = lines[len(lines) - 1].split()
               bestAlgoD[s] = lastLineItems[len(lastLineItems) - 1]
               stocksBeingUsed.append(s)
               print ("bestAlgoD[s]\n" + str(bestAlgoD[s]))
         
      print ("bestAlgoD\n" + str(bestAlgoD))
      print ("stocksBeingUsed\n" + str(stocksBeingUsed))
      
      return bestAlgoD, stocksBeingUsed
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDailyOrderedStocks(self, tg, gapData, stockData, stocks):
      
      gapCandidates = tg.getGapCandidates(gapData, stockData)
      
      betaCandidates = tg.getBetaCandidates(stockData)
            
      avgVolData = tg.getAverageVolumeData(stockData)
      
      lastDaysVolGtrCandidates = tg.getLastDaysVolumeGtrData(stockData)
            
      lastDaysVolLessCandidates = tg.getLastDaysVolumeLessData(stockData)
            
      volumeCandidates = tg.getVolumeCandidates(avgVolData, stockData)
      
      spreadCandidates = tg.getSpreadCandidates(stockData)

      #trendCandidates = tg.getTrendCandidates(stockData)
      trendCandidates = []

      orderedStocks = tg.orderStocks(\
         gapCandidates, lastDaysVolGtrCandidates, lastDaysVolLessCandidates, \
         volumeCandidates, spreadCandidates, trendCandidates, betaCandidates, avgVolData, stocks)

      # stocksWBestAlgo = tg.getBestAlgo(orderedStocks)
       
      # Merge average volume and gap data stocks
      
#      print ("Stocks with opening day gap > average gap ordered by largest gap\n" + str(orderedStocks))
#      print ("Stocks with last day Vol > average vol ordered by largest volume\n" + str(orderedStocks2))
      
      return orderedStocks
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDailyGapData(self, tg, dc, stocks):

      gapData = {}
      
      # Get gap data from file
      for stock in stocks:
         gpPath = self.dailyChartPath + stock + self.dailyGapExt
         if not os.path.exists(gpPath):
            continue
         gapData[stock] = dc.readDailyGapData(gpPath)
         
      print ("gapData\n" + str(gapData))
      
      return gapData

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDailyStockData(self, tg, dc, stocks):

      stockData = {}
      
      # Get daily stock data from file
      for stock in stocks:
         dcPath = self.dailyChartPath + stock + self.dailyChartExt
         if not os.path.exists(dcPath):
            continue
         stockData[stock] = dc.readDailyBarChart(dcPath)
         
      #print ("stockData " + str(stockData))
      
      return stockData

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getStockStrFromDailyCharts(self):
         
      stocks = []
      
      # Get gap data from files already loaded by below algo
      with os.scandir(self.dailyChartPath ) as dcp:
         for entry in dcp:
            if entry.name.endswith(self.dailyChartExt) and entry.is_file():
               print ("entry " + str(entry.name))
               if self.todaysDateInDcPath("dc/" + entry.name):
                  continue

               stocks.append(str(entry.name.replace(self.dailyChartExt,"")))      
      
      return stocks
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getStockStrFromTestMinuteCharts(self):
         
      stocks = []

      for rootPath, directories, paths in os.walk("test"):
         for path in paths:
            if path.endswith(self.minuteChartExt):
               if os.stat(rootPath + "/" + path).st_size > 10000:
                  stockName = path.replace("active","") 
                  stockName = stockName.replace(self.minuteChartExt,"")
                  if stockName not in stocks:
                     print ("stockName: " + str(stockName))
                     stocks.append(stockName)      
      
      return stocks
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def todaysDateInDcPath(self, path): 
      
      with open(path, 'r') as f:
         lastLine = f.readlines()[-1]
      
      ts = time()
      dt = datetime.fromtimestamp(ts).strftime('%Y%m%d')

      print("lastLine " + str(lastLine))
      print("dt " + str(dt))

      if dt in lastLine:
         print("dt is in lastline" + str(dt))
         return 1
         
      # Yesterday
      dt = str(int(dt) - 1)
      if dt in lastLine:
         print("dt -1 is in lastline" + str(dt))
         return 1

      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPathsModTimeToday(self, path): 
      
      ts = time()
      st = datetime.fromtimestamp(ts).strftime('%Y%m%d')
      
      modTime = pathlib.Path(path).stat().st_mtime
      mTime = datetime.fromtimestamp(modTime).strftime('%Y%m%d')
            
      print ("st " + str(st))
      print ("mTime " + str(mTime))
      print ("path " + str(path))
      
      if int(st) == int(mTime):
         return 1
         
      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def updateDailyCharts(self, tg, dc, stocks):
   
      validStocks = []
      validLDStocks = []
      
      for stock in stocks:
         dcPath = "dc/" + stock + ".dc"
         
         # Only get stocks that have not been updated today
         if not os.path.exists(dcPath):  
            validStocks.append(stock)
            continue
            
         if not self.isPathsModTimeToday(dcPath):
            validStocks.append(stock)
            continue
            
         if not self.todaysDateInDcPath(dcPath):
            validStocks.append(stock)
            continue
      
      stocks = validStocks
      
      print ("validStocks " + str(stocks))

      gapData = {}
      
      for stock in stocks:
         try:  
            dailyData = eval(tg.getDailyData(stock, 13))
         except Exception: 
            print ("Unable to get Daily data")
            traceback.print_exc()
            sleep(13)
            continue
            
         #print ("dailyData " + str(dailyData))
         #print ("len dailyData " + str(len(dailyData)))
            
         # polygon.io is timing out
         if len(dailyData) == 0:
            print ("len of dailyData == 0")
            break
            
         # IPO. One day of data. 8 items means only one day of data, an IPO skip
         if len(dailyData) == 8:
            print ("len of dailyData == 8")
            sleep(13)
            continue
            
         gapAvg, gapHi, gapLo, gapHiDate, gapHiVol = tg.getDailyGaps(dailyData, dc)
         
         gapData = [gapAvg, gapHi, gapLo, gapHiDate, gapHiVol]
         
         dbc = dc.getDailyBarChart(dailyData)
         
         dc.writeDailyBarChart(dbc, stock, self.dailyChartPath)
         dc.writeDailyGapData(gapData, stock, self.dailyChartPath)
         
         print ("writing of the new DC is successful")
         
         sleep(13)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getStocksWithDailyData(self, stocks, minDaysData):
   
      parsedStocks = []
      
      # Return a list of stocks with at least "minDaysData" worth of data
      for stock in stocks:
         path = "bestAlgos/" + stock + ".bs"
         
         if not os.path.exists(path):
            continue
         
         # Get last line from path
         with open(path, 'r') as sp:
            lines = sp.readlines()
         lastLine = lines[len(lines) - 1]

         b, m, e = lastLine.rpartition(" days")
         items = b.split()

         print ("items " + str(items))

         numDaysData = items[len(items) - 1]
         print ("numDaysData " + str(numDaysData))
         
         if int(numDaysData) < int(minDaysData):
            print ("skipping stock due to lack of data; minDaysData  " + " " + stock + " " + str(minDaysData))
            continue
         
         parsedStocks.append(stock)
         
      return parsedStocks      
       
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getStockCandidates(self, tg, dc, stocks, findPreMarketMovers, useLiveDailyData):
   
      # Take static stocks and movers and get their daily charts if not already up to date
      validLDStocks = []
      validStocks = []
      
      # Find the premarket movers
      if findPreMarketMovers:
         movers = tg.getPreMarketMovers()
                        
         print ("movers " + str(movers))

         for mover in movers:
            dcPath = "dc/" + mover + ".dc"
            
            # Only get stocks that have not been updated today
            
            if os.path.exists(dcPath):
               #if self.todaysDateInDcPath(dcPath):
               stocks.append(mover)
               continue

            print ("mover " + str(mover))
            
            try:
               dailyData = eval(tg.getDailyData(mover, 13))
            except Exception: 
               print ("Unable to get Daily data")
               traceback.print_exc()
               continue
               
            #print ("dailyData " + str(dailyData))
            #print ("len dailyData " + str(len(dailyData)))
               
            # polygon.io is timing out
            if len(dailyData) == 0:
               break
               
            # IPO. One day of data. 8 items means only one day of data, an IPO skip
            if len(dailyData) == 8:
               print ("IPO skipping " + str(mover))
               sleep(13)
               continue
               
            gapAvg, gapHi, gapLo, gapHiDate, gapHiVol = tg.getDailyGaps(dailyData, dc)
            
            gapData = [gapAvg, gapHi, gapLo, gapHiDate, gapHiVol]
            #print ("gapData: " + str(gapData))
            
            dbc = dc.getDailyBarChart(dailyData)
            
            dc.writeDailyBarChart(dbc, mover, self.dailyChartPath)
            dc.writeDailyGapData(gapData, mover, self.dailyChartPath)
            print ("DC file written for " + str(mover))

            sleep(13)

            stocks.append(mover)
      
      validStocks = stocks
      
      print ("validStocks " + str(validStocks))
      print ("validStocks len" + str(len(validStocks)))

      if useLiveDailyData:
         gapData = {}
         for stock in validStocks:
            dcPath = "dc/" + stock + ".dc"
            
            # Only get stocks that have been updated today
            if not os.path.exists(dcPath):
               continue
               
            #if self.isPathsModTimeToday(dcPath):               
            #if self.todaysDateInDcPath(dcPath):
            validLDStocks.append(stock)

         validStocks = validLDStocks
      
      print ("validStocks " + str(validStocks))
      print ("validStocks len" + str(len(validStocks)))

      return validStocks

