'''
Algorithms module
'''

class Algorithm:
  def __init__(self, data):
    self.algorithm = data['profile']['algorithm']
    self.delay = data['profile']['tradingDelayBars']
    self.profitPctTrigger = data['profile']['profitPctTrigger']
    self.profitPctTriggerBar = data['profile']['profitPctTriggerBar']
    self.reversalPctTrigger = data['profile']['reversalPctTrigger']
    self.volumeRangeBars = data['profile']['volumeRangeBars']
    self.amountPct = data['profile']['amountPct']
    self.aggressiveOpen = data['profile']['aggressiveOpen']
    self.aggressiveClose = data['profile']['aggressiveClose']
    self.aggressiveOpenPct = data['profile']['aggressiveOpenPct']
    self.aggressiveClosePct = data['profile']['aggressiveClosePct']
    self.rangeTrade = data['profile']['rangeTrade']
    
  def ready(self, currentNumBars):
    if int(self.delay) < currentNumBars:
      return True
    else:
      return False
        
  # Method to determine if a position should be taken
  def takeAction(self, currentPrice, barColumn, barChart):
    self.barChart = barChart
    twobo1bc = TwoBarOpen1BarClose(2, barChart)
    #fivebo5bc = FiveBarOpen5BarClose(5)
    #fivebo2bc = FiveBarOpen2BarClose(5)
    
    if self.algorithm == "2BarOpen1BarClose":
      self.action = twobo1bc.algorithm(currentPrice, barColumn)
    '''if self.algorithm == "5BarOpen5BarClose":
      self.action = fivebo5bc.algorithm(currentPrice, barColumn)
    if self.algorithm == "5BarOpen2BarClose":
      self.action = fivebo2bc.algorithm(currentPrice,barColumn)
    '''
    return 1

class TwoBarOpen1BarClose(Algorithm):
  def __init__(self, numBars, barChart):
    self.hi = 0
    self.lo = 1
    self.op = 2
    self.cl = 3
    self.volume = 4
    self.numBars = numBars
    self.barChart = barChart
    
  def algorithm(self, currentPrice, column):
    returnVal = None

    # Compare the current price to the previous 2 bars.
    # Action triggered if current price is < or > lowest/highest close/open
    
    # Get the price of the combined bars
    previousHigh = self.highestCloseOpenPrice(column)
    previousLow = self.lowestCloseOpenPrice(column)

    if currentPrice >= previousHigh:
      return "buy"
    if currentPrice <= previousLow:
      return "sell"
      
    return returnVal
    
  def highestCloseOpenPrice(self, column):
    n = 1
    maxPriceArr = []
    while n <= self.numBars:
      open = self.barChart[column - n][self.op]
      close = self.barChart[column - n][self.cl]
   
      maxPriceArr[n] = open
      if close > open:
        maxPriceArr[n] = close
      n += 1
    # End while
    
    # Compare all max prices and find the highest price
    clean = True
    n = 1
    while n <= self.numBars:
      if clean:
        maxPrice = maxPrice[n]
        clean = False
        
      if maxPriceArr[n+1] > maxPrice:
        maxPrice = maxPriceArr[n+1]
        
      n += 1
    return maxPrice
      
  def lowestCloseOpenPrice(self, column):
    n = 1
    minPriceArr = []
    while n <= self.numBars:
      open = self.barChart[column - n][2]
      close = self.barChart[column - n][3]
   
      minPriceArr[n] = open
      if close > open:
        minPriceArr[n] = close
      n += 1
    # End while
    
    # Compare all max prices and find the highest price
    clean = True
    n = 1
    while n <= self.numBars:
      if clean:
        minPrice = minPrice[n]
        clean = False
        
      if minPriceArr[n+1] < minPrice:
        minPrice = minPriceArr[n+1]
        
      n += 1
      
    return minPrice
            
  
