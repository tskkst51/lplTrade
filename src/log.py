# Log class

import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Log:

   def __init__(self, debugFlag, verboseFlag, logPath, debugPath, offLine, testMode=0):
      self.totGain = 0.0
      self.grandTotal = 0.0
      self.strAction = ""
      self.debugFlag = debugFlag
      self.verboseFlag = verboseFlag
      self.logPath = logPath
      self.debugPath = debugPath
      self.wins = 0
      self.losses = 0
      self.totalTrades = 0
      self.offLine = 0
      self.testMode = testMode
      
   def debug(self, msg):
      if self.debugFlag:
         #with open(self.debugPath, "a+", encoding="utf-8") as debugFile:
         #   debugFile.write (msg + "\n")
         #print ("DBG : " + msg)
         print (msg)
      
   def verbose(self, msg):
      if self.verboseFlag:
         self.debug (msg)
      
   def error(self, msg):
      self.msg = msg
      print ("ERR : " + self.msg)
      
   def warning(self, msg):
      self.msg = msg
      print ("WARN: " + self.msg)
      
   def info(self, msg):
      self.msg = msg
      print ("INFO: " + msg)
      #if self.debugFlag:
      #   self.debug("INFO: " + msg)
      
   def mg(self, msg):
      self.msg = msg
      print (self.msg)
      if self.debugFlag:
         self.debug(msg)

   def success(self, msg):
      self.msg = msg
      print ("SUCCESS: " + self.msg)
      
   def header(self, date):
      self.hdr =      "ACTION      GAIN  TOTAL WIN %  BARS TRADES TIME"
      self.hdrLine = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      return ("\n" + date + "\n" + self.hdr + "\n" + self.hdrLine + "\n")
      
   def infoStamp(self, liveActions):
      return ("\n" + liveActions)
      
   def execution(self, ticker, closed, time):
      self.ticker = ticker
      self.closed = closed
      self.time = time
      print ("SUCCESS: " + self.msg)
      
   def logIt(self, action, price, barLength, time, numTrades):
      totGain = grandTotal = ""
      if action == 1:
         self.strAction = "buy"
         self.priceSet = float(price)
      elif action == 2:
         self.strAction = "sell"
         self.priceSet = float(price)

      else:
         self.totGain = float(self.priceSet) - float(price)
         if self.totGain > 0 and self.strAction == "sell":
            self.wins += 1
            self.totalTrades += 1
         elif self.totGain < 0 and self.strAction == "sell":
            self.losses += 1
            self.totalTrades += 1
         elif self.totGain > 0 and self.strAction == "buy":
            self.losses += 1
            self.totalTrades += 1
         elif self.totGain < 0 and self.strAction == "buy":
            self.wins += 1
            self.totalTrades += 1
            
         if self.strAction == "buy":
            self.totGain = self.totGain*-1
               
         self.strAction = "close"
         self.priceSet = 0.0
         self.grandTotal += self.totGain

         totGain = format(self.totGain, '.2f')
         grandTotal = format(self.grandTotal, '.2f')

      if self.strAction == "close":
         winPct = 0.0
         print ("wins: " + str(self.wins) + " losses: " + str(self.losses))
         
         if self.wins == 0:
            print("Not calculating win % ")
         else:
            winPct = int(self.wins / self.totalTrades * 100)
         
         price = round(float(price), 2)
         
         with open(self.logPath, "a+", encoding="utf-8") as logFile:
            logFile.write (
               self.strAction + "   " + str(price) + " " + str(totGain) + " " + str(grandTotal)  + " " + str(winPct)  + "%   " + str(barLength) + " "  + str(numTrades) + "     " + str(time) + "\n")
      else:
         with open(self.logPath, "a+", encoding="utf-8") as logFile:
            logFile.write (
               self.strAction + " " + str(price) + "                             " + str(time) + "\n")
      
      self.totGain = 0.0
      return 1

# end Log
