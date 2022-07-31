## DB methods

'''
Db module
'''

import os

import subprocess
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DB:
   def __init__(self, d, day):

      pgPath = "/Applications/Postgres.app/Contents/Versions/14/bin/"

      self.d = d
      self.dbPath = "db/" + day
      self.dbLog = "db/" + day + "/log"
      self.seqAlgos = "LO_HI_HS_OC_CC_OO_EO_EC"
      self.tmpFile = "/tmp/dbTmp"
      self.day = day
      self.port = self.getRunningPort(day)
      self.cl = pgPath + "psql algos -p " + str(self.port) + " -q -t -c '\\a' -c \""
      self.clF = pgPath + "psql algos -p " + str(self.port) + " -q -t -c '\\a' -o " + self.tmpFile + " -c \""
      self.timeBar = [1,3,5]
      
      # 625 rows when running 5^5 open close bars
      # 256 rows when running 4^4 open close bars 
      self.openCloseBars = 4
      self.openCloseBarsPlusTimeBar = 5

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def checkDB(self):

      port = self.getRunningPort(self.day)
      if not port:
         if not self.startDB():
            return 1

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNewPort(self, day):

      return random.randint(7000,8000)
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def runSQL(self, cmd):

      cmdStatus = os.popen(cmd).read().splitlines()

      if cmdStatus:
         return cmdStatus
      
      return 0
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def startDB(self, day):

      port = getNewPort()
      
      status = os.popen("pg_ctl -D " + self.dbPath + " -p " + port + " -l " + self.dbLog + " start").read().splitlines()
      
      os.environ["dbPort"] = str(status[0])

      return status[0]
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getNumTestRows(self, algo):
         
      if algo in self.seqAlgos:
         return self.openCloseBars**self.openCloseBars
               
      return self.openCloseBarsPlusTimeBar**self.openCloseBars

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getTestTimebars(self):
         
      return self.timeBar

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def skip1MinSeqTest(self, algo):
   
      if algo in self.seqAlgos:
         return 1
         
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getRunningPort(self, day):
   
      dbStr = "db/" + day
      status = 0
            
      status = os.popen("ps -ef | grep " + dbStr + " | awk '{print $12}'").read().splitlines()
      
      if status[0]:
         return status[0]
      
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def insertAlgoData(self, sym, line):
   
      if line == None or line == "":
         return

      lineTokens = line.split()
         
      winPct = lineTokens[2].split('%')
      gain = lineTokens[1] 
      algo = lineTokens[3]

      if gain == None or gain == '' or gain == ' ':
         gain = 0.0
         
      if winPct[0] == None or winPct[0] == '' or winPct[0] == ' ':
         winPct[0] = 0.0
         
      if self.algoTestCaseAlreadyRan(sym, algo) > 0:
         return
      
      sqlCmd = self.cl + "INSERT INTO algoData (sym, algo, gain, winPct) VALUES ('" + sym + "','" + algo + "','" + gain + "','" + winPct[0] + "')\""

      self.runSQL(sqlCmd)
               
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def insertNoPriceAlgoData(self, sym, algo):

      winPct = "0"
      gain = "0.0"
   
      if self.algoTestCaseAlreadyRan(sym, algo) > 0:
         return
         
      sqlCmd = self.cl + "INSERT INTO algoData (sym, algo, gain, winPct) VALUES ('" + sym + "','" + algo + "','" + gain + "','" + winPct + "')\""

      self.runSQL(sqlCmd)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algoTestCaseAlreadyRan(self, sym, algo):
            
      sqlCmd = self.cl + "SELECT count(sym) FROM algoData WHERE sym = '" + sym + "' and algo = '" + algo + "'\""

      status = self.runSQL(sqlCmd)
            
      #dbRes = os.popen(sqlCmd).read().splitlines()

      if len(status) == 0:
         return 0

      if int(status[0]) > 0:
         return 1
         
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algoTestPurposeAlreadyRan(self, sym, algo, algoCode):
      # TB1_OO_QM examples if 625 rows then already ran
      # TB2_IT_QM
      # TB5_OO_QM

      algoCode = algo.split("_")
      algoCode = algoCode[1]
      
      numTestRows = self.getNumTestRows(algoCode)
      
      algoMod = algo + "%"
      
      sqlCmd = self.cl + "SELECT count(algo) FROM algoData WHERE algo like '" + algoMod + "' and sym = '" + sym + "'\""

      status = self.runSQL(sqlCmd)
            
      if status == 0:
         return 0
                  
      if int(status[0]) >= numTestRows:
         return 1
      
      return 0
              
# end Db
