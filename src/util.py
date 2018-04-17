# lplTrade and company
# Let's trade some assets
#

import sys
import os
from time import gmtime, strftime

class Log:
  def __init__(self):
    pass
  def debug(self, msg):
    self.msg = msg
    print ("DEBUG: " + self.msg)
  def error(self, msg):
    self.msg = msg
    print ("ERROR: " + self.msg)
  def warning(self, msg):
    self.msg = msg
    print ("WARNING: " + self.msg)
  def info(self, msg):
    self.msg = msg
    print ("INFO: " + self.msg)
  def success(self, msg):
    self.msg = msg
    print ("SUCCESS: " + self.msg)
  def execution(self, ticker, closed, time):
    self.ticker = ticker
    self.closed = closed
    self.time = time
    print ("SUCCESS: " + self.msg)
# end Log

class Time:
  def __init__(self):
    pass
  def now(self):
    self.now = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    #now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print (self.now)
#end Time

if __name__ == "__main__":
        pass

log = Log()
time = Time()

log.error("yikes")
log.info("info")
log.warning("warning")
log.success("success")

time.now()

exit()
