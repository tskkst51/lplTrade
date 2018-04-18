# lplTrade and company
# Let's trade some assets
#

import sys
import os
from time import gmtime, strftime, sleep
#import krakenex
#from pykrakenapi import KrakenAPI
import bitstamp.client
from pusher import Pusher
import json
from optparse import OptionParser

#import pusher

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

class Price:
  def __init__(self, numBars, endTime=None):
    self.numBars = numBars
    self.endTime = endTime
  def load(self):
    print (self.numBars)
    print (self.numBars)
#end Time

if __name__ == "__main__":
        pass

parser = OptionParser()
parser.add_option("-p"  , "--profile", dest="profile",
  help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
  action="store_false", dest="verbose", default=True,
  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

with open(options.profile) as jsonData:
    d = json.load(jsonData)
    print (d["profile"])
    print (d["profiles"]["chartTypeBars"])
    ##or key, val in d.iteritems():
    	#print ("attr: " + key + "value:" + val)

log = Log()
time = Time()

# Configure price array
price = Price(d["profiles"]["profile1"]["chartTypeBars"], d["profiles"]["profile1"]["endTime"])

log.debug("Chart type: " + price.numBars + "bars")
log.debug("End Time: " + price.endTime)

log.error("yikes")
log.info("info")
log.warning("warning")
log.success("success")

time.now()


#json.dump(options.profile)

#api = krakenex.API()
#k = KrakenAPI(api)
#ohlc, last = k.get_ohlc_data("BCHUSD")
#print(ohlc)
#tm = k.get_server_time()
#print (tm)
#ai = k.get_asset_info
#print (ai)
#print (k.get_tradable_asset_pairs(None))
#print (k.get_tradable_asset_pairs(None,"BCHUSD"))
#print (k.get_tradable_asset_pairs(None,"BTCUSD"))


# bitstamp client
#
# currencies: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, 
# 		ltceur, ltcbtc, ethusd, etheur, ethbtc, bchusd, bcheur, bchbtc

public_client = bitstamp.client.Public()
for i in range(0, 20):
  print(public_client.ticker()['volume'])
  print(public_client.ticker()['last'])
  print(public_client.ticker()['timestamp'])
  sleep(2)
  i += 1

# pusher
# pusher = Pusher(
#   app_id='511221',
#   key='5e2e9920fc698e55daac',
#   secret='ebd723b242a9aa35e0de',
#   cluster='us2',
#  ssl=True
# )
# pusher.trigger('my-channel', 'my-event', {'message': 'hello world'})

exit()
