# Log class

class Log:
	def __init__(self):
		print ("\n")
		self.totGain = 0.0
		self.grandTotal = 0.0
		self.strAction = ""
		
	def debug(self, msg):
		self.msg = msg
		print ("DEBUG: " + self.msg)
		
	def error(self, msg):
		self.msg = msg
		print ("ERROR: " + self.msg)
		
	def warning(self, msg):
		self.msg = msg
		print ("WARNING: " + self.msg)
		
	def info(self, msg):
		self.msg = msg
		print ("INFO: " + self.msg)
		
	def msg(self, msg):
		self.msg = msg
		print (self.msg)
		
	def success(self, msg):
		self.msg = msg
		print ("SUCCESS: " + self.msg)
		
	def header(self, date):
		self.hdr =		 "ACTION OPEN GAIN/(LOSS)	TOTAL BARSINPOS	TIME"
		self.hdrLine = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		return ("\n" + date + "\n" + self.hdr + "\n" + self.hdrLine + "\n")
		
	def infoStamp(self, service, sym, chartType, openBars, closeBars):
		self.hdr = "Ex: " + service + " SYM: " + sym + " Bar chart (min): " + str(chartType) + " Open bars: " + str(openBars) + " Clase Bars: " + str(closeBars)
		return ("\n" + self.hdr)
		
	def execution(self, ticker, closed, time):
		self.ticker = ticker
		self.closed = closed
		self.time = time
		print ("SUCCESS: " + self.msg)
		
	def logIt(self, action, price, barLength, time, logPath):
		totGain = grandTotal = ""
		if action == 1:
			self.strAction = "buy"
			self.priceSet = float(price)
		elif action == 2:
			self.strAction = "sell"
			self.priceSet = float(price)

		else:
			self.totGain = float(self.priceSet) - float(price)
			if self.strAction == "buy":
				#if self.totGain < 0:
				self.totGain = self.totGain*-1
			#elif self.strAction == "sell":
				#if self.totGain < 0:
				#self.totGain = self.totGain*-1
					
			self.strAction = "close"
			self.priceSet = 0.0
			self.grandTotal += self.totGain

			totGain = format(self.totGain, '.2f')
			grandTotal = format(self.grandTotal, '.2f')

		if self.strAction == "close":
			with open(logPath, "a+", encoding="utf-8") as logFile:
				logFile.write (
					self.strAction + "	" + str(price) + " " + str(totGain) + " " + str(grandTotal)	 + "		" + str(barLength) + "   " + str(time) + "\n")
		else:
			with open(logPath, "a+", encoding="utf-8") as logFile:
				logFile.write (
					self.strAction + " " + str(price) + "							  		" + str(time) + "\n")
		
		self.totGain = 0.0
		return 1

# end Log
