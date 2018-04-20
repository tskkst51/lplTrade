# lplTrade and company
# Let's trade some assets
#

import sys
import os
import io
from time import gmtime, strftime, sleep, time
#import krakenex
#from pykrakenapi import KrakenAPI
import bitstamp.client
from pusher import Pusher
import json
from optparse import OptionParser
from array import array
import numpy

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

class MyTime:
  def __init__(self):
    tm = ""
    pass
  def now(self):
    self.tm = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    #now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print (self.tm)
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
	
#end Time

if __name__ == "__main__":
        pass

# Parse options
parser = OptionParser()

parser.add_option("-p"  , "--profile", dest="profile",
  help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
  action="store_true", dest="quiet", default=False,
  help="don't print status messages to stdout")
parser.add_option("-v", "--verbose",
  action="store_true", dest="verbose", default=False,
  help="verbose")
parser.add_option("-c", "--currency", type="string",
  action="store", dest="currency", default=False,
  help="currency to buy: btc... eth... bch...")
parser.add_option("-a", "--alt", type="string",
  action="store", dest="alt", default=False,
  help="alternate currency to buy: usd... uer... btc... eth... bch...")
parser.add_option("-l", "--log",
  action="store", dest="log",
  help="write report to FILE", metavar="FILE")

(options, args) = parser.parse_args()
print (options.verbose)
print (options.profile)
print (options.currency)
print (options.alt)

with open(options.profile) as jsonData:
	d = json.load(jsonData)
print (d["profile"])

# Price array hi lo open close volume
hi = 0
lo = 1
open = 2
close = 3
volume = 4
barChart = [[0,0,0,0,0]]
i = 0;

currency = d["profile"]["currency"]
alt = d["profile"]["alt"]
timeBar = d["profile"]["timeBar"]
service = d["profile"]["service"]
log = d["profile"]["log"]

# publicClient = connection.connect(service)
publicClient = bitstamp.client.Public()

print ("any currency: ")
print (options.currency)
print ("any alt: ")
print (options.alt)

# Overide from the CL
if options.currency:
	currency = options.currency
	
if options.alt:
	alt = options.alt
	
print ("currency: ")
print (currency)
print ("alt: ")
print (alt)

print ("loop for " + timeBar + " minutes")

tm = MyTime()

#f = open("myfile.txt", "r", encoding="utf-8")
# Endless loop
while True:
	# Set the loop time from the profile
	endBarLoop = time() + 60 * int(timeBar)
	#endBarLoop = time() + 10 * 1
	
	intitialVol = float(publicClient.ticker(currency, alt)['volume'])
	barChart[i][open] = barChart[i][hi] = barChart[i][lo] = float(publicClient.ticker(currency, alt)['last'])
	while True:
		
		vol = float(publicClient.ticker(currency, alt)['volume'])
		currentPrice = float(publicClient.ticker(currency, alt)['last'])
		stamp = publicClient.ticker(currency, alt)['timestamp']
		
		if currentPrice > barChart[i][hi]:
			barChart[i][hi] = currentPrice
			
		if currentPrice < barChart[i][lo]:
			barChart[i][lo] = currentPrice
					
		barChart[i][volume] =  vol - intitialVol
			
		sleep(10)

		print (tm.now())
		print ("bar " + str(i) + " currentPrice: " + str(currentPrice))
		print ("hi:     lo:    open:   close: vol")
		print(barChart[i])
		if time() >= endBarLoop:
			print ("\n")
			barChart[i][close] = currentPrice
			print (barChart[i])
			barChart.append([0,0,0,0,0])
			i += 1
			break
			
		priceEval = Price(timeBar)
		#action = priceEval.EvaluatePrice() "buy/sell..."
		HandleAction(action)

	# end bar loop
	if i == 20: break
	
# end execution loop

def HandleAction(action):
	algorithm = d['profile']['algorithm']
	
	
	return 1
	
exit()
os.environ['TZ'] = 'MST'
# os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
tzset()

log = Log()

# Create array for n d.timeBar
	

log.debug("Chart type: " + price.numBars + "bars")
log.debug("End Time: " + price.endTime)

log.error("yikes")
log.info("info")
log.warning("warning")
log.success("success")

tm.now()


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
