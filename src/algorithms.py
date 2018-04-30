'''
Algorithms module
'''
import io

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm(object):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def __init__(self, data):
		self.algorithmName = str(data['profile']['algorithm'])
		self.delay = int(data['profile']['tradingDelayBars'])
		self.profitPctTrigger = float(data['profile']['profitPctTrigger'])
		self.profitPctTriggerBar = int(data['profile']['profitPctTriggerBar'])
		self.reversalPctTrigger = float(data['profile']['reversalPctTrigger'])
		self.volumeRangeBars = int(data['profile']['volumeRangeBars'])
		self.amountPct = float(data['profile']['amountPct'])
		self.aggressiveOpen = int(data['profile']['aggressiveOpen'])
		self.aggressiveClose = int(data['profile']['aggressiveClose'])
		self.aggressiveOpenPct = float(data['profile']['aggressiveOpenPct'])
		self.aggressiveClosePct = float(data['profile']['aggressiveClosePct'])
		self.rangeTrade = int(data['profile']['rangeTrade'])
		self.rangeTradeBars = int(data['profile']['rangeTradeBars'])
		self.currency = str(data['profile']['currency'])
		self.alt = str(data['profile']['alt'])
		self.openBars = int(data['profile']['openBars'])
		self.closeBars = int(data['profile']['closeBars'])
		self.intraLowerHighsBars = int(data['profile']['intraLowerHighsBars'])
		self.intraHigherLowsBars = int(data['profile']['intraHigherLowsBars'])
		self.useIntras = int(data['profile']['useIntras'])
		self.reverseLogic = int(data['profile']['reverseLogic'])
		self.buyNearLow = int(data['profile']['buyNearLow'])
		self.sellNearHi = int(data['profile']['sellNearHi'])
		self.closePositionFudge = float(data['profile']['closePositionFudge'])
		self.shortTermTrendBars = int(data['profile']['shortTermTrendBars'])
		self.longTermTrendBars = int(data['profile']['longTermTrendBars'])
		self.waitForNextBar = int(data['profile']['waitForNextBar'])
		self.endTradingTime = float(data['profile']['endTradingTime'])
		self.profitPctTriggerAmt = float(data['profile']['profitPctTriggerAmt'])
		self.intraHigherHighsBars = float(data['profile']['intraHigherHighsBars'])
		self.intraLowerLowsBars = float(data['profile']['intraLowerLowsBars'])
		
		self.position = "closed"
		self.positionType = 0
		self.positionPrice = 0.0
		self.stopLoss = 0.0
		self.stopGain = 0.0
		self.initialStopGain = 0.0
		self.initialStopLoss = 0.0
		self.hiOpenCloseLimit = 0.0
		self.loOpenCloseLimit = 0.0
		
		self.hi = 0
		self.lo = 1
		self.open = 2
		self.close = 3
		self.volume = 4
		
		self.buy = 1
		self.sell = 2
		self.triggerBars = self.openBars
		self.dirty = False
		self.currentBar = 0
		self.nextBar = 0
		self.rangeTradeValue = False
		self.rangeHi = 0.0
		self.rangeLo = 0.0
		self.printDirty = False
		
		self.intraHigherHigh = 0.0
		self.intraHigherLows = 0.0
		self.intraHiValues = [0.0]	
		self.intraLowValues = [0.0]	

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def ready(self, currentNumBars):
	
		if self.rangeTrade and self.rangeTradeBars > self.delay:
			self.delay = self.rangeTradeBars
		if self.delay < currentNumBars:
			return True
		else:
			return False
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setClosePrices(self, currentPrice):
	
		posOut = 0.0
		
		if self.positionType == self.buy:
			posOut = self.loOpenCloseLimit - self.closePositionFudge
		elif self.positionType == self.sell:
			posOut = self.hiOpenCloseLimit + self.closePositionFudge

		self.stopGain = self.stopLoss = posOut
		
		return
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setInitialClosePrices(self, currentPrice):
		
		# Only set initial close prices once per transaction
		if self.dirty:
			return
			
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
		
		self.dirty = True
		
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

		if self.rangeTrade:
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
	
		if self.rangeTrade:
			if float(currentPrice) <= (self.rangeHi) and float(currentPrice) >= float(self.rangeLo):
				
				print ("in range between " + str(self.rangeHi) +	" and " + str(self.rangeLo))

				return True

		return False
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def openPosition(self, buyOrSell, price):

		self.positionType = buyOrSell
		self.position = "open"
		self.positionPrice = price
		self.triggerBars = self.closeBars
		self.setInitialClosePrices(price)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def closePosition(self):

		self.positionType = 0
		#self.initialStopGain = 0.0
		#self.initialStopLoss = 0.0
		self.dirty = False
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

		if len(barChart) < self.rangeTradeBars:
			return
			
		if self.rangeTrade:
			self.rangeHi = self.getHighestCloseOpenPrice(self.rangeTradeBars, barChart)
			self.rangeLo = self.getLowestCloseOpenPrice(self.rangeTradeBars, barChart)
			
		return

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def takeAction(self, currentPrice, barChart):
		barChart = barChart
								
		action = self.algorithm(currentPrice, self.triggerBars, barChart)

		return action

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def algorithm(self, currentPrice, bars, barChart):
		returnVal = 0

		# Compare the current price to the previous n bars to determine action.
		# Action is either buy or sell.
		# Action triggered if current price is < or > lowest/highest close/open
		# range set from the passed in json profile. 

		# Get the hi low price of the combined bars
		#if not self.aggressiveOpen and not self.aggressiveClose: 
			#hiOpenCloseLimit = self.highestCloseOpenPrice(bars, barChart)
			#self.loOpenCloseLimit = self.lowestCloseOpenPrice(bars, barChart)
									
			#self.hiOpenCloseLimit = self.getHighestCloseOpenPrice(bars, barChart)
			#self.loOpenCloseLimit = self.getLowestCloseOpenPrice(bars, barChart)
									
		# Get the highest open and lowest low price of the combined bars
		#elif self.aggressiveOpen and self.aggressiveClose: 
			#hiOpenCloseLimit = self.highestOpenPrice(bars, barChart)
			#self.loOpenCloseLimit = self.lowestClosePrice(bars, barChart)
			
			#self.hiOpenCloseLimit = self.getHighestCloseOpenPrice(bars, barChart)
			#self.loOpenCloseLimit = self.getLowestCloseOpenPrice(bars, barChart)

		if self.useIntras:
			intraLowerHighs = intraHigherLows = 0
			intraLowerLows = intraHigherHighs = 0
			intraBuy = intraSell = False
			
			intraHigherHighs = self.getIntraHigherHighs()
			intraLowerLows = self.getIntraLowerLows()
			intraLowerHighs = self.getIntraLowerHighs()
			intraHigherLows = self.getIntraHigherLows()
					
			if intraHigherLows and not intraLowerHighs:
				intraBuy = True
			if intraLowerHighs and not intraHigherLows:
				intraSell = True
					
			if currentPrice > self.hiOpenCloseLimit and intraBuy:
				return 1
			if currentPrice < self.loOpenCloseLimit and intraSell:
				return 2
		
		if currentPrice > self.hiOpenCloseLimit:
			return 1
		if currentPrice < self.loOpenCloseLimit:
			return 2

		return returnVal
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getLowestCloseOpenPrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2
		
		if len(barChart) - 2 <= self.closeBars:
			return
		if len(barChart) - 2 <=	self.openBars:
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
			n = 0
			
			if len(barChart) - 2 <= self.intraLowerHighsBars:
				return
			if len(barChart) - 2 <=	self.intraHigherLowsBars:
				return
			
			self.intraHiValues = [0.0] * self.intraHigherLowsBars	
			self.intraLoValues = [0.0] * self.intraLowerHighsBars	
		
			barChartLen = len(barChart) - 2
	
			while n < self.intraHigherLowsBars:
				self.intraLoValues[n] = barChart[barChartLen - n][self.lo]
				n += 1
			n = 0
			while n < self.intraLowerHighsBars:
				self.intraHiValues[n] = barChart[barChartLen - n][self.hi]
				n += 1
		return

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setOpenCloseLimits(self, barChart):
	
		#print ("triggerBars: " + str(self.triggerBars)
		if not self.aggressiveOpen and not self.aggressiveClose: 
			self.hiOpenCloseLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			self.loOpenCloseLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
		elif self.aggressiveOpen and self.aggressiveClose: 
			self.hiOpenCloseLimit = self.getHighestCloseOpenPrice(self.triggerBars, barChart)
			self.loOpenCloseLimit = self.getLowestCloseOpenPrice(self.triggerBars, barChart)
			
		return

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setLoLimits(self, barChart):
	
		self.loOpenCloseLimit = self.getLowestCloseOpenPrice(self.openBars, barChart)

		return

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraHigherHighs(self):	
		n = 0
		lowest = self.intraLoValues[0]
		
		while n < self.intraHigherLowsBars:
			lo = self.intraHiValues[n]
			if lo < lowest:
				return False
			n += 1
		return True
 		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraLowerLows(self):	
		n = 0
		lowest = self.intraLoValues[0]
		
		while n < self.intraHigherLowsBars:
			lo = self.intraHiValues[n]
			if lo < lowest:
				return False
			n += 1
		return True
 		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraLowerHighs(self):	
		n = 0
		highest = self.intraHiValues[0]
		
		while n < self.intraLowerHighsBars:
			hi = self.intraHiValues[n]
			if hi > highest:
				return False
			n += 1
		return True
 		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraHigherLows(self):	
		n = 0
		lowest = self.intraLoValues[0]
		
		while n < self.intraHigherLowsBars:
			lo = self.intraLoValues[n]
			if lo > lowest:
				return False
			n += 1
		return True
 				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getHighestCloseOpenPrice(self, numBars, barChart):
		n = 0
		maxPriceArr = [0.0] * numBars	
		barChartLen = len(barChart) - 2
		
		if len(barChart) - 2 <= self.closeBars:
			return
		if len(barChart) - 2 <=	self.openBars:
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
	def lowestClosePrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

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
	def highestClosePrice(self, numBars, barChart):
		n = 0
		maxPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

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
	def lowestOpenPrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

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
	def highestOpenPrice(self, numBars, barChart):
		n = 0
		maxPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

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
	def lowestIntraBarPrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

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
	def highestIntraBarPrice(self, numBars, barChart):
		n = 0
		maxPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

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
	def lowestHiLoIntraBarPrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

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
		n = 0
		maxPriceArr = [0.0] * numBars	
		barChartLen = len(barChart) - 2
	
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
