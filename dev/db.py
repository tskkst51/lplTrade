## DB methods

'''
Db module
'''

import os

import subprocess

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DB:
   def __init__(self, d, day):

      self.d = d
      dbPath = "db/" + day
      dbLog = "db/" + day + "/log"
      
      # 625 running 5^5
      # 256 running 4^4
      
      self.seqAlgos = "LO_HI_HS_OC_CC_OO_EO_EC"

      self.numTestRows = 625
      self.numTestSeqRows = 256
      self.day = day

      self.tmpFile = "/tmp/dbTmp"
      
      self.port = self.getRunningPort()
      #print ("self.port " + str(self.port))

      self.cl = "psql algos -p " + str(self.port) + " -q -t -c '\\a' -c \""
      self.clF = "psql algos -p " + str(self.port) + " -q -t -c '\\a' -o " + self.tmpFile + " -c \""
      
#      self.cl = "psql algos -p " + str(self.port) + " -q -t -c '\\a' -c \""
#      self.clF = "psql algos -p " + str(self.port) + " -q -t -c '\\a' -o " + self.tmpFile + " -c \""
      
      #self.db = pg.open("pq://localhost:5678/Users/tsk/w/lplTrade/db/test")

      #self.clF = "psql algos -L " + self.tmpFile + "-o \"-p " + port + "\" -q -t " + "-c \a -c \""

      #self.stop = "pg_ctl -D " + dbPath + " stop"
      #self.start = "pg_ctl -D " + dbPath + " -l " + dbLog + " start"

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def skip1MinSeqTest(self, algo):
   
      if algo in self.seqAlgos:
         return 1
         
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getRunningPort(self):
   
      dbStr = "db/" + self.day
      port = 0
      
      port = os.popen("ps -ef | grep " + dbStr + " | awk '{print $12}'").read().splitlines()
      
      if len(port) == 0:
         print ("FAILED to get port ")
      
      print ("Port ffound " + str(port))
      
      return int(port[0])
       
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
      
      os.system(sqlCmd)
         
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def insertNoPriceAlgoData(self, sym, algo):
         
      winPct = "0"
      gain = "0.0"
   
      if self.algoTestCaseAlreadyRan(sym, algo) > 0:
         return
         
      sqlCmd = self.cl + "INSERT INTO algoData (sym, algo, gain, winPct) VALUES ('" + sym + "','" + algo + "','" + gain + "','" + winPct + "')\""
      
      os.system(sqlCmd)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algoTestCaseAlreadyRan(self, sym, algo):
            
      if self.execSQL(self.cl + "SELECT count(sym) FROM algoData WHERE sym = '" + sym + "' and algo = '" + algo + "'\""):
         return 1
      
#      sqlCmd = self.cl + "SELECT count(sym) FROM algoData WHERE sym = '" + sym + "' and algo = '" + algo + "'\""
#                     
#      dbRes = os.popen(sqlCmd).read().splitlines()
#
#      if len(dbRes) == 0:
#         return 0
#         
##      if dbRes == None or dbRes == "" or dbRes == " ":
##         return 0
#
#      #print ("dbRes: " + str(dbRes[0]))
#      #print ("sqlCmd: " + str(sqlCmd))
#
#      if int(dbRes[0]) > 0:
#         #print ("algo RANNNNN ")
#         return 1
         
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algoTestPurposeAlreadyRan(self, sym, algo):
      # TB1_OO_QM examples if 625 rows then already ran
      # TB2_IT_QM
      # TB5_OO_QM
                  
      count = 0

      algoCode = algo.split("_")
      algoCode = algoCode[1]
      
      numTestRows = self.numTestRows
      if self.skip1MinSeqTest(algoCode):
         numTestRows = self.numTestSeqRows
      
      algoMod = algo + "%"

      dbRes = self.execSQL(self.cl + "SELECT count(sym) FROM algoData WHERE sym = '" + sym + "' and algo = '" + algo + "'\"")
      
#      sqlCmd = self.cl + "SELECT count(algo) FROM algoData WHERE algo like '" + algoMod + "' and sym = '" + sym + "'\""
#             
#      dbRes = os.popen(sqlCmd).read().splitlines()
#     
      print ("Num of Rows returned " + str(dbRes))
      
      if dbRes >= numTestRows:
         return 1

##      if dbRes == None or dbRes == "" or dbRes == " " or dbRes == 0:
##         return 0
#         
#      print ("dbRes: " + str(dbRes))
#      print ("numTestRows: " + str(numTestRows))
               
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def execSQL(self, sqlCmd):
                  
      # Check DB

      if self.getRunningPort() < 3:
         cmd = self.cl + "pg_ctl -D db/" + self.day + " -l db/" + self.day + "/logfile start"
         startDBRes  = os.popen(cmd).read().splitlines()
         print ("startDBRes: " + str(startDBRes))
         return 0
         
      dbRes = os.popen(sqlCmd).read().splitlines()

      print ("dbRes: " + str(dbRes))
      
      if len(dbRes) == 0:
         return 0

      return dbRes[0]

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def testStart(self):
   
      os.system(self.d.dbTestStart)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def testReStart(self):
   
      os.system(self.d.dbTestStop)
      os.system(self.d.dbTestStart)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def testStop(self):
   
      os.system(self.d.dbTestStop)
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def openTestDB(self):
         
      return self.db
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def select(self, str):
   
      res = self.db.execute("select * from algoData")
      
      print ("res: " + str(res))
      
#      pg_ctl -D /Users/tsk/w/lplTrade/db/test -l db/test/logfile stop
#
#
#>>> db.execute("CREATE TABLE emp (emp_first_name text, emp_last_name text, emp_salary numeric)")
#>>> make_emp = db.prepare("INSERT INTO emp VALUES ($1, $2, $3)")
#>>> make_emp("John", "Doe", "75,322")
#>>> with db.xact():
#...  make_emp("Jane", "Doe", "75,322")
#...  make_emp("Edward", "Johnson", "82,744")
#

        
# end Db
