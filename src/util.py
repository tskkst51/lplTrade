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
buyAction = buy = 1
sellAction = sell = 2

currency = str(d["profile"]["currency"])
alt = str(d["profile"]["alt"])
symbol = currency + alt
timeBar = int(d["profile"]["timeBar"])
service = str(d["profile"]["service"])
algorithm = str(d["profile"]["algorithm"])
tradingDelayBars = int(d["profile"]["tradingDelayBars"])
openBuyBars = int(d["profile"]["openBuyBars"])
closeBuyBars = int(d["profile"]["closeBuyBars"])
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
		debugFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))

with open(logPath, "a+", encoding="utf-8") as logFile:
	logFile.write(lg.infoStamp(service, symbol, timeBar, openBuyBars, closeBuyBars))
with open(logPath, "a+", encoding="utf-8") as logFile:
	logFile.write(lg.header(tm.now()))

currency = str(d["profile"]["currency"])
alt = str(d["profile"]["alt"])
symbol = currency + alt
timeBar = int(d["profile"]["timeBar"])
service = str(d["profile"]["service"])
algorithm = str(d["profile"]["algorithm"])
tradingDelayBars = int(d["profile"]["tradingDelayBars"])
openBuyBars = a.openBuyBars
closeBuyBars = a.closeBuyBars
profile = str(d["profile"])

lg.info ("symbol " + str(symbol))
lg.info ("timeBar " + str(timeBar))
lg.info ("openBuyBars " + str(openBuyBars))
lg.info ("closeBuyBars " + str(closeBuyBars))

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
inBullTrade = inBearTrade = 0
# Main loop. Loop forever or to a.endTime
while True:

	# Set the initial loop time from the profile. Default None
	endBarLoopTime = time() + 60 * timeBar
	if debug:
		endBarLoopTime = time() + 5 * timeBar

	# initialVol = cn.getVolume(currency, alt)
	initialVol = 1.0
	
	cp = cn.getCurrentPrice(currency, alt)

	barChart[i][op] = barChart[i][hi] = barChart[i][lo] = float(cp)
	
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
			sleep(2)
		
		# Next bar
		if time() >= endBarLoopTime:
			lg.info(tm.now())
			barChart[i][cl] = currentPrice
			
			# Open position on close of previous bar range
			if not a.inPosition() and a.getExecuteOnOpen() and a.ready(i):
			
				print("Executing on open...")
				print("currentPrice getOpenBuyPrice getOpenSellPrice\n" + str(currentPrice) + "     " + str(a.getOpenBuyPrice()) + "      " +	str(a.getOpenSellPrice()))
				
				action = a.takeAction(currentPrice, barChart)
				if action == buyAction:
					if currentPrice >= a.getOpenBuyPrice():
						a.openPosition(buy, currentPrice, i)
						
						if a.getReverseLogic():
							lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
							lg.info("revAction: " + str(action))
						else:	
							lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
				elif action == sellAction:
					if currentPrice <= a.getOpenSellPrice():
						a.openPosition(sell, currentPrice, i)
						
						if a.getReverseLogic():
							lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
						else:	
							lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

			# Close position on open of previous bar range
			elif a.inPosition() and a.getExecuteOnClose() and a.ready(i):
				print("Executing on close...")
				print("currentPrice	gethighestCloseBuyPrice getLowestCloseSellPrice\n" + str(currentPrice) + "        " +	str(a.getHighestCloseBuyPrice()) + "        " +	str(a.getLowestCloseSellPrice()))
				if a.getPositionType() == buyAction:
					if currentPrice <= a.getHighestCloseBuyPrice():
						a.closePosition(currentPrice, i)
						lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
						triggered = False
				elif a.getPositionType() == sellAction:
					if currentPrice >= a.getLowestCloseSellPrice():
						a.closePosition(currentPrice, i)
						lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
						triggered = False

			lg.info ("BAR: " + str(barChart[i]) + " action " + str(action))	
			lg.info ("current price: " + str(currentPrice) + " " + str(action))
			a.setAllLimits(barChart, currentPrice, i)
			barChart.append([0.0,0.0,0.0,0.0,0.0])

			i += 1

			# Keep track of the bars in a position
			if a.inPosition():
				a.setBarCount()

			break
			
		print(str(currentPrice))

		# Wait n number of bars before trading
		if not a.ready(i):
			continue

		# Wait till next bar before trading if set
		if not a.inPosition():
			if a.getWaitForNextBar() and i < a.getNextBar():
				print("Waiting for next bar...")
				continue

		action = a.takeAction(currentPrice, barChart)
		
		if a.getTrendTrigger():			
			if a.getBullTrend():
				if not a.inPosition():
					print ( "OPEN BUY. BULL TREND")
					a.openPosition(1, currentPrice, i)
					
					if a.getReverseLogic():
						lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
					else:	
						lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
				else:
					if inBearTrade:
						a.closePosition(currentPrice, i)
						lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
						print ( "CLOSE BULL TREND POSITION.")
						inBullTrade = False

				inBullTrade = True

			elif a.getBearTrend():
				if not a.inPosition():
					a.openPosition(2, currentPrice, i)
					if a.getReverseLogic():
						lg.logIt(buy, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
					else:
						lg.logIt(sell, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
					print ( "OPEN SELL BEAR TREND")
				else:
					if inBullTrade:
						a.closePosition(currentPrice, i)
						lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
						print ( "CLOSE SELL TREND POSITION.")
						inBearTrade = False

				inBearTrade = True
			#elif a.inPosition():
				#a.closePosition(currentPrice, i)
				#lg.logIt(0, str(currentPrice), str(a.getBarsInPosition()), #tm.now(), logPath)
				#print ( "CLOSE ANY TREND POSITION")
			continue
							
		# Block trading if we are in a range and range trading is set
		if a.getPriceInRange(currentPrice) and not a.inPosition():
			continue

		# Detect a reversal pattern in the current bar. triggerring when
		# current bar is > than previous bar
		if a.inPosition() and a.doReversal():
			previousBarLen = float(barChart[i-1][cl] - barChart[i-1][op])
			currentBarLen = barChart[i][op] - currentPrice
			
			if previousBarLen < 0.0 and currentBarLen > 0.0:
				# Bars going different directions
				continue
			
			# Get rid of negative length bars
			if previousBarLen < 0.0:
				previousBarLen = previousBarLen * -1
			if currentBarLen < 0.0:
				currentBarLen = currentBarLen * -1
				
			currentOpen = barChart[i][op]

			currentHi = 0.0
			if action == buyAction:
				currentHi = barChart[i][hi]
			else:
				currentHi = barChart[i][lo]
				
			print("barLengths; current: " + str(currentBarLen) + " prev: " + str(previousBarLen))
			
			# Add an aditional percentage to currentBarLen for larger moves
			if currentBarLen > previousBarLen: 
				if a.getReversalLimit(currentHi, currentOpen, currentPrice):
					lg.info("triggered due to reversal detected!")
					a.closePosition(currentPrice, i)
					lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)

		print (str(currentPrice))

		if (action == buyAction or action == sellAction) and not a.inPosition() and not a.getExecuteOnOpen():
			#if a.getReverseLogic():
				#if action == buyAction:
					#print ("OPEN reversal logic applied buy -> sell...")
					#action = sellAction
					#a.openBuyLimit = a.openSellLimit
				#elif action == sellAction:
					#print ("OPEN reversal logic applied sell -> buy...")
					#action = buyAction
					#a.openSellLimit = a.openBuyLimit

			a.openPosition(action, currentPrice, i)

			if a.getReverseLogic():
				revAction = buyAction
				if action == buyAction: 
					revAction = sellAction
				lg.info("revAction: " + str(revAction) + " action " + str(action))
				lg.logIt(revAction, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
			else:
				lg.logIt(action, str(currentPrice), str(a.getBarsInPosition()), tm.now(), logPath)
									
			triggered = False


		if a.inPosition() and not a.getExecuteOnClose():
			#if a.getReverseLogic():
				#if action == buyAction:
					#print ("CLOSE reversal logic applied buy -> sell...")
					#action = sellAction
					#a.closeBuyLimit = a.closeSellLimit
				#elif action == sellAction:
					#print ("CLOSE reversal logic applied sell -> buy...")
					#action = buyAction
					#a.closeSellLimit = a.closeBuyLimit
			# In a position and still in first bar
			#if a.getCurrentBar() == i:								
			#	print ("In first bar...")
				#print ("InitialStopGain() " + str(a.getInitialStopGain()))
				#print ("In first bar...")
				#if a.getPositionType() == buyAction:
				#	if currentPrice > a.getInitialStopGain() or currentPrice < #a.getInitialStopLoss():
			#			triggered = True
			#	elif a.getPositionType() == sellAction:
			#		if currentPrice < a.getInitialStopGain() or currentPrice > a.getInitialStopLoss():
			#			triggered = True

			# In a position and in next bar
			#else:				
			profitTarget = a.getProfitTarget()
			if a.getPositionType() == buyAction:
				if currentPrice > profitTarget:
					lg.info("PROFIT TARGET MET: " + str(profitTarget))
					#a.setCloseBuyStop(currentPrice)
					triggered = True
				#elif currentPrice < a.getHighestCloseBuyPrice():
				elif currentPrice < a.getClosePrice():
					triggered = True
			elif a.getPositionType() == sellAction:
				if currentPrice < profitTarget:
					lg.info("PROFIT TARGET MET: " + str(profitTarget))
					# a.setCloseSellStop(currentPrice)
					triggered = True
				#elif currentPrice > a.getLowestCloseSellPrice():
				elif currentPrice > a.getClosePrice():
					triggered = True
							
			if triggered:				
				lg.logIt(close, str(currentPrice), str(a.getBarsInPosition()), tm.now(),	logPath)
								
				# Position is closed
				a.closePosition(currentPrice, i)
			
				triggered = False

			continue
				
		# th = Thread(a.logIt(action, currentPrice, str(a.getBarsInPosition()), tm.now(), logPath))
		# Write to log file
		
	# end bar loop
	#if i == 20: break
	
# end execution loop

lg.error("error")
lg.info("info")
lg.warning("warning")
lg.success("success")

exit()
