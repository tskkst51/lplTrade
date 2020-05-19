'''
Algorithms module
'''
import io

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm(object):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def __init__(self, data):
	
		# Required standard settings
		self.algorithmName = str(data['profileTradeData']['algorithm'])
		self.currency = str(data['profileTradeData']['currency'])
		self.alt = str(data['profileTradeData']['alt'])
		self.openBuyBars = int(data['profileTradeData']['openBuyBars'])
		self.closeBuyBars = int(data['profileTradeData']['closeBuyBars'])
		self.openSellBars = int(data['profileTradeData']['openSellBars'])
		self.closeSellBars = int(data['profileTradeData']['closeSellBars'])
		self.tradingDelayBars = int(data['profileTradeData']['tradingDelayBars'])
		
		# Open position using lowest close bars 
		# Close position using highest open bars 
		# Make sure their are >= 2 bars when using 
		self.aggressiveOpen = int(data['profileTradeData']['aggressiveOpen'])
		self.aggressiveClose = int(data['profileTradeData']['aggressiveClose'])

		# Increase the number of bars used determining close price
		self.increaseCloseBars = int(data['profileTradeData']['increaseCloseBars'])
		self.increaseCloseBarsMax = int(data['profileTradeData']['increaseCloseBarsMax'])
		self.gainTrailStop = int(data['profileTradeData']['gainTrailStop'])
		
		# Additional value to add to close triggers
		self.closePositionFudge = float(data['profileTradeData']['closePositionFudge'])
		
		# Don't trade unless out of a range
		self.rangeTradeBars = int(data['profileTradeData']['rangeTradeBars'])
		
		# Use intras for determining open/close
		self.useIntras = int(data['profileTradeData']['useIntras'])
		self.intraHigherHighsBars = int(data['profileTradeData']['intraHigherHighsBars'])
		self.intraLowerLowsBars = int(data['profileTradeData']['intraLowerLowsBars'])
		self.intraLowerHighsBars = int(data['profileTradeData']['intraLowerHighsBars'])
		self.intraHigherLowsBars = int(data['profileTradeData']['intraHigherLowsBars'])
		
		# Wait for next bar before opening a position
		self.waitForNextBar = int(data['profileTradeData']['waitForNextBar'])

		# Yet to implement.	BELOW HERE HASN"T BEEN IMPLEMENTED yet
		
		self.endTradingTime = float(data['profileTradeData']['endTradingTime'])
		self.profitPctTriggerAmt = float(data['profileTradeData']['profitPctTriggerAmt'])
		
		# reverseLogic appears to be best for short term charts and
		# low liquidity
		self.reverseLogic = int(data['profileTradeData']['reverseLogic'])
		self.buyNearLow = int(data['profileTradeData']['buyNearLow'])
		self.sellNearHi = int(data['profileTradeData']['sellNearHi'])
		self.aggressiveOpenPct = float(data['profileTradeData']['aggressiveOpenPct'])
		self.aggressiveClosePct = float(data['profileTradeData']['aggressiveClosePct'])
		self.profitPctTrigger = float(data['profileTradeData']['profitPctTrigger'])
		self.profitPctTriggerBar = float(data['profileTradeData']['profitPctTriggerBar'])
		self.reversalPctTrigger = float(data['profileTradeData']['reversalPctTrigger'])
		self.volumeRangeBars = int(data['profileTradeData']['volumeRangeBars'])
		self.amountPct = float(data['profileTradeData']['amountPct'])

		# Use trend indicators to increase amount to trade
		self.shortTrendBars = int(data['profileTradeData']['shortTrendBars'])
		self.midTrendBars = int(data['profileTradeData']['midTrendBars'])
		self.longTrendBars = int(data['profileTradeData']['longTrendBars'])
		self.megaTrendBars = int(data['profileTradeData']['megaTrendBars'])
		
		self.trendTrigger = int(data['profileTradeData']['trendTrigger'])
		
		self.executeOnClose = int(data['profileTradeData']['executeOnClose'])
		self.executeOnOpen = int(data['profileTradeData']['executeOnOpen'])

		self.intraBarMaxCounter = int(data['profileTradeData']['intraBarMaxCounter'])

		self.dynamic = int(data['profileTradeData']['dynamic'])
		
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
		self.highestcloseBuyLimit = 0.0
		self.lowestcloseBuyLimit = 0.0
		self.highestcloseSellLimit = 0.0
		self.lowestcloseSellLimit = 99999999.999999
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
		self.longMegaBars = 0.0
		
		self.shortTrend = self.midTrend = 0.0
		self.longTrend = self.megaTrend = 0.0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def takeAction(self, currentPrice, barChart):
		barChart = barChart
								
		action = self.algorithm(currentPrice, barChart)

		return action
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def algorithm(self, currentPrice, barChart):
		returnVal = 0
		
		# Use intraday bars. e.g. don't wait for next bar to enter trade
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

			if self.inPosition():
				print ("A close buy limit " + str(self.closeBuyLimit))
				print ("A close sell limit " +	str(self.closeSellLimit))
				if currentPrice < self.closeBuyLimit:
					#print ( "close buy limit reached " + str(self.closeBuyLimit))
					#if self.getReverseLogic():
						#return 2
					return 1
				if currentPrice > self.closeSellLimit:
					#print ("close sell limit reached " +	str(self.closeSellLimit))
					#if self.getReverseLogic():
						#return 1
					return 2
					
			if not self.inPosition():
				if currentPrice > self.openBuyLimit and intraBuy:
					print ("A open buy limit set " + str(self.openBuyLimit))
					#if self.getBullTrend() and self.getReverseLogic():
						#return 2
					return 1
				if currentPrice < self.openSellLimit and intraSell:
					print ("A open sell limit set " +	str(self.openSellLimit))
					#if self.getBearTrend() and self.getReverseLogic():
						#return 1
					return 2
		else:
			if self.inPosition():
				print ("close buy limit " + str(self.closeBuyLimit))
				print ("close sell limit " +	str(self.closeSellLimit))
				if currentPrice > self.closeBuyLimit:
					#if self.getReverseLogic():
						#return 2
					return 1
				if currentPrice > self.closeSellLimit:
					#if self.getReverseLogic():
						#return 1
					return 2
			else:
				if currentPrice > self.openBuyLimit:
					print ( "open buy limit set " + str(self.openBuyLimit))
					#if self.getReverseLogic():
						#return 2
					return 1
				if currentPrice < self.openSellLimit:
					print ("open sell limit set " +	str(self.openSellLimit))
					#if self.getReverseLogic():
						#return 1
					return 2

		return returnVal
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def ready(self, currentNumBars):
	
		if self.rangeTradeBars > self.tradingDelayBars:
			self.tradingDelayBars = self.rangeTradeBars
			
		#if self.shortTrendBars > self.tradingDelayBars:
			#self.tradingDelayBars = self.shortTrendBars
			
		#if self.longTrendBars > self.tradingDelayBars:
			#self.tradingDelayBars = self.longTrendBars
		
		if self.tradingDelayBars <= currentNumBars:
			return True
		else:
			return False
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def priceInRange(self, currentPrice):
	
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

		self.triggerBars = 0
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
		
		self.lowestcloseSellLimit = self.closeSellLimit
		self.highestcloseBuyLimit = self.closeBuyLimit

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
		#if gain > 0:
		#	self.waitForNextBar = 1
			
		self.closePositionPrice = price

		print ("\n")
		print ("POSITION CLOSED")
		print ("open price: " + str(self.openPositionPrice))
		print ("close price: " + str(self.closePositionPrice))
		print ("current Price: " + str(price))
		print ("stopPrice: " + str(self.getClosePrice()) + "\n")
		print ("bar Count In Position: " + str(self.barCountInPosition) + "\n")

		self.openPositionPrice = self.closePositionPrice = 0.0
		self.topIntraBar = 0.0
		self.setNextBar(bar+1)
		self.positionType = 0
		self.intraBarCounter = self.currentBar = 0
		self.highestcloseBuyLimit = 0.0
		self.lowestcloseSellLimit = 0.0
		
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
	def setBarCount(self):

		self.barCount += 1

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
				#print ("low intra: " + str(barChart[barChartLen - n][self.lo]))
				self.intraLowValues[n] = barChart[barChartLen - n][self.lo]
				n += 1
			n = 0
			while n < loopHiIterator:
				#print ("hi intra: " + str(barChart[barChartLen - n][self.hi]))
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

			print ("top " + str(top))
			print ("open " + str(open))
			print ("self.topIntraBar " + str(self.topIntraBar))
			print ("currentPrice " + str(currentPrice))
			print ("self.intraBarCounter " + str(self.intraBarCounter))
			print ("self.intraBarMaxCounter " + str(self.intraBarMaxCounter))
			print ("self.revDirty " + str(self.revDirty))

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

		#self.triggerBars = 0
		self.barCountInPosition = 0
		self.setRangeLimits(barChart)
		self.setIntraListLimits(barChart)
		self.setIntraLimits()
		self.setTrendLimits(barChart, currentPrice)
		self.setOpenCloseLimits(barChart, currentPrice)
		
		#self.setProfitTarget(currentPrice)
		
		self.revDirty = False
		self.barCountInPosition = bar - self.currentBar

		if self.useIntras:
			print ("intraHigherLows intraHigherHighs " + str(self.intraHigherLows) + 
			   " " + str(self.intraHigherHighs)) 
			print ("intraLowerHighs intraLowerLows " + str(self.intraLowerHighs) + 
			   " " + str(self.intraLowerLows))

		self.setDynamic(currentPrice, bar)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setTrendLimits(self, barChart, currentPrice):

		self.setShortTrend("short", barChart, currentPrice)
		self.setMidTrend("mid", barChart, currentPrice)
		self.setLongTrend("long", barChart, currentPrice)
		self.setMegaTrend("mega", barChart, currentPrice)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setShortTrend(self, trendType, barChart, currentPrice):

		if self.shortTrendBars == 0:
			return
	
		self.shortTrend = 0.0
		barChartLen = len(barChart)
		print (str(barChartLen) + " " + str(self.shortTrendBars))
		if barChartLen <= self.shortTrendBars:
			return
			
		shortTrendBarLen = barChartLen - self.shortTrendBars
		
		self.setTrendValues(trendType, barChart, barChartLen, shortTrendBarLen, currentPrice)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setMidTrend(self, trendType, barChart, currentPrice):
		if self.midTrendBars == 0:
			return
	
		self.midTrend = 0.0
		barChartLen = len(barChart)
		print (str(barChartLen) + " " + str(self.midTrendBars))
		if barChartLen <= self.midTrendBars:
			return
			
		midTrendBarLen = barChartLen - self.midTrendBars
		
		self.setTrendValues(trendType, barChart, barChartLen, midTrendBarLen, currentPrice)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setLongTrend(self, trendType, barChart, currentPrice):
		if self.longTrendBars == 0:
			return
	
		self.longTrend = 0.0
					
		barChartLen = len(barChart)
		print (str(barChartLen) + " " + str(self.longTrendBars))
		if barChartLen <= self.longTrendBars:
			return
			
		longTrendBarLen = barChartLen - self.longTrendBars
		
		self.setTrendValues(trendType, barChart, barChartLen, longTrendBarLen, currentPrice)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setMegaTrend(self, trendType, barChart, currentPrice):
		if self.megaTrendBars == 0:
			return
	
		self.megaTrend = 0.0
					
		barChartLen = len(barChart)
		print (str(barChartLen) + " " + str(self.megaTrendBars))
		if barChartLen <= self.megaTrendBars:
			return
			
		megaTrendBarLen = barChartLen - self.megaTrendBars
		
		self.setTrendValues(trendType, barChart, barChartLen, megaTrendBarLen, currentPrice)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setTrendValues(self, trendType, barChart, barChartLen, i, currentPrice):
		# 0.0 - no trend; 1.[0-9] - bull; 2.[0-9] - bear
		# the fractional value is the strength 0 weak 9 strong

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
			trend = 1.0
		elif loBarPosition > hiBarPosition:
			# Bear trend
			trend = 3.0

		# Get the range of bars
		if highest > lowest:
			range = highest - lowest
		else:
			range = lowest - highest
			
		pctInTrend = pctInTrendRnd = 0.0

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
		trend += pctInTrendRnd
		
		if trendType == "short":
			self.shortTrend = trend
		elif trendType == "mid":
			self.midTrend = trend
		elif trendType == "long":
			self.longTrend = trend
		elif trendType == "mega":
			self.megaTrend = trend

		print(trendType + "Trend: " + str(trend))
		
		#print("loBarPosition: " + str(loBarPosition))
		#print("hiBarPosition: " + str(hiBarPosition))
		#print("highest: " + str(highest))
		#print("lowest: " + str(lowest))
		#print("range: " + str(range))
		#print("penetration: " + str(penetration))
		#print("pctInTrend: " + str(pctInTrend))
		#print("pctInTrendRnd: " + str(pctInTrendRnd) + "\n")
		#print("current: " + str(currentPrice))
		
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
	def setCloseBuyLimit(self, barChart, currentPrice):
	
		if self.aggressiveClose:
			# Use with execute on close otherwise intra lows will knock us out
			self.closeBuyLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("aggressiveClose closeBuyLimit " + str(self.closeBuyLimit))
		
		elif self.getExecuteOnClose():
			self.closeBuyLimit = self.getHighestClosePrice(self.triggerBars, barChart)
			if not self.inPosition():
				print ("getExecuteOnClose closeBuyLimit " + str(self.openBuyLimit))

		else:
			self.closeBuyLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("closeBuyLimit " + str(self.closeBuyLimit))
		
		# Always use the lowest/highest close once set for execute on close
		
		if self.inPosition():
			print ("bars in position: " + str(self.getBarsInPosition()))
			
		if self.closePositionFudge and self.closeBuyLimit != 0.0:			
			self.closeBuyLimit -= (self.closePositionFudge - float(self.getBarsInPosition()))
			print ("closeBuyLimit AFTER fudge " + str(self.closeBuyLimit))

		# Move the buy limit closer to the price if in a gain
		if self.gainTrailStop and self.getGain(currentPrice):
				if (currentPrice - self.gainTrailStop) > self.closeBuyLimit:
					self.closeBuyLimit = currentPrice - self.gainTrailStop
					print ("closeBuyLimit AFTER gainTrailStop " + str(self.closeBuyLimit))				
			
		if self.closeBuyLimit > self.highestcloseBuyLimit:
			self.highestcloseBuyLimit = self.closeBuyLimit
			print ("closeBuyhighestLimit set " + str(self.highestcloseBuyLimit))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCloseSellLimit(self, barChart, currentPrice):
	
		if self.aggressiveClose:
			# Use with execute on close otherwise intra highs will knock us out
			self.closeSellLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("aggressiveClose closeSellLimit " + str(self.closeSellLimit))
				
		elif self.getExecuteOnClose():
			self.closeSellLimit = self.getLowestClosePrice(self.triggerBars, barChart)
			if not self.inPosition():
				print ("getExecuteOnClose closeSellLimit " + str(self.closeSellLimit))

		else:
			self.closeSellLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			if self.inPosition():
				print ("closeSellLimit " + str(self.closeSellLimit))
		
		if self.inPosition():
			print ("bars in position: " + str(self.getBarsInPosition()))
			
		if self.closePositionFudge and self.closeSellLimit != 0.0:
			self.closeSellLimit += (self.closePositionFudge - float(self.getBarsInPosition()))
			print ("closeSellLimit AFTER fudge " + str(self.closeSellLimit))

		# Move the sell limit closer to the price if in a gain
		if self.gainTrailStop and self.getGain(currentPrice):
				if (currentPrice + self.gainTrailStop) < self.closeSellLimit:
					self.closeSellLimit = currentPrice + self.gainTrailStop
					print ("closeSellLimit AFTER gainTrailStop " + str(self.closeSellLimit))


		if self.closeSellLimit < self.lowestcloseSellLimit:
			self.lowestcloseSellLimit = self.closeSellLimit
			print ("closeSelllowestLimit AFTER fudge " + str(self.lowestcloseSellLimit))
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenCloseLimits(self, barChart, currentPrice):
		
		if (self.getBullTrend() or self.getBearTrend()) and self.inPosition():
			if self.increaseCloseBars:
				if self.getBarsInPosition() < self.increaseCloseBarsMax:
					self.triggerBars += self.getBarsInPosition()
					print("in trend increasing close bars: " + str(self.getBarsInPosition()) + "triggerBars: " + str(self.triggerBars))
			
		self.setOpenBuyLimit(barChart)
		self.setOpenSellLimit(barChart)
		self.setCloseBuyLimit(barChart, currentPrice)
		self.setCloseSellLimit(barChart, currentPrice)
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getGain(self, currentPrice):

		if currentPrice > self.openPositionPrice:
			return True

		return False
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getInitialStopLoss(self):

		return self.initialStopLoss
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getInitialStopGain(self):

		return self.initialStopGain
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getClosePrice(self):

		if self.positionType == self.buy:
			return self.closeBuyLimit
		elif self .positionType == self.sell:
			return self.closeSellLimit
			
		return 0.0
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestCloseBuyPrice(self):

		return self.lowestcloseBuyLimit
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestCloseBuyPrice(self):

		return self.highestcloseBuyLimit		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestCloseSellPrice(self):

		return self.lowestcloseSellLimit
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestCloseSellPrice(self):

		return self.highestcloseSellLimit		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getOpenSellPrice(self):

		return self.openSellLimit		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getOpenBuyPrice(self):

		return self.openBuyLimit
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
	def getPriceInRange(self, currentPrice):

		if self.rangeTradeBars:
			return self.priceInRange(currentPrice)

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
	def getExecuteOnClose(self):
	
		return self.executeOnClose
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getExecuteOnOpen(self):
	
		return self.executeOnOpen
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getBarsInPosition(self):
	
		return self.barCount 
		#return self.barCountInPosition 
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getProfitTarget(self):

		return self.profitTarget

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getShortTrend(self):

		return self.shortTrend
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getMidTrend(self):

		return self.midTrend
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLongTrend(self):

		return self.longTrend
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getMegaTrend(self):

		return self.megaTrend
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getTrendTrigger(self):

		return self.trendTrigger
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getBearTrend(self):
		# Bear trend means mid, mega and long trends are bearish
		
		#if self.getShortTrend() >= 3.0 and self.getMidTrend() >= 3.0 and self.getLongTrend() >= 3.0:
		if self.getMegaTrend() >= 3.0 and self.getMidTrend() >= 3.0 and self.getLongTrend() >= 3.0:
			print("IN BEAR TREND")
			return True
		
		return False
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getBullTrend(self):
		# Bull trend means mid, long and mega are bullish
		
		#shortTrend = self.getShortTrend()
		midTrend = self.getMidTrend()
		longTrend = self.getLongTrend()
		megaTrend = self.getMegaTrend()
			
		#if shortTrend >= 1.0 and shortTrend <= 2.0:
		if midTrend >= 1.0 and midTrend <= 2.0:
			if longTrend >= 1.0 and longTrend <= 2.0:
				if megaTrend >= 1.0 and megaTrend <= 2.0:
					print("IN BULL TREND")
					return True
		
		return False
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getDynamic(self):

		return self.dynamic
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraHigherHighs(self):
		if not self.intraHigherHighsBars:
			return False

		if len(self.intraHiValues) < self.intraHigherHighsBars:
			return False

		#print ("intra hi values: " + str(len(self.intraHiValues)))

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

			
			
