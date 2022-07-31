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
   def __init__(self, path):

      d = {}
      with open(path) as jsonData:
         try:
            d = json.load(jsonData)
         except: 
            print ("json load error 1") 
            try:
               sleep(1)
               d = json.load(jsonData)
            except: 
               print ("json load error 2") 
               try:
                  sleep(1)
                  d = json.load(jsonData)
               except: 
                  print ("json load error 3") 
               
      self.pfValues = d
      self.origPfValues = d
      
      return
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getPFValues(self):
   
      return self.pfValues
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initProfile(self, d):
   
      # Turn off all algo's 
      d["timeBar"] = str(0)
      d["doHiLoSeq"] = str(0)
      d["doHiLo"] = str(0)
      d["doHiSeq"] = str(0)
      d["doHiBuyLoSellSeq"] = str(0)
      d["doLoSeq"] = str(0)
      d["doOpenCloseSeq"] = str(0)
      d["doOpensSeq"] = str(0)
      d["doClosesSeq"] = str(0)
      d["doOpensCloses"] = str(0)
      d["doTrends"] = str(0)
      d["doQuickProfit"] = str(0)
      d["doReverseBuySell"] = str(0)
      d["doRangeTradeBars"] = str(0)
      d["useAvgBarLimits"] = str(0)
      d["doPatterns"] = str(0)
      d["doAverageVolume"] = str(0)
      d["doVolumeLastBar"] = str(0)
      d["aggressiveClose"] = str(0)
      d["aggressiveOpen"] = str(0)
      d["doAllPatterns"] = str(0)
      d["doHammers"] = str(0)
      d["doReversals"] = str(0)
      d["doPriceMovement"] = str(0)
      d["doExecuteOnOpen"] = str(0)
      d["doExecuteOnClose"] = str(0)
      d["doTrailingStop"] = str(0)
      d["doOnlySells"] = str(0)
      d["doOnlyBuys"] = str(0)
      d["quitMaxProfit"] = str(0)
      d["quitMaxLoss"] = str(0)
      d["doSessions"] = str(0)
      d["waitForNextBar"] = str(0)
      d["tradingDelayBars"] = str(0)
      d["averageVolumeOpen"] = str(0)
      d["averageVolumeClose"] = str(0)
      d["volumeLastBarOpen"] = str(0)
      d["volumeLastBarClose"] = str(0)
      d["doOnlyTrends"] = str(0)
      d["doInPosTracking"] = str(0)
      d["doDynamic"] = str(0)
      d["useAvgBarLimits"] = str(0)
      d["doTriggers"] = str(0)
      d["doDoubleUp"] = str(0)
      d["doubleUpMax"] = str(0)
      
      return d
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuyValue(self, d, value, info):
   
      d["openBuyBars"] = str(value)
      
      info += "OB" + str(value) + "_"
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenSellValue(self, d, value, info):
   
      d["openSellBars"] = str(value)
      
      info += "OS" + str(value) + "_"
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuyValue(self, d, value, info):
   
      d["closeBuyBars"] = str(value)
      
      info += "CB" + str(value) + "_"
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseSellValue(self, d, value, info):
   
      d["closeSellBars"] = str(value)
      
      info += "CS" + str(value)
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setCloseBuySellValues(self, d, value, info):
   
      d["closeBuyBars"] = str(value)
      d["closeSellBars"] = str(value)
      
      info += "CB" + str(value) + "_CS" + str(value)
   
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenBuySellValues(self, d, value, info):
   
      d["openBuyBars"] = str(value)
      d["openSellBars"] = str(value)
         
      info += "OB" + str(value) + "_OS" + str(value) + "_"
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseBuySellValues(self, d, value, info):
   
      d["openBuyBars"] = str(value)
      d["openSellBars"] = str(value)
      d["closeBuyBars"] = str(value)
      d["closeSellBars"] = str(value)
         
      info += "OB" + str(value) + " OS" + str(value) + " "
      info += "CB" + str(value) + " CS" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setDoubleUps(self, d, value, info):
   
      d["doDoubleUp"] = "1"      
      d["doubleUpMax"] = str(value)      
      info += "DU" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setInRangeBars(self, d, value, info):
   
      d["doRangeTradeBars"] = str(value)      
      info += "IR" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setTradingDelayBars(self, d, value, info):
   
      d["tradingDelayBars"] = str(value)      
      info += "DB" + str(value) + " "
      
      return info 
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setAlgoValues(self, d, algo, value, info):
   
      # return info, the algo string
      # d -> profile data
      # algo from the CL can be any combination of algorithms
      # HS AO AC AV AL AB TR QP HL TR PT RV HM RP IT BO SO DY"
   
      info = ""
      
      d["timeBar"] = str(value)
      info += "TB" + str(value) + "_"

      if "HS" in algo:
         d["doHiLoSeq"] = str(1)
         info += "HS_"

      if "HI" in algo:
         d["doHiSeq"] = str(1)
         info += "HI_"
      
      if "BL" in algo:
         d["doHiBuyLoSellSeq"] = str(1)
         info += "BL_"

      if "OC" in algo:
         d["doOpenCloseSeq"] = str(1)
         info += "OC_"
         
      if "OO" in algo:
         d["doOpensSeq"] = str(1)
         info += "OO_"
         
      if "CC" in algo:
         d["doClosesSeq"] = str(1)
         info += "CC_"
         
      if "PL" in algo:
         d["doOpensCloses"] = str(1)
         info += "PL_"
      
      if "LO" in algo:
         d["doLoSeq"] = str(1)
         info += "LO_"
      
      if "EO" in algo:
         d["doExecuteOnOpen"] = str(1)
         info += "EO_"
      
      if "EC" in algo:
         d["doExecuteOnClose"] = str(1)
         info += "EC_"

      if "HL" in algo:
         d["doHiLo"] = str(1)
         info += "HL_"
         
      if "TR" in algo:
         d["doTrends"] = str(1)
         info += "TR_"
   
      if "TS" in algo:
         d["doTrailingStop"] = str(1)
         info += "TS_"
   
      if "SS" in algo:
         d["doSessions"] = str(1)
         info += "SS_"
   
      if "BO" in algo:
         d["doOnlyBuys"] = str(1)
         info += "BO_"
   
      if "SO" in algo:
         d["doOnlySells"] = str(1)
         info += "SO_"
   
      if "QP" in algo:
         d["doQuickProfit"] = str(1)
         info += "QP_"
   
      if "RP" in algo:
         d["doReverseBuySell"] = str(1)
         info += "RV_"
   
      if "AB" in algo:
         d["useAvgBarLimits"] = str(1)
         info += "AB_"
   
      if "PT" in algo:
         d["doPatterns"] = str(1)
         info += "PT_"
   
      if "PA" in algo:
         d["doAllPatterns"] = str(1)
         info += "PA_"
   
      if "HM" in algo:
         d["doHammers"] = str(1)
         info += "HM_"
   
      if "RV" in algo:
         d["doReversals"] = str(1)
         info += "RV_"
   
      if "AC" in algo:
         d["aggressiveClose"] = str(1)
         info += "AC_"
   
      if "AO" in algo:
         d["aggressiveOpen"] = str(1)
         info += "AO_"
   
      if "PM" in algo:
         d["doPriceMovement"] = str(1)
         info += "PM_"
   
      if "QM" in algo:
         d["quitMaxProfit"] = str(1)
         info += "QM_"
         
      if "QL" in algo:
         d["quitMaxLoss"] = str(1)
         info += "QL_"
         
      if "WT" in algo:
         d["waitForNextBar"] = str(1)
         info += "WT_"

      if "AV" in algo:
         d["averageVolumeClose"] = str(1)
         info += "AV_"

      if "VI" in algo:
         d["averageVolumeOpen"] = str(1)
         info += "VI_"

      if "AL" in algo:
         d["volumeLastBarClose"] = str(1)
         info += "AL_"

      if "LI" in algo:
         d["volumeLastBarOpen"] = str(1)
         info += "LI_"
         
      if "OT" in algo:
         d["doOnlyTrends"] = str(1)
         info += "OT_"
         
      if "IT" in algo:
         d["doInPosTracking"] = str(1)
         info += "IT_"
         
      if "DY" in algo:
         d["doDynamic"] = str(1)
         info += "DY_"
         
      if "UA" in algo:
         d["useAvgBarLimits"] = str(1)
         info += "UA_"
         
      if "TG" in algo:
         d["doTriggers"] = str(1)
         info += "TG_"
         
#      if "DU" in algo:
#         d["doDoubleUp"] = str(1)
#         info += "DU_"
         
      if "DU" in algo:
         b, m, bar = algo.rpartition("DU")
         bars, m, e = bar.partition("_")
         self.setDoubleUps(d, bars, "")
         
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

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setProfileValues(self, path):

      with open(path) as f:
         self.pfValues = json.load(f)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def gv(self, key):

      return self.pfValues[key]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOrigValues(self):

      return self.origPfValues

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def gov(self, key):

      return self.origPfValues[key]


