# Library for connection to API's

import bitstamp.client
from log import *
from time import sleep
import traceback
#from bitfinex.client import Client

class ConnectBitFinex:
	def __init__(self, service="bitstamp"):
		self.service = service

		self.clientBFX = Client()

		#symbols = client.symbols()
		#print(symbols)

		symbol = 'btcusd'

		#print(self.clientBFX.ticker(symbol))
		#print(client.today(symbol))
		#print(client.stats(symbol))

		#parameters = {'limit_asks': 2, 'limit_bids': 2}

		#print(client.lendbook('btc', parameters))
		#print(client.order_book(symbol, parameters))

	def getCurrentPrice(self, currency="btc", alt="usd"):
		symbol = currency + alt
		mid = self.clientBFX.ticker(symbol)["mid"]
		return mid


# Connect to API service providers: bit stamp kraken etrade ibkr lakebtc

class ConnectBitStamp:
	def __init__(self, service="bitstamp"):
		self.service = service
		
	def connectPublic(self):	
		# bitstamp client
		#
		# currencies: btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, 
		#		 ltceur, ltcbtc, ethusd, etheur, ethbtc, bchusd, bcheur, bchbtc

		self.publicClient = bitstamp.client.Public()
		return (self.publicClient)
		# publicClient = connection.connect(service)
		
	def connectPrivate(self):	
		# TODO
		self.privateClient = ""
		return (self.privateClient)
		
	def getVolume(self, currency="btc", alt="usd"):	
		vol = 0.0
		while True:
			try:
				vol = float(self.publicClient.ticker(currency, alt)['volume'])
			except:
				#print("Caught exception in getVolume for bitstamp. Retrying...")
				sleep(2)
				continue
			break
			
		return (vol)
			
	def getCurrentPrice(self, currency="btc", alt="usd"):		
		cp = 0.0
		ctr = 0
		while True:
			ctr += 1
			try:
				cp = float(self.publicClient.ticker(currency, alt)['last'])
			except:
				#print("Caught exception in getCurrentPrice for bitstamp. Retrying...")
				#sleep(1)
				print(traceback.format_exc())
				continue
			break
			
		return (cp)
			
	def getTimeStamp(self, currency="btc", alt="usd"): 
		stamp = 0.0
		while True:
			try:
				stamp = float(self.publicClient.ticker(currency, alt)['timestamp'])
			except:
				#print ("Caught exception in getCurrentPrice for bitstamp. Retrying...")		
				sleep(2)
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
