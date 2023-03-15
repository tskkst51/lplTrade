## lpltG is the master. Fires off lpltL jobs after pre market analysis
## lpltG should not trade

import lplTrade as lpl
import pyetrade
import sys
import os
import time
import json
import os.path
from optparse import OptionParser
from time import time, sleep
import pathlib
from shutil import copyfile

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

verbose = debug = quiet = False

parser = OptionParser()

parser.add_option("-a", "--alt", type="string",
   action="store", dest="alt", default=False,
   help="alternate currency to buy: usd... uer... btc... eth... bch...")

parser.add_option("-b", "--sandBox",
   action="store_true", dest="sandBox", help="Sandbox connection value")
   
parser.add_option("-c"  , "--profileConnectPath", dest="profileConnectPath",
   help="write report to FILE", metavar="FILE")

parser.add_option("-d", "--debug",
   action="store_true", dest="debug", help="don't lg.debug to logfile")
   
parser.add_option("-m", "--marketDataType", type="string",
   action="store", dest="marketDataType", default=False,
   help="currency to buy: btc... eth... bch...")

offLine = 0
parser.add_option("-o", "--offLine",
   action="store_true", dest="offLine", help="offLine")

parser.add_option("-p"  , "--profileTradeDataPath", dest="profileTradeDataPath",
   help="write report to FILE", metavar="FILE")
   
parser.add_option("-q", "--quiet",
   action="store_true", dest="quiet", default=False,
   help="don't lg.debug to stdout")
   
parser.add_option("-r", "--resume",
   action="store_true", dest="resume", help="resume")

parser.add_option("-s", "--stocks", type="string",
   action="store", dest="stocks", default=False,
   help="stock to bua/selly: AAPL")
      
parser.add_option("-u", "--currency", type="string",
   action="store", dest="currency", default=False,
   help="currency to buy: btc... eth... bch...")

parser.add_option("-v", "--verbose",
   action="store_true", dest="verbose", help="verbose")
   
parser.add_option("-t", "--timeBar", type="string",
   action="store", dest="timeBar", default=False,
   help="time bar: 1 5 10 minute...")
   
parser.add_option("-w", "--workPath", type="string",
   action="store", dest="workPath", default=False,
   help="work directory. default lplTrade...")

parser.add_option("-i", "--onlyUpdateDailyStocks",
   action="store_true", dest="onlyUpdateDailyStocks", help="onlyUpdateDailyStocks")
   
(clOptions, args) = parser.parse_args()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def isStoppedOut(stock):

   if quitMaxProfit:          
      if a[stock].getTotalGain() >= a[stock].getTargetProfit() and a[stock].getTotalGain() != 0.0:
         lg1.info ("MAX PROFIT REACHED, Gain: Bar: " + str(a[stock].getTotalGain()) + " " + str(barCtr))
         lg1.info ("MAX PROFIT TARGET: " + str(a[stock].getTargetProfit()))
         lg1.info ("MAX PROFIT FACTOR: " + str(maxProfit))
         lg1.info ("MAX PROFIT CLOSE PRICE: " + str(last))
         lg1.info ("MAX PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 2
                  
         # We are out with our PROFIT
      if doTrailingStop and positionTaken[stock] == stoppedOut:
         lg1.info ("TRAILING STOP REACHED, Gain: Bar: " + str(a[stock].getTotalGain()) + " " + str(barCtr))
         lg1.info ("MAX PROFIT TARGET: " + str(a[stock].getTargetProfit()))
         lg1.info ("MAX PROFIT FACTOR: " + str(maxProfit))
         lg1.info ("MAX PROFIT CLOSE PRICE: " + str(last))
         lg1.info ("MAX PROFIT TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 4
         
   if quitMaxLoss:            
      if a[stock].getTotalLoss() <= a[stock].getTargetLoss() and a[stock].getTotalLoss() != 0.0:
         lg1.info ("MAX LOSS REACHED, Gain: Bar: " + str(a[stock].getTotalLoss()) + " " + str(barCtr))
         lg1.info ("MAX LOSS TARGET: " + str(a[stock].getTargetLoss()))
         lg1.info ("MAX LOSS FACTOR: " + str(maxLoss))
         lg1.info ("MAX LOSS CLOSE PRICE: " + str(last))
         lg1.info ("MAX LOSS TIME: " + str(barCtr * timeBar) + " minutes")
         
         return 3
   return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def runTests(stocks):

   # Lauch tests in parallel mode. Wait for all pid's to finish then exit

   symsRunning = []
   pids = {}
   ctr = 1
   for sym in stocks:
      if ctr % maxNumProcesses != 0 and ctr <= maxNumProcesses:
         pids[sym] = th.launchStock(sym, os.path.basename(workPath))
         symsRunning.append(sym)
         print ("symsRunning after adding" + str(symsRunning))
         ctr += 1
      else:
         print ("sym in the Q " + str(sym))
         
#         if not sym in symsRunning:
#            symsRunning.append(sym)
            
         loop = True
         while loop:
            for s in symsRunning:
               if pids[s].poll() == None:
                  #print ("pid: " + str(pids[s]))
                  sleep(2)
               else:
                  lg1.debug ("Gotta poll value of: " + str(pids[s].poll()))
                  lg1.debug ("for : " + str(s))
                  pids.pop(s)
                  #print ("pids after remove " + str(pids))
                  #print ("symsRunning before remove " + str(symsRunning))
                  symsRunning.remove(s)
                  #print ("symsRunning after remove " + str(symsRunning))
                  if not sym in symsRunning:
                     symsRunning.append(sym)
                  #print ("symsRunning after append" + str(symsRunning))
                  pids[sym] = th.launchStock(sym, os.path.basename(workPath))
                  #print ("pids running after append" + str(pids))
                  loop = False   
                  break
   loop = True
   while loop:
      #print ("pids last loop " + str(pids))
      for s, p in pids.items():
         #print ("pids last loop stock " + str(s))
         if pids[s].poll() == None:
            sleep(2)
         else:
            pids.pop(s)
            #print ("len pids " + str(len(pids)))
            if len(pids) == 0:
               loop = False
            break

   # Print any remaining test processes. Shouldn't be any
   
   os.system("ps -ef | grep 'testDB.sh' | grep -v grep") 

   return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getStocksFromBCDir(path):

   stocks = []

   for rootPath, directories, paths in os.walk(path):
      for path in paths:
         if path.endswith(".bc"):
            if os.stat(rootPath + "/" + path).st_size > 1000:
               stockName = path.replace("active","") 
               stockName = stockName.replace(".bc","")
               if stockName not in stocks:
                  print ("stockName: " + str(stockName))
                  stocks.append(stockName)      
   
   return stocks

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getAutoStocks(orderType, numStocksToTrack):

   srcPath = "daysBest/latest"
   #if isinstance(orderType, int):
   if int(orderType) == int(magicNumber):
      srcPath = "daysBest/latestMN"
   elif int(orderType) == int(percent):
      srcPath = "daysBest/latestPC"
   
   print ("magicNumber " + str(magicNumber))
   print ("orderType " + str(orderType))
   print ("srcPath " + str(srcPath))
   
   dstPath="profiles/autoStocks.txt"
   numStocks = 0
   lastStock = ""
   daysBestStocks = []
   
   #assert(numDaysTestData)

   with open(srcPath, 'r') as pp:
      lines = pp.readlines()
   
   print ("lines " + str(lines))
   print ("len lines " + str(len(lines)))

   print ("numStocksToTrack " + str(numStocksToTrack))
   print ("numDaysTestData " + str(numDaysTestData))

   # line ['RAPT', '4.20', '3', '39.47']

   # Read from first line
   for line in lines:
      line = line.split()
      if numStocks < numStocksToTrack:
         # Check for dups
         if line[0] == lastStock:
            print ("found duplicate " + str(line[0]))
            continue
            
         # Don't use stocks with daily gains less than the value: e.g $2.0
         if float(line[1]) < daysBestAvgDailyGain:
            print ("stock excluded < daysBestAvgDailyGain " + str(line))
            continue
            
         # Don't use stocks with e.g: test data > 4 days
         # This is set to get stocks with not much test data 
         # Reversing this 6/22/22 so we get only stocks with test data >
         if int(line[2]) > numDaysTestData:
            with open(dstPath, 'a') as pp:
               pp.write(line[0] + "\n")
               print ("stock selected auto " + str(line))
            
            daysBestStocks.append(line[0])
            
            lastStock = line[0]
            numStocks += 1
         else:
            print ("line excluded < numDaysTestData " + str(line))
   
   return daysBestStocks 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def genProfile(algo, stock):

   if not offLine:
      print ("genProfile algo " + str(algo) + " " + str(stock))
      
      cmd = "python3 bin/profileGenerator.py -a " + algo + " -d \"\""
      if os.system(cmd) > 0:
         print("Cannot create profile from " + str(cmd) + " " + str(algo))
         return 1
      
   return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def analyzeStocks(pf, pr, tg, dc, preOrPost, useLiveDailyData, stocks, onlyUpdateDailyStocks, numDaysTestData, daysBestStocks):

   if useStocksFromDailyCharts:
      stocks = pr.getStockStrFromDailyCharts()
      if useTestMinuteCharts:
         stocks += pr.getStockStrFromTestMinuteCharts()
         # Remove duplicates
         stocks = list(set(stocks))

   if not onlyUpdateDailyStocks:
      print ("stocks len\n" + str(len(stocks)))
      if len(stocks) > numStocksToProcessInPremarket:
         while len(stocks) > numStocksToProcessInPremarket:
            print ("SKIPPING " + str(stocks[-1]))
            del stocks[-1]

   
   print ("useLiveDailyData\n" + str(useLiveDailyData))
   print ("stocks\n" + str(stocks))
   print ("stocks len\n" + str(len(stocks)))
   
   if onlyUpdateDailyStocks:
      pr.updateDailyCharts(tg, dc, stocks)
      exit (1)

   # Candidates come from premarket movers internet site, daily charts, ETF movers
   candidates = pr.getStockCandidates(tg, dc, stocks, findPreMarketMovers, findYahooMovers, useLiveDailyData, 1)
   
   # Only use candidates that have a minimum number of days test data
   if numDaysTestData:
      candidates = pr.getStocksWithDailyData(candidates, numDaysTestData)
      
   print ("candidates getStocksWithDailyData\n" + str(candidates))
   print ("candidates getStocksWithDailyData len " + str(len(candidates)))
   
   # Only use candidates within price range
   if minStockPrice or maxStockPrice:
      candidates = pr.getStocksWithinPriceRange(candidates, minStockPrice, maxStockPrice)
   
   print ("candidates getStocksWithinPriceRange\n" + str(candidates))
   print ("candidates getStocksWithinPriceRange len " + str(len(candidates)))

   # Exclude stocks listed in the exclusion list
   if excludeStocks:
      candidates = pr.removeStocksFromExclusionList(candidates)
   
   print ("candidates removeStocksFromExclusionList\n" + str(candidates))
   print ("candidates removeStocksFromExclusionList len " + str(len(candidates)))

   # Suck in the yearly data charts for the candidates
   dailyStockData = pr.getDailyStockData(tg, dc, candidates)

   tg.setAllStocksArr(dailyStockData)
   
   # Calculate the premarket gap movement of the candidates
   dailyGapData = pr.getDailyGapData(tg, dc, candidates)
   
   # Get an ordered list of the best candidates 
   orderedStocks = pr.getDailyOrderedStocks(tg, dailyGapData, dailyStockData, candidates, daysBestStocks)

   print ("orderedStocks\n" + str(orderedStocks))

   #if useDaysBest and not onlyUpdateDailyStocks:
   #   stocks = daysBestStocks
 
   # Pick the proper algorithm to use based on saved algo data
   algoData, stocks = pr.getAlgorithm(orderedStocks, useDefaultAlgo, useStocksWithNoTestData, pf.gv("defaultAlgoStr"))

   # LIVE run lpltSlave.py with the #1-... stock candidate
   # If it profits out. invoke with best performing at the moment

   return algoData, stocks
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load profileTradeData data

pf = lpl.Profile(clOptions.profileTradeDataPath)
cf = lpl.Profile(clOptions.profileConnectPath)

d = pf.getPFValues()
c = cf.getPFValues()

# Get trading elements
#d = loadProfileData(clOptions.profileTradeDataPath)

# Get connection elements
#c = loadProfileData(clOptions.profileConnectPath)

dInitial = d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set data variables

# Price array, hi, lo, open, close, volume, date indexes
hi = 0
lo = 1
op = 2
cl = 3
vl = 4
bl = 5
sH = 6
sL = 7
dt = 8

# Values set by the trading service
svcBid = 0
svcAsk = 1
svcLast = 2
svcVol = 3
svcDate = 4

# Keep track of average volume based on all bars
avgVol = 0

barChart = [[]]

resumedBarCharCtr = 0

barCtr = exitTrading = 0

close = action = noAction = 0
buyAction = buy = 1
sellAction = sell = 2
executeOnOpenPosition = 1
executeOnClosePosition = 2
#last = bid = ask = 0.0
forceClose = 1

stocks = []

stock = str(pf.gv("stock"))
stocksStr = str(pf.gv("stocks"))
stocksFile = str(pf.gv("stocksFile"))
stocks = stocksStr.split(',')
etfs = str(pf.gv("etfs"))
profileName = str(pf.gv("profileName"))
currency = str(pf.gv("currency"))
alt = str(pf.gv("alt"))
timeBar = int(pf.gv("timeBar"))
service = str(pf.gv("service"))
algorithms = str(pf.gv("algorithms"))
tradingDelayBars = int(pf.gv("tradingDelayBars"))
openBuyBars = int(pf.gv("openBuyBars"))
closeBuyBars = int(pf.gv("closeBuyBars"))
openSellBars = int(pf.gv("openSellBars"))
closeSellBars = int(pf.gv("closeSellBars"))
profileTradeData = str(d)
resume = int(pf.gv("resume"))
workPath = str(pf.gv("workPath"))
waitForTopMinute = int(pf.gv("waitForTopMinute"))
halfDayEndTime = str(pf.gv("halfDayEndTime"))
halfDays = str(pf.gv("halfDays"))
preMarket = str(pf.gv("preMarket"))
afterMarket = str(pf.gv("afterMarket"))
preMarketAnalysis = int(pf.gv("preMarketAnalysis"))
afterMarketAnalysis = int(pf.gv("afterMarketAnalysis"))
afterMarketEndTime = int(pf.gv("afterMarketEndTime"))
onlyUpdateDailyStocks = int(pf.gv("onlyUpdateDailyStocks"))
numDaysTestData = int(pf.gv("numDaysTestData"))
useDaysBest = int(pf.gv("useDaysBest"))
daysBestAvgDailyGain = float(pf.gv("daysBestAvgDailyGain"))

useStocksFromDailyCharts = int(pf.gv("useStocksFromDailyCharts"))
findPreMarketMovers = int(pf.gv("findPreMarketMovers"))
findYahooMovers = int(pf.gv("findYahooMovers"))

maxStocksToTrade = int(pf.gv("maxStocksToTrade"))
maxNumProcesses = int(pf.gv("maxNumProcesses"))

doTrailingStop = int(pf.gv("doTrailingStop"))
maxProfit = float(pf.gv("maxProfit"))
maxLoss = float(pf.gv("maxLoss"))
quitMaxProfit = int(pf.gv("quitMaxProfit"))
quitMaxLoss = int(pf.gv("quitMaxLoss"))
useLiveDailyData = int(pf.gv("useLiveDailyData"))
useDefaultAlgo = int(pf.gv("useDefaultAlgo"))
useStocksWithNoTestData = int(pf.gv("useStocksWithNoTestData"))
useTestMinuteCharts = int(pf.gv("useTestMinuteCharts"))
minStockPrice = float(pf.gv("minStockPrice"))
maxStockPrice = float(pf.gv("maxStockPrice"))
excludeStocks = int(pf.gv("excludeStocks"))
stockOrderFile = str(pf.gv("stockOrderFile"))
defaultStocks = str(pf.gv("defaultStocks"))
useDefaultStocks = int(pf.gv("useDefaultStocks"))

# Make sure stocksFileMultiplier is "1" or more...
stocksFileMultiplier = float(pf.gv("stocksFileMultiplier"))
numStocksToProcessInPremarket = int(pf.gv("numStocksToProcessInPremarket"))
loopDelay = float(pf.gv("loopDelay"))
useFirstMinuteAvgs = int(pf.gv("useFirstMinuteAvgs"))

masterMode = 1

# Connection service profile 'c'
#offLine = int(pf.gv("offLine"))
sandBox = int(cf.gv("sandBox"))
maxNumStocksToTrade = int(cf.gv("maxNumStocksToTrade"))


dailyChartPath = "dc/"
dailyChartExt = ".dc"
minuteChartPath = "test/bc/"
minuteChartExt = ".bc"
dailyGapExt = ".gp"
bestAlgosPath = "bestAlgos/"
bestAlgosExt = ".bs"

#symbol = currency + alt
symbol = [""]

marketDataType = "intraday"
numBars = {}

lastMinuteOfLiveTrading = 155958

marketOpen = 0
firstTimeThru = 0
magicNumber = 2
percent = 3

#new_dict = { new_list: [] for new_list in range(4)} 

# Add ETF stocks to stocksStr
#if preMarketAnalysis:
#   stocks += etfs.split(",")

positionTaken = {}
stocksChart = {}
pathsChart = {}
profileData = {}
serviceValues = {}
doOnceOnOpen = {}
doOnceOnClose = {}
dirty = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overide profileTradeData data with command line data

if int(clOptions.currency):
   currency = clOptions.currency
   
if clOptions.alt:
   alt = clOptions.alt
   
if clOptions.stocks:
   print ("pf.gv(stocks] " + str(pf.gv("stocks")))
   stocks.append(clOptions.stocks)
#   d["stocks"] = str(stocks)
#print ("d[stocks] " + str(d["stocks")))

if clOptions.debug:
   debug = int(clOptions.debug)

if clOptions.verbose:
   verbose = int(clOptions.verbose)
   
if clOptions.resume:
   resume = int(clOptions.resume)
   
if clOptions.sandBox:
   sandBox = clOptions.sandBox

if clOptions.marketDataType:
   marketDataType = clOptions.marketDataType

if clOptions.offLine:
   offLine = clOptions.offLine

if clOptions.timeBar:
   timeBar = clOptions.timeBar
   #d["timeBar"] = str(timeBar)
   
if clOptions.workPath:
   workPath = clOptions.workPath
   #d["workPath"] = str(workPath)

if clOptions.onlyUpdateDailyStocks:
   onlyUpdateDailyStocks = 1


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set stocks to trade based on pre market analysis

if offLine:
   resume = 1
   preMarketAnalysis = 0

if masterMode:
   timeBar = 1
   #d["timeBar"] = "1"
   
if not offLine:
   if useDefaultStocks:
      stocks = defaultStocks.split(',')
   elif stocksFile != "" and not onlyUpdateDailyStocks:
      stocks = getAutoStocks(stocksFile, round(maxNumStocksToTrade * stocksFileMultiplier, 2))   
   
   elif preMarketAnalysis:
   
      logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
      
      # Instantiate the needed objects
      l = lpl.Log(0, 0, logPath, "/tmp/oo", "", 0)
      pr = lpl.Premarket(minuteChartPath, minuteChartExt, dailyChartPath, dailyChartExt, dailyGapExt, bestAlgosPath, bestAlgosExt)
      tg = lpl.Target(c, d, l)
      dc = lpl.Dailychart()
      
      daysBestStocks = []
      
      if useDaysBest:
         daysBestStocks = getAutoStocks(useDaysBest, numStocksToProcessInPremarket)   
         print (" stocks after getauto" + str(daysBestStocks))
         print (" stocks len after getauto " + str(len(daysBestStocks)))
         
      algoData, stocks = analyzeStocks(pf, pr, tg, dc, "pre", useLiveDailyData, stocks, onlyUpdateDailyStocks, numDaysTestData, daysBestStocks)
      
      if onlyUpdateDailyStocks:
         exit (0)
   
      print ("pre market analysis stocks " + str(stocks))

# Trim list of stocks to maxNumStocksToTrade max

if offLine and clOptions.stocks:
   stocks = clOptions.stocks
print ("stocks before " + str(stocks))
print ("stocks len " + str(len(stocks)))
print ("offLine " + str(offLine))

if offLine and not clOptions.stocks:
   if workPath:
      stocks = getStocksFromBCDir(workPath + "/bc")
else:
   if isinstance(stocks, str):
      stocks = stocks.split(",")
      

   # Insert the default stocks into the first array positions
   if useDefaultStocks:   
      print ("stocks before defaultStocks " + str(stocks))
      print ("defaultStocks " + str(defaultStocks))
      defaultStocksArr = defaultStocks.split(",")
      for s in defaultStocksArr:
         stocks.insert(0, s)
      print ("stocks after defaultStock insert " + str(stocks))
      
   if stocksFile == "":   
      totalStocks = round(maxNumStocksToTrade * stocksFileMultiplier, 2)
      if len(stocks) > totalStocks:
         while len(stocks) > totalStocks:
            del stocks[-1]

print ("stocks after" + str(stocks))
print ("stocks len " + str(len(stocks)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

if service == "bitstamp":
   cn = lpl.ConnectBitStamp(service, currency, alt)
   cn.connectPublic()
elif service == "bitfinex":
   cn = lpl.ConnectBitFinex()
elif service == "eTrade":
   symbol = stock
   cn = lpl.ConnectEtrade(c, stocks, debug, verbose, marketDataType, sandBox, offLine)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up stock arrays

for stock in stocks:
   stocksChart[stock] = [[0.0,0.0,0.0,0.0,0,0.0,0,0,""]]
   pathsChart[stock] = {}
   profileData[stock] = {}
   positionTaken[stock] = 0
   doOnceOnOpen[stock] = 0
   doOnceOnClose[stock] = 0
   dirty[stock] = 0

# Save the order for later inspection
if not offLine:
   oCtr = 0
   for stock in stocks:
      oCtr += 1
      with open(stockOrderFile, "a+") as orderFile:
         orderFile.write('%s' % str(stock) + " " + str(oCtr) + "\n")
            
print ("stocks after" + str(stocks))
print ("stocks len " + str(len(stocks)))

# Setup paths

cwd = os.getcwd()
wcwd = ""

# dcPath isn't used in the master
dcPath = cwd + "/dc/" + "AAPL" + ".dc"

if workPath:
   os.chdir(workPath)
   wcwd = os.getcwd()

tm = lpl.Time()
lg = {}

for stock in stocks:
   logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
   debugPath = clOptions.profileTradeDataPath.replace("profiles", "debug")
   barChartPath = clOptions.profileTradeDataPath.replace("profiles", "bc")
   pricesPath = clOptions.profileTradeDataPath.replace("profiles", "prices")
   testPath = clOptions.profileTradeDataPath.replace("profiles", "test")
   statsPath = clOptions.profileTradeDataPath.replace("profiles", "logs")

   logPath = logPath.replace(".json_" + stock, stock + ".ls")
   debugPath = debugPath.replace(".json_" + stock, stock + ".dm")
   #slaveDebugPath = debugPath.replace(".json_" + stock, stock + ".ds")
   barChartPath = barChartPath.replace(".json_" + stock, stock + ".bc")
   pricesPath = pricesPath.replace(".json_" + stock, stock + ".pr")
   testPath = testPath.replace(".json_" + stock, stock + ".tt")
   statsPath = statsPath.replace(".json_" + stock, stock + ".st")

   logPath = logPath.replace(".json", "")
   debugPath = debugPath.replace(".json", "")
   #slaveDebugPath = slaveDebugPath.replace(".json", "")
   barChartPath = barChartPath.replace(".json", "")
   pricesPath = pricesPath.replace(".json", "")
   testPath = testPath.replace(".json", "")
   statsPath = statsPath.replace(".json", "")
   
   # Populate the strings and log object
   lp = logPath + stock + ".log"
   db = debugPath + stock + ".dm"
   #ds = slaveDebugPath + stock + ".ds"
   bp = barChartPath + stock + ".bc"
   pp = pricesPath + stock + ".pr"
   tp = testPath + stock + ".tt"
   st = statsPath + stock + ".st"
      
   #pathsChart[stock] = {"logPath" : lp, "debugPath" : db, "barChartPath" : bp, "pricesPath" : pp, "testPath" : tp, "slaveDebugPath" : ds}
   pathsChart[stock] = {"logPath" : lp, "debugPath" : db, "barChartPath" : bp, "pricesPath" : pp, "testPath" : tp, "statsPath" : st}
      
   lg[stock] = lpl.Log(debug, verbose, pathsChart[stock]['logPath'], pathsChart[stock]['debugPath'], pathsChart[stock]['statsPath'], offLine)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize trading objects

ba = {}
tr = {}
lm = {}
a = {}
pr = {}
pa = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm,  barcharts objects

#stocks = stocks.split(",")

# find best profile to run against list of stocks
for stock in stocks:
#   if preMarketAnalysis:
#      if genProfile(algoData[stock], stock):
#         exit (1)
#      profileData[stock] = loadProfileData(clOptions.profileTradeDataPath)
#   else:
#      # Use default list
#      profileData[stock] = d

   profileData[stock] = pf.readProfile(clOptions.profileTradeDataPath)
   #profileData[stock] = loadProfileData(clOptions.profileTradeDataPath)
   ba[stock] = lpl.Barchart(pathsChart[stock]['barChartPath'], offLine, timeBar)
   tr[stock] = lpl.Trends(profileData[stock], lg[stock], cn, ba[stock], offLine, stock)
   lm[stock] = lpl.Limits(profileData[stock], lg[stock], cn, ba[stock], pf, stock)
   pr[stock] = lpl.Price(cn, offLine)
   pa[stock] = lpl.Pattern(profileData[stock], ba[stock], lg[stock])
   dc = lpl.Dailychart()
   dy = lpl.Dynamic(timeBar, dcPath, dc, offLine)
   a[stock] = lpl.Algorithm(profileData[stock], lg[stock], cn, ba[stock], tr[stock], lm[stock], pa[stock], pr[stock], dy, offLine, stock)
   ut = lpl.Util()
   th = lpl.Thred(ut, offLine, cwd, wcwd)

lg1 = lg[stocks[0]]
a1 = a[stocks[0]]
tr1 = tr[stocks[0]]
lm1 = lm[stocks[0]]
pr1 = pr[stocks[0]]
pa1 = pa[stocks[0]]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if useFirstMinuteAvgs:
   testDir = "test/"
   firstMinuteAvgs = []
   if offLine:
      testDir = cwd + "/test/"
   for s in stocks:
      firstMinuteAvgs.append(ba[s].getMinuteBarAvgs(s, timeBar, testDir))
      print ("firstMinuteAvgs " + str(firstMinuteAvgs))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set end time

lg1.debug ("halfDays set to: " + halfDays)
lg1.debug ("getDateMonthDayYear " + str(cn.getDateMonthDayYear()))

if str(cn.getDateMonthDayYear()) in halfDays:
   lastMinuteOfLiveTrading = int(halfDayEndTime)
   lg1.debug ("lastMinuteOfLiveTrading is set to: " + str(lastMinuteOfLiveTrading))
   
   lg1.debug ("Half day trading is set to: " + halfDayEndTime)
   lg1.debug ("It must be a day after a holiday: " + halfDays)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize files


for stock in stocks:

   with open(pathsChart[stock]['debugPath'], "a+", encoding="utf-8") as debugFile:
      debugFile.write(lg[stock].infoStamp(a1.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
      debugFile.write(lg[stock].header(tm.now(), stock))
   
   lg1.info("Using " + pathsChart[stock]['debugPath'] + " as debug file")
   
#   with open(pathsChart[stock]['slaveDebugPath'], "a+", encoding="utf-8") as slaveDebugFile:
#      slaveDebugFile.write(lg[stock].header(tm.now(), stock))
#   
#   lg1.info("Using " + pathsChart[stock]['slaveDebugPath'] + " as slave debug file")
   
   with open(pathsChart[stock]['logPath'], "a+", encoding="utf-8") as logFile:
      logFile.write(lg[stock].infoStamp(a1.getLiveProfileValues(d, clOptions.profileTradeDataPath)))
      logFile.write(lg[stock].header(tm.now(), stock))
   
   lg1.info("Using " + pathsChart[stock]['logPath'] + " as log file")
   
   with open(pathsChart[stock]['barChartPath'], "a+", encoding="utf-8") as resumeFile:
      lg1.info("Using " + pathsChart[stock]['barChartPath'] + " as bar chart file")
   
   with open(pathsChart[stock]['pricesPath'], "a+", encoding="utf-8") as priceFile:
      lg1.info("Using " + pathsChart[stock]['pricesPath'] + " as prices file")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Display profile data

lg1.debug ("Reading profileTrade data from: " + clOptions.profileTradeDataPath + "\n")
lg1.debug ("Using symbol: " + symbol)
for stock in stocks:
   lg1.debug ("Last trade: " + str(cn.getLastTrade(stock)))
lg1.debug ("Minute bar chart: " + str(timeBar))
lg1.debug ("openBuyBars: " + str(openBuyBars))
lg1.debug ("closeBuyBars: " + str(closeBuyBars))
lg1.debug ("openSellBars: " + str(openSellBars))
lg1.debug ("closeSellBars: " + str(closeSellBars))
lg1.debug ("tradingDelayBars: " + str(tradingDelayBars))
lg1.debug ("sand: " + str(sandBox))
lg1.debug ("offLine: " + str(offLine))
lg1.debug ("marketDataType: " + cn.getMarketDataType())
lg1.debug ("dateTimeUTC: " + cn.getDateTimeUTC())
lg1.debug ("dateTime: " + cn.getDateTime())
lg1.debug ("getQuoteStatus: " + cn.getQuoteStatus())
lg1.debug ("workPath: " + workPath)
lg1.debug (a1.getAlgorithmMsg())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize based on live or offLine state 

last = {}
bid = {}
ask = {}
vol = {}
initialVol = {}
populatedStocks = []

# Start trading at the top of the minute
if not offLine:
   if waitForTopMinute and not resume:
      tm.waitUntilTopMinute()
   if preMarket and waitForTopMinute:
      tm.waitUntilTopMinute()

numPrices = {}

# Init buffers
if offLine:
   for stock in stocks:
      numPrices = pr[stock].initPriceBuffer(pathsChart[stock]['pricesPath'])
      lg[stock].debug ("number of prices from file: " + str(numPrices))
      if numPrices > 10:
         populatedStocks.append(stock)
         
   stocks = populatedStocks
   
lg1.debug ("Start bar: " + str(barCtr))
lg1.debug ("resume: " + str(resume))

if stock in stocks:
   lm[stock].setTradingDelayBars()
   ba[stock].setTimeBarValue(timeBar)

barCtr = 0
# Read in barChart and resume from it
if resume:
   for stock in stocks:
      bcSize = pathlib.Path(pathsChart[stock]['barChartPath']).stat().st_size
      
      lg1.verbose ("Size of barchart file " + str(stock) + " : " + str(bcSize))
   
      # Ignore reading from barChart if it is empty
      if bcSize:
         numBars[stock] = ba[stock].read(pathsChart[stock]['barChartPath'], stocksChart[stock], timeBar)
         
         lg1.debug ("Number of bars in file on disk : " + str(numBars[stock]))
         
         barCtr = numBars[stock]
         if not offLine:
            barCtr = numBars[stock] - 1
            
      # If offline then iterate over the stored bar chart starting at bar 0
      if offLine:
         barCtr = 0
            
      # We're live, program halted and now resumed. Initilize a new bar and trade on
      else:
         ba[stock].appendBar(stocksChart[stock])
         a[stock].setAllLimits(stocksChart[stock], barCtr, last[stock])
         
lg1.debug ("Start bar: " + str(barCtr))

setProfit = 0

# Start trading at beginning of day
#if not offLine:
#   if not preMarket:
#      if a1.getMarketBeginTime():
#         lg1.info("Waiting till the market opens...")
#         cn.waitTillMarketOpens(a1.getMarketOpenTime())

# CALL setStockValues SKIPPING OPEN VALUE WHICH IS THE CLOSE OF THE LAST DAY   
# observed at least 3 prices being the close of prev day

#if preMarketAnalysis:
#   for stock in stocks:
#      # Launch lpltL.py
#      pass


print ("stocks " + str(stocks))
print ("stocks len " + str(len(stocks)))

if offLine:
   pr[stock].setNextBar(timeBar)

pid = {}
numLaunchedPids = 0

if useDefaultStocks and not offLine:
   pid = th.launchStocks(stocks, maxStocksToTrade, os.path.basename(workPath))
elif preMarketAnalysis and not offLine and stocksFile == "":
   pid = th.launchAlgos(algoData, maxStocksToTrade, os.path.basename(workPath))
#if not preMarketAnalysis and not offLine:
elif stocksFile != "" and not offLine:
   pid = th.launchStocks(stocks, maxStocksToTrade, os.path.basename(workPath))

if offLine:
   runTests(stocks)
   exit (0)
       
if pid:
   numLaunchedPids = len(pid)

if (quitMaxProfit or doTrailingStop) and maxProfit == 0.0:
   lg1.debug ("Max profit not set and it should be! ")
   exit (2)

lg1.debug ("stocks " + str(stocks))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop. Loop forever. Pause trading during and after market hours 

firstTime = 1

while True:

   # Start trading at beginning of day
   if not a1.doPreMarket():
      #if not marketOpen:
         #if a.getMarketBeginTime():
      lg1.info("Waiting till the market opens...")
      cn.waitTillMarketOpens(a1.getMarketBeginTime())
      #marketOpen += 1

   # Start looping at beginning of day
#   if not a1.doPreMarket():
#      if not offLine and not marketOpen:
#         if a1.getMarketBeginTime():
#            lg1.info("Waiting till the market opens...")
#            cn.waitTillMarketOpens(a1.getMarketOpenTime())
#            marketOpen += 1

   
   endBarLoopTime = cn.adjustTimeToTopMinute(cn.getTimeHrMnSecs() + (100 * timeBar))

   print ("cn.getTimeHrMnSecs() " + str(cn.getTimeHrMnSecs()))
   print ("endBarLoopTime " + str(endBarLoopTime))

   # Set the initial price
   if firstTime:
      if service == "eTrade":
         serviceValues = cn.setStockValues(stocksChart, 0, stocks)
         lg1.debug ("serviceValues 1\n" + str(serviceValues))
      
      for stock in stocks:
         lg1.debug ("serviceValues[stock] " + str(serviceValues[stock]))
         bid[stock], ask[stock], last[stock], vol[stock]  = \
            pr[stock].getNextPriceArr(serviceValues[stock], barCtr)
      firstTime = 0
                  
   lg1.debug ("End bar time : " + str(endBarLoopTime))
   lg1.debug ("Start time: " + str(cn.getTimeStamp()))
         
   for stock in stocks:
      initialVol[stock] = serviceValues[stock][svcVol]
      
   for stock in stocks:
      if firstTimeThru == 0:
         ba[stock].loadFirstBar(stocksChart[stock], cn.getTimeStamp(), barCtr, bid[stock], ask[stock], last[stock], initialVol[stock])
         firstTimeThru += 1
      else:
         ba[stock].loadInitBar(stocksChart[stock], cn.getTimeStamp(), barCtr, bid[stock], ask[stock], last[stock], initialVol[stock])
   
   a1.setCurrentBar(barCtr)
   a1.setNextBar(barCtr + 1)

   # Set do on open or close to 0
   for stock in stocks:
      doOnceOnOpen[stock] = 0
      doOnceOnClose[stock] = 0
      dirty[stock] = 0
      
   # Set all decision points at the end of the previous bar            
   for stock in stocks:
      a[stock].setAllLimits(stocksChart[stock], barCtr, last[stock])

   # Manage PID's
   if preMarketAnalysis:
      ctr = 0
      for stock in stocks:
         if ctr >= maxNumProcesses:
            if len(pid[stock]) > 0:
               if not th.isPIDRunning(pid[stock]):
                  print ("POP PID FROM RUNNING QUEUE")
               ctr += 1

   # Loop until each bar has ended
   while True:
      # Too much data causes tests to run slower. Use a delay getting data
      if not offLine and loopDelay > 0:
         sleep(loopDelay)
      
      # Set the values from the trading service
      serviceValues = cn.setStockValues(stocksChart, barCtr, stocks)

      lg1.debug ("serviceValues " + str(serviceValues))

      a[stock].unsetActionOnOpenBar()
      
      for stock in stocks:
         bid[stock], ask[stock], last[stock], vol[stock] = pr[stock].getNextPriceArr(serviceValues[stock], barCtr)
         vol[stock] = cn.getTotalVolume(stock) - initialVol[stock]         

      lg1.debug ("vol[stock] \n" + str(vol[stock]))
       
      # Set the profit to gain
      if not setProfit:
         if quitMaxProfit > 0.0:
            setProfit += 1
            for stock in stocks:
               a[stock].setTargetProfit(last[stock], maxProfit)
               lg[stock].debug("Min profit set to: " + str(a[stock].getTargetProfit()))
               a[stock].setTargetLoss(last[stock], maxLoss)
               lg[stock].debug("Max loss set to: " + str(a[stock].getTargetLoss()))

      # Do one time on open
      if not doOnceOnOpen:
         for stock in stocks:
            a[stock].setActionOnOpenBar()
            if not masterMode:
               positionTaken[stock] = a[stock].takePosition(bid, ask, last, vol, barChart, barCtr)
            doOnceOnOpen[stock] += 1
            a[stock].unsetActionOnOpenBar()

#      for stock in stocks:
#         exitVal = isStoppedOut(stock)
#         if exitVal > 0:
#            lg[stock].info ("\nSTOPPED OUT: " + stock)
#            #exit(exitVal)

      for stock in stocks:
         lg[stock].info ("\nSYM : " + str(stock) + "\n")
         lg[stock].info ("BAR : " + str(barCtr))
         lg[stock].info ("HI  : " + str(stocksChart[stock][barCtr][hi]))
         lg[stock].info ("LAST: " + str(last[stock]))
         lg[stock].info ("BID : " + str(bid[stock]))
         lg[stock].info ("ASK : " + str(ask[stock]))
         lg[stock].info ("LO  : " + str(stocksChart[stock][barCtr][lo]))
         lg[stock].info ("VOL : " + str(vol[stock]) + "\n")
                     
      if not offLine:
         for stock in stocks:
            ba[stock].loadBar(stocksChart[stock], vol[stock], barCtr, bid[stock], ask[stock], last[stock])
                  
      # Save off the prices so they can be later used in offLine mode
      if not offLine:
         for stock in stocks:
            # Write prices and barcharts for 1-5 min charts
            pr[stock].write(pathsChart[stock]['pricesPath'], ask[stock], bid[stock], last[stock], vol[stock], barCtr)

      print("endBarLoopTime " + str(endBarLoopTime))
      print ("cn.getTimeHrMnSecs() " + str(cn.getTimeHrMnSecs()))
      
      # Beginning of next bar. 2nd clause is for offline mode
      if cn.getTimeHrMnSecs() >= endBarLoopTime or pr[stock].isNextBar(timeBar):      
         
         # After first bar, compare first bar movement
#         if useFirstMinuteAvgs and barCtr == 1:
#            firstBarLen = []
#            for stock in firstMinuteAvgs:
#               fbl = ba[stock].getFirstBarLen(ba[stock], 0)
#               fbl - firstMinuteAvgs[stock]
            
         # Only do beginning of the bar section once
         for stock in stocks:
            if dirty[stock]:
               continue
            dirty[stock] += 1
         
            if not offLine:
               ba[stock].loadEndBar(stocksChart[stock], cn.getTimeStamp(), barCtr, bid[stock], ask[stock], last[stock], vol[stock])            
            
            # Print out the bar chart. Only print the last 20 bars
            if not offLine:
               ba[stock].write(stocksChart[stock], pathsChart[stock]['barChartPath'], barCtr)
         
            lg[stock].info ("Stock: " + str(stock) + "\n")
            lg[stock].info ("Last price: " + str(last[stock]) + " Position: " + str(positionTaken[stock]))
            lg[stock].info ("Average Volume: " + str(ba[stock].getAvgVol()))
            lg[stock].info ("Average Bar length: " + str(ba[stock].getAvgBarLen()))
   
            lg1.debug ("\nNEW BAR ===========================================\n")
            lg1.debug ("STOCKK " + stock + " LASTT " + str(last[stock]))
            
            a[stock].setActionOnCloseBar()
            
            if not masterMode:
               positionTaken[stock] = a[stock].takePosition(bid[stock], ask[stock], last[stock], vol[stock], stocksChart[stock], barCtr)
               
            a[stock].unsetActionOnCloseBar()

            if not offLine:
               ba[stock].appendBar(stocksChart[stock])
            
            # Keep track of the bars in a position
            if a[stock].inPosition():
               ba[stock].setBarsInPosition()
   
         barCtr += 1
         break
         
         # End of bar reached.
      
      for stock in stocks:
         if not masterMode:
            positionTaken[stock] = a[stock].takePosition(bid[stock], ask[stock], last[stock], vol[stock], stocksChart[stock], barCtr)

#      for stock in stocks:
#         exitVal = isStoppedOut(stock)
#         if exitVal > 0:
#            lg[stock].info ("\nSTOPPED OUT: " + stock)

#      for stock in stocks:
#         if a[stock].getWaitForNextBar() and barCtr < a[stock].getNextBar():
#            lg[stock].debug("Waiting for next bar...")
#            continue

      # Close out of any position at the end of the day
      for stock in stocks:
         if not offLine and not a[stock].getAfterMarket():
            if a[stock].isMarketExitTime():
               if a[stock].inPosition():
                  if not masterMode:
                     a[stock].closePosition(barCtr, stocksChart[stock], bid, ask, forceClose)
               ba[stock].loadEndBar(stocksChart[stock], cn.getTimeStamp(), barCtr, bid[stock], ask[stock], last[stock], vol[stock])
               ba[stock].write(stocksChart[stock], pathsChart[stock]['barChartPath'], barCtr)

               exitTrading += 1

#      if exitTrading and afterMarketAnalysis:
#         if not offLine and afterMarketEndTime:
#            # Wait for afterMarketEndTime 8pm
#            while afterMarketEndTime > cn.getTimeHrMnSecs():
#               print ("afterMarketEndTime " + str(afterMarketEndTime))
#               print ("cn.getTimeHrMnSecs() " + str(cn.getTimeHrMnSecs()))
#               sleep(10)
#            
#            logPath = clOptions.profileTradeDataPath.replace("profiles", "logs")
#            
#            # Instantiate the needed objects
#            l = lpl.Log(0, 0, logPath, "/tmp/oo", 0)
#            pr = lpl.Premarket(minuteChartPath, minuteChartExt, dailyChartPath, dailyChartExt, dailyGapExt, bestAlgosPath, bestAlgosExt)
#            tg = lpl.Target(c, d, l)
#            dc = lpl.Dailychart()
#            
#            algoData, stocks = analyzeStocks(pr, tg, dc, "post", useLiveDailyData, stocks, onlyUpdateDailyStocks, 0, "")
#            exit (0)
         
      if exitTrading:
         exit(0)
         

#      # Halt program at end of trading day
#      if cn.getTimeHrMnSecs() > lastMinuteOfLiveTrading and not a1.getAfterMarket():
#         if not offLine:
#            for stock in stocks:
#               if a[stock].inPosition():
#                  a[stock].closePosition(barCtr, stocksChart[stock], bid[stock], ask[stock], forceClose)
#
#               # Write last bar
#               ba[stock].write(stocksChart[stock], pathsChart[stock]['barChartPath'], barCtr)
#               # ba[stock].fixSessionHiLo(pathsChart[stock]['barChartPath'])
#         
#            lg1.info("Program exiting due to end of day trading")
#
#         exit (3)
      # end minute loop
   # end continuous loop
# end execution loop

