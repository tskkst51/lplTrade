# Log class

class Log:
	def __init__(self):
		print ("\n")
		self.totGain = 0.0
		self.lossGain = 0.0
		
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
		self.hdr =		 "SYM   OPEN    TIME CLOSE TREND GAIN/(LOSS) TOTAL $"
		self.hdrLine = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		return ("\n" + date + "\n" + self.hdr + "\n" + self.hdrLine + "\n")
		
	def execution(self, ticker, closed, time):
		self.ticker = ticker
		self.closed = closed
		self.time = time
		print ("SUCCESS: " + self.msg)
		
	def logIt(self, symbol, action, price, time, logPath):
		
		if action == 1:
			strAction = "buy"
			self.priceSet = float(price)
		elif action == 2:
			strAction = "sell"
			self.priceSet = float(price)
		else:
			strAction = "close"
			self.totGain = float(self.priceSet) - float(price)
			if action > 1:
				#self.totGain = "-" + str(self.totGain)
				self.totGain = self.totGain*-1
				print (str(self.totGain) + str(self.totGain*-1))
			elif action == 2:
				if self.totGain < 0:
					self.totGain = self.totGain * -1
				
			self.priceSet = 0.0

		truncTotGain = format(self.totGain, '.2f')
		
		with open(logPath, "a+", encoding="utf-8") as logFile:
			logFile.write (str(symbol) + " " +
				strAction + " " + str(price) + " " + str(time) + " " + str(truncTotGain)  + "\n")
		
		self.totGain = 0.0
		return 1

# end Log
