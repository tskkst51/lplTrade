## Target methods

'''
target module
'''

import os
from time import time, sleep
#import time
from datetime import datetime
import urllib.request
import json
import lplTrade as lpl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Target:
   def __init__(self, c, d, l):
   
      self.c = c # Connect object
      self.d = d # profile data object
      self.l = l # Log object
      
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
      self.gapHiData = 3
      self.gapHiVol = 4

      self.avgBL = 0.0
      self.avgVol = 0
      self.avgVolTime = 0

      # api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-01-01/2020-12-17?
      # apiKey=qL6W5A65SakAuO1ffC2iCjGXY4NTtvP_
      
      #self.url = 'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/'
      
      self.url = "https://api.polygon.io/v2/aggs/ticker/"
      self.rang = "/range/1/day/"
      
      # Original
      self.key = "?apiKey=qL6W5A65SakAuO1ffC2iCjGXY4NTtvP_"
      # Crypto key
      #self.key = "?apiKey=qL6W5A65SakAuO1ffC2iCjGXY4NTtvP_"
      
      self.preMarketURL = "https://thestockmarketwatch.com/markets/pre-market/today.aspx"
   
      self.priceLimits = str(self.d["profileTradeData"]["priceLimits"])
      self.spreadLimits = str(self.d["profileTradeData"]["spreadLimits"])
      self.numSpreadSamples = int(self.d["profileTradeData"]["numSpreadSamples"])
      self.gapThreshold = float(self.d["profileTradeData"]["gapThreshold"])
      self.volThreshold = float(self.d["profileTradeData"]["volThreshold"])
      self.betaThreshold = float(self.d["profileTradeData"]["betaThreshold"])
      self.greaterVolumeThreshold = float(self.d["profileTradeData"]["greaterVolumeThreshold"])
      self.lessVolumeThreshold = float(self.d["profileTradeData"]["lessVolumeThreshold"])
      self.minDailyVol = int(self.d["profileTradeData"]["minDailyVol"])
      
      self.allStocks = []


   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isValidSpread(self, stock):
   
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLastDaysVolumeGtrData(self, stockData):
   
      lastDayVolumeGtr = {} 
      
      # Calculate the last day volume and the percent it's increased for each stock

      print ("stockData: " + str(stockData))
      
      for key, value in stockData.items():
         vLen = len(value)
         ctr = 0
         for v in value:
            if v[self.vl] == 0:
               continue
            if ctr == vLen - 2:
               volItems = []
               secondToLastDaysVol = v[self.vl]
            if ctr == vLen - 1:
               print (str(v))
               if v[self.vl] or secondToLastDaysVol == 0:
                  continue
               if v[self.vl] > secondToLastDaysVol:
                  volItems.append(1)
                  volItems.append(v[self.vl] / secondToLastDaysVol)
                  lastDayVolumeGtr[key] = volItems
               else:
                  volItems.append(0)
                  volItems.append(secondToLastDaysVol / v[self.vl])
                  lastDayVolumeGtr[key] = volItems
               
            ctr += 1

      print ("\nlast days volume > previous day and amount > \n" + str(lastDayVolumeGtr))
      
      return lastDayVolumeGtr
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getLastDaysVolumeLessData(self, stockData):
   
      lastDayVolumeLess = {} 
      
      # Calculate the last day volume and the percent it's increased for each stock

      for key, value in stockData.items():
         vLen = len(value)
         ctr = 0
         for v in value:
            if v[self.vl] == 0:
               continue
            if ctr == vLen - 2:
               volItems = []
               secondToLastDaysVol = v[self.vl]
            if ctr == vLen - 1:
               if v[self.vl] or secondToLastDaysVol == 0:
                  continue
               if v[self.vl] < secondToLastDaysVol:
                  volItems.append(1)
                  volItems.append(secondToLastDaysVol / v[self.vl])
                  lastDayVolumeLess[key] = volItems
               else:
                  volItems.append(0)
                  volItems.append(v[self.vl] / secondToLastDaysVol)
                  lastDayVolumeLess[key] = volItems                  
            
            ctr += 1
               
      print ("\nlast days volume < previous day and amount > \n" + str(lastDayVolumeLess))
      
      return lastDayVolumeLess
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAverageVolumeData(self, stockData):
   
      totalVolume = 0
      avgVol = {} 
      
      # Calculate the average volume for each stock

      for key, value in stockData.items():
         ctr = 0
         totalVolume = 0
         for v in value:
            if v[self.vl] == 0:
               continue
            totalVolume += v[self.vl]
            ctr += 1
         avgVol[key] = round(totalVolume / ctr, 2)
                  
      print ("\nAverage volume over days " + str(ctr) + "\n" + str(avgVol))
      
      return avgVol

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDailyTrends(self, stockData):

      trends = [0,0,0,0,0,0,0,0,0,0]
      
      dailyTrends = {}
      tr = {}

      allStocks = self.getAllStocksArr()

      for stocks in allStocks:
         cn = lpl.ConnectEtrade(self.c, stocks, 1, 1, "intraday", False, 0)         
               
         for stock in stocks:
            tr[stock] = lpl.Trends(self.d, self.l, cn, 0, 0, stock)
            
            stockValues = cn.setStockValues(0, 0, "")
         
            print ("stockData[stock] len\n" + str(len(stockData[stock])) + " " + str(stock))
            
            tr[stock].setTrendLimits(stockData[stock], len(stockData[stock]), 0, 0)
            
            trends[self.bearS] = tr[stock].isBearShortTrend()
            trends[self.bearM] = tr[stock].isBearMidTrend()
            trends[self.bearL] = tr[stock].isBearLongTrend()
            trends[self.bearE] = tr[stock].isBearMegaTrend()
            trends[self.bearU] = tr[stock].isBearSuperTrend()
            
            trends[self.bullS] = tr[stock].isBullShortTrend()
            trends[self.bullM] = tr[stock].isBullMidTrend()
            trends[self.bullL] = tr[stock].isBullLongTrend()
            trends[self.bullE] = tr[stock].isBullMegaTrend()
            trends[self.bullU] = tr[stock].isBullSuperTrend()
      
            print ("trends " + str("trends\n" + str(trends)))
            
            dailyTrends[stock] = trends
            trends = [0,0,0,0,0,0,0,0,0,0]
         
      print ("dailyTrends " + str(dailyTrends))

      return dailyTrends

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTrendCandidates(self, stockData):

      shortWeight = 16
      midWeight = 8
      longWeight = 4
      megaWeight = 2
      superWeight = 1
      
#      shortWeight = 1
#      midWeight = 2
#      longWeight = 3
#      megaWeight = 4
#      superWeight = 5

      trendCandidates = {}

      dailyTrends = self.getDailyTrends(stockData)
      
      for stock, trends in stockData.items():
         bearStrength = \
            dailyTrends[stock][self.bearS] * shortWeight + \
            dailyTrends[stock][self.bearM] * midWeight + \
            dailyTrends[stock][self.bearL] * longWeight + \
            dailyTrends[stock][self.bearE] * megaWeight + \
            dailyTrends[stock][self.bearU] * superWeight
               
         bullStrength = \
            dailyTrends[stock][self.bullS] * shortWeight + \
            dailyTrends[stock][self.bullM] * midWeight + \
            dailyTrends[stock][self.bullL] * longWeight + \
            dailyTrends[stock][self.bullE] * megaWeight + \
            dailyTrends[stock][self.bullU] * superWeight
         
         print ("bullStrength " + str(stock) + " " + str(bullStrength))     
         print ("bearStrength " + str(stock) + " " + str(bearStrength))
         
         # Test which values work best 
         trendCandidates[stock] = [bullStrength, bearStrength]
         
      print ("trendCandidates " + str(trendCandidates))
      print ("trendCandidates len " + str(len(trendCandidates)))
      
      return trendCandidates
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getVolumeCandidates(self, avgVolData, stockData):

      volCandidates = {}
      lastLine = {}
      
      # getlast line from daily files
      for key, value in stockData.items():
         lastLine[key] = stockData[key][len(value) - 1]
         
      for gKey, avgVol in avgVolData.items():
         for lKey, lValue in lastLine.items():
            if gKey == lKey:
               volCandidates[gKey] = round(lValue[self.vl] / avgVol, 2)
                        
      print ("\nAmount previous days volume is > average volume \n" + str(volCandidates))

      return volCandidates

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBetaCandidates(self, stockData):
   
      totalBeta = 0
      betaCandidates = {} 
      lastLine = {}
      
      # Calculate the average beta for each stock
      # Calculate the average beta against the last weeks beta

      # Get last lines beta
      for key, value in stockData.items():
         lastLine[key] = stockData[key][len(value) - 1][self.hi] - \
            stockData[key][len(value) - 1][self.lo] 

      for key, value in stockData.items():
         ctr = 0
         totalBeta = 0
         lastClose = 0
         for v in value:
            totalBeta += v[self.hi] - v[self.lo]
            lastClose = v[self.cl]
            ctr += 1
         avgBeta = round((totalBeta / ctr) / lastClose, 4)
         lastLineBetaGtr = round((lastLine[key] / avgBeta) / lastClose, 4)
         
         betaCandidates[key] = lastLineBetaGtr 
         #betaCandidates[key] = [round((totalBeta / ctr) / lastClose, 4), lastLine[key]]
                  
      print ("\n Last line bar length > average beta over days " + str(ctr) + "\n" + str(betaCandidates))
      
      return betaCandidates
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getGapCandidates(self, gapData, stockData):
   
      ask = 1
      
      gapCandidates = {}
      lastLine = {}

      bids, asks = self.getBidsAsks()

      # getlast line from daily files
      for key, value in stockData.items():
         lastLine[key] = stockData[key][len(value) - 1]

      for gKey, gValue in gapData.items():
         for aKey, aValue in asks.items():
            for lKey, lValue in lastLine.items():
               if gKey == aKey and gKey == lKey:
                  print ("gKey\n" + str(gKey))
                  print ("aKey\n" + str(aKey))
                  print ("lKey\n" + str(lKey))
                  gAvg = self.getGapAvg(gValue)
                  gCurr = self.getCurrentGap(lValue, aValue)
                  print ("lValue\n" + str(lValue))
                  print ("aValue\n" + str(aValue))
                  gapCandidates[gKey] = gCurr / gAvg
                     
      print ("\ngap Candidates by amount > \n" + str(gapCandidates))

      return gapCandidates
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCurrentGap(self, d, d2):
   
      asks = 0      
      
      # d2 is an array. Get the avg of all values
      for ctr in range(self.numSpreadSamples):
         asks += d2[ctr]
         print ("\nasks \n" + str(asks))
         print ("\nctr \n" + str(ctr))
         
      askAvg = round(asks / self.numSpreadSamples, 2)
      
      val = d[self.cl] - askAvg
                  
      if val < 0:
         val = val*-1

      return val 

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getGapAvg(self, d):

      return d[self.gapAvg] 

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getCloseOpenDiff(self, d, d2):

      val = d[self.cl] - d2[self.op]
      if val < 0:
         val = val*-1
         
      return val 

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getAllStocksArr(self):
      
      return self.allStocks

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAllStocksArr(self, stockData):
      
      stocks = []
      
      print ("stockData len\n" + str(len(stockData)))
      
      # Create arrays of stocks, 20 at a time, since Etrade can only handle 20
      ctr = 1
      for key, value in stockData.items():
         if ctr % 20 == 0:
            self.allStocks.append(stocks)
            stocks = []
         stocks.append(key)
         ctr += 1
      
      self.allStocks.append(stocks)
      
      print ("get20StockArr allStocks\n" + str(self.allStocks))
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBidsAsks(self):

      stockValues = {}
             
      bids = {}
      asks = {}
      
      allStocks = self.getAllStocksArr()

      # Load all the bids and asks values from the service (Etrade) into the dicts
      for stocks in allStocks:
         cn = lpl.ConnectEtrade(self.c, stocks, 1, 1, "intraday", False, 0)         
         
         stockVals = []
         
         for ctr in range(self.numSpreadSamples):
            stockValues = cn.setStockValues(0, 0, "")
            stockVals.append(stockValues)
         
         print ("stockVals\n" + str(stockVals))
         
         bidList = []
         askList = []
         
         for stock in stocks:
            for ctr in range(len(stockVals)):
               for k, v in stockVals[ctr].items():
                  if k == stock:
                     bidList.append(v[0])
                     askList.append(v[1])
               bids[stock] = bidList
               asks[stock] = askList
            bidList = []
            askList = []
            
      print ("bids\n" + str(bids))
      print ("asks\n" + str(asks))
      
      return bids, asks
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getSpreadCandidates(self, stockData):
      
      stockValues = {}
                   
      bids, asks = self.getBidsAsks()
      
      # Calculate the average of the bid ask differences
      
      diffs = []
      priceDiffs = {}
      avgDiffs = {}
      
      diffTotal = 0.0
      for k, v in bids.items():
         for k2, v2 in asks.items():
            if k == k2:
               for ctr in range(self.numSpreadSamples):
                  diffs.append(round(float(v2[ctr]) - float(v[ctr]), 2))
                  
               #print ("diffs\n" + str(k) + str(diffs))
               
               for d in diffs:
                  diffTotal += d
                  
               #print ("diffTotal\n" + str(k)  + str(diffTotal))
               
               avgDiffs = diffTotal / self.numSpreadSamples
               diffTotal = 0.0
               priceDiffs[k] = [v[ctr], round(avgDiffs, 2)]
               
               #print ("avgDiffs\n" + str(k)  + str(avgDiffs))
               
         diffs = []
         
      print ("priceDiffs\n" + str(priceDiffs))
      
      # Compare found spread values with limits

      priceLimits = self.priceLimits.split(',')
      spreadLimits = self.spreadLimits.split(',')

      print ("priceLimits\n" + str(priceLimits))
      print ("spreadLimits\n" + str(spreadLimits))

      spreadCandidates = {}
      losers = []
      
      for k, v in priceDiffs.items():
         for limit in range(len(spreadLimits)):
            if v[0] < int(priceLimits[limit]):
               if v[1] <= float(spreadLimits[limit]):
                  spreadCandidates[k] = 1
                  break
               else:
                  spreadCandidates[k] = 0
                  losers.append([k, v[1]]) 
                  break
                  
      print ("spreadCandidates\n" + str(spreadCandidates))
      print ("losers\n" + str(losers))
      
      print ("stockData count\n" + str(len(stockData)))
      print ("spreadCandidates count\n" + str(len(spreadCandidates)))
      
      return spreadCandidates
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getBestAlgo(self, orderedStocks):
   
      # Get the best algo 
   
      for stock in orderedStocks:
         pass
         
      return
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeAnalysisData(self, path, oGaps, ldvGtr, ldvLess, vl, sp, tr, av):

      with open(path, "a+") as analyzeData:
         for v in av:
            analyzeData.write("avr daily vol\n")
            analyzeData.write(str(v))
            analyzeData.write("\n")
   
         for g in oGaps:
            analyzeData.write("gapCandidates\n")
            analyzeData.write(str(g))
            analyzeData.write("\n")
   
         for ldvg in ldvGtr:
            analyzeData.write("lastDaysVolGtrCandidates\n")
            analyzeData.write(str(ldvg))
            analyzeData.write("\n")
         
         for ldvl in ldvLess:
            analyzeData.write("lastDaysVolLessCandidates\n")
            analyzeData.write(str(ldvl))
            analyzeData.write("\n")
            
         for v in vl:
            analyzeData.write("volumeCandidates\n")
            analyzeData.write(str(v))
            analyzeData.write("\n")
         
         for s in sp:
            analyzeData.write("spreadCandidates\n")
            analyzeData.write(str(s))
            analyzeData.write("\n")
      
         for t in tr:
            analyzeData.write("trendCandidates\n")
            analyzeData.write(str(t))
            analyzeData.write("\n")
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def testResultsExists(self, stock):
   
      testPath = "totalResults/" + stock + ".tr"
      
      if os.path.exists(testPath):
         statinfo = os.stat(testPath)
         if statinfo.st_size > 50:
            print ("found results for " + str(testPath))
            return 1
         
      return 0
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def orderStocks(self, gapCandidates, lastDaysVolGtrCandidates, lastDaysVolLessCandidates, \
         volumeCandidates, spreadCandidates, trendCandidates, betaCandidates, avgVolData, stocks):
   
      doSpread = doGap = 1
      doVolLess = doVolGtr  = doBeta = doTrend = doTestData = doAvgVol = doVolume = 0
            
      ts = time()
      dt = str(datetime.fromtimestamp(ts).strftime('%Y%m%d'))
      path = "analyzeResults/" + dt + ".ay"

      print ("all stocks\n" + str(stocks))
      print ("stocks len\n" + str(len(stocks)))
      
      # Determination:
      # Test results must exists
      # Sort based on:
      #   largest gap data
      #   trend must be in bull if no bulls exist use bears. Eliminate stocks that are flat
      #   
      #   must have previous day volume > avg
      
      spreads = sorted(spreadCandidates.items(), key=lambda x: x[1], reverse=True)
      oGaps = sorted(gapCandidates.items(), key=lambda x: x[1], reverse=True)
      ldvGtr = sorted(lastDaysVolGtrCandidates.items(), key=lambda x: x[1], reverse=True)
      ldvLess = sorted(lastDaysVolLessCandidates.items(), key=lambda x: x[1], reverse=True)
      vl = sorted(volumeCandidates.items(), key=lambda x: x[1], reverse=True)
      #tr = sorted(trendCandidates.items(), key=lambda x: x[1], reverse=True)
      tr = []
      bt = sorted(betaCandidates.items(), key=lambda x: x[1], reverse=True)

      volStocks = []
      
      if doAvgVol:
         for stock, vol in avgVolData.items():
            print ("stock: avg daily vol:\n" + str(stock) + " " + str(vol))
            if vol > self.minDailyVol:
               volStocks.append(stock)
            
         stocks = volStocks
         
         print ("stocks after average vol threshold\n" + str(stocks))
         print ("threshold\n" + str(self.minDailyVol))
         print ("stocks len\n" + str(len(stocks)))

      testDataStocks = []

      if doTestData:
         ctr = 0
         for s in stocks:
            if self.testResultsExists(s):
               testDataStocks.append(s)
            ctr += 1
            
         stocks = testDataStocks
         
         print ("stocks after no test data\n" + str(stocks))
         print ("stocks len\n" + str(len(stocks)))

      if not os.path.exists(path):
         self.writeAnalysisData(path, oGaps, ldvGtr, ldvLess, vl, spreads, tr, avgVolData)

      if doSpread:
         print ("spreadData\n")
         for p in spreads:
            ctr = 0
            for s in stocks:
               if p[0] == s:
                  print (str(p))
                  if p[1] == 0:
                     print (s + " spread > thresh " + str(p[1]) + " popped")
                     stocks.pop(ctr)
               ctr += 1
               
         print ("stocks after spread\n" + str(stocks))
         print ("stocks len\n" + str(len(stocks)))

      print ("oGaps\n" + str(oGaps))
      
      if doGap:
         gapStocks = []
         # Reset stock list on gaps
         print ("gapData\n")
         for g in oGaps:
            ctr = 0 
            for s in stocks:
               if s == g[0]:
                  print (str(g))
                  if g[1] > self.gapThreshold:
                     print (s + " gap > thresh " + str(g[1]) + " adding")
                     gapStocks.append(s)
                  else:
                     print (s + " gap < thresh " + str(g[1]) + " popped")
                  break
                     
               ctr += 1
         
         stocks = gapStocks
      
         print ("stocks after gap ordering\n" + str(stocks))
         print ("stocks len\n" + str(len(stocks)))

      if doBeta:
         betaStocks = []
         ctr = 0 
         for s in stocks:
            for b in bt:
               if s == b[0]:
                  print (str(b))
                  if b[1] > self.betaThreshold:
                     betaStocks.append(s)
                     print (s + " beta > thresh " + str(b[1]) + " added")
                     stocks.pop(ctr)
                  else:
                     print (s + " beta < thresh " + str(b[1]) + " popped")  
                  break             
            ctr += 1
   
         stocks = betaStocks
         
         print ("stocks after betas > betaThreshold\n" + str(self.betaThreshold) + " "  + str(stocks))
         print ("stocks len\n" + str(len(stocks)))

      if doVolume:      
         volStocks = []
         ctr = 0 
         for v in vl:
            for s in stocks:
               if s == v[0]:
                  print (str(v))
                  if v[1] > self.volThreshold:
                     volStocks.append(s)
                     print (s + " vol > thresh " + str(v[1]) + " added")
                  else:
                     print (s + " vol < thresh " + str(v[1]) + " popped")               
                  break
               ctr += 1

         stocks = volStocks
         print ("stocks after average vol > volThreshold\n" + str(self.volThreshold) + " "  + str(stocks))
         print ("stocks len\n" + str(len(stocks)))
               
      if doTrend:
         trendStocks = []
         print ("trendCandidates order based on trend value")
         ctr = 0
         for s in stocks:
            for t in tr:
               if s == t[0]:
                  if t[1][0] > 11 or t[1][1] > 11:
                     trendStocks.append(s)
                     print (str(s) + " added bull or bear trend > 11")
                  print (str(t))
            ctr += 1
            
         stocks = trendStocks
         
   #         if bullStrength > 8:
   #            trendCandidates[stock] = bullStrength
   #         elif bearStrength > 8:
   #            trendCandidates[stock] = bearStrength

      if doVolLess:
         print ("lastDaysVolLessCandidates order based on last day less vol")
         for l in ldvLess:
            for s in stocks:
               if s == l[0]:
                  print (str(l))

      if doVolGtr:
         gtrStocks = []
         
         print ("lastDaysVolGtrCandidates order based on last day greater vol")
         for g in ldvGtr:
            ctr = 0 
            for s in stocks:
               if s == g[0]:
                  print (str(g))
                  if g[1][0] == 1:
                     if g[1][1] > self.greaterVolumeThreshold:
                        gtrStocks.append(s)
                        print (s + " greaterVolume > thresh " + str(g[1][1]) + " added")
                  else:
                     print (s + " vol > thresh " + str(g[1][1]) + " popped")
                  break              
               ctr += 1
               
         stocks = gtrStocks
         
         print ("stocks after lastDaysVolGtrCandidates > greaterVolumeThreshold\n" + str(self.greaterVolumeThreshold) + " "  + str(stocks))
         
      print ("stocks\n" + str(stocks))
      print ("stocks len\n" + str(len(stocks)))
      
      return stocks

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDailyGaps(self, d, dc):

      dataLen = len(d)
               
      i = 0

      dayClose = []
      dayOpen = []
      dayDate = []
      dayVol = []
      
      highest = 0.0
      lowest = 9999999999.99
      
      gap = 0.0
      
      hiDate = ""
      hiVol = 0.0

      # Calculate the average gap between the close and the open
      for i in range(dataLen):
         if type(d) is dict:
            for k, v in d:
               if k == 'c':
                  dayClose.append(v)
               if k == 'o':
                  dayOpen.append(v)
               if k == 't':
                  dayDate.append(dc.getDateFromEpoch(v))
               if k == 'v':
                  dayVol.append(v)
         else:
            for k, v in d[i].items():
               if k == 'c':
                  dayClose.append(v)
               if k == 'o':
                  dayOpen.append(v)
               if k == 't':
                  dayDate.append(dc.getDateFromEpoch(v))
               if k == 'v':
                  dayVol.append(v)
      
      for n in range(i):
         diff = dayClose[n] - dayOpen[n + 1]
         if diff < 0:
            gap += diff*-1
            diff *=-1
         else:
            gap += diff    
         
         hi = diff
         lo = diff
         
         if hi > highest:
            highest = hi
            hiDate = str(dayDate[n + 1])
            hiVol = str(dayVol[n + 1])
            
         if lo < lowest:
            lowest = lo
      
      avg = (gap / i)
            
      return avg, highest, lowest, hiDate, hiVol
                  
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getPreMarketMovers(self):
   
      path = "/tmp/preMarketSuckDown"
      
      try:
         data = os.system("curl " + self.preMarketURL + " >" + path + " 2>&1")
      except (TimeoutError, URLError) as e:
         return ""
      
      e = e3 = e5 = e7 = ""
      s = s1 = s2 = s3 = ""
      stocks = []
      
      # We grab the top 4 pre market movers and analyze

      with open(path, 'r') as preData:
         for line in preData:
            if "tdGainersDesktop" in line:
               b, m, e = line.partition("stock=")
               b, m, e2 = e.partition("stock=")
               b, m, e3 = e2.partition("stock=")
               b, m, e4 = e3.partition("stock=")
               b, m, e5 = e4.partition("stock=")
               b, m, e6 = e5.partition("stock=")
               b, m, e7 = e6.partition("stock=")
               b, m, e8 = e7.partition("stock=")
      
      s, m, j = e.partition("\"")
      s1, m, j = e3.partition("\"")
      s2, m, j = e5.partition("\"")
      s3, m, j = e7.partition("\"")
      
      stocks.append(s3)
      stocks.append(s2)
      stocks.append(s1)
      stocks.append(s)
            
      return stocks

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTodaysDateData(self): 
         
      ts = time()
      date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
      
      yearMonth, sep, day = date.rpartition('-')
      year, sep, month = yearMonth.partition('-')
      
      return date, year, month, day
      #return date, year, month, str(int(day) - 1)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getDailyData(self, stock, months):
   
      date, year, month, day = self.getTodaysDateData()
      
      print (str(self.getTodaysDateData()))
      
      # Sometimes the day is one char 
      if len(day) == 1:
         day = "0" + day
      
      #day = str(int(day) + 1)
      
      endDate = year + "-" + month + "-" + day
      
      beginMonth = str(int(month) - months)
      
      # month = 2 - 6 months = -4 subtract from 12 and decrease the year by 1

      if int(beginMonth) < 0:
         beginMonth = int(beginMonth)*-1
         beginMonth = str(12 - beginMonth)
         year = str(int(year) - 1)
      
      if beginMonth == "0":
         beginMonth = "01"
         
      if len(beginMonth) == 1:
         beginMonth = "0" + beginMonth

      beginDate = year + "-" + beginMonth + "-" + day
            
      url = self.url + stock + self.rang + beginDate + "/" + endDate + self.key
      
      print (url)
      
      try:   
         with urllib.request.urlopen(url) as response:
            data = str(response.read())
      except TimeoutError:
         return ""
         
      #print ("data1 " + str(data))
      b, m, l = data.partition('[')
      #print ("L " + str(l))
      data, m2, l = l.partition(']')
      
      #print ("L " + str(l))
      #print ("data " + str(data))
      return data



