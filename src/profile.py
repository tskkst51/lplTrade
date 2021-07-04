## Profile methods

'''
profile module
'''

import json
import yaml
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
   def __init__(self):
      return
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initProfile(self, d):
   
      # Turn off all algo's 
      d["profileTradeData"]["timeBar"] = str(0)
      d["profileTradeData"]["doHiLoSeq"] = str(0)
      d["profileTradeData"]["doHiLo"] = str(0)
      d["profileTradeData"]["doHiSeq"] = str(0)
      d["profileTradeData"]["doLoSeq"] = str(0)
      d["profileTradeData"]["doOpenCloseSeq"] = str(0)
      d["profileTradeData"]["doOpensSeq"] = str(0)
      d["profileTradeData"]["doClosesSeq"] = str(0)
      d["profileTradeData"]["doOpensCloses"] = str(0)
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
      d["profileTradeData"]["doAllPatterns"] = str(0)
      d["profileTradeData"]["doHammers"] = str(0)
      d["profileTradeData"]["doReversals"] = str(0)
      d["profileTradeData"]["doPriceMovement"] = str(0)
      d["profileTradeData"]["doExecuteOnOpen"] = str(0)
      d["profileTradeData"]["doExecuteOnClose"] = str(0)
      d["profileTradeData"]["doTrailingStop"] = str(0)
      d["profileTradeData"]["doOnlySells"] = str(0)
      d["profileTradeData"]["doOnlyBuys"] = str(0)
      d["profileTradeData"]["quitMaxProfit"] = str(0)
      d["profileTradeData"]["quitMaxLoss"] = str(0)
      d["profileTradeData"]["doSessions"] = str(0)
      d["profileTradeData"]["waitForNextBar"] = str(0)
      d["profileTradeData"]["tradingDelayBars"] = str(0)
      d["profileTradeData"]["averageVolumeOpen"] = str(0)
      d["profileTradeData"]["averageVolumeClose"] = str(0)
      d["profileTradeData"]["volumeLastBarOpen"] = str(0)
      d["profileTradeData"]["volumeLastBarClose"] = str(0)
      d["profileTradeData"]["doOnlyTrends"] = str(0)
      
      return d
      
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
   def setInRangeBars(self, d, value, info):
   
      d["profileTradeData"]["doRangeTradeBars"] = str(value)      
      info += "IR" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTradingDelayBars(self, d, value, info):
   
      d["profileTradeData"]["tradingDelayBars"] = str(value)      
      info += "DB" + str(value) + " "
      
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

      if "HI" in algo:
         d["profileTradeData"]["doHiSeq"] = str(1)
         info += "HI_"
      
      if "OC" in algo:
         d["profileTradeData"]["doOpenCloseSeq"] = str(1)
         info += "OC_"
         
      if "OO" in algo:
         d["profileTradeData"]["doOpensSeq"] = str(1)
         info += "OO_"
         
      if "CC" in algo:
         d["profileTradeData"]["doClosesSeq"] = str(1)
         info += "CC_"
         
      if "PL" in algo:
         d["profileTradeData"]["doOpensCloses"] = str(1)
         info += "PL_"
      
      if "LO" in algo:
         d["profileTradeData"]["doLoSeq"] = str(1)
         info += "LO_"
      
      if "EO" in algo:
         d["profileTradeData"]["doExecuteOnOpen"] = str(1)
         info += "EO_"
      
      if "EC" in algo:
         d["profileTradeData"]["doExecuteOnClose"] = str(1)
         info += "EC_"
      
      if "TR" in algo:
         d["profileTradeData"]["doTrends"] = str(1)
         info += "TR_"
   
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
   
      if "PA" in algo:
         d["profileTradeData"]["doAllPatterns"] = str(1)
         info += "PA_"
   
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
   
      if "QM" in algo:
         d["profileTradeData"]["quitMaxProfit"] = str(1)
         info += "QM_"
         
      if "QL" in algo:
         d["profileTradeData"]["quitMaxLoss"] = str(1)
         info += "QL_"
         
      if "WT" in algo:
         d["profileTradeData"]["waitForNextBar"] = str(1)
         info += "WT_"

      if "AV" in algo:
         d["profileTradeData"]["averageVolumeClose"] = str(1)
         info += "AV_"

      if "AL" in algo:
         d["profileTradeData"]["volumeLastBarClose"] = str(1)
         info += "AL_"

      if "VI" in algo:
         d["profileTradeData"]["averageVolumeOpen"] = str(1)
         info += "VI_"

      if "LI" in algo:
         d["profileTradeData"]["volumeLastBarOpen"] = str(1)
         info += "LI_"
         
      if "OT" in algo:
         d["profileTradeData"]["doOnlyTrends"] = str(1)
         info += "OT_"

      if "DB" in algo:
         b, m, bar = algo.rpartition("DB")
         bars, m, e = bar.partition("_")
         self.setTradingDelayBars(d, bars, "")
         
      if "IR" in algo:
         b, m, bar = algo.rpartition("IR")
         bars, m, e = bar.partition("_")
         self.setInRangeBars(d, bars, "")
         
      return info
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def readProfileY(self, path):
         
      with open(path) as f:
         return yaml.load(f, Loader=yaml.FullLoader)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def readProfile(self, path):
   
      with open(path) as f:
         return json.load(f)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeProfile(self, path, data, stock):
   
      if stock:
         #path = path + "_" + stock + "_" + str(os.getpid())
         path = path + "_" + stock
         
      with open(path, 'w') as f:
         json.dump(data, f, indent=2)
         f.flush()
         f.flush()
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writeProfileY(self, path, data, stock):

      if stock:
         path = path + "_" + stock + "_" + str(os.getpid())
         
      with open(path, 'x') as f:
         yaml.dump(data, f, indent=2)
         f.flush()
         f.flush()
       
       


