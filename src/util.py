# lplTrade and company
# Let's trade some assets
#

#import krakenex
#from pykrakenapi import KrakenAPI
#import pusher
#import bitstamp.client
#from pusher import Pusher

import sys
import os
import io
import json
from time import time
from classes import *
from algorithms import *
from array import array
from optparse import OptionParser

if __name__ == "__main__":
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

parser = OptionParser()

parser.add_option("-p"  , "--profilePath", dest="profilePath",
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

(clOptions, args) = parser.parse_args()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load profile data

with open(clOptions.profilePath) as jsonData:
  d = json.load(jsonData)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set globals

# Price array hi lo open close volume
hi = 0
lo = 1
op = 2
cl = 3
volume = 4
barChart = [[0.0,0.0,0.0,0.0,0.0]]
i = 0;

currency = d["profile"]["currency"]
alt = d["profile"]["alt"]
timeBar = d["profile"]["timeBar"]
service = d["profile"]["service"]
algorithm = d["profile"]["algorithm"]
tradingDelayBars = d["profile"]["tradingDelayBars"]
profile = str(d["profile"])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overide profile data with command line data

if clOptions.currency:
  currency = clOptions.currency
  
if clOptions.alt:
  alt = clOptions.alt
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log file based on profile path

logPath = clOptions.profilePath.replace(".json", ".log")
logPath = logPath.replace("profiles", "logs")

lg = Log()
tm = Time()

with open(logPath, "a+", encoding="utf-8") as logFile:
  logFile.write(lg.header(tm.now()))

lg.info ("Reading profile data from: " + clOptions.profilePath)
lg.info ("Using currency: " + currency + " Alt currency: " + alt)
lg.message (timeBar + " Minute bar chart")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

cn = Connect(service)
cn.connectPublic()
# cn.connectPrivate()

# Initialize algorithm
algo = Algorithm(d)

# Main loop
while True:
  # Set the initial loop time from the profile. Default None
  
  #endBarLoopTime = time() + 60 * int(timeBar)
  endBarLoopTime = time() + 60
  
  # initialVol = float(publicClient.ticker(currency, alt)['volume'])
  initialVol = cn.getVolume(currency, alt)
  
  barChart[i][op] = barChart[i][hi] = barChart[i][lo] = cn.getCurrentPrice(currency, alt)
  
  # Loop until each bar has ended
  while True:
    # Load the barChart 
    vol = cn.getVolume(currency, alt)
    currentPrice = cn.getCurrentPrice(currency, alt)
    stamp = cn.getTimeStamp(currency, alt)
    
    if currentPrice > barChart[i][hi]:
      barChart[i][hi] = currentPrice
      
    if currentPrice < barChart[i][lo]:
      barChart[i][lo] = currentPrice
          
    barChart[i][volume] =  vol - initialVol
      
    sleep(3)

    print (tm.now())
    print ("bar " + str(i) + " currentPrice: " + str(currentPrice))
    print ("hi:     lo:    open:   close: vol")
    print(barChart[i])
          
    if time() >= endBarLoopTime:
      print ("\n")
      barChart[i][close] = currentPrice
      print (barChart[i])
      barChart.append([0,0,0,0,0])
      i += 1
      break
      
    if not algo.ready(i):
      continue
      
    action = algo.takeAction(currentPrice, i, barChart)
    
    if action == "buy" or action == "sell":
      triggered = algo.trigger()
      if triggered:
        pass
        # create thread to monitor position
        # Thread(createPosition)
      

  # end bar loop
  if i == 20: break
  
# end execution loop
  
exit()
os.environ['TZ'] = 'MST'
# os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
tzset()

# Create array for n d.timeBar
  

lg.debug("Chart type: " + price.numBars + "bars")
lg.debug("End Time: " + price.endTime)

lg.error("yikes")
lg.info("info")
lg.warning("warning")
lg.success("success")


#json.dump(clOptions.profilePath)

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
#     ltceur, ltcbtc, ethusd, etheur, ethbtc, bchusd, bcheur, bchbtc

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
