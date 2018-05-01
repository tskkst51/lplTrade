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
		self.openBars = int(data['profile']['openBars'])
		self.closeBars = int(data['profile']['closeBars'])
		self.delay = int(data['profile']['tradingDelayBars'])
		
		# Open position using lowest close bars 
		# Close position using highest open bars 
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

		# Yet to implement.  BELOW HERE HASN"T BEEN IMPLEMENTED yet
		
		self.endTradingTime = float(data['profile']['endTradingTime'])
		self.profitPctTriggerAmt = float(data['profile']['profitPctTriggerAmt'])
		self.reverseLogic = int(data['profile']['reverseLogic'])
		self.buyNearLow = int(data['profile']['buyNearLow'])
		self.sellNearHi = int(data['profile']['sellNearHi'])
		self.aggressiveOpenPct = float(data['profile']['aggressiveOpenPct'])
		self.aggressiveClosePct = float(data['profile']['aggressiveClosePct'])
		self.profitPctTrigger = float(data['profile']['profitPctTrigger'])
		self.profitPctTriggerBar = int(data['profile']['profitPctTriggerBar'])
		self.reversalPctTrigger = float(data['profile']['reversalPctTrigger'])
		self.volumeRangeBars = int(data['profile']['volumeRangeBars'])
		self.amountPct = float(data['profile']['amountPct'])

		# Use trend indicators ot increase amount to trade
		self.shortTermTrendBars = int(data['profile']['shortTermTrendBars'])
		self.longTermTrendBars = int(data['profile']['longTermTrendBars'])
		
		# Before open/closing a position, wait for the close
		# Default is to open/close when intra bar passes limit
		self.waitForClose = int(data['profile']['waitForClose'])
		
		# Class variables
		self.position = "closed"
		self.positionType = 0
		self.positionPrice = 0.0
		self.stopLoss = 0.0
		self.stopGain = 0.0
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
		self.triggerBars = self.openBars
		self.currentBar = 0
		self.nextBar = 0
		self.rangeTradeValue = False
		self.rangeHi = 0.0
		self.rangeLo = 0.0
		
		self.intraHiValues = [0.0]	
		self.intraLowValues = [0.0]	

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def ready(self, currentNumBars):
	
		if self.rangeTradeBars > self.delay:
			self.delay = self.rangeTradeBars
			
		if self.shortTermTrendBars > self.delay:
			self.delay = self.shortTermTrendBars
			
		if self.longTermTrendBars > self.delay:
			self.delay = self.longTermTrendBars
		
		if self.delay < currentNumBars:
			return True
		else:
			return False
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setClosePrices(self, currentPrice):
	
		posOut = 0.0
		
		if self.positionType == self.buy:
			posOut = self.closeBuyLimit
			#posOut = float(self.closeBuyLimit) - self.closePositionFudge
		elif self.positionType == self.sell:
			posOut = self.closeSellLimit
			#posOut = float(self.closeSellLimit) + self.closePositionFudge

		self.stopGain = self.stopLoss = posOut
		
		return
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setInitialClosePrices(self, currentPrice):
				
		hiLoDiff = self.hiOpenCloseLimit - self.loOpenCloseLimit
		
		print ("Hi Lo diff: " + str(hiLoDiff) + "\n")
		
		if self.positionType == self.buy:
			posGain = float(currentPrice) + (float(hiLoDiff) * float(self.profitPctTriggerBar))
			posLoss = self.loOpenCloseLimit - self.closePositionFudge
		elif self.positionType == self.sell:
			posGain = float(currentPrice) - (float(hiLoDiff) * float(self.profitPctTriggerBar)) 
			posLoss = self.hiOpenCloseLimit + self.closePositionFudge

		self.initialStopGain = posGain
		self.initialStopLoss = posLoss
				
		return
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getInitialStopLoss(self):

		return self.initialStopLoss
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getInitialStopGain(self):

		return self.initialStopGain
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getStopLoss(self):

		return self.stopLoss
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
	def getOpenBars(self):
	
		return self.openBars
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getCloseBars(self):
	
		return self.closeBars
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setReversalLimit(self):
	
		if not self.reverseLogic:
			return False

		
		return self.reverseLogic

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getReversalLimit(self):
	
		return self.reverseLogic

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getWaitForNextBar(self):
	
		return self.waitForNextBar
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getProfitPctTriggerAmt(self):
	
		return self.profitPctTriggerAmt

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def inRangeTrade(self, currentPrice):
	
		if self.rangeTradeBars:
			if float(currentPrice) <= (self.rangeHi) and float(currentPrice) >= float(self.rangeLo):
				if not self.inPosition():
					print ("in range between " + str(self.rangeHi) +	" and " + str(self.rangeLo))

				return True

		return False
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def openPosition(self, buyOrSell, price):

		self.positionType = buyOrSell
		self.position = "open"
		self.positionPrice = price
		self.triggerBars = self.closeBars
		#self.setInitialClosePrices(price)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def closePosition(self):

		self.positionType = 0
		self.position = "close"
		self.positionPrice = 0.0
		self.triggerBars = self.openBars
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def inPosition(self):
			
		if self.position == "open":
			return True
		else:
			return False
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getPrice(self):

		return self.price
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCurrentBar(self, bar):

		self.currentBar = bar
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getCurrentBar(self):

		return self.currentBar
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setNextBar(self, nextBar):
		
		self.nextBar = nextBar
		
		return
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getNextBar(self):
	
		return self.nextBar

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getPositionPrice(self):
	
		return self.positionPrice		
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setRangeLimits(self, barChart):

		if not self.rangeTradeBars:
			return
			
		if len(barChart) < self.rangeTradeBars:
			return
			
		if self.rangeTradeBars:
			self.rangeHi = self.getHighestCloseOpenPrice(self.rangeTradeBars, barChart)
			self.rangeLo = self.getLowestCloseOpenPrice(self.rangeTradeBars, barChart)
			
		return
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setAllLimits(self, barChart):

		if len(barChart) < self.rangeTradeBars:
			return
		
		self.setRangeLimits(barChart)
		self.setIntraLimits(barChart)
		self.setOpenCloseLimits(barChart)
		self.setReversalLimit()

		return

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def takeAction(self, currentPrice, barChart):
		barChart = barChart
								
		action = self.algorithm(currentPrice, self.triggerBars, barChart)

		return action

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def algorithm(self, currentPrice, bars, barChart):
		returnVal = 0
		
		if self.useIntras:
			intraLowerHighs = intraHigherLows = 0
			intraLowerLows = intraHigherHighs = 0
			intraBuy = intraSell = False
			
			intraHigherHighs = self.getIntraHigherHighs()
			intraLowerLows = self.getIntraLowerLows()
			intraLowerHighs = self.getIntraLowerHighs()
			intraHigherLows = self.getIntraHigherLows()
			print("self.intraLowValues: ")
			print(self.intraLowValues)
			print("self.intraHighValues: ")
			print(self.intraHiValues)
			
			print("intraHigherLows intraLowerLows " + str(intraHigherLows) + " " + str(intraLowerLows))
			print("intraLowerHighs intraHigherHighs " + str(intraLowerHighs) + " " +  str(intraHigherHighs))
			
			if self.aggressiveOpen:
				if intraHigherLows and not intraLowerHighs:
					intraBuy = True
				if intraLowerHighs and not intraHigherLows:
					intraSell = True
			else:
				if intraHigherHighs and intraHigherLows:
					intraBuy = True
				if intraLowerHighs and not intraLowerLows:
					intraSell = True
				
			if not self.inPosition():
				if currentPrice > self.openBuyLimit and intraBuy:
					return 1
				if currentPrice < self.openSellLimit and intraSell:
					return 2
			else:
				if currentPrice > self.closeBuyLimit and intraBuy:
					return 1
				if currentPrice < self.closeSellLimit and intraSell:
					return 2
		else:
			if currentPrice > self.openBuyLimit:
				print( self.openBuyLimit)
				return 1
			if currentPrice < self.openSellLimit:
				print( self.openSellLimit)
				return 2

		return returnVal
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestCloseOpenPrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 1
		
		if len(barChart) < self.closeBars:
			return
		if len(barChart) <	self.openBars:
			return
			
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
	def setIntraLimits(self, barChart):
	
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
				self.intraLowValues[n] = barChart[barChartLen - n][self.lo]
				n += 1
			n = 0
			while n < loopHiIterator:
				self.intraHiValues[n] = barChart[barChartLen - n][self.hi]
				n += 1
		return
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenCloseLimits(self, barChart):
		
		self.setOpenBuyLimit(barChart)
		self.setOpenSellLimit(barChart)
		self.setCloseBuyLimit(barChart)
		self.setCloseSellLimit(barChart)
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenBuyLimit(self, barChart):
	
		if self.aggressiveOpen:
			self.openBuyLimit = self.getHighestClosePrice(self.triggerBars, barChart)
			print("aggressiveOpen openBuyLimit " + str(self.openBuyLimit))
		else:
			self.openBuyLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCloseBuyLimit(self, barChart):
	
		if self.aggressiveClose:
			self.closeBuyLimit = self.getLowestClosePrice(self.triggerBars, barChart)
			print("aggressiveClose closeBuyLimit " + str(self.closeBuyLimit))
		else:
			self.closeBuyLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenSellLimit(self, barChart):
	
		if self.aggressiveOpen:
			self.openSellLimit = self.getLowestClosePrice(self.triggerBars, barChart)
			print("aggressiveOpen openSellLimit " + str(self.openSellLimit))
		else:
			self.openSellLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setCloseSellLimit(self, barChart):
	
		if self.aggressiveClose:
			self.closeSellLimit = self.getHighestClosePrice(self.triggerBars, barChart)
			print("aggressiveClose closeSellLimit " + str(self.closeSellLimit))
		else:
			self.closeSellLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	'''def setOpenCloseLimits(self, barChart):
	
		#print ("triggerBars: " + str(self.triggerBars)
		if not self.aggressiveOpen and not self.aggressiveClose: 
			self.hiOpenCloseLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			self.loOpenCloseLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
		elif self.aggressiveOpen and self.aggressiveClose: 
			self.hiOpenCloseLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			self.loOpenCloseLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			
		return
'''
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraHigherHighs(self):
		if len(self.intraHiValues) < self.intraHigherHighsBars:
			return False

		n = 0
		highest = self.intraHiValues[0]
		
		while n < self.intraHigherHighsBars:
			hi = self.intraHiValues[n]
			if hi > highest:
				return False
			n += 1
		return True

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraLowerHighs(self):	
		if len(self.intraHiValues) < self.intraLowerHighsBars:
			return False
			
		n = 0
		highest = self.intraHiValues[0]
		
		while n < self.intraLowerHighsBars:
			hi = self.intraHiValues[n]
			if hi < highest:
				return False
			n += 1
		return True
 		

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraLowerLows(self):	
		if len(self.intraLowValues) < self.intraLowerLowsBars:
			return False
			
		n = 0
		lowest = self.intraLowValues[0]
		
		while n < self.intraLowerLowsBars:
			lo = self.intraLowValues[n]
			if lo < lowest:
				return False
			n += 1
		return True
 		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraHigherLows(self):	
		if len(self.intraLowValues) < self.intraHigherLowsBars:
			return False

		n = 0
		lowest = self.intraLowValues[0]
		
		while n < self.intraHigherLowsBars:
			lo = self.intraLowValues[n]
			if lo > lowest:
				return False
			n += 1
		return True
 				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestCloseOpenPrice(self, numBars, barChart):
		if len(barChart) < numBars:
			return 0.0

		n = 0
		maxPriceArr = [0.0] * numBars	
		barChartLen = len(barChart) - 1
		
		if len(barChart) < self.closeBars:
			return
		if len(barChart) <	self.openBars:
			return
				
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

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def highestHiLoIntraBarPrice(self, numBars, barChart):
	
		if len(barChart) < numBars:
			return 0.0

		n = 0
		maxPriceArr = [0.0] * numBars	
		barChartLen = len(barChart) - 1
	
		while n < numBars:
			hi = barChart[barChartLen - n][self.hi]
			lo = barChart[barChartLen - n][self.lo]
 
			maxPriceArr[n] = hi
			if lo > hi:
				maxPriceArr[n] = lo
			n += 1
		# End while
		
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
		# End while

		return float(maxPrice)
