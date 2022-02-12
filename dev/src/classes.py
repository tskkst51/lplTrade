'''
Classes module
'''
from time import strftime, gmtime, sleep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Time:

	def __init__(self):
		tm = ""
		
	def now(self):
		self.tm = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
		return (self.tm)
		
	def waitUntilTopMinute(self):
		secs = strftime("%S", gmtime())
		waitSecs = 60 - int(secs)
		print ("Waiting: " + str(waitSecs) + " seconds to start trading!! ...")
		while True:
			secs = strftime("%S", gmtime())
			if str(secs) == "00":
				break
			sleep(1)
		
		return
		
#end Time

class Price:
	def __init__(self, numBars, endTime=None):
		self.numBars = numBars
		self.endTime = endTime
	def load(self):
		print (self.numBars)
		print (self.endTime)
	def evaluatePrice(self):
		print (self.numbars)
		
#end Price

class Trade:
	def __init__(self, numBars, endTime=None):
		self.sellTime = 0
		self.sellDate = 0
		self.sellPrice = 0
	def load(self):
		print (self.numBars)
		print (self.endTime)
	def evaluatePrice(self):
		print (self.numbars)
		
#end Price

