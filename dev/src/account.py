import json
from trade_interface import TradeInterface

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Account:

   def __init__(self, d):
   
      self.sandConsumerKey = str(d["profileConnectET"]["sandConsumerKey"])
      self.sandConsumerSecret = str(d["profileConnectET"]["sandConsumerSecret"])
      self.consumerKey = str(d["profileConnectET"]["consumerKey"])
      self.consumerSecret = str(d["profileConnectET"]["consumerSecret"])
      self.oauthKeysPath = str(d["profileConnectET"]["oauthKeysPath"])
      self.marketDataType = str(d["profileConnectET"]["marketDataType"])
      self.offLine = int(d["profileConnectET"]["offLine"])
      self.browserPath = str(d["profileConnectET"]["browser_path_Darwin"])

      self.sandBox = False
      #self.debug = debug
      
      accountDict = {}
      accountDict['consumer_key'] = consumerKey
      accountDict['consumer_secret'] = consumerSecret
      accountKeys = {'production': accountDict}

      if sandBox:
         accountDict['consumer_key'] = consumerKey
         accountDict['consumer_secret'] = consumerSecret
         accountKeys = {'sandbox': accountDict}

      self.ti = TradeInterface(accountKeys, self.sandBox, self.browserPath) 

   def getAccount():
      pass

   def getCurrentPrice(stock):
      #acct.get_current_price(stock) -> float:
      pass

   def checkOrderStatus():
      #acct.check_order_status(self, order_id: int) -> Optional[str]:
      pass

   def listPositions(stock):
      #acct.list_positions(self) -> List[Tuple[str, float, float, float]]:
      pass

   def placeLimitOrder(stock):
      #acct.place_limit_order(self,
#                          action: str,
#                          symbol: str,
#                          quantity: int,
#                          limit_price: float,
#                          session: str,
#                          prev_order_id: Optional[int],
#                          order_term: str = 'GOOD_UNTIL_CANCEL') -> Tuple[int, str]:
      pass
    
   def placeStopOrder():
#     acct.place_stop_order(self,
#                         action: str,
#                         symbol: str,
#                         quantity: int,
#                         stop_price: float,
#                         session: str,
#                         prev_order_id: int,
#                         order_term: str = 'GOOD_UNTIL_CANCEL') -> Tuple[int, str]:

#    def place_stop_order(self,
      pass


   def getAccountBalance():
      #acct.get_account_balance()
      pass
   
   def getAccounttPositions():
      #acct.get_account_positions()
      pass

   def cancelOrder():
      #acct.cancel_order(self, order_id: int) -> str:
      pass
   
   