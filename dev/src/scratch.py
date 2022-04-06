# Scratch 

	def setShortTrend(self, trendType, barChart, currentPrice):

		if self.shortTermTrendBars == 0:
			return
	
		self.shortTermTrend = 0.0
		barChartLen = len(barChart) - 1
		
		if barChartLen <= self.shortTermTrendBars:
			return
			
		shortTrendBarLen = barChartLen - self.shortTermTrendBars
		
		setTrendValues(trendType, barChart, barChartLen, shortTrendBarLen, currentPrice)
		
	def setMidTrend(self, trendType, barChart, currentPrice):
		if self.midTermTrendBars == 0:
			return
	
		self.midTermTrend = 0.0
		barChartLen = len(barChart) - 1
		
		if barChartLen <= self.midTermTrendBars:
			return
			
		midTrendBarLen = barChartLen - self.midTermTrendBars
		
		setTrendValues(trendType, barChart, barChartLen, midTrendBarLen, currentPrice)
		
	def setLongTrend(self, trendType, barChart, currentPrice):
		if self.longTermTrendBars == 0:
			return
	
		self.longTermTrend = 0.0
					
		barChartLen = len(barChart) - 1
		if barChartLen <= self.longTermTrendBars:
			return
			
		longTrendBarLen = barChartLen - self.longTermTrendBars
		
		setTrendValues(trendType, barChart, barChartLen, longTrendBarLen, currentPrice)
		
	def setTrendValues(trendType, barChart, barChartLen, i, currentPrice):
	
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
			trend = 2.0

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
			self.shortTermTrend = trend
		elif trendType == "mid":
			self.midTermTrend = trend
		elif trendType == "long":
			self.longTermTrend = trend

		#self.shortTermTrend += pctInTrendRnd

		print(trendType + "TermTrend: " + str(trend))
		print("loBarPosition: " + str(loBarPosition))
		print("hiBarPosition: " + str(hiBarPosition))
		print("highest: " + str(highest))
		print("lowest: " + str(lowest))
		print("range: " + str(range))
		print("penetration: " + str(penetration))
		print("pctInTrend: " + str(pctInTrend))
		print("pctInTrendRnd: " + str(pctInTrendRnd) + "\n")

		
		# ORIGINAL CODE.....
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
			
		
