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
from time import time, sleep
from classes import *
from connect import *
from log import *
from algorithms import *
from array import array
from optparse import OptionParser

if __name__ == "__main__":
				pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

parser = OptionParser()

parser.add_option("-p"	, "--profilePath", dest="profilePath",
	help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
	action="store_true", dest="quiet", default=False,
	help="don't print to stdout")
parser.add_option("-d", "--debug",
	action="store_true", dest="debug", default=False,
	help="don't print to logfile")
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
i = 0
debug = 1

currency = str(d["profile"]["currency"])
alt = str(d["profile"]["alt"])
symbol = currency + alt
timeBar = int(d["profile"]["timeBar"])
service = str(d["profile"]["service"])
algorithm = str(d["profile"]["algorithm"])
tradingDelayBars = int(d["profile"]["tradingDelayBars"])
openBars = int(d["profile"]["openBars"])
closeBars = int(d["profile"]["closeBars"])
profile = str(d["profile"])

#os.environ['TZ'] = 'MST'
#os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
#tzset()	
#print (time.strftime('%X %x %Z'))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overide profile data with command line data

if clOptions.currency:
	currency = clOptions.currency
	
if clOptions.alt:
	alt = clOptions.alt
	
if clOptions.debug:
	debug = clOptions.alt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log file based on profile path

logPath = clOptions.profilePath.replace(".json", ".log")
logPath = logPath.replace("profiles", "logs")

if debug:
	debugPath = clOptions.profilePath.replace(".json", ".debug")
	debugPath = debugPath.replace("profiles", "logs")

lg = Log()
debug = Log()
tm = Time()

# Delay start time to sync with top of the minute
#tm.waitUntillTopMinute()
with open(logPath, "a+", encoding="utf-8") as logFile:
	logFile.write(lg.header(tm.now()))

if debug:
	with open(debugPath, "a+", encoding="utf-8") as debugFile:
		debugFile.write(debug.header(tm.now()))

lg.info ("Reading profile data from:\n" + clOptions.profilePath)
lg.info ("Using currency: " + symbol)
lg.info (str(timeBar) + " Minute bar chart")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

cn = Connect(service)
cn.connectPublic()
# cn.connectPrivate()

# Initialize algorithm
a = Algorithm(d)

close = 0
buyAction = 1
sellAction = 2
dirty = False

# Main loop
while True:
	# Set the initial loop time from the profile. Default None
	
	endBarLoopTime = time() + 15 * timeBar
	#endBarLoopTime = time() + 60 * timeBar

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
					
		barChart[i][volume] =	vol - initialVol
		
		sleep(3)
		
		if time() >= endBarLoopTime:
			barChart[i][cl] = currentPrice
			lg.info (str(barChart[i]))
			lg.info ("current price: " + str(currentPrice))
			barChart.append([0,0,0,0,0])
			i += 1
			break
			
		if not a.ready(i):
			continue
				
		# buy/sell connect to third party service
		
		action = a.takeAction(float(currentPrice), barChart)
		
		if action == buyAction or action == sellAction:
			lg.info ("action 0 none, 1 buy, 2 sell: " + str(action))
		
		if (action == buyAction or action == sellAction) and not a.inPosition():
			a.openPosition(action, currentPrice)
			a.setCurrentBar(i)
			
			lg.trigger(symbol, action, currentPrice, tm.now(), logPath)
			lg.info("Position Open" + "\n")
			lg.info(str(symbol) + "\n" + str(sellAction) + "\n" + str(currentPrice) + "\n" + str(tm.now() + "\n"))
							
		if a.inPosition():	
			lg.info ("initial bar: " + str(a.getCurrentBar()))
			lg.info ("current bar: " + str(i))
			lg.info ("current price: " + str(currentPrice))
			# In a position and still in first bar
			if a.getCurrentBar() == i:
				lg.info ("INITIAL close prices set!!")
				a.setInitialClosePrices(currentPrice)
				stopLoss = a.getInitialStopLoss()
				stopGain = a.getInitialStopGain()
				lg.info("stop gain: " + str(stopGain))
				lg.info("stop loss: " + str(stopLoss))
				
			# In a position and in next bar
			if a.getCurrentBar() < i:
				a.setClosePrices(currentPrice)
				stopLoss = a.getStopLoss()
				stopGain = a.getStopGain()
				lg.info ("NEXT close prices set!!")
				lg.info("stop gain: " + str(stopGain))
				lg.info("stop loss: " + str(stopLoss))
				
			triggered = False
			
			if a.getCurrentBar() == i:
				if action == buyAction:
					if float(currentPrice) > float(stopGain) or float(currentPrice) < float(stopLoss):
						triggered = True
				elif action == sellAction:
					if float(currentPrice) < float(stopGain) or float(currentPrice) > float(stopLoss):
						triggered = True
			else:
				if action == buyAction:
					if float(currentPrice) < float(stopLoss):
						triggered = True
				elif action == sellAction:
					if float(currentPrice) > float(stopGain):
						triggered = True
					
			if triggered:
					lg.trigger(symbol, close, currentPrice, tm.now(), logPath)
					lg.info(str(symbol) + str(sellAction) + str(currentPrice) + str(tm.now()))
					lg.info("Close info. currentPrice: " + str(currentPrice))
					lg.info("Close info. stopGain: " + str(stopGain))
					lg.info("Close info. stopLoss: " + str(stopLoss))
					# Position is closed
					a.closePosition()
					lg.info("Position Closed" + "\n")
					lg.info ("current close price: " + str(currentPrice))
					#a.setCurrentBar(i)
			continue
				
		# th = Thread(a.trigger(action, currentPrice, tm.now(), logPath))
		#triggered = a.trigger(action, currentPrice, tm.now(), logPath)
		# Write to log file
		
	# end bar loop
	#if i == 20: break
	
# end execution loop

lg.error("yikes")
lg.info("info")
lg.warning("warning")
lg.success("success")

exit()
