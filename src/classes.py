'''
Classes module
'''
from time import gmtime, strftime, sleep
import bitstamp.client

class Log:
  def __init__(self):
    print ("\n")
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
  def message(self, msg):
    self.msg = msg
    print (self.msg)
  def success(self, msg):
    self.msg = msg
    print ("SUCCESS: " + self.msg)
  def header(self, date):
    self.hdr =     "SYM  OPEN   TIME CLOSE TIME GAIN/(LOSS) TOTAL $"
    self.hdrLine = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    return ("\n" + date + "\n" + self.hdr + "\n" + self.hdrLine + "\n")
  def execution(self, ticker, closed, time):
    self.ticker = ticker
    self.closed = closed
    self.time = time
    print ("SUCCESS: " + self.msg)
# end Log

class Time:
  def __init__(self):
    tm = ""
    pass
  def now(self):
    self.tm = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    return (self.tm)
#end Time

class Price:
  def __init__(self, numBars, endTime=None):
    self.numBars = numBars
    self.endTime = endTime
  def load(self):
    print (self.numBars)
    print (self.endTime)
  def evaluatePrice(self):
    print (self.numbars)
#end Price

class Connect:
  def __init__(self, service="bitstamp"):
    self.service = service
    pass
    
  def connectPublic(self):  
    if (self.service == "bitstamp"):
      self.publicClient = bitstamp.client.Public()
    return (self.publicClient)
    # publicClient = connection.connect(service)
    
  def connectPrivate(self):  
    # TODO
    if (self.service == "bitstamp"):
      self.privateClient = ""
    return (self.privateClient)
    
  def getVolume(self, currency="btc", alt="usd"):  
    vol = 0.0
    if (self.service == "bitstamp"):
      vol = float(self.publicClient.ticker(currency, alt)['volume'])
    return (vol)
      
  def getCurrentPrice(self, currency="btc", alt="usd"):    
      cp = 0.0
      if (self.service == "bitstamp"):
        cp = float(self.publicClient.ticker(currency, alt)['last'])
      return (cp)
      
  def getTimeStamp(self, currency="btc", alt="usd"): 
      stamp = 0.0
      if (self.service == "bitstamp"):
        stamp = float(self.publicClient.ticker(currency, alt)['timestamp'])
      return (stamp)
