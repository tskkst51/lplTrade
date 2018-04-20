# Library for connection to API's

import bitstamp.client

class Connect:
  def __init__(self, service="bitstamp"):
    self.service = service
    self.publicClient = "service"
    self.privateClient = "service"
    pass
    
  def connect(self):    
    if (self.service == "bitStamp"):
      self.publicClient = bitstamp.client.Public()
      return (self.publicClient)
    # publicClient = connection.connect(service)
    
  def getVolume(self, currency="btc", alt="usd"):    
    if (self.service == "bitStamp"):
      vol = float(self.publicClient.ticker(currency, alt)['volume'])
      return (vol)
      
  def getCurrentPrice(self, currency="btc", alt="usd"):    
      if (self.service == "bitStamp"):
        cp = float(self.publicClient.ticker(currency, alt)['last'])
      return (cp)
      
  def getCurrentPrice(self, currency="btc", alt="usd"):    
      if (self.service == "bitStamp"):
        price = float(self.publicClient.ticker(currency, alt)['last'])
      return (price)
    