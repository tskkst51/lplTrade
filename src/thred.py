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
   def __init__(self, ut, offLine, cwd):
      
      self.offLine = offLine
      self.cwd = cwd
      self.ut = ut
      
      self.logPath = os.getcwd() + "/logs/"
      self.debugPath = os.getcwd() + "/debug/"
      
      self.launchScript = os.getcwd() + "/scripts/runMaster.sh"
      if offLine:
         self.launchScript = cwd + "/scripts/runMaster.sh"
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPIDRunning(self, pid):
   
      print ("pid : " + str(pid))
      if pid.poll() != None:
         return 0
      return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def launchStocks(self, stocks, maxStocksToTrade):
      
      algo = "TB3_OC_QM_OB2_OS2_CB3_CS3_TR"
      #algo = "TB3_HI_QM_OB2_OS2_CB4_CS4_TR"
      #algo = "TB2_HL_HS_AL_QM_OB2_OS2_CB3_CS3_QP"
      p = {}
      
      ctr = 0
      for stock in stocks:
         if ctr >= maxStocksToTrade:
            return p
            
         self.ut.writePath(self.logPath + "active" + stock + ".ls", algo)
         self.ut.writePath(self.debugPath + "active" + stock + ".ds", algo)
         
         print ("SLAVESSSSSSSSSS[stock]\n" + self.launchScript + " " + stock + " " + algo)
         p[stock] = Popen([self.launchScript, stock, algo])
         ctr += 1
         sleep(1)

      return p
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def launchAlgos(self, algoData, maxStocksToTrade):
      
      p = {}
      
      ctr = 0
      for stock, algo in algoData.items():
         if ctr >= maxStocksToTrade:
            return p

         # Log path needs to be created before the slave is invoked so stdout is cosher
         self.ut.writePath(self.logPath + "active" + stock + ".ls", algo)
         self.ut.writePath(self.debugPath + "active" + stock + ".ds", algo)
         
         print ("SLAVESSSSSSSSS launchAlgos\n" + self.launchScript + " " + stock + " " + algo)
         p[stock] = Popen([self.launchScript, stock, algo])
         ctr += 1
         sleep(1)

      return p
