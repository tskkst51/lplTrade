# lplTrade and company
# Let's trade some assets
#

#import krakenex
#from pykrakenapi import KrakenAPI
#import pusher
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

# Price array hi lo open close volume indexes
hi = 0
lo = 1
op = 2
cl = 3
volume = 4

barChart = [[0.0,0.0,0.0,0.0,0.0]]

i = 0
debug = 0

close = action = 0
buyAction = 1
sellAction = 2

currency = str(d["profile"]["currency"])
alt = str(d["profile"]["alt"])
symbol = currency + alt
timeBar = int(d["profile"]["timeBar"])
service = str(d["profile"]["service"])
algorithm = str(d["profile"]["algorithm"])
tradingDelayBars = int(d["profile"]["tradingDelayBars"])
openBars = int(d["profile"]["openBuyBars"])
closeBars = int(d["profile"]["closeBuyBars"])
profile = str(d["profile"])

#os.environ['TZ'] = 'MST'
#os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
#tzset()	
#print (time.strftime('%X %x %Z'))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overide profile data with command line data

if int(clOptions.currency):
	currency = clOptions.currency
	
if clOptions.alt:
	alt = clOptions.alt
	
if clOptions.debug:
	debug = int(clOptions.debug)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup log and debug file based on profile name and path

logPath = clOptions.profilePath.replace(".json", ".log")
logPath = logPath.replace("profiles", "logs")

debugPath = clOptions.profilePath.replace(".json", ".debug")
debugPath = logPath.replace("profiles", "logs")

if debug:
	debugPath = clOptions.profilePath.replace(".json", ".debug")
	debugPath = debugPath.replace("profiles", "logs")

lg = Log()
debugLog = Log()
tm = Time()

# Delay start time to sync with top of the minute
if not debug:
	tm.waitUntilTopMinute()

#if debug:
	#with open(debugPath, "a+", encoding="utf-8") as debugFile:
		#debugFile.write(debugLog.header(tm.now()))

lg.info ("Reading profile data from:\n" + clOptions.profilePath + "\n")
lg.info ("Using currency: " + symbol)
lg.info ("Start time: " + str(timeBar) + " Minute bar chart\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize algorithm

a = Algorithm(d)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Write header data to logs

if debug:
	with open(debugPath, "a+", encoding="utf-8") as debugFile:
		debugFile.write(lg.infoStamp(service, symbol, timeBar, openBars, closeBars))

with open(logPath, "a+", encoding="utf-8") as logFile:
	logFile.write(lg.infoStamp(service, symbol, timeBar, openBars, closeBars))
with open(logPath, "a+", encoding="utf-8") as logFile:
	logFile.write(lg.header(tm.now()))

currency = str(d["profile"]["currency"])
alt = str(d["profile"]["alt"])
symbol = currency + alt
timeBar = int(d["profile"]["timeBar"])
service = str(d["profile"]["service"])
algorithm = str(d["profile"]["algorithm"])
tradingDelayBars = int(d["profile"]["tradingDelayBars"])
openBars = a.openBuyBars
closeBars = a.closeBuyBars
profile = str(d["profile"])

lg.info ("symbol " + str(symbol))
lg.info ("timeBar " + str(timeBar))
lg.info ("openBars " + str(openBars))
lg.info ("closeBars " + str(closeBars))
if int(a.aggressiveOpen) > 0:
	lg.info ("aggresive open " + str(a.aggressiveOpen))
if int(a.aggressiveClose) > 0:
	lg.info ("aggresive close " + str(a.aggressiveClose))
if int(a.useIntras) > 0:
	lg.info ("intraHigherHighsBars " + str(a.intraHigherHighsBars))
	lg.info ("intraLowerLowsBars " + str(a.intraLowerLowsBars))
	lg.info ("intraLowerHighsBars " + str(a.intraLowerHighsBars))
	lg.info ("intraHigherLowsBars " + str(a.intraHigherLowsBars))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup connection to the exchange service

if service == "bitstamp":
	cn = ConnectBitStamp(service)
	cn.connectPublic()
elif service == "bitfinex":
	cn = ConnectBitFinex()

#cn.connectPrivate()

# Main loop. Loop forever or to a.endTime
while True:

	# Set the initial loop time from the profile. Default None
	endBarLoopTime = time() + 60 * timeBar
	if debug:
		endBarLoopTime = time() + 15 * timeBar

	# initialVol = cn.getVolume(currency, alt)
	initialVol = 1.0
	
	cp = cn.getCurrentPrice(currency, alt)

	barChart[i][op] = barChart[i][hi] = barChart[i][lo] = float(cp)
	stopPrice = 0.0
	stopPriceGain = 0.0
	
	# Loop until each bar has ended
	while True:
		# Load the barChart 
		# vol = cn.getVolume(currency, alt)
		vol = 1.0

		currentPrice = float(cn.getCurrentPrice(currency, alt))

		#currentPrice = float(cn.getCurrentPrice(currency, alt))
		#stamp = cn.getTimeStamp(currency, alt)
		
		if currentPrice > barChart[i][hi]:
			barChart[i][hi] = currentPrice
			
		if currentPrice < barChart[i][lo]:
			barChart[i][lo] = currentPrice
					
		barChart[i][volume] =	vol - initialVol
		
		if debug:
			sleep(4)
		else:
			sleep(1)
		
		# Next bar
		if time() >= endBarLoopTime:
			tm.now()
			barChart[i][cl] = currentPrice
			lg.info ("BAR: " + str(barChart[i]) + " action " + str(action))
				
			a.setAllLimits(barChart)
			barChart.append([0.0,0.0,0.0,0.0,0.0])
			if a.getStopPrice() != 0.0:
				lg.info ("stopPrice: " + str(a.getStopPrice()))
			if a.getOpenPrice() != 0.0:
				lg.info ("openPrice: " + str(a.getOpenPrice()))
	
			lg.info ("current price: " + str(currentPrice) + " " + str(action))
			# Open position on close of previous bar range
			if action and not a.inPosition() and a.getExecuteOnClose():
				print("Executing on open...")
				print("currentPrice  getOpenPrice " + str(currentPrice) + " " +	str(a.getOpenPrice()))
				if a.getPositionType() == buyAction:
					if currentPrice >= a.getOpenPrice():
						a.triggerExecution(currentPrice, i)
						lg.logIt(buy, str(currentPrice), tm.now(), logPath)
				if a.getPositionType() == sellAction:
					if currentPrice >= a.getOpenPrice():
						a.triggerExecution(currentPrice, i)
						lg.logIt(buy, str(currentPrice), tm.now(), logPath)

			# Execute on the close of the previous bar range
			if action and a.inPosition() and a.getExecuteOnClose():
				print("Executing on close...")
				print("currentPrice  getStopPrice " + str(currentPrice) + " " +	str(a.getStopPrice()))

				if a.getPositionType() == buyAction:
					if currentPrice <= a.getStopPrice():
						a.triggerExecution(currentPrice, i)
						lg.logIt(close, str(currentPrice), tm.now(), logPath)
						triggered = False
				elif a.getPositionType() == sellAction:
					if currentPrice >= a.getStopPrice():
						a.triggerExecution(currentPrice, i)
						lg.logIt(close, str(currentPrice), tm.now(), logPath)
						triggered = False
			
			i += 1

			if a.inPosition():
				a.setBarCount(i)

			break
			
		# Wait n number of bars before trading
		if not a.ready(i):
			continue

		if not a.inPosition():				
			if a.getWaitForNextBar() and i < a.getNextBar():
				continue
				
		# buy/sell connect to third party service
		# connect to third party service
		
		action = a.takeAction(currentPrice, barChart)

		# Block trading if we are in a range and range trading is set
		if a.getInRangeTrade(currentPrice) and not a.inPosition():
			continue

		#if a.getExecuteOnClose():
			#continue

		# Detect a reversal pattern in the current bar
		# Exit position 
		if action and a.inPosition() and a.reversalPctTrigger > 0.0:
			previousBarLen = float(barChart[i-1][cl] - barChart[i-1][op])
			currentBarLen = barChart[i][hi] - barChart[i][op]
			if previousBarLen < 0.0 and currentBarLen > 0.0:
				# Bars going different directios
				continue
			if previousBarLen < 0.0:
				previousBarLen = previousBarLen * -1
			if currentBarLen < 0.0:
				currentBarLen = currentBarLen * -1
			if action == buyAction:
				currentHi = barChart[i][hi]
				currentOpen = barChart[i][op]
			else:
				currentHi = barChart[i][lo]
				currentOpen = barChart[i][op]
			
			print(str(currentBarLen) + " " + str(previousBarLen))
			if currentBarLen > previousBarLen: 
				if a.getReversalLimit(currentHi, currentOpen, currentPrice):
					lg.info("triggered due to reversal detected!")
					a.triggerExecution(currentPrice, i)
					lg.logIt(close, str(currentPrice), tm.now(), logPath)

		if (action == buyAction or action == sellAction) and not a.inPosition():
		
			a.setCurrentBar(i)
			a.openPosition(action, currentPrice)

			lg.logIt(action, str(currentPrice), str(a.getBarsInPosition), tm.now(), logPath)
			
			print("\n")
			lg.info("POSITION OPEN")
			lg.info("buy/sell: " + str(action))
			lg.info("Initial stopGain: " + str(a.getInitialStopGain()))
			lg.info("Initial stopLoss: " + str(a.getInitialStopLoss()))
			lg.info("Position Price: " + str(currentPrice))
						
		triggered = False

		if a.inPosition() and not a.getExecuteOnClose():
			print (str(currentPrice))
			stopPrice = a.getStopPrice()
			
			# In a position and still in first bar
			if a.getCurrentBar() == i:
				#a.setInitialClosePrices(currentPrice)
				#stopLoss = a.getInitialStopLoss()
				#stopGain = a.getInitialStopGain()
				
				#lg.info("Initial stop gain: " + str(stopGain))
				#lg.info("Initial stop loss: " + str(stopLoss))
								
				if a.getPositionType() == buyAction:
					if currentPrice > a.initialStopGain or currentPrice < a.initialStopLoss:
						triggered = True
				elif a.getPositionType() == sellAction:
					if currentPrice < a.initialStopGain or currentPrice > a.initialStopLoss:
						triggered = True

			# In a position and in next bar
			else:				
				if a.getPositionType() == buyAction:
					#if a.getProfitPctTriggerAmt() > 0.0:
						#lg.info("getProfitPctTriggerAmt > 0.0:")
						#lg.info("initial position price: " + str(a.getPositionPrice()))
						#if currentPrice > (a.getPositionPrice() + a.getProfitPctTriggerAmt()):
							#lg.info("triggered 1")
							#triggered = True
					profitTarget = a.getProfitTarget() + currentPrice
					if currentPrice > profitTarget:
						lg.info("PROFIT TARGET MET: " + profitTarget)
						triggered = True
					if currentPrice < stopPrice:
						triggered = True
				elif a.getPositionType() == sellAction:
					profitTarget = a.getProfitTarget() - currentPrice
					if currentPrice < profitTarget:
						lg.info("PROFIT TARGET MET: " + profitTarget)
						triggered = True
					if currentPrice > stopPrice:
						triggered = True
					#if a.getProfitPctTriggerAmt() > 0.0:
						#lg.info("getProfitPctTriggerAmt > 0.0:")
						#lg.info("initial position price: " + str(a.getPositionPrice()))
						#if currentPrice < (a.getPositionPrice() - a.getProfitPctTriggerAmt()):
							#lg.info("currentPrice: <	initial position + current price")
						#if currentPrice < (a.getPositionPrice() + a.getProfitPctTriggerAmt()):
							#triggered = True
							#lg.info("triggered 2")
								
			if triggered:
				lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(),	logPath)
									
				a.triggerExecution(currentPrice, i)
				
				# Position is closed
				#a.closePosition()
				#a.setNextBar(i+1)
				triggered = False

			continue
				
		# th = Thread(a.logIt(action, currentPrice, tm.now(), logPath))
		#triggered = a.logIt(action, currentPrice, tm.now(), logPath)
		# Write to log file
		
	# end bar loop
	#if i == 20: break
	
# end execution loop

lg.error("error")
lg.info("info")
lg.warning("warning")
lg.success("success")

exit()
