# Log class

import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Log:

   def __init__(self, debugFlag, verboseFlag, logPath, debugPath, statsPath, offLine):
      self.totGain = 0.0
      self.grandTotal = 0.0
      self.strAction = ""
      self.debugFlag = debugFlag
      self.verboseFlag = verboseFlag
      self.logPath = logPath
      self.debugPath = debugPath
      self.statsPath = statsPath
      self.wins = 0
      self.losses = 0
      self.totalTrades = 0
      self.offLine = offLine
      self.noMsgs= 0
      if not debugFlag:
         self.noMsgs= 1
         
   def debug(self, msg):
      if self.noMsgs:
         return
      if self.debugFlag:
         if self.offLine:
            print (msg)
         else:
            with open(self.debugPath, 'a+') as f:
               f.write ('%s' % "DEB: " + str(msg) + "\n")
      
   def verbose(self, msg):
      if self.noMsgs:
         return
      if self.verboseFlag:
         if self.offLine:
            self.debug (msg)
         else:
            with open(self.debugPath, 'a+') as f:
               f.write ('%s' % "VER: " + str(msg) + "\n")
      
   def error(self, msg):
      if self.noMsgs:
         return
      if self.offLine:
         self.msg = msg
         print ("ERR : " + self.msg)
      else:
         with open(self.debugPath, 'a+') as f:
            f.write ('%s' % "ERR: " + str(msg) + "\n")

   def warning(self, msg):
      if self.noMsgs:
         return
      if self.offLine:
         self.msg = msg
         print ("WARN: " + self.msg)
      else:
         with open(self.debugPath, 'a+') as f:
            f.write ('%s' % "WARN: " + str(msg) + "\n")

   def info(self, msg):
      if self.offLine:
         self.msg = msg
         print ("INFO: " + msg)
      else:
         with open(self.debugPath, 'a+') as f:
            f.write ('%s' % "INFO: " + str(msg) + "\n")

   def stats(self, msg):
#      if self.noMsgs:
#         return
      #if self.offLine:
      print ("STATS: " + msg)
      with open(self.statsPath, 'a+') as f:
         f.write (str(msg) + "\n")
         
   def trade1stBarHeader(self, stock, timeBar):
      hdrLine = "~~~~~~~~~~ 1st BAR " + str(timeBar) + " minute chart " + stock + " ~~~~~~~~~~~~~~~~~~~~~~"
      if self.offLine:
         print ("STATS: " + hdrLine)
      with open(self.statsPath, 'a+') as f:
         f.write ('%s' % hdrLine + "\n")

   def mg(self, msg):
      self.msg = msg
      print (self.msg)
      if self.debugFlag:
         self.debug(msg)

   def success(self, msg):
      self.msg = msg
      print ("SUCCESS: " + self.msg)
      
   def header(self, date, stock):
      self.hdr =      "ACTION      GAIN  TOTAL WIN %  BARS TRADES TIME"
      self.hdrLine = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      return ("\n" + stock + " " + date + "\n" + self.hdr + "\n" + self.hdrLine + "\n")
      
   def infoStamp(self, liveActions):
      return ("\n" + liveActions)
      
   def execution(self, ticker, closed, time):
      self.ticker = ticker
      self.closed = closed
      self.time = time
      print ("SUCCESS: " + self.msg)
      
   def logIt(self, action, price, barLength, time, numTrades, gain):
      totGain = grandTotal = ""
      
      time = time.split()
      time = time[1]
      
      print("Time with no year " + str(time))

      if action == 1:
         print ("BUYYYYYY " + str(price))
         self.strAction = "buy"
         self.priceSet = float(price)
      elif action == 2:
         print ("SELLLLL " + str(price))
         self.strAction = "sell"
         self.priceSet = float(price)

      else:
         print ("gainnn " + str(gain))
         if gain:
            print ("gainnn " + str(gain))
            self.totGain += gain
            if gain > 0:
               self.wins += 1
            else:
               self.losses += 1
            #self.totGain = float(self.priceSet) - float(price) + gain
         else:
            self.totGain = float(self.priceSet) - float(price)
            
            if self.totGain > 0 and self.strAction == "sell":
               self.wins += 1
            elif self.totGain < 0 and self.strAction == "sell":
               self.losses += 1
            elif self.totGain > 0 and self.strAction == "buy":
               self.losses += 1
            elif self.totGain < 0 and self.strAction == "buy":
               self.wins += 1
         
         self.totalTrades += 1
            
         if self.strAction == "buy" and not gain:
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
         #price = float(price)
         
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
