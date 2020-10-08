## Test all lplTrade profile combinations. Output best combinations
## Create one profile file, changing values defined above. 
## Execute lpltTrade with a the same profile file with varying values.
## Save the profile values the high, low, last prices and the dates they happened
## iterate over all values to find the most favorable WOW

import json
import os
import time
import simplejson
import lplTrade as lpl
from optparse import OptionParser
from pathlib import Path
import subprocess
import sys

# Definitions

openBuyBars = [1,2,3,4,5]     # OB
openSellBars = [3,4,5]    # OS
closeBuyBars = [3,4,5]    # CB
closeSellBars = [3,4,5]   # CS
timeBar = [1,2,3,4,5]       # TB
aggressiveOpen = [0,1]      # AO
aggressiveClose = [0,1]     # AC
doHiLo = [1]           # HL
doHiLoSeq = [1]           # HLS
doExecuteOnOpen = [0,1]     # EO
doTrends = [1]            # TR
doQuickProfit = [1]       # QP
doRangeTradeBars = [2,3,4,5]    # IR
doOpensCloses = [0,1]       # OC
doExecuteOnClose = [0,1]    # EC
doHiLoOnClose = [0,1]       # HLC
doHiLoOnOpen = [0,1]        # HL
doReversalPattern = [0,1]   # RP
doQuickReversal = [0,1]     # QR
doReverseBuySell = [1]    # reverse position RP
doDynamic = [0,1]           # DY
doOnlySells = [0,1]         # OS
doOnlyBuys = [0,1]          # OB
useAvgBarLimits = [1]     # ABL
doTrendsdoPatterndoRT = [1]
usePricesFromFile = 1
write1_5MinData = 1
resume = 1
tradingDelayBars = range(2,20) # DB
quickProfitMax = [0,1]         # QP
waitForNextBar = [0,1]         # WN
profitPctTrigger = [0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002]
quitMaxProfit = [0,1]          # QP
bearTrendValue = [1.5,1.6,1.7,1.8,1.9]
bullTrendValue = [3.5,3.4,3.3,3.2,3.1]
shortTrendBars = [6,8,10,12]
midTrendBars = [12,16,20,24]
longTrendBars = [18,24,30,36]
megaTrendBars = [24,32,40,48]
   
originalProfile = {}

parseInfo = ""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getLastLine(path):

   lastLine = ""
   with open(path) as f:
      for line in f:
         pass
      lastLine = line
   return lastLine
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getGain(line):

   lineTokens = line.split()
   
   gain = lineTokens[3]

   return float(gain)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseLastLine(line, info):

   parsedLine = ""
   lineTokens = line.split()

   if len(lineTokens) < 2:
      print ("Last line " + str(line))
      return ""
   
   lastClose = lineTokens[1]
   gain = lineTokens[3]
   pct = lineTokens[4]
   
   parsedLine = lastClose + " " + gain + " " + pct + info

   return parsedLine
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def writeParsedLine(path, line):

   line += parseInfo
   with open(path, "a") as f:
      f.write(line + "\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def writeParsedHeader(path, line):

   with open(path, "a") as f:
      f.write(line)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getHeader(stock):

   bars = "BARS: Open/Close: DB Trend: TS TM TL TM TS Range: RT"
   
   algos = "ALGOs: HiLoSeq: HL ExOnOpen: EO Trends: TR Range: IR Quick Rev: Quick Profit: QP QR,RP,DY,OS,OB,ABL"
   
   #header = stock + " " + bars + "\n" + algos + "\n"
   header = stock + "\n"
   
   return header
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getParseInfo():

   return parseInfo
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setBuySellValues(value, info):

   d["profileTradeData"]["openBuyBars"] = str(value)
   d["profileTradeData"]["openSellBars"] = str(value)
   d["profileTradeData"]["closeBuyBars"] = str(value)
   d["profileTradeData"]["closeSellBars"] = str(value)
   
   info += "DB " + str(value) + " "
   
   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setAlgoValues(algo, value, info):

   if algo == "timeBar":
      d["profileTradeData"]["timeBar"] = str(value)
      info += " TB " + str(value) + " "

   if algo == "doHiLo":
      d["profileTradeData"]["doHiLo"] = str(value)
      info += "HL " + str(value) + " "
   #else:
   #   d["profileTradeData"]["doHiLo"] = str(0)

   if algo == "doHiLoSeq":
      d["profileTradeData"]["doHiLoSeq"] = str(value)
      info += "HLS " + str(value) + " "
   else:
      d["profileTradeData"]["doHiLoSeq"] = str(0)

   if algo == "doTrends":
      d["profileTradeData"]["doTrends"] = str(value)
      info += "TR " + str(value) + " "
   else:
      d["profileTradeData"]["doTrends"] = str(0)

   if algo == "doQuickProfit":
      d["profileTradeData"]["doQuickProfit"] = str(value)
      info += "QP " + str(value) + " "
   else:
      d["profileTradeData"]["doQuickProfit"] = str(0)
     
   if algo == "doReverseBuySell":
      d["profileTradeData"]["doReverseBuySell"] = str(value)
      info += "RBS " + str(value) + " "
   else:
      d["profileTradeData"]["doReverseBuySell"] = str(0)

   if algo == "doRangeTradeBars":
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "IR " + str(value) + " "
   else:
      d["profileTradeData"]["doRangeTradeBars"] = str(0)

   if algo == "useAvgBarLimits":
      d["profileTradeData"]["useAvgBarLimits"] = str(value)
      info += "ABL " + str(value) + " "
   else:
      d["profileTradeData"]["useAvgBarLimits"] = str(0)

   if algo == "doTrendsdoABLdoRT":
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["useAvgBarLimits"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "TR 1 ABL 1 IR " + str(value) + " "

   if algo == "doTrendsdoPatterndoRT":
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPatterns"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "TR 1 PT 1 IR " + str(value) + " "

   if algo == "doPatterndoRT":
      d["profileTradeData"]["doPatterns"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "PT 1 IR " + str(value) + " "

   if algo == "doTR_RBS_ABL_RT":
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["useAvgBarLimits"] = str(1)
      d["profileTradeData"]["doReverseBuySell"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "TR 1 RBS 1 ABL 1 IR " + str(value) + " "

   if algo == "doTrendsdoQPdoRT":
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "TR 1 QP 1 IR " + str(value) + " "

   if algo == "doTrendsdoRT":
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "TR 1 IR " + str(value) + " "

   if algo == "doTrendsOnly":
      d["profileTradeData"]["doTrends"] = str(1)
      info += "TR " + str(value) + " "

   if algo == "doTrendsdoQP":
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      info += "TR 1 QP " + str(value) + " "

   if algo == "doTrendsdoABL":
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["useAvgBarLimits"] = str(1)
      info += "TR 1 ABL " + str(value) + " "

   if algo == "doOnlyTrends":
      d["profileTradeData"]["doOnlyTrends"] = str(1)
      info += "DOTR " + str(value) + " "

   if algo == "doAgrOpenClose":
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "AC 1 TR 1 IR: " + str(value) + " "

   return info

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getProfileValues():

   readinfo = ""
   
   for algo, value in d['profileTradeData'].items():

      if algo == "timeBar":
         if value > str(0):
            readinfo += " TB " + str(value) + " "
   
      if algo == "doHiLo":
         if value > str(0):
            readinfo += "HL " + str(value) + " "
         
      if algo == "doHiLoSeq":
         if value > str(0):
            readinfo += "HLS " + str(value) + " "
         
      if algo == "doTrends":
         if value > str(0):
            readinfo += "TR " + str(value) + " "
   
      if algo == "doQuickProfit":
         if value > str(0):
            readinfo += "QP " + str(value) + " "
        
      if algo == "doReverseBuySell":
         if value > str(0):
            readinfo += "RBS " + str(value) + " "
   
      if algo == "doRangeTradeBars":
         if value > str(0):
            readinfo += "IR " + str(value) + " "
            
      if algo == "useAvgBarLimits":
         if value > str(0):
            readinfo += "ABL " + str(value) + " "

      if algo == "openBuyBars":
         if value > str(0):
            readinfo += "DB " + str(value) + " "

   return readinfo

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def initParseInfo():

   return " "

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def removeFiles(fresh):

   # Remove data files
   if fresh:
      for stock in symbols:
         parsePath = "logs/parse" + stock + ".log"
         lgFile = "logs/output" + stock + ".tt"
         resultsPath = "logs/active" + stock + ".log"
         if os.path.exists(parsePath):
            os.remove(parsePath)
         if os.path.exists(lgFile):
            os.remove(lgFile)
         if os.path.exists(resultsPath):
            os.remove(resultsPath)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def readProfile(path):

   with open(path) as jsonData:
      d = json.load(jsonData)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def writeOriginalProfile(path, data):

   with open(path, 'w') as fp:
       json.dump(data, fp, indent=2)
       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def writeLog(src, dst):

   return os.system("cp "+ src + " " + dst)

# Create dict of all default 

wp = cdp = tdp = stocks = lplt = ""
fresh = False

#lplt = "bin/lplt.py"
lplt = "/Users/tknitter/w/gitWS/lplTrade/bin/lplt.py"
prog = "/Users/tknitter/w/gitWS/lplW/bin/python3 " + lplt + " "

parser = OptionParser()

parser.add_option("-p"  , "--tdp", dest="tdp",
   help="profile template", metavar="FILE")

parser.add_option("-c"  , "--cdp", dest="cdp",
   help="e.g. etrade profile", metavar="FILE")

parser.add_option("-w", "--wp", type="string",
   action="store", dest="wp", default=None,
   help="work directory. default lplTrade...")

parser.add_option("-s", "--stocks", type="string",
   action="store", dest="stocks", default=None,
   help="stock to bua/selly: AAPL")
   
parser.add_option("-a", "--algo", type="string",
   action="store", dest="algo", default=None,
   help="algorithm")
   
parser.add_option("-f", "--fresh",
   action="store_true", dest="fresh", help="fresh")

parser.add_option("-x", "--exitMaxProfit",
   action="store_true", dest="exitMaxProfit", help="exitMaxProfit")

(clOptions, args) = parser.parse_args()

algo = ""
wp = clOptions.wp
cdp = clOptions.cdp
tdp = clOptions.tdp
stocks = clOptions.stocks
fresh = clOptions.fresh
algo = clOptions.algo
exitMaxProfit = clOptions.exitMaxProfit

testAlgos = {}
if algo:
   if algo == "doTrendsdoRT":
      testAlgos['doTrendsdoRT'] = doRangeTradeBars
   elif algo == "doPatterndoRT":
      testAlgos['doPatterndoRT'] = doRangeTradeBars
   elif algo == "doTrendsdoPatterndoRT":
      testAlgos['doTrendsdoPatterndoRT'] = doRangeTradeBars
   elif algo == "doTrendsdoABLdoRT":
      testAlgos['doTrendsdoABLdoRT'] = doRangeTradeBars
   elif algo == "doTR_RBS_ABL_RT":
      testAlgos['doTR_RBS_ABL_RT'] = doRangeTradeBars
   elif algo == "doTrendsdoQPdoRT":
      testAlgos['doTrendsdoQPdoRT'] = doRangeTradeBars
   elif algo == "doReverseBuySell":
      testAlgos['doReverseBuySell'] = [1]
   elif algo == "doTrendsOnly":
      testAlgos['doTrendsOnly'] = [1]
   elif algo == "doTrendsdoQP":
      testAlgos['doTrendsdoQP'] = [1]      
   elif algo == "doTrendsdoABL":
      testAlgos['doTrendsdoABL'] = [1]   
   elif algo == "doOnlyTrends":
      testAlgos['doOnlyTrends'] = [1]   
   elif algo == "doAgrOpenClose":
      testAlgos['doAgrOpenClose'] = [1]
   elif algo == "doRangeTradeBars":
      testAlgos['doRangeTradeBars'] = doRangeTradeBars
      
else: # Default
   #testAlgos['doHiLoSeq'] = doHiLoSeq # Set as default in orig profile
   testAlgos['doHiLo'] = doHiLo # Set as default in orig profile
   testAlgos['doTrends'] = doTrends
   testAlgos['doRangeTradeBars'] = doRangeTradeBars
   testAlgos['useAvgBarLimits'] = useAvgBarLimits
   testAlgos['doTrendsdoPatterndoRT'] = doTrendsdoPatterndoRT

#testAlgos['doQuickProfit'] = doQuickProfit
#testAlgos['doReverseBuySell'] = doReverseBuySell FIXXX

if not wp:
   print ("options are invalid. Need -w workPath -p profilePath ")
   exit(1)

if os.chdir(wp):
   exit(1)

if not os.path.exists(lplt):
   print ("Trading program doesn't exist!! " + lplt)
   exit(1)

if not cdp or not tdp:
   print ("options are invalid. Need -w workPath -p profilePath ")
   exit(1)

# Get trading elements
with open(tdp) as jsonData:
   originalProfile = json.load(jsonData)

with open(tdp) as jsonData:
   d = json.load(jsonData)

if not stocks:
   stocks = str(d["profileTradeData"]["stocks"])

# Execute shell sript to populate site path with latest code
home = str(Path.home())

shellCmd = home + "/bin/lplt.sh"

os.system(shellCmd)

symbols = stocks.split(",")

removeFiles(fresh)

for stock in symbols:
   parsePath = "logs/parse" + stock + ".log"
   #writeParsedLine(parsePath, getHeader(stock))

dirty = 0
infoTime = ""
highestGain = 0.0

for minBar in timeBar:

   #info = initParseInfo()

   for algo, values in testAlgos.items():

      readProfile(tdp)
      
      for value in values:      
         for bars in openBuyBars:
            info = initParseInfo()
            info = setAlgoValues("timeBar", minBar, info)
            #info = setAlgoValues("doHiLo", 1, info)
            info = setAlgoValues(algo, value, info)
            info = setBuySellValues(bars, info)
            
            # Dump new settings
            with open(tdp, 'w') as fp:
                json.dump(d, fp, indent=2)
         
            for stock in symbols:
               bcPath = "bc/active" + stock + ".bc"
               resultsPath = "logs/active" + stock + ".log"
               parsePath = "logs/parse" + stock + ".pr"
               lgFile = "logs/output" + stock + ".tt"
                              
               if not os.path.exists(bcPath):
                  print ("Can't find file: " + str(bcPath) + " skipping it...\n")
                  continue
               
               args = " -d -o "
               if exitMaxProfit:
                  args += " -x " 

               cmd = prog + args + " -c " + cdp + " -s " + stock + " -p " + tdp + " > " + lgFile
               
               exitVal = os.system(cmd)
               
               lastLine = getLastLine(resultsPath) 
               parsedLine = parseLastLine(lastLine, info)
               
               if parsedLine == "":
                  print (str(stock) + " produced no results" + str(parsedLine))
                  continue
                  
               gain = getGain(lastLine)
               if gain > highestGain:
                  lastGain = highestGain
                  highestGain = gain
                  parsedLine += str(highestGain)
               
               if exitVal == 512:
                  parsedLine += " MP"
                  
                  svPath = "profiles/saved/active" + stock + "_hiGain_" + str(highestGain) + ".sv"
                  rsPath = "profiles/saved/results" + stock + "_hiGain_" + str(highestGain) + ".rs"
                  pfPath = "profiles/saved/profiles" + stock + "_hiGain_" + str(highestGain) + ".pr"
                  writeLog(lgFile, svPath)
                  writeLog(resultsPath, rsPath)
                  writeLog(tdp, pfPath)
                  #removeLog(tdp, pfPath)

               print (str(stock) + " " + str(parsedLine))
            
               # ... and save it's peices to be later examined
               writeParsedLine(parsePath, stock + " " + parsedLine)
               
            dirty += 1            
            
   writeOriginalProfile(tdp, originalProfile) 

exit(0)    



