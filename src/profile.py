## Profile methods

'''
profile module
'''

import json
import os
import time
import simplejson
import lplTrade as lpl
from optparse import OptionParser
from pathlib import Path
import subprocess
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Profile:
   def __init__(self, d):
   
      info = ""
      
      # Turn off all algo's 
      d["profileTradeData"]["timeBar"] = str(0)
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
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuyValue(self, d, value, info):
   
      d["profileTradeData"]["openBuyBars"] = str(value)
      
      info += "OB" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenSellValue(self, d, value, info):
   
      d["profileTradeData"]["openSellBars"] = str(value)
      
      info += "OS" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyValue(self, d, value, info):
   
      d["profileTradeData"]["closeBuyBars"] = str(value)
      
      info += "CB" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellValue(self, d, value, info):
   
      d["profileTradeData"]["closeSellBars"] = str(value)
      
      info += "CS" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuySellValues(self, d, value, info):
   
      d["profileTradeData"]["closeBuyBars"] = str(value)
      d["profileTradeData"]["closeSellBars"] = str(value)
      
      info += "CB" + str(value) + "_CS" + str(value)
   
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuySellValues(self, d, value, info):
   
      d["profileTradeData"]["openBuyBars"] = str(value)
      d["profileTradeData"]["openSellBars"] = str(value)
         
      info += "OB" + str(value) + "_OS" + str(value) + "_"
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseBuySellValues(self, d, value, info):
   
      d["profileTradeData"]["openBuyBars"] = str(value)
      d["profileTradeData"]["openSellBars"] = str(value)
      d["profileTradeData"]["closeBuyBars"] = str(value)
      d["profileTradeData"]["closeSellBars"] = str(value)
         
      info += "OB" + str(value) + " OS" + str(value) + " "
      info += "CB" + str(value) + " CS" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAlgoValues(self, d, algo, value, info):
   
      # algo from the CL can be any combination of algorithms
      # HS AO AC AV AL AB TR QP HL TR PT RV HM RP IT BO SO "
   
      info = ""
      
      d["profileTradeData"]["timeBar"] = str(value)
      info += "TB" + str(value) + "_"

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
   def readProfile(self, path):
   
      with open(path) as jsonData:
         return json.load(jsonData)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeProfile(self, path, data):
   
      with open(path, 'w') as fp:
          json.dump(data, fp, indent=2)
       


