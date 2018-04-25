'''
Algorithms module
'''
import io

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Algorithm(object):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def __init__(self, data):
		# self.algorithm = data['profile']['algorithm']
		self.delay = int(data['profile']['tradingDelayBars'])
		self.profitPctTrigger = float(data['profile']['profitPctTrigger'])
		self.profitPctTriggerBar = int(data['profile']['profitPctTriggerBar'])
		self.reversalPctTrigger = float(data['profile']['reversalPctTrigger'])
		self.volumeRangeBars = int(data['profile']['volumeRangeBars'])
		self.amountPct = float(data['profile']['amountPct'])
		self.aggressiveOpen = data['profile']['aggressiveOpen']
		self.aggressiveClose = data['profile']['aggressiveClose']
		self.aggressiveOpenPct = float(data['profile']['aggressiveOpenPct'])
		self.aggressiveClosePct = float(data['profile']['aggressiveClosePct'])
		self.rangeTrade = data['profile']['rangeTrade']
		self.currency = str(data['profile']['currency'])
		self.alt = str(data['profile']['alt'])
		self.openBars = int(data['profile']['openBars'])
		self.closeBars = int(data['profile']['closeBars'])
		
		self.position = "closed"
		self.positionPrice = 0.0
		self.type = 0
		self.stopLoss = 0.0
		self.stopGain = 0.0
		self.previousHigh = 0.0
		self.previousLow = 0.0
		self.hi = 0
		self.lo = 1
		self.buy = 1
		self.sell = 2
		self.open = 2
		self.close = 3
		self.volume = 4
		self.triggerBars = self.openBars
		self.notInPosition = True
		self.nextBar = 0
		self.positionType = 0
		self.currentBar = 0
		self.initialStopGain = 0.0
		self.initialStopLoss = 0.0
		self.dirty = False

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
	
		if self.positionType == self.buy:
			posOut = self.previousLow
		elif self.positionType == self.sell:
			posOut = self.previousHigh

		self.stopGain = posOut
		self.stopLoss = posOut

		return
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setInitialClosePrices(self, currentPrice):
				
		if self.dirty:
			return
			
		hiLoDiff = self.previousHigh - self.previousLow
		
		print ("Hi Lo diff: " + str(hiLoDiff))
		print ("position type: " + str(self.positionType))
		
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
	def getProfitPctTriggerBar(self):

		return self.profitPctTriggerBar
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def openPosition(self, buyOrSell, price):

		self.positionType = buyOrSell
		self.position = "open"
		self.positionPrice = price
		self.triggerBars = self.closeBars
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def closePosition(self):

		self.positionType = 0
		self.initialStopGain = 0.0
		self.initialStopLoss = 0.0
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
	def getPositionType(self):

		return self.positionType
		
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
	def notInPosition(self):

		self.notInPosition = False
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getNotInPosition(self):

		return self.notInPosition

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setNotInPosition(self):

		self.notInPosition

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setNextBar(self, bar):

		self.nextBar = bar

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def getNextBar(self):

		return self.nextBar

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def algorithm(self, currentPrice, bars, barChart):
		returnVal = 0

		# Compare the current price to the previous n bars.
		# Action triggered if current price is < or > lowest/highest close/open

		# Get the price of the combined bars
		self.previousHigh = self.highestCloseOpenPrice(bars, barChart)
		self.previousLow = self.lowestCloseOpenPrice(bars, barChart)
			  
		#print ("Highest hi: " + str(self.previousHigh))
		#print ("Lowest lo: " + str(self.previousLow))
		#print ("currentPrice: " + str(currentPrice))
		
		if currentPrice > self.previousHigh:
			return 1
			
		if currentPrice < self.previousLow:
			return 2

		return returnVal
				
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
		return float(maxPrice)
		
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def lowestCloseOpenPrice(self, numBars, barChart):
		n = 0
		minPriceArr = [0.0] * numBars
		barChartLen = len(barChart) - 2

		while n < numBars:
			open = barChart[barChartLen - n][self.open]
			close = barChart[barChartLen - n][self.close]
 
			minPriceArr[n] = open
			if close < open:
				minPriceArr[n] = close
			n += 1
		# End while
			
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
						
	
