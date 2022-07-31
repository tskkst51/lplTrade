## Thred methods

'''
thred module
'''

import os
import asyncio
from subprocess import Popen,PIPE
import mmap
from time import sleep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Thred():
   def __init__(self, ut, offLine, cwd, wcwd):
      
      self.offLine = offLine
      self.cwd = cwd
      self.wcwd = wcwd
      self.ut = ut
      
      self.logPath = os.getcwd() + "/logs/"
      self.debugPath = os.getcwd() + "/debug/"

      self.launchScript = cwd + "/scripts/runMaster.sh"
      if offLine:
         self.launchScript = cwd + "/scripts/testDB.sh"
         self.logPath = wcwd + "/logs/"
         self.debugPath = wcwd + "/debug/"
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPIDRunning(self, pid):
   
      print ("pid : " + str(pid))
      if pid.poll() != None:
         return 0
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def launchStock(self, stock, testDate):
      
      # Change default algo in premarket.py as well
      algo = "TB1_OC_QM_OB5_OS5_CB2_CS2_TR_IR5"
      #algo = "TB3_OC_QM_OB2_OS2_CB3_CS3_TR"
      #algo = "TB3_HI_QM_OB2_OS2_CB4_CS4_TR"
      #algo = "TB2_HL_HS_AL_QM_OB2_OS2_CB3_CS3_QP"
      p = {}

      print ("testDate " + testDate)
      
      #self.ut.writePath(self.logPath + "active" + stock + ".ls", algo)
      #self.ut.writePath(self.debugPath + "active" + stock + ".ds", algo)
      
      if testDate:
         algo = "none"
         p = Popen([self.launchScript, testDate, algo, stock])
      else:
         p = Popen([self.launchScript, stock, algo, ""])

      return p

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def launchStocks(self, stocks, maxStocksToTrade, testDate):
      
      # Change default algo in premarket.py as well
      algo = "TB1_OC_QM_OB5_OS5_CB2_CS2_TR_IR5"
      #algo = "TB3_OC_QM_OB2_OS2_CB3_CS3_TR"
      #algo = "TB3_HI_QM_OB2_OS2_CB4_CS4_TR"
      #algo = "TB2_HL_HS_AL_QM_OB2_OS2_CB3_CS3_QP"
      p = {}

      print ("testDate " + testDate)
      
      ctr = 0
      for stock in stocks:
         if ctr >= maxStocksToTrade:
            return p
            
         self.ut.writePath(self.logPath + "active" + stock + ".ls", algo)
         self.ut.writePath(self.debugPath + "active" + stock + ".ds", algo)
         
         if testDate:
            algo = "none"
            p[stock] = Popen([self.launchScript, testDate, algo, stock])
         else:
            p[stock] = Popen([self.launchScript, stock, algo, ""])
         ctr += 1
         sleep(1)

      return p
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def launchAlgos(self, algoData, maxStocksToTrade, testDate):
      
      p = {}
      
      print ("testDate " + testDate)

      ctr = 0
      for stock, algo in algoData.items():
         if ctr >= maxStocksToTrade:
            return p
         
         # Log path needs to be created before the slave is invoked so stdout is kosher
         self.ut.writePath(self.logPath + "active" + stock + ".ls", algo)
         self.ut.writePath(self.debugPath + "active" + stock + ".ds", algo)
         
         if testDate:
            print ("SLAVESS test launchAlgos\n" + self.launchScript + " " + stock + " " + algo)
            p[stock] = Popen([self.launchScript, stock, algo, testDate])
         else:
            print ("SLAVESS live launchAlgos\n" + self.launchScript + " " + stock + " " + algo)
            p[stock] = Popen([self.launchScript, stock, algo, ""])
         ctr += 1
         sleep(1)

      return p
