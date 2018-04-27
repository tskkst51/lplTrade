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
			
		self.position = "closed"
		self.positionType = 0
		self.positionPrice = 0.0
		self.stopLoss = 0.0
		self.stopGain = 0.0
		self.initialStopGain = 0.0
		self.initialStopLoss = 0.0
		self.previousHigh = 0.0
		self.previousLow = 0.0
		
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def ready(self, currentNumBars):
		if self.delay < currentNumBars:
			return True
		else:
			return False
				
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def takeAction(self, currentPrice, barChart):
		barChart = barChart
				
		action = self.algorithm(currentPrice, self.triggerBars, barChart)

		return action
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setClosePrices(self, currentPrice):
	
		posOut = 0.0
		
		if self.positionType == self.buy:
			posOut = self.previousLow
		elif self.positionType == self.sell:
			posOut = self.previousHigh

		self.stopGain = self.stopLoss = posOut
		
		return
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setInitialClosePrices(self, currentPrice):
		
		# Only set initial close prices once per transaction
		if self.dirty:
			return
			
		hiLoDiff = self.previousHigh - self.previousLow
		
		print ("Hi Lo diff: " + str(hiLoDiff) + "\n")
		
		if self.positionType == self.buy:
			posGain = float(currentPrice) + (float(hiLoDiff) * float(self.profitPctTriggerBar))
			posLoss = self.previousLow
		elif self.positionType == self.sell:
			posGain = float(currentPrice) - (float(hiLoDiff) * float(self.profitPctTriggerBar)) 
			posLoss = self.previousHigh

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
	def getInRangeTrade(self):
	
		print ("self.rangeTrade " + str(self.rangeTrade))
		if self.rangeTrade:
			return self.rangeTradeValue
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getOpenBars(self):
	
		return self.openBars
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getCloseBars(self):
	
		return self.closeBars
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getReverseLogic(self):
	
		return self.reverseLogic
				
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def inRangeTrade(self, currentPrice, rangeHi, rangeLo):
	
		self.rangeTradeValue = False
		
		if self.rangeTrade:
			print ("inRangeTrade: " + str(rangeHi) + " wiatTilNextBar: " + str(rangeLo) + "\n")
			if float(currentPrice) <= (float(rangeHi) or float(currentPrice) >= float(rangeLo)):
				print ("yes\n")
				self.rangeTradeValue = True

		return self.rangeTradeValue
				
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
	def algorithm(self, currentPrice, bars, barChart):
		returnVal = 0

		# Compare the current price to the previous n bars.
		# Action triggered if current price is < or > lowest/highest close/open
		
		intraLowerHighs = intraHigherLows = 0
		
		# Get the hi low price of the combined bars
		if not self.aggressiveOpen and not self.aggressiveClose: 
			self.previousHigh = self.highestCloseOpenPrice(bars, barChart)
			self.previousLow = self.lowestCloseOpenPrice(bars, barChart)
									
		# Get the highest open and lowest low price of the combined bars
		elif self.aggressiveOpen and self.aggressiveClose: 
			self.previousHigh = self.highestOpenPrice(bars, barChart)
			self.previousLow = self.lowestClosePrice(bars, barChart)

		if self.inRangeTrade(currentPrice, self.highestCloseOpenPrice(self.rangeTradeBars, barChart), self.lowestCloseOpenPrice(self.rangeTradeBars, barChart)):
			print ("Not trading in range!!\n")
			return returnVal

		if self.useIntras:
			intraLowerHighs = self.getIntraLowerHighs(self.intraLowerHighsBars, barChart)
			intraHigherLows = self.getIntraHigherLows(self.intraHigherLowsBars, barChart)
			print ("True or false of Lower highs: " + str(intraLowerHighs))
			print ("True or false of Higher lows: " + str(intraHigherLows))

		#print ("\nHighest open/close hi: " + str(self.previousHigh))
		#print ("currentPrice: " + str(currentPrice))
		#print ("Lowest open/close lo: " + str(self.previousLow))
		#print ("")
		
		if self.useIntras:
			if currentPrice > self.previousHigh and intraHigherLows and not intraLowerHighs:
				return 1
			if currentPrice < self.previousLow and intraLowerHighs and not intraHigherLows:
				return 2
		else:
			if currentPrice > self.previousHigh:
				return 1
			if currentPrice < self.previousLow:
				return 2

		return returnVal
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def lowestCloseOpenPrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

		while n < numBars:
			assert (n >= 0)
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
	def getIntraHigherLows(self, numBars, barChart):

		n = numHigherLows = 0
		numHiLows = [0.0] * numBars	
		barChartLen = len(barChart) - 2
	
		while n < numBars:
			assert (n >= 0)
			lows = barChart[barChartLen - n][self.lo]
 
			numHiLows[n] = lows

			n += 1
			
		print ("Higher lows: " + str(numHiLows))
		
		# Compare all max prices and find the highest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				highest = numHiLows[n]
				clean = False
				continue
			
			if numHiLows[n] > highest:
				highest = numHiLows[n]
				numHigherLows += 1
			
			n += 1

		if numHigherLows + 1 == self.intraHigherLowsBars:
			print ("num of higher lows is TRUE!!!")
			return True
			
		return False
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getIntraLowerHighs(self, numBars, barChart):

		n = numLowerHighs = 0
		numHiLos = [0.0] * numBars	
		barChartLen = len(barChart) - 2
	
		while n < numBars:
			assert (n >= 0)
			hiLo = barChart[barChartLen - n][self.lo]
 
			numHiLos[n] = hiLo

			n += 1

		print ("Lower Highs: " + str(numHiLos))
		
		# Compare all max prices and find the highest price
		clean = True
		n = 0
		while n < numBars:
			if clean:
				highest = numHiLos[n]
				clean = False
				continue
			
			if numHiLos[n] < highest:
				highest = numHiLos[n]
				numLowerHighs += 1
			
			n += 1

		if numLowerHighs + 1 == self.intraLowerHighsBars:
			print ("num of lower highs is TRUE!!!")
			return True
			
		return False
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def highestCloseOpenPrice(self, numBars, barChart):
		n = 0
		maxPriceArr = [0.0] * numBars	
		barChartLen = len(barChart) - 2
	
		while n < numBars:
			assert (n >= 0)
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
			assert (n >= 0)
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
			assert (n >= 0)
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
			assert (n >= 0)
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
			assert (n >= 0)
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
			assert (n >= 0)
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
			assert (n >= 0)
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
			assert (n >= 0)
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
			assert (n >= 0)
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
