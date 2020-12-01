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
doHiLoSeq = [1]           # Hi Lo Sequence
doEOO = [1]     # Execute on open
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
doTRdoPTdoRT = [2,3,4,5]
doTRdoPTdoRTdoAV = [2,3,4,5]
doTRdoPTdoRTdoVL = [2,3,4,5]
doTRdoPTdoRTdoAVdoVL = [2,3,4,5]
doTRdoPTdoRTdoAVdoVLdoQP = [2,3,4,5]
doAVdoVLdoQPdoTRdoRT = [2,3,4,5]
doAVdoVLdoQPdoTRdoAOdoACdoRT = [2,3,4,5]
doAVdoVLdoQPdoTRdoAOdoAC = [1]
doAverageVolume = [1]
doVolumeLastBar = [1]
doVolumeLastBardoTR = [1]
doVLdoQP = [1]
doAVdoVL = [1]
doPM = [1]
doAVdoVLdoQP = [1]
doHiLoSeqdoHiLoDoAV = [1]
doHiLoSeqdoHiLoDoAVdoAOdoAC = [1]
doHiLoSeqdoHiLoDoAVdoAOdoACdoIT = [1]
doHiLoSeqdoHiLo = [1]
doHiLodoIT = [1]
doHiLodoAVdoIT = [1]
doHiLodoITdoQP = [1]
doHiLodoITdoQPdoAL = [1]
doHiLodoITdoQPdoHM = [1]
doHammer = [1]
doHMdoITdoQP = [1]
doHiLodoAVdoTR = [1]
doHiLoSeqdoHiLoDoAL = [1]
doHiLoSeqdoHiLoDoALDoAV = [1]
doAVdoTR = [1]
doAVdoTRdoAL = [1]
doAVdoTRdoPT = [1]
doQPdoAV = [1]
doAVdoVLdoPM = [1]
doAVdoVLdoACdoAO = [1]
doAVdoVLdoACdoAOdoQP = [1]
doAVdoVLdoACdoAOdoPT = [1]
doAVdoTRdoACdoAO = [1]
doAVdoTRdoACdoAOdoPT = [1]
doAVdoVLdoQPdoTR = [1]
doAVdoVLdoQPdoTRdoPT = [1]
doAVdoTRdoACdoAOdoPTdoQP = [1]
doAVdoVLdoAOdoACdoTR = [1]
doHiLoSeqdoAVdoVLdoAOdoACdoTR = [1]
doAVdoAOdoACdoTR = [1]
doAVdoAOdoACdoTRdoIR = [2,3,4,5]
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
   d["profileTradeData"]["doPriceMovement"] = str(0)
   d["profileTradeData"]["doExecuteOnOpen"] = str(0)
   d["profileTradeData"]["doInPosTracking"] = str(0)
   
#   if algo == "HL":
#      d["profileTradeData"]["doHiLo"] = str(1)
#      info += "HL "
#
#   if algo == "HS":
#      d["profileTradeData"]["doHiLoSeq"] = str(1)
#      info += "HS "
#
#   if algo == "TR":
#      d["profileTradeData"]["doTrends"] = str(1)
#      info += "TR "
#
#   if algo == "QP":
#      d["profileTradeData"]["doQuickProfit"] = str(1)
#      info += "QP "
#
#   if algo == "RV":
#      d["profileTradeData"]["doReverseBuySell"] = str(1)
#      info += "RV "
#
#   if algo == "AV":
#      d["profileTradeData"]["useAvgBarLimits"] = str(1)
#      info += "AV "
#
#   if algo == "AL":
#      d["profileTradeData"]["useAvgBarLimits"] = str(1)
#      info += "AL "
#
#   if algo == "PT":
#      d["profileTradeData"]["doPatterns"] = str(1)
#      info += "PT "
#
#   if algo == "AC":
#      d["profileTradeData"]["aggressiveClose"] = str(1)
#      info += "AC "
#
#   if algo == "AO":
#      d["profileTradeData"]["aggressiveOpen"] = str(1)
#      info += "AO "
#
#   if algo == "PM":
#      d["profileTradeData"]["doPriceMovement"] = str(1)
#      info += "PM "
#
#   if algo == "EO":
#      d["profileTradeData"]["doExecuteOnOpen"] = str(1)
#      info += "EO "
#
#   if algo == "RT":
#      d["profileTradeData"]["doRangeTradeBars"] = str(1)
#      info += "RT " + str(value) + " "
#
   # Turn on specifc algo
   if algo == "doHiLo":
      d["profileTradeData"]["doHiLo"] = str(1)
      info += "HL "

   if algo == "doHammer":
      d["profileTradeData"]["doPatterns"] = str(1)
      info += "HM "

   if algo == "doHMdoITdoQP":
      d["profileTradeData"]["doPatterns"] = str(1)
      d["profileTradeData"]["doInPosTracking"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      info += "HM IT VL "

   if algo == "doHiLodoITdoQP":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doInPosTracking"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      info += "HL IT QP "
      
   if algo == "doHiLodoITdoQPdoHM":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doInPosTracking"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      d["profileTradeData"]["doPatterns"] = str(1)
      info += "HL IT QP HM "

   if algo == "doHiLodoITdoQPdoAL":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doInPosTracking"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      info += "HL IT QP AL "

   if algo == "doHiLodoIT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doInPosTracking"] = str(1)
      info += "HL IT "

   if algo == "doHiLodoAVdoIT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doInPosTracking"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      info += "HL AV IT "

   if algo == "doHiLoSeq":
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      info += "HLS "
      
   if algo == "doHiLoSeqdoHiLo":
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      d["profileTradeData"]["doHiLo"] = str(1)
      info += "HLS HL "
      
   if algo == "doHiLoSeqdoHiLoDoAV":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      info += "HLS HL AV "
      
   if algo == "doHiLodoAVdoTR":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      info += "HL AV TR "
      
   if algo == "doHiLoSeqdoHiLoDoAVdoAOdoAC":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      info += "HLS HL AV AO AC "
      
   if algo == "doHiLoSeqdoHiLoDoAVdoAOdoACdoIT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["doInPosTracking"] = str(1)
      info += "HLS HL AV AO AC IT "


   if algo == "doHiLoSeqdoHiLoDoAL":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      info += "HLS HL AL "
      
   if algo == "doHiLoSeqdoHiLoDoALDoAV":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      info += "HLS HL AL AV "
            
   if algo == "doEOO":
      d["profileTradeData"]["doExecuteOnOpen"] = str(1)
      info += "EO "

   if algo == "doTrends":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      info += "HL TR "

   if algo == "doAverageVolume":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      info += "HL AV "
      
   if algo == "doVolumeLastBar":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      info += "HL AL "

   if algo == "doVLdoQP":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      info += "HL AL QP "

   if algo == "doVolumeLastBardoTR":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      info += "HL TR "

   if algo == "doPM":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doPriceMovement"] = str(value)
      info += "HL AL "

   if algo == "doAVdoVL":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      info += "HL AV AL "
      
   if algo == "doAVdoVLdoPM":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doPriceMovement"] = str(value)
      info += "HL AV AL PM "
      
   if algo == "doAVdoVLdoQPdoTR":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      info += "HL AV AL QP TR " 
            
   if algo == "doAVdoVLdoQPdoTRdoRT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      d["profileTradeData"]["doPatterns"] = str(value)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL AV AL QP TR PT IR " + str(value) + " "
      
   if algo == "doAVdoVLdoQPdoTRdoAOdoACdoRT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      d["profileTradeData"]["doPatterns"] = str(value)
      d["profileTradeData"]["aggressiveClose"] = str(value)
      d["profileTradeData"]["aggressiveOpen"] = str(value)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL AV AL QP TR PT AO AC IR " + str(value) + " "
      
   if algo == "doAVdoVLdoQPdoTRdoAOdoAC":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      d["profileTradeData"]["doPatterns"] = str(value)
      d["profileTradeData"]["aggressiveClose"] = str(value)
      d["profileTradeData"]["aggressiveOpen"] = str(value)
      info += "HL AV AL QP TR PT AO AC "
      
   if algo == "doAVdoVLdoQP":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      info += "HL AV AL QP "
      
   if algo == "doAVdoVLdoQPdoTRdoPT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      d["profileTradeData"]["doPatterns"] = str(value)
      info += "HL AV AL QP TR PT "
      
   if algo == "doAVdoTR":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      info += "HL AV TR "

   if algo == "doAVdoTRdoPT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      d["profileTradeData"]["doPatterns"] = str(value)
      info += "HL AV TR PT "

   if algo == "doAVdoTRdoAL":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      d["profileTradeData"]["doVolumeLastBar"] = str(value)
      d["profileTradeData"]["doTrends"] = str(value)
      info += "HL AV AL TR "

   if algo == "doQPdoAV":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      d["profileTradeData"]["doAverageVolume"] = str(value)
      info += "HL QP AV "
              
   if algo == "doQuickProfit":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(value)
      info += "HL QP "
              
   if algo == "doReverseBuySell":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doReverseBuySell"] = str(value)
      info += "HL RBS "
      
   if algo == "doRangeTradeBars":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL IR " + str(value) + " "

   if algo == "useAvgBarLimits":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["useAvgBarLimits"] = str(value)
      info += "HL ABL "

   if algo == "doTRdoABLdoRT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["useAvgBarLimits"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL TR ABL IR " + str(value) + " "

   if algo == "doTRdoPTdoRT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPTs"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL TR PT IR " + str(value) + " "

   if algo == "doTRdoPTdoRTdoAV":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPTs"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL AV TR PT IR " + str(value) + " "

   if algo == "doTRdoPTdoRTdoVL":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPTs"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL AL TR PT IR " + str(value) + " "

   if algo == "doTRdoPTdoRTdoAVdoVL":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPTs"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL AV AL TR PT IR " + str(value) + " "

   if algo == "doTRdoPTdoRTdoAVdoVLdoQP":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPTs"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL AV AL TR PT QP IR " + str(value) + " "

   if algo == "doPTdoRT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doPTs"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL PT IR " + str(value) + " "

   if algo == "doTR_RBS_ABL_RT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["useAvgBarLimits"] = str(1)
      d["profileTradeData"]["doReverseBuySell"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL TR RBS ABL IR " + str(value) + " "

   if algo == "doTRdoQPdoRT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL TR QP IR " + str(value) + " "

   if algo == "doTRdoRT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL TR IR " + str(value) + " "

   if algo == "doTrendsOnly":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      info += "HL TRO "

   if algo == "doTRdoQP":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      info += "HL TR QP "

   if algo == "doTRdoABL":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["useAvgBarLimits"] = str(1)
      info += "HL TR ABL "

   if algo == "doOnlyTrends":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["doOnlyTrends"] = str(1)
      info += "HL DOTR "

   if algo == "doAVdoVLdoACdoAO":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      info += "HL AO AC AV AL "
      
   if algo == "doAVdoVLdoACdoAOdoPT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doPatterns"] = str(1)
      info += "HL AO AC AV AL PT "
      
   if algo == "doAVdoVLdoACdoAOdoQP":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      info += "HL AO AC AV AL QP "
      
   if algo == "doAVdoTRdoACdoAO":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      info += "HL AO AC AV TR "
      
   if algo == "doAVdoTRdoACdoAOdoPT":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPatterns"] = str(1)
      info += "HL AO AC AV TR PT "
      
   if algo == "doAVdoTRdoACdoAOdoPTdoQP":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doPatterns"] = str(1)
      d["profileTradeData"]["doQuickProfit"] = str(1)
      info += "HL AO AC AV TR PT QP "
      
   if algo == "doAVdoAOdoACdoTR":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      info += "HL AO AC AV TR "
      
   if algo == "doAVdoAOdoACdoTRdoIR":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "HL AO AC AV TR IR " + str(value) + " "
      
   if algo == "doAVdoVLdoAOdoACdoTR":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      info += "HL AO AC AV AL TR "
      
   if algo == "doHiLoSeqdoAVdoVLdoAOdoACdoTR":
      d["profileTradeData"]["doHiLoSeq"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doAverageVolume"] = str(1)
      d["profileTradeData"]["doVolumeLastBar"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doHiLo"] = str(0)
      info += "HLS AO AC AV AL TR "
      
   if algo == "doAgrOpenClose":
      d["profileTradeData"]["doHiLo"] = str(1)
      d["profileTradeData"]["aggressiveClose"] = str(1)
      d["profileTradeData"]["aggressiveOpen"] = str(1)
      d["profileTradeData"]["doTrends"] = str(1)
      d["profileTradeData"]["doRangeTradeBars"] = str(value)
      info += "AC TR IR: " + str(value) + " "

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
   if algo == "doTRdoRT":
      testAlgos['doTRdoRT'] = doRangeTradeBars
   elif algo == "doPTdoRT":
      testAlgos['doPTdoRT'] = doRangeTradeBars
   elif algo == "doTRdoPTdoRT":
      testAlgos['doTRdoPTdoRT'] = doTRdoPTdoRT
   elif algo == "doAVdoTRdoAL":
      testAlgos['doAVdoTRdoAL'] = doAVdoTRdoAL
   elif algo == "doAVdoVLdoQPdoTR":
      testAlgos['doAVdoVLdoQPdoTR'] = doAVdoVLdoQPdoTR
   elif algo == "doAVdoVLdoQPdoTRdoPT":
      testAlgos['doAVdoVLdoQPdoTRdoPT'] = doAVdoVLdoQPdoTRdoPT
   elif algo == "doAVdoTR":
      testAlgos['doAVdoTR'] = doAVdoTR
   elif algo == "doAVdoTRdoPT":
      testAlgos['doAVdoTRdoPT'] = doAVdoTRdoPT
   elif algo == "doAVdoVLdoQP":
      testAlgos['doAVdoVLdoQP'] = doAVdoVLdoQP
   elif algo == "doAVdoVLdoACdoAO":
      testAlgos['doAVdoVLdoACdoAO'] = doAVdoVLdoACdoAO
   elif algo == "doAVdoTRdoACdoAO":
      testAlgos['doAVdoTRdoACdoAO'] = doAVdoTRdoACdoAO
   elif algo == "doAVdoTRdoACdoAOdoPT":
      testAlgos['doAVdoTRdoACdoAOdoPT'] = doAVdoTRdoACdoAOdoPT
   elif algo == "doAVdoTRdoACdoAOdoPTdoQP":
      testAlgos['doAVdoTRdoACdoAOdoPTdoQP'] = doAVdoTRdoACdoAOdoPTdoQP
   elif algo == "doAVdoVLdoAOdoACdoTR":
      testAlgos['doAVdoVLdoAOdoACdoTR'] = doAVdoVLdoAOdoACdoTR
   elif algo == "doAVdoAOdoACdoTR":
      testAlgos['doAVdoAOdoACdoTR'] = doAVdoAOdoACdoTR
   elif algo == "doAVdoAOdoACdoTRdoIR":
      testAlgos['doAVdoAOdoACdoTRdoIR'] = doAVdoAOdoACdoTRdoIR
   elif algo == "doHiLoSeqdoAVdoVLdoAOdoACdoTR":
      testAlgos['doHiLoSeqdoAVdoVLdoAOdoACdoTR'] = doHiLoSeqdoAVdoVLdoAOdoACdoTR
   elif algo == "doAVdoVL":
      testAlgos['doAVdoVL'] = doAVdoVL
   elif algo == "doTRdoPTdoRTdoAV":
      testAlgos['doTRdoPTdoRTdoAV'] = doTRdoPTdoRTdoAV
   elif algo == "doTRdoPTdoRTdoVL":
      testAlgos['doTRdoPTdoRTdoVL'] = doTRdoPTdoRTdoVL
   elif algo == "doTRdoPTdoRTdoAVdoVL":
      testAlgos['doTRdoPTdoRTdoAVdoVL'] = doTRdoPTdoRTdoAVdoVL
   elif algo == "doAVdoVLdoQPdoTRdoRT":
      testAlgos['doAVdoVLdoQPdoTRdoRT'] = doAVdoVLdoQPdoTRdoRT
   elif algo == "doAVdoVLdoQPdoTRdoAOdoACdoRT":
      testAlgos['doAVdoVLdoQPdoTRdoAOdoACdoRT'] = doAVdoVLdoQPdoTRdoAOdoACdoRT
   elif algo == "doAVdoVLdoQPdoTRdoAOdoAC":
      testAlgos['doAVdoVLdoQPdoTRdoAOdoAC'] = doAVdoVLdoQPdoTRdoAOdoAC
      
   elif algo == "doTRdoPTdoRTdoAVdoVLdoQP":
      testAlgos['doTRdoPTdoRTdoAVdoVLdoQP'] = doTRdoPTdoRTdoAVdoVLdoQP
   elif algo == "doTRdoABLdoRT":
      testAlgos['doTRdoABLdoRT'] = doTRdoABLdoRT
   elif algo == "doTR_RBS_ABL_RT":
      testAlgos['doTR_RBS_ABL_RT'] = doRangeTradeBars
   elif algo == "doTRdoQPdoRT":
      testAlgos['doTRdoQPdoRT'] = doRangeTradeBars
   elif algo == "doReverseBuySell":
      testAlgos['doReverseBuySell'] = [1]
   elif algo == "doTrendsOnly":
      testAlgos['doTrendsOnly'] = [1]
   elif algo == "doTRdoQP":
      testAlgos['doTRdoQP'] = [1]      
   elif algo == "doTRdoABL":
      testAlgos['doTRdoABL'] = [1]   
   elif algo == "doOnlyTrends":
      testAlgos['doOnlyTrends'] = [1]   
   elif algo == "doAgrOpenClose":
      testAlgos['doAgrOpenClose'] = [1]
   elif algo == "doRangeTradeBars":
      testAlgos['doRangeTradeBars'] = doRangeTradeBars
   elif algo == "doVolumeLastBar":
      testAlgos['doVolumeLastBar'] = doVolumeLastBar
   elif algo == "doAverageVolume":
      testAlgos['doAverageVolume'] = doAverageVolume
   elif algo == "doAVdoVLdoQPdoTR":
      testAlgos['doAVdoVLdoQPdoTR'] = doAVdoVLdoQPdoTR
   elif algo == "doQuickProfit":
      testAlgos['doQuickProfit'] = doQuickProfit
   elif algo == "doAVdoVLdoQPdoTRdoPT":
      testAlgos['doAVdoVLdoQPdoTRdoPT'] = doAVdoVLdoQPdoTRdoPT
   elif algo == "doTrends":
      testAlgos['doTrends'] = doTrends
   elif algo == "doAVdoVLdoACdoAOdoQP":
      testAlgos['doAVdoVLdoACdoAOdoQP'] = doAVdoVLdoACdoAOdoQP
   elif algo == "doAVdoVLdoACdoAOdoPT":
      testAlgos['doAVdoVLdoACdoAOdoPT'] = doAVdoVLdoACdoAOdoPT
   elif algo == "doAVdoVLdoPM":
      testAlgos['doAVdoVLdoPM'] = doAVdoVLdoPM
   elif algo == "doPM":
      testAlgos['doPM'] = doPM
   elif algo == "doHiLo":
      testAlgos['doHiLo'] = doHiLo
   elif algo == "doHiLoSeq":
      testAlgos['doHiLoSeq'] = doHiLoSeq
   elif algo == "doEOO":
      testAlgos['doEOO'] = doEOO
   elif algo == "doVolumeLastBardoTR":
      testAlgos['doVolumeLastBardoTR'] = doVolumeLastBardoTR
   elif algo == "doVLdoQP":
      testAlgos['doVLdoQP'] = doVLdoQP
   elif algo == "doHiLoSeqdoHiLoDoAV":
      testAlgos['doHiLoSeqdoHiLoDoAV'] = doHiLoSeqdoHiLoDoAV
   elif algo == "doHiLoSeqdoHiLoDoAL":
      testAlgos['doHiLoSeqdoHiLoDoAL'] = doHiLoSeqdoHiLoDoAL
   elif algo == "doHiLoSeqdoHiLoDoALDoAV":
      testAlgos['doHiLoSeqdoHiLoDoALDoAV'] = doHiLoSeqdoHiLoDoALDoAV
   elif algo == "doHiLoSeqdoHiLoDoAVdoAOdoAC":
      testAlgos['doHiLoSeqdoHiLoDoAVdoAOdoAC'] = doHiLoSeqdoHiLoDoAVdoAOdoAC      
   elif algo == "doHiLoSeqdoHiLoDoAVdoAOdoACdoIT":
      testAlgos['doHiLoSeqdoHiLoDoAVdoAOdoACdoIT'] = doHiLoSeqdoHiLoDoAVdoAOdoACdoIT      
   elif algo == "doHiLodoAVdoTR":
      testAlgos['doHiLodoAVdoTR'] = doHiLodoAVdoTR
   elif algo == "doHiLodoIT":
      testAlgos['doHiLodoIT'] = doHiLodoIT
   elif algo == "doHiLodoAVdoIT":
      testAlgos['doHiLodoAVdoIT'] = doHiLodoAVdoIT
   elif algo == "doHiLoSeqdoHiLo":
      testAlgos['doHiLoSeqdoHiLo'] = doHiLoSeqdoHiLo
   elif algo == "doHiLodoITdoQP":
      testAlgos['doHiLodoITdoQP'] = doHiLodoITdoQP
   elif algo == "doHiLodoITdoQPdoAL":
      testAlgos['doHiLodoITdoQPdoAL'] = doHiLodoITdoQPdoAL
   elif algo == "doHammer":
      testAlgos['doHammer'] = doHammer
   elif algo == "doHMdoITdoQP":
      testAlgos['doHMdoITdoQP'] = doHMdoITdoQP
   elif algo == "doHiLodoITdoQPdoHM":
      testAlgos['doHiLodoITdoQPdoHM'] = doHiLodoITdoQPdoHM
            
      
else: # Default
   #testAlgos['doHiLoSeq'] = doHiLoSeq # Set as default in orig profile
   testAlgos['doHiLo'] = doHiLo # Set as default in orig profile
   testAlgos['doTrends'] = doTrends
   testAlgos['doAverageVolume'] = doAverageVolume
   testAlgos['doVolumeLastBar'] = doVolumeLastBar
   testAlgos['doVLdoQP'] = doVLdoQP
   testAlgos['doHiLoSeqdoHiLoDoAV'] = doHiLoSeqdoHiLoDoAV
   testAlgos['doHiLoSeqdoHiLoDoAVdoAOdoAC'] = doHiLoSeqdoHiLoDoAVdoAOdoAC
   testAlgos['doAVdoVL'] = doAVdoVL
   testAlgos['doAVdoVLdoPM'] = doAVdoVLdoPM
   testAlgos['doAVdoTR'] = doAVdoTR
   testAlgos['doAVdoVLdoQP'] = doAVdoVLdoQP
   testAlgos['doAVdoVLdoQPdoTR'] = doAVdoVLdoQPdoTR
   testAlgos['doAVdoTRdoAL'] = doAVdoTRdoAL
   testAlgos['doAVdoVLdoACdoAO'] = doAVdoVLdoACdoAO

   #testAlgos['doAVdoTRdoPT'] = doAVdoTRdoPT
   #testAlgos['doTRdoPTdoRTdoAVdoVL'] = doTRdoPTdoRTdoAVdoVL
   #testAlgos['doTRdoPTdoRTdoAVdoVLdoQP'] = doTRdoPTdoRTdoAVdoVL
   
   
   #testAlgos['doQPdoAV'] = doQPdoAV
   
   #testAlgos['doRangeTradeBars'] = doRangeTradeBars
   
   # useAvgBarLimits seems to not work. Fix it
   #testAlgos['useAvgBarLimits'] = useAvgBarLimits
   
#   testAlgos['doTRdoPTdoRT'] = doTRdoPTdoRT
#   testAlgos['doTRdoPTdoRTdoAV'] = doTRdoPTdoRTdoAV
#   testAlgos['doTRdoPTdoRTdoVL'] = doTRdoPTdoRTdoVL
#   testAlgos['doTRdoPTdoRTdoAVdoVL'] = doTRdoPTdoRTdoAVdoVL
#   testAlgos['doTRdoPTdoRTdoAVdoVLdoQP'] = doTRdoPTdoRTdoAVdoVLdoQP

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

#timeBar = [5]

for minBar in timeBar:

   #info = initParseInfo()

   for algo, values in testAlgos.items():

      readProfile(tdp)
      
      for value in values:
         for bars in openBuyBars:
#            # Reduce the iterations for range trading
#            if value > 1:
#               #if value % bars == 0:
#               if bars % value == 0:
#                  continue       
            
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



