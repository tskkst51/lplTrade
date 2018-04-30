# Library for connection to API's

import bitstamp.client
from log import *
from time import sleep

# Connect to API service providers: bit stamp kraken etrade ibkr lakebtc

class Connect:
	def __init__(self, service="bitstamp"):
		self.service = service
		
	def connectPublic(self):	
		# bitstamp client
		#
		# currencies: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, 
		#		 ltceur, ltcbtc, ethusd, etheur, ethbtc, bchusd, bcheur, bchbtc

		if (self.service == "bitstamp"):
			self.publicClient = bitstamp.client.Public()
		return (self.publicClient)
		# publicClient = connection.connect(service)
		
	def connectPrivate(self):	
		# TODO
		if (self.service == "bitstamp"):
			self.privateClient = ""
		return (self.privateClient)
		
	def getVolume(self, currency="btc", alt="usd"):	
		vol = 0.0
		while True:
			try:
				if (self.service == "bitstamp"):
					vol = float(self.publicClient.ticker(currency, alt)['volume'])
			except:
				#print("Caught exception in getVolume for bitstamp. Retrying...")
				sleep(1)
				continue
			break
			
		return (vol)
			
	def getCurrentPrice(self, currency="btc", alt="usd"):		
		cp = 0.0
		while True:
			try:
				if (self.service == "bitstamp"):
					cp = float(self.publicClient.ticker(currency, alt)['last'])
			except:
				#print("Caught exception in getCurrentPrice for bitstamp. Retrying...")
				sleep(1)
				continue
			break
			
		return (cp)
			
	def getTimeStamp(self, currency="btc", alt="usd"): 
		stamp = 0.0
		while True:
			try:
				if (self.service == "bitstamp"):
					stamp = float(self.publicClient.ticker(currency, alt)['timestamp'])
			except:
				#print ("Caught exception in getCurrentPrice for bitstamp. Retrying...")		
				sleep(1)
				continue
			break
			
		return (stamp)
		
# pusher
# pusher = Pusher(
#	 app_id='511221',
#	 key='5e2e9920fc698e55daac',
#	 secret='ebd723b242a9aa35e0de',
#	 cluster='us2',
#	ssl=True
# )
# pusher.trigger('my-channel', 'my-event', {'message': 'hello world'})

#api = krakenex.API()
#k = KrakenAPI(api)
#ohlc, last = k.get_ohlc_data("BCHUSD")
#print(ohlc)
#tm = k.get_server_time()
#print (tm)
#ai = k.get_asset_info
#print (ai)
#print (k.get_tradable_asset_pairs(None))
#print (k.get_tradable_asset_pairs(None,"BCHUSD"))
#print (k.get_tradable_asset_pairs(None,"BTCUSD"))
