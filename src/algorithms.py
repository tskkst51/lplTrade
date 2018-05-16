'''
Algorithms module
'''
import io

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm(object):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def __init__(self, data):
	
		# Required standard settings
		self.algorithmName = str(data['profile']['algorithm'])
		self.currency = str(data['profile']['currency'])
		self.alt = str(data['profile']['alt'])
		self.openBuyBars = int(data['profile']['openBuyBars'])
		self.closeBuyBars = int(data['profile']['closeBuyBars'])
		self.openSellBars = int(data['profile']['openSellBars'])
		self.closeSellBars = int(data['profile']['closeSellBars'])
		self.delay = int(data['profile']['tradingDelayBars'])
		
		# Open position using lowest close bars 
		# Close position using highest open bars 
		# Make sure their are >= 2 bars when using 
		self.aggressiveOpen = int(data['profile']['aggressiveOpen'])
		self.aggressiveClose = int(data['profile']['aggressiveClose'])
		
		# Additional value to add to close triggers
		self.closePositionFudge = float(data['profile']['closePositionFudge'])
		
		# Don't trade unless out of a range
		self.rangeTradeBars = int(data['profile']['rangeTradeBars'])
		
		# Use intras for determining open/close
		self.useIntras = int(data['profile']['useIntras'])
		self.intraHigherHighsBars = int(data['profile']['intraHigherHighsBars'])
		self.intraLowerLowsBars = int(data['profile']['intraLowerLowsBars'])
		self.intraLowerHighsBars = int(data['profile']['intraLowerHighsBars'])
		self.intraHigherLowsBars = int(data['profile']['intraHigherLowsBars'])
		
		# Wait for next bar before opening a position
		self.waitForNextBar = int(data['profile']['waitForNextBar'])

		# Yet to implement.	BELOW HERE HASN"T BEEN IMPLEMENTED yet
		
		self.endTradingTime = float(data['profile']['endTradingTime'])
		self.profitPctTriggerAmt = float(data['profile']['profitPctTriggerAmt'])
		self.reverseLogic = int(data['profile']['reverseLogic'])
		self.buyNearLow = int(data['profile']['buyNearLow'])
		self.sellNearHi = int(data['profile']['sellNearHi'])
		self.aggressiveOpenPct = float(data['profile']['aggressiveOpenPct'])
		self.aggressiveClosePct = float(data['profile']['aggressiveClosePct'])
		self.profitPctTrigger = float(data['profile']['profitPctTrigger'])
		self.profitPctTriggerBar = float(data['profile']['profitPctTriggerBar'])
		self.reversalPctTrigger = float(data['profile']['reversalPctTrigger'])
		self.volumeRangeBars = int(data['profile']['volumeRangeBars'])
		self.amountPct = float(data['profile']['amountPct'])

		# Use trend indicators ot increase amount to trade
		self.shortTermTrendBars = int(data['profile']['shortTermTrendBars'])
		self.midTermTrendBars = int(data['profile']['shortTermTrendBars'])
		self.longTermTrendBars = int(data['profile']['longTermTrendBars'])
		
		self.executeOnCloseBuy = int(data['profile']['executeOnCloseBuy'])
		self.executeOnCloseSell = int(data['profile']['executeOnCloseSell'])

		self.intraBarMaxCounter = int(data['profile']['intraBarMaxCounter'])

		self.dynamic = int(data['profile']['dynamic'])
		
		# Class variables
		self.position = "close"
		self.positionType = 0
		self.openPositionPrice = 0.0
		self.closePositionPrice = 0.0
		self.stopBuy = 0.0
		self.stopSell = 0.0
		self.initialStopGain = 0.0
		self.initialStopLoss = 0.0
				
		self.openBuyLimit = 0.0
		self.closeBuyLimit = 0.0
		self.openSellLimit = 0.0
		self.closeSellLimit = 0.0
				
		self.hi = 0
		self.lo = 1
		self.open = 2
		self.close = 3
		self.volume = 4
		
		self.buy = 1
		self.sell = 2
		self.triggerBars = self.openBuyBars
		self.currentBar = 0
		self.nextBar = 0
		self.rangeTradeValue = False
		self.rangeHi = 0.0
		self.rangeLo = 0.0
		
		self.intraHiValues = [0.0]	
		self.intraLowValues = [0.0]

		self.topIntraBar = 0.0
		self.intraBarCounter = 0
		self.revDirty = False
		self.barCount = 0
		self.barCountInPosition = 0 
		self.dirtyWaitForNextBar = False
		self.profitTarget = 0.0
		self.shortTermTrend = 0.0
		self.midTermTrend = 0.0
		self.longTermTrend = 0.0

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def takeAction(self, currentPrice, barChart):
		barChart = barChart
								
		action = self.algorithm(currentPrice, self.triggerBars, barChart)

		return action
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def algorithm(self, currentPrice, bars, barChart):
		returnVal = 0
		
		if self.useIntras:
			intraBuy = intraSell = False
			higherHighs = higherLows = lowerHighs = lowerLows = False

			# Set boolean if intra bar conditions are true 
			if self.intraHigherHighsBars and self.intraHigherLowsBars:
				if self.intraHigherHighs and self.intraHigherLows:
					print ("HERE1")
					intraBuy = True

			elif self.intraHigherHighsBars and not self.intraHigherLowsBars:
				if self.intraHigherHighs:
					print ("HERE2")
					intraBuy = True

			elif self.intraHigherLowsBars and not self.intraHigherHighsBars:
				if self.intraHigherLows:
					print ("HERE3")
					intraBuy = True

			if self.intraLowerLowsBars and self.intraLowerHighsBars:
				if self.intraLowerLows and self.intraLowerHighs:
					print ("HERE4")
					intraSell = True

			elif self.intraLowerLowsBars and not self.intraLowerHighsBars:
				if self.intraLowerLows:
					print ("HERE5")
					intraSell = True

			elif self.intraLowerHighsBars and not self.intraLowerLowsBars:
				if self.intraLowerHighs:
					print ("HERE6")
					intraSell = True

			if not self.inPosition():
				if currentPrice > self.openBuyLimit and intraBuy:
					print ( "open buy limit set " + str(self.openBuyLimit))
					return 1
				if currentPrice < self.openSellLimit and intraSell:
					print ("open sell limit set " +	str(self.openSellLimit))
					return 2
		else:
			if self.inPosition():
				print ("close buy limit " + str(self.closeBuyLimit))
				print ("close sell limit " +	str(self.closeSellLimit))
				if currentPrice > self.closeBuyLimit:
					return 1
				if currentPrice > self.closeSellLimit:
					return 2
			else:
				if currentPrice > self.openBuyLimit:
					print ( "open buy limit set " + str(self.openBuyLimit))
					return 1
				if currentPrice < self.openSellLimit:
					print ("open sell limit set " +	str(self.openSellLimit))
					return 2

		return returnVal
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def ready(self, currentNumBars):
	
		if self.rangeTradeBars > self.delay:
			self.delay = self.rangeTradeBars
			
		if self.shortTermTrendBars > self.delay:
			self.delay = self.shortTermTrendBars
			
		#if self.longTermTrendBars > self.delay:
			#self.delay = self.longTermTrendBars
		
		if self.delay <= currentNumBars:
			return True
		else:
			return False
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def inRangeTrade(self, currentPrice):
	
		if self.rangeTradeBars:
			if float(currentPrice) <= (self.rangeHi) and float(currentPrice) >= float(self.rangeLo):
				if not self.inPosition():
					print ("in range between " + str(self.rangeHi) +	" and " + str(self.rangeLo))

				return True

		return False
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def waitingForBestPrice(self, currentPrice):
	
		if self.waitForBestPrice:
			return
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def openPosition(self, buyOrSell, price, bar):

		if buyOrSell == self.buy:
			self.triggerBars = self.closeBuyBars
		elif buyOrSell == self.sell:
			self.triggerBars = self.closeSellBars

		print("\n")
		print("POSITION OPEN")
		print("buy/sell: " + str(buyOrSell))
		print("Position Price: " + str(price))

		self.positionType = buyOrSell
		self.position = "open"
		self.openPositionPrice = price
		self.setInitialClosePrices(price)
		self.barCount = 0
		self.barCountInPosition = 0
		self.setCurrentBar(bar)
		self.setProfitTarget(price)

		print("Initial stopGain: " + str(self.getInitialStopGain()))
		print("Initial stopLoss: " + str(self.getInitialStopLoss()))

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def closePosition(self, price, bar):

		gain = 0
		self.position = "close"
				
		if self.positionType == self.buy:
			self.triggerBars = self.openBuyBars
			gain = price - self.openPositionPrice
		elif self.positionType == self.sell:
			self.triggerBars = self.openSellBars
			gain = self.openPositionPrice - price

		# Wait for next bar if previous trade was a gain
		if gain > 0:
			self.waitForNextBar = 1
			
		self.closePositionPrice = price

		print ("\n")
		print ("POSITION CLOSED")
		print ("open price: " + str(self.openPositionPrice))
		print ("close price: " + str(self.closePositionPrice))
		print ("current Price: " + str(price))
		print ("stopPrice: " + str(self.getStopPrice()) + "\n")
		print ("bar Count In Position: " + str(self.barCountInPosition) + "\n")

		self.openPositionPrice = self.closePositionPrice = 0.0
		self.topIntraBar = 0.0
		self.setNextBar(bar+1)
		self.positionType = 0
		self.intraBarCounter = self.currentBar = 0
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def doReversal(self):
		if self.reversalPctTrigger > 0.0:
			return True

		return False

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def inPosition(self):
			
		if self.position == "open":
			return True
		else:
			return False

	# Setter definitions

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getReverseLogic(self):
	
		return self.reverseLogic
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCloseBuyStop(self, currentPrice):
	
		self.closeBuyLimit = currentPrice
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCloseSellStop(self, currentPrice):
	
		self.closeSellLimit = currentPrice
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setDynamic(self, currentPrice, bar):
	
		if not self.dynamic:
			return
	
	# if in a gain position set stop just above
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setBarCount(self, barCount):

		self.barCount = barCount

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setProfitTarget(self, currentPrice):

		if not self.profitPctTrigger:
			return
			
		print ("open position price: " + str(self.openPositionPrice))
		print ("profit pct trigger: " + str(self.profitPctTrigger))

		if self.positionType == self.buy:
			self.profitTarget = currentPrice + (self.openPositionPrice * self.profitPctTrigger)
		elif self.positionType == self.sell:
			self.profitTarget = currentPrice - (self.openPositionPrice * self.profitPctTrigger)

		print ("profit pct value: " + str(self.profitTarget))

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setIntraLimits(self):
	
			self.intraHigherHighs = self.getIntraHigherHighs()
			self.intraLowerLows = self.getIntraLowerLows()
			self.intraLowerHighs = self.getIntraLowerHighs()
			self.intraHigherLows = self.getIntraHigherLows()

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setIntraListLimits(self, barChart):
	
		if self.useIntras:
			if len(barChart) < self.intraLowerHighsBars:
				return
			if len(barChart) <	self.intraHigherLowsBars:
				return
			if len(barChart) < self.intraLowerLowsBars:
				return
			if len(barChart) <	self.intraHigherHighsBars:
				return
			
			loopLowIterator = loopHiIterator = 0
			
			if self.intraHigherLowsBars > self.intraLowerLowsBars:
				loopLowIterator = int(self.intraHigherLowsBars)
			else:
				loopLowIterator = self.intraLowerLowsBars
				
			if self.intraLowerHighsBars > self.intraHigherHighsBars:
				loopHiIterator = self.intraLowerHighsBars
			else:
				loopHiIterator = self.intraHigherHighsBars
				
			self.intraLowValues = [0.0] * loopLowIterator	
			self.intraHiValues = [0.0] * loopHiIterator	
		
			barChartLen = len(barChart) - 1
	
			n = 0
			while n < loopLowIterator:
				print (str(barChart[barChartLen - n][self.lo]))
				self.intraLowValues[n] = barChart[barChartLen - n][self.lo]
				n += 1
			n = 0
			while n < loopHiIterator:
				print (str(barChart[barChartLen - n][self.hi]))
				self.intraHiValues[n] = barChart[barChartLen - n][self.hi]
				n += 1	
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setInitialClosePrices(self, currentPrice):

		hiLoDiff = self.openBuyLimit - self.openSellLimit
		
		print ("Hi Lo diff: " + str(hiLoDiff) + "\n")
		
		if hiLoDiff == 0.0:
			hiLoDiff = 5.0

		if self.positionType == self.buy:
			posGain = float(currentPrice) + hiLoDiff * self.profitPctTriggerBar
			posLoss = self.closeBuyLimit - self.closePositionFudge
		elif self.positionType == self.sell:
			posGain = float(currentPrice) - (float(hiLoDiff) * float(self.profitPctTriggerBar)) 
			posLoss = self.closeSellLimit + self.closePositionFudge

		self.initialStopGain = posGain
		self.initialStopLoss = posLoss

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getReversalLimit(self, top, open, currentPrice):
	
		if self.reversalPctTrigger == 0.0:
			return False

		# Have to wait for the top to form so keep track of the top
		# top - open = length
		# length * reversal pct == price to sell

		print ("top " + str(top))
		print ("open " + str(open))
		print ("self.topIntraBar " + str(self.topIntraBar))
		print ("currentPrice " + str(currentPrice))
		print ("self.intraBarCounter " + str(self.intraBarCounter))
		print ("self.intraBarMaxCounter " + str(self.intraBarMaxCounter))
		print ("self.revDirty " + str(self.revDirty))

		# if not in a gain position get out
		if self.positionType == self.buy:
			if currentPrice < self.openPositionPrice:
				return False
		elif self.positionType == self.sell:
			if currentPrice > self.openPositionPrice:
				return False

		if not self.revDirty:
			self.topIntraBar = top
			self.revDirty = True
			self.intraBarCounter = 0
			return False

		if self.positionType == self.buy:
			if currentPrice >= top:
				self.topIntraBar = currentPrice
				self.intraBarCounter = 0
				return

			#if top >= self.topIntraBar:
			#	self.topIntraBar = top
			#	return False

			barLen = top - open

		elif self.positionType == self.sell:
			bottom = top
			if currentPrice <= bottom:
				self.topIntraBar = currentPrice
				self.intraBarCounter = 0
				return

			#if top <= self.topIntraBar:
			#	self.topIntraBar = top
			#	return False

			barLen = open - top

		if self.intraBarCounter < self.intraBarMaxCounter:
			# Wait 10 checks for top to be higher than previous
			print("intraBarCounter: " + str(self.intraBarCounter))
			self.intraBarCounter += 1
			return False
		
		targetPrice = (barLen * self.reversalPctTrigger)
		sellPrice = top - targetPrice

		print ("barLen " + str(barLen))
		print ("targetPrice " + str(targetPrice))
		print ("sell price " + str(sellPrice))

		if self.positionType == self.buy:
			if sellPrice < currentPrice:
				return True
		elif self.positionType == self.sell:
			if sellPrice > currentPrice:
				return True

		return False
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCurrentBar(self, bar):

		self.currentBar = bar
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setNextBar(self, nextBar):
		
		self.nextBar = nextBar

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setRangeLimits(self, barChart):

		if not self.rangeTradeBars:
			return
			
		if len(barChart) < self.rangeTradeBars:
			return
			
		if self.rangeTradeBars:
			self.rangeHi = self.getHighestCloseOpenPrice(self.rangeTradeBars, barChart)
			self.rangeLo = self.getLowestCloseOpenPrice(self.rangeTradeBars, barChart)
					
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setAllLimits(self, barChart, currentPrice, bar):

		if len(barChart) < self.rangeTradeBars:
			return
		
		self.setRangeLimits(barChart)
		self.setIntraListLimits(barChart)
		self.setIntraLimits()
		self.setTrendLimits(barChart, currentPrice)
		self.setOpenCloseLimits(barChart)
		#self.setProfitTarget(currentPrice)
		self.revDirty = False
		self.barCountInPosition = bar - self.currentBar

		if self.useIntras:
			print ("intraHigherLows intraHigherHighs " + str(self.intraHigherLows) + " " + str(self.intraHigherHighs)) 
			print ("intraLowerHighs intraLowerLows " + str(self.intraLowerHighs) + " " + str(self.intraLowerLows))

		self.setDynamic(currentPrice, bar)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setTrendLimits(self, barChart, currentPrice):
		# 0.0 - no trend; 1.[0-9] - bull; 2.[0-9] - bear
		# the fractional value is the strength 0 weak 9 strong

		if self.shortTermTrendBars == 0 or self.midTermTrendBars == 0 or self.longTermTrendBars == 0:
			return

		self.shortTermTrend = self.midTermTrend = self.longTermTrend = 0.0

		barChartLen = len(barChart) - 1
			
		if barChartLen <= self.shortTermTrendBars:
			return
			
		i = barChartLen - self.shortTermTrendBars
		lowest = 999999999.99
		highest = 0.0
		loBarPosition = hiBarPosition = 0
			
		while i < barChartLen:
			if barChart[i][self.lo] < lowest:
				lowest = barChart[i][self.lo]
				loBarPosition = i
			if barChart[i][self.hi] > highest:
				highest = barChart[i][self.hi]
				hiBarPosition = i
			i += 1
		
		# Comparing bar positions of the hi and lo gives us the trend
		if loBarPosition == hiBarPosition:
			return
		elif loBarPosition < hiBarPosition:
			# Bull trend
			self.shortTermTrend = 1.0
		elif loBarPosition > hiBarPosition:
			# Bear trend
			self.shortTermTrend = 2.0
		
		if highest > lowest:
			range = highest - lowest
		else:
			range = lowest - highest
			
		pctInTrend = pctInTrendRnd = 0

		# Determine where in the range the current price is
		penetration = 0.0
		if currentPrice <= lowest:
			pctInTrendRnd = 0.00
		elif currentPrice >= highest:
			pctInTrendRnd = 0.9999
		else:
			penetration = currentPrice - lowest
			pctInTrend = penetration / range
			pctInTrendRnd = round(pctInTrend, 2)

		# if pctInTrend > 1: then position is higher then the high of the range
		# and denoted with 0.9999 set above
		self.shortTermTrend += pctInTrendRnd

		print("loBarPosition: " + str(loBarPosition))
		print("hiBarPosition: " + str(hiBarPosition))
		print("highest: " + str(highest))
		print("lowest: " + str(lowest))
		print("range: " + str(range))
		print("penetration: " + str(penetration))
		print("pctInTrend: " + str(pctInTrend))
		print("pctInTrendRnd: " + str(pctInTrendRnd))
		print("shortTermTrend: " + str(self.shortTermTrend))

#==========================================================

		if barChartLen <= self.midTermTrendBars:
			return

		i = barChartLen - self.midTermTrendBars
		lowest = 999999999.99
		highest = 0.0
		loBarPosition = hiBarPosition = 0
			
		while i < barChartLen:
			if barChart[i][self.lo] < lowest:
				lowest = barChart[i][self.lo]
				loBarPosition = i
			if barChart[i][self.hi] > highest:
				highest = barChart[i][self.hi]
				hiBarPosition = i
			i += 1
		
		# Comparing bar positions of the hi and lo gives us the trend
		if loBarPosition == hiBarPosition:
			return
		elif loBarPosition < hiBarPosition:
			# Bull trend
			self.midTermTrend = 1.0
		elif loBarPosition > hiBarPosition:
			# Bear trend
			self.midTermTrend = 2.0
		
		if highest > lowest:
			range = highest - lowest
		else:
			range = lowest - highest
			
		pctInTrend = pctInTrendRnd = 0

		# Determine where in the range the current price is
		penetration = 0.0
		if currentPrice <= lowest:
			pctInTrendRnd = 0.00
		elif currentPrice >= highest:
			pctInTrendRnd = 0.9999
		else:
			penetration = currentPrice - lowest
			pctInTrend = penetration / range
			pctInTrendRnd = round(pctInTrend, 2)

		# if pctInTrend > 1: then position is higher then the high of the range
		# and denoted with 0.9999 set above
		self.midTermTrend += pctInTrendRnd

		print("loBarPosition: " + str(loBarPosition))
		print("hiBarPosition: " + str(hiBarPosition))
		print("highest: " + str(highest))
		print("lowest: " + str(lowest))
		print("range: " + str(range))
		print("penetration: " + str(penetration))
		print("pctInTrend: " + str(pctInTrend))
		print("pctInTrendRnd: " + str(pctInTrendRnd))
		print("midTermTrend: " + str(self.midTermTrend))

#==========================================================

		if barChartLen <= self.longTermTrendBars:
			return

		i = barChartLen - self.longTermTrendBars
		lowest = 999999999.99
		highest = 0.0
		loBarPosition = hiBarPosition = 0
			
		while i < barChartLen:
			if barChart[i][self.lo] < lowest:
				lowest = barChart[i][self.lo]
				loBarPosition = i
			if barChart[i][self.hi] > highest:
				highest = barChart[i][self.hi]
				hiBarPosition = i
			i += 1
		
		# Comparing bar positions of the hi and lo gives us the trend
		if loBarPosition == hiBarPosition:
			return
		elif loBarPosition < hiBarPosition:
			# Bull trend
			self.longTermTrend = 1.0
		elif loBarPosition > hiBarPosition:
			# Bear trend
			self.longTermTrend = 2.0
		
		if highest > lowest:
			range = highest - lowest
		else:
			range = lowest - highest
			
		pctInTrend = pctInTrendRnd = 0

		# Determine where in the range the current price is
		penetration = 0.0
		if currentPrice <= lowest:
			pctInTrendRnd = 0.00
		elif currentPrice >= highest:
			pctInTrendRnd = 0.9999
		else:
			penetration = currentPrice - lowest
			pctInTrend = penetration / range
			pctInTrendRnd = round(pctInTrend, 2)

		# if pctInTrend > 1: then position is higher then the high of the range
		# and denoted with 0.9999 set above
		self.longTermTrend += pctInTrendRnd

		print("loBarPosition: " + str(loBarPosition))
		print("hiBarPosition: " + str(hiBarPosition))
		print("highest: " + str(highest))
		print("lowest: " + str(lowest))
		print("range: " + str(range))
		print("penetration: " + str(penetration))
		print("pctInTrend: " + str(pctInTrend))
		print("pctInTrendRnd: " + str(pctInTrendRnd))
		print("longTermTrend: " + str(self.longTermTrend))
			
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenBuyLimit(self, barChart):
	
		if self.aggressiveOpen:
			self.openBuyLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			if not self.inPosition():
				print ("aggressiveOpen openBuyLimit " + str(self.openBuyLimit))
		else:
			self.openBuyLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			if not self.inPosition():
				print ("openBuyLimit " + str(self.openBuyLimit))

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenSellLimit(self, barChart):
	
		if self.aggressiveOpen:
			self.openSellLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			print ("aggressiveOpen openSellLimit " + str(self.openSellLimit))
		else:
			self.openSellLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			if not self.inPosition():
				print ("openSellLimit " + str(self.openSellLimit))
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCloseBuyLimit(self, barChart):
	
		if self.aggressiveClose:
			# Use with execute on close otherwise intra lows will knock us out
			self.closeBuyLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("aggressiveClose closeBuyLimit " + str(self.closeBuyLimit))
		else:
			self.closeBuyLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("closeBuyLimit " + str(self.closeBuyLimit))
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCloseSellLimit(self, barChart):
	
		if self.aggressiveClose:
			# Use with execute on close otherwise intra highs will knock us out
			self.closeSellLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("aggressiveClose closeSellLimit " + str(self.closeSellLimit))
		else:
			self.closeSellLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("closeSellLimit " + str(self.closeSellLimit))
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenCloseLimits(self, barChart):
		
		self.setOpenBuyLimit(barChart)
		self.setOpenSellLimit(barChart)
		self.setCloseBuyLimit(barChart)
		self.setCloseSellLimit(barChart)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getInitialStopLoss(self):

		return self.initialStopLoss
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getInitialStopGain(self):

		return self.initialStopGain
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getStopPrice(self):

		if self.positionType == self.buy:
			return self.closeBuyLimit
		elif self .positionType == self.sell:
			return self.closeSellLimit
			
		return 0.0
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getOpenPrice(self):

		if self.positionType == self.buy:
			return self.openBuyLimit
		elif self .positionType == self.sell:
			return self.openSellLimit
			
		return 0.0
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getStopGain(self):

		return self.stopGain
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getPositionType(self):

		return self.positionType
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getRangeBars(self):
	
		if self.rangeBars >= currentBar:
			return 1
		
		return 0
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getInRangeTrade(self, currentPrice):

		if self.rangeTradeBars:
			return self.inRangeTrade(currentPrice)

		return False

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getWaitForNextBar(self):
	
		return self.waitForNextBar
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getProfitPctTriggerAmt(self):
	
		return self.profitPctTriggerAmt
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getCurrentBar(self):

		return self.currentBar
						
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getNextBar(self):
	
		return self.nextBar

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getPositionPrice(self):
	
		return self.positionPrice		
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getExecuteOnCloseBuy(self):
	
		return self.executeOnCloseBuy
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getExecuteOnCloseSell(self):
	
		return self.executeOnCloseSell
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getBarsInPosition(self):
	
		return self.barCountInPosition 

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getProfitTarget(self):

		return self.profitTarget

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getShortTermTrend(self):

		return self.shortTermTrend

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getMidTermTrend(self):

		return self.midTermTrend

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLongTermTrend(self):

		return self.longTermTrend

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getDynamic(self):

		return self.dynamic

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraHigherHighs(self):
		if not self.intraHigherHighsBars:
			return False

		if len(self.intraHiValues) < self.intraHigherHighsBars:
			return False

		print (str(len(self.intraHiValues)))

		n = 1
		highest = self.intraHiValues[0]
		
		while n < self.intraHigherHighsBars:
			hi = self.intraHiValues[n]
			if hi >= highest:
				return False
			highest = self.intraHiValues[n]
			n += 1
		return True

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraLowerHighs(self):	
		if not self.intraLowerHighsBars:
			return False
		if len(self.intraHiValues) < self.intraLowerHighsBars:
			return False
			
		n = 1
		highest = self.intraHiValues[0]
		
		while n < self.intraLowerHighsBars:
			hi = self.intraHiValues[n]
			if hi <= highest:
				return False
			highest = self.intraHiValues[n]
			n += 1
		return True

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraLowerLows(self):	
		if not self.intraLowerLowsBars:
			return False
		if len(self.intraLowValues) < self.intraLowerLowsBars:
			return False
			
		n = 1
		lowest = self.intraLowValues[0]
		
		while n < self.intraLowerLowsBars:
			lo = self.intraLowValues[n]
			if lo <= lowest:
				return False
			lowest = self.intraLowValues[n]
			n += 1
		return True
 		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraHigherLows(self):	
		if not self.intraHigherLowsBars:
			return False
		if len(self.intraLowValues) < self.intraHigherLowsBars:
			return False

		n = 1
		lowest = self.intraLowValues[0]
		
		while n < self.intraHigherLowsBars:
			lo = self.intraLowValues[n]
			if lo >= lowest:
				return False
			lowest = self.intraLowValues[n]
			n += 1
		return True
 				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestCloseOpenPrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1
			
		while n < numBars:
			open = barChart[barChartLen - n][self.open]
			close = barChart[barChartLen - n][self.close]
 
			minPriceArr[n] = open
			if close < open:
				minPriceArr[n] = close
			n += 1
			
		#print ("min price arr: " + str(minPriceArr))
		
		# Compare all min prices and find the lowest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				minPrice = minPriceArr[n]
				clean = False
				continue
			
			if minPriceArr[n] < minPrice:
				minPrice = minPriceArr[n]
			
			n += 1

		return float(minPrice)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestCloseOpenPrice(self, numBars, barChart):

		if len(barChart) < numBars:
			return 0.0

		n = 0
		maxPriceArr = [0.0] * numBars	
		barChartLen = len(barChart) - 1
						
		while n < numBars:
			open = barChart[barChartLen - n][self.open]
			close = barChart[barChartLen - n][self.close]
 
			maxPriceArr[n] = open
			if close > open:
				maxPriceArr[n] = close
			n += 1
			
		#print ("max price arr: " + str(maxPriceArr))
		
		# Compare all max prices and find the highest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				maxPrice = maxPriceArr[n]
				clean = False
				continue
			
			if maxPriceArr[n] > maxPrice:
				maxPrice = maxPriceArr[n]
			
			n += 1

		return float(maxPrice)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestClosePrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1

		# Fill the list
		while n < numBars:
			minPriceArr[n] = barChart[barChartLen - n][self.close]
			n += 1
			
		# Compare all the closes and find the lowest price
		clean = True
		n = 0
		
		while n < numBars:
			if clean:
				minPrice = minPriceArr[n]
				clean = False
				continue
			
			if minPriceArr[n] < minPrice:
				minPrice = minPriceArr[n]
			
			n += 1

		return float(minPrice)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestClosePrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		maxPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1

		# Fill the list
		while n < numBars:
			maxPriceArr[n] = barChart[barChartLen - n][self.close]
			n += 1
			
		# Compare all the closes and find the highest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				maxPrice = maxPriceArr[n]
				clean = False
				continue
			
			if maxPriceArr[n] > maxPrice:
				maxPrice = maxPriceArr[n]
			
			n += 1
		# End while

		return float(maxPrice)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestOpenPrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1

		# Fill the list
		while n < numBars:
			minPriceArr[n] = barChart[barChartLen - n][self.open]
			n += 1
			
		# Compare all the closes and find the lowest price
		clean = True
		n = 0
		
		while n < numBars:
			if clean:
				minPrice = minPriceArr[n]
				clean = False
				continue
			
			if minPriceArr[n] < minPrice:
				minPrice = minPriceArr[n]
			
			n += 1

		return float(minPrice)
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestOpenPrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		maxPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1

		# Fill the list
		while n < numBars:
			maxPriceArr[n] = barChart[barChartLen - n][self.open]
			n += 1
			
		# Compare all the closes and find the highest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				maxPrice = maxPriceArr[n]
				clean = False
				continue
			
			if maxPriceArr[n] > maxPrice:
				maxPrice = maxPriceArr[n]
			
			n += 1
		# End while

		return float(maxPrice)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestIntraBarPrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1

		# Fill the list
		while n < numBars:
			minPriceArr[n] = barChart[barChartLen - n][self.lo]
			n += 1
			
		# Compare all the closes and find the lowest price
		clean = True
		n = 0
		
		while n < numBars:
			if clean:
				minPrice = minPriceArr[n]
				clean = False
				continue
			
			if minPriceArr[n] < minPrice:
				minPrice = minPriceArr[n]
			
			n += 1

		return float(minPrice)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestIntraBarPrice(self, numBars, barChart):

		if len(barChart) < numBars:
			return 0.0

		n = 0
		maxPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1

		# Fill the list
		while n < numBars:
			maxPriceArr[n] = barChart[barChartLen - n][self.hi]
			n += 1
			
		# Compare all the closes and find the highest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				maxPrice = maxPriceArr[n]
				clean = False
				continue
			
			if maxPriceArr[n] > maxPrice:
				maxPrice = maxPriceArr[n]
			
			n += 1
		# End while

		return float(maxPrice)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getlowestHiLoIntraBarPrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1

		while n < numBars:
			hi = barChart[barChartLen - n][self.hi]
			lo = barChart[barChartLen - n][self.lo]
 
			minPriceArr[n] = hi
			if lo < hi:
				minPriceArr[n] = lo
			n += 1
			
		# Compare all min prices and find the lowest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				minPrice = minPriceArr[n]
				clean = False
				continue
			
			if minPriceArr[n] < minPrice:
				minPrice = minPriceArr[n]
			
			n += 1

		return float(minPrice)

			
			
