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

openCloseBuySellBars = [1,2,3,4,5]     # OB OS CB CS

openBuySellBars = [1,2,3,4,5]     # OB OS
closeBuySellBars = [1,2,3,4,5]     # CB CS

openBuyBars = [1,2,3,4,5]     # OB
openSellBars = [1,2,3,4,5]    # OS
closeBuyBars = [1,2,3,4,5]    # CB
closeSellBars = [1,2,3,4,5]   # CS
timeBar = [1,2,3,4,5]       # TB

usePricesFromFile = 1
resume = 1

tradingDelayBars = range(2,20) # DB

quickProfitMax = [0,1]         # QP
waitForNextBar = [0,1]         # WN
profitPctTrigger = [0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002]
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
   
   parsedLine = lastClose + " " + gain + " " + pct + " " + info

   return parsedLine
   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def writeParsedLine(path, line):

#   if os.path.exists(path):
#      os.remove(path)
   
   line += parseInfo
   with open(path, "a") as f:
      f.write(line + "\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def writeParsedLineRemoveDups(path, date, newLine):
   
   tmpPath = "/tmp/fileBuffer"
   
   lines = []
   found = 0
   
   if not os.path.exists(path):
      newLine += parseInfo
      with open(path, "a") as f:
         f.write(newLine + "\n")
      return

   with open(path) as f:
      lines = [line.rstrip() for line in f]
   
   with open(tmpPath, "w") as o:
      for line in lines:
         if date in line:
            if not found:
               o.write(newLine + "\n")
            found += 1
         else:
            o.write(line + "\n")
   
   os.rename(tmpPath, path)

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
def setOpenBuyValue(value, info):

   d["profileTradeData"]["openBuyBars"] = str(value)
   
   info += "OB" + str(value) + " "
   
   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setOpenSellValue(value, info):

   d["profileTradeData"]["openSellBars"] = str(value)
   
   info += "OS" + str(value) + " "
   
   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setCloseBuyValue(value, info):

   d["profileTradeData"]["closeBuyBars"] = str(value)
   
   info += "CB" + str(value) + " "
   
   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setCloseSellValue(value, info):

   d["profileTradeData"]["closeSellBars"] = str(value)
   
   info += "CS" + str(value) + " "
   
   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setCloseBuySellValues(value, info):

   d["profileTradeData"]["closeBuyBars"] = str(value)
   d["profileTradeData"]["closeSellBars"] = str(value)
   
   info += "CB" + str(value) + "_CS" + str(value)

   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setOpenBuySellValues(value, info):

   d["profileTradeData"]["openBuyBars"] = str(value)
   d["profileTradeData"]["openSellBars"] = str(value)
      
   info += "OB" + str(value) + "_OS" + str(value) + "_"
   
   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setOpenCloseBuySellValues(value, info):

   d["profileTradeData"]["openBuyBars"] = str(value)
   d["profileTradeData"]["openSellBars"] = str(value)
   d["profileTradeData"]["closeBuyBars"] = str(value)
   d["profileTradeData"]["closeSellBars"] = str(value)
      
   info += "OB" + str(value) + " OS" + str(value) + " "
   info += "CB" + str(value) + " CS" + str(value) + " "
   
   return info 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setAlgoValues(algo, value, info):

   info = ""
   
   d["profileTradeData"]["timeBar"] = str(value)
   info += "TB" + str(value) + "_"
      
   # Turn off all algo's 
   d["profileTradeData"]["doHiLoSeq"] = str(0)
   d["profileTradeData"]["doHiLo"] = str(0)
   d["profileTradeData"]["doTrends"] = str(0)
   d["profileTradeData"]["doQuickProfit"] = str(0)
   d["profileTradeData"]["doReverseBuySell"] = str(0)
   d["profileTradeData"]["doRangeTradeBars"] = str(0)
   d["profileTradeData"]["useAvgBarLimits"] = str(0)
   d["profileTradeData"]["doPatterns"] = str(0)
   d["profileTradeData"]["doAverageVolume"] = str(0)
   d["profileTradeData"]["doVolumeLastBar"] = str(0)
   d["profileTradeData"]["aggressiveClose"] = str(0)
   d["profileTradeData"]["aggressiveOpen"] = str(0)
   d["profileTradeData"]["doPatterns"] = str(0)
   d["profileTradeData"]["doHammers"] = str(0)
   d["profileTradeData"]["doReversals"] = str(0)
   d["profileTradeData"]["doPriceMovement"] = str(0)
   d["profileTradeData"]["doExecuteOnOpen"] = str(0)
   d["profileTradeData"]["doExecuteOnClose"] = str(0)
   d["profileTradeData"]["doTrailingStop"] = str(0)
   d["profileTradeData"]["doOnlySells"] = str(0)
   d["profileTradeData"]["doOnlyBuys"] = str(0)
   d["profileTradeData"]["quitMaxProfit"] = str(0)
   d["profileTradeData"]["doSessions"] = str(0)
   d["profileTradeData"]["waitForNextBar"] = str(0)
   
   # algo from the CL can be any combination of algorithms
   # HS AO AC AV AL AB TR QP HL TR PT RV HM RP IT BO SO "

   if "HL" in algo:
      d["profileTradeData"]["doHiLo"] = str(1)
      info += "HL_"
      
   if "HS" in algo:
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      info += "HS_"

   if "TR" in algo:
      d["profileTradeData"]["doTrends"] = str(1)
      info += "TR_"

   if "AV" in algo:
      d["profileTradeData"]["doAverageVolume"] = str(1)
      info += "AV_"

   if "AL" in algo:
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      info += "AL_"

   if "TS" in algo:
      d["profileTradeData"]["doTrailingStop"] = str(1)
      info += "TS_"

   if "SS" in algo:
      d["profileTradeData"]["doSessions"] = str(1)
      info += "SS_"

   if "BO" in algo:
      d["profileTradeData"]["doOnlyBuys"] = str(1)
      info += "BO_"

   if "SO" in algo:
      d["profileTradeData"]["doOnlySells"] = str(1)
      info += "SO_"

   if "QP" in algo:
      d["profileTradeData"]["doQuickProfit"] = str(1)
      info += "QP_"

   if "RP" in algo:
      d["profileTradeData"]["doReverseBuySell"] = str(1)
      info += "RV_"

   if "AB" in algo:
      d["profileTradeData"]["useAvgBarLimits"] = str(1)
      info += "AB_"

   if "PT" in algo:
      d["profileTradeData"]["doPatterns"] = str(1)
      info += "PT_"

   if "HM" in algo:
      d["profileTradeData"]["doHammers"] = str(1)
      info += "HM_"

   if "RV" in algo:
      d["profileTradeData"]["doReversals"] = str(1)
      info += "RV_"

   if "AC" in algo:
      d["profileTradeData"]["aggressiveClose"] = str(1)
      info += "AC_"

   if "AO" in algo:
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      info += "AO_"

   if "PM" in algo:
      d["profileTradeData"]["doPriceMovement"] = str(1)
      info += "PM_"

   if "EO" in algo:
      d["profileTradeData"]["doExecuteOnOpen"] = str(1)
      info += "EO_"

   if "EC" in algo:
      d["profileTradeData"]["doExecuteOnClose"] = str(1)
      info += "EC_"

   if "QM" in algo:
      d["profileTradeData"]["quitMaxProfit"] = str(1)
      info += "QM_"
      
   if "WT" in algo:
      d["profileTradeData"]["waitForNextBar"] = str(1)
      info += "WT_"

   return info

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
         outFile = "/tmp/output.tt"
         
         if os.path.exists(parsePath):
            os.remove(parsePath)
         if os.path.exists(lgFile):
            os.remove(lgFile)
         if os.path.exists(resultsPath):
            os.remove(resultsPath)
         if os.path.exists(outFile):
            os.remove(outFile)

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

#~~~~~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
wp = cdp = tdp = stocks = lplt = ""

fresh = False

#lplt = "bin/lplt.py"
lplt = "/Users/tknitter/w/gitWS/lplTrade/bin/lplt.py"
prog = "/Users/tknitter/w/gitWS/lplW/bin/python3 " + lplt + " "

cwd = os.getcwd()

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

infoTime = ""
highestGain = 0.0

#timeBar = [5]

for minBar in timeBar:

   readProfile(tdp)
   info = initParseInfo()
      
   for openBars in openCloseBuySellBars:
      for closeBars in closeBuySellBars:
#         for obb in openBuyBars:
#            for osb in openSellBars:
#               for cbb in closeBuyBars:
#                  for csb in closeSellBars:               
      
                     info = setAlgoValues(algo, minBar, info)
                  
                     # Both decision bars change
                     
#                     info = setOpenCloseBuySellValues(openBars, info)

                     info = setOpenBuySellValues(openBars, info)
                     info = setCloseBuySellValues(closeBars, info)
      
#                     # Each decision bar changes 
#                     info = setOpenBuyValue(obb, info)
#                     info = setOpenSellValue(osb, info)
#                     info = setCloseBuyValue(cbb, info)
#                     info = setCloseSellValue(csb, info)
      
                     # Dump new settings
                     with open(tdp, 'w') as fp:
                         json.dump(d, fp, indent=2)
                  
                     for stock in symbols:
                        bcPath = "bc/active" + stock + ".bc"
                        resultsPath = "logs/active" + stock + ".log"
                        parsePath = "logs/parse" + stock + ".pr"
                        #lgFile = "logs/output" + stock + ".tt"
                        outFile = "/tmp/output.tt"
                                       
                        if not os.path.exists(bcPath):
                           print ("Can't find file: " + str(bcPath) + " skipping it...\n")
                           continue
                        
                        args = " -d -o "
                        if exitMaxProfit:
                           args += " -x " 
               
                        # Create files based off of the stock, algo and date
                        cmd = prog + args + " -c " + cdp + " -s " + stock + " -p " + tdp + " > " + outFile
                        
                        date = os.path.basename(wp)
                        
                        algoPath = cwd + "/exitResults/" + stock + "_" + info + ".ex"
                        
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
                           parsedLine += " " + str(highestGain)
                        
                        if exitVal == 512:
                           parsedLine += " MP"
                           
                           rsPath = "profiles/saved/results" + stock + "_hiGain_" + str(highestGain) + ".rs"
                           pfPath = "profiles/saved/profiles" + stock + "_hiGain_" + str(highestGain) + ".pr"
                           writeLog(resultsPath, rsPath)
                           writeLog(tdp, pfPath)
                                          
                        print (str(stock) + " " + str(parsedLine))
                     
                        # ... and save it's peices to be later examined
                        writeParsedLine(parsePath, stock + " " + parsedLine)
                        #writeParsedLine(algoPath, date + " " + stock + " " + parsedLine)
                        writeParsedLineRemoveDups(algoPath, date, date + " " + stock + " " + parsedLine)
                                    
   writeOriginalProfile(tdp, originalProfile) 

exit(0)    



