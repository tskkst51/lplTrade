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
		
	def trigger(self, symbol, action, price, time, logPath):
		
		if action == 1:
			strAction = "buy"
			self.lossGain = float(price)
		elif action == 2:
			strAction = "sell"
			self.lossGain = float(price)
		else:
			strAction = "close"
			self.totGain = float(self.lossGain) - float(price)
			self.lossGain = 0

		with open(logPath, "a+", encoding="utf-8") as logFile:
			logFile.write (str(symbol) + " " +
				strAction + " " + str(price) + " " + str(time) + " " + str(self.totGain)  + "\n")
		
		return 1

# end Log
