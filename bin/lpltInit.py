import pyetrade
import os
import io
import time
import json
import platform
from optparse import OptionParser
from trade_interface import TradeInterface

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

parser = OptionParser()

parser.add_option("-c"	, "--profileConnectPath", dest="profileConnectPath",
	help="write report to FILE", metavar="FILE")
	
parser.add_option("-b", "--sandBox",
   action="store_true", dest="sandBox", help="sandBox connection type")

parser.add_option("-a", "--autoConnect",
   action="store_true", dest="autoConnect", help="use Tradeinterface to connect automatically")

(clOptions, args) = parser.parse_args()

print ("Getting connection profile from : " + clOptions.profileConnectPath + "\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load profile data

with open(clOptions.profileConnectPath) as jsonData:
	c = json.load(jsonData)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set profile data

sandConsumerKey = str(c["profileConnectET"]["sandConsumerKey"])
sandConsumerSecret = str(c["profileConnectET"]["sandConsumerSecret"])
consumerKey = str(c["profileConnectET"]["consumerKey"])
consumerSecret = str(c["profileConnectET"]["consumerSecret"])
oauthKeysPath = str(c["profileConnectET"]["oauthKeysPath"])
sandBox = int(c["profileConnectET"]["sandBox"])
browserPath = str(c["profileConnectET"]["browser_path_Darwin"])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overide profileTradeData data with command line data

# Create proper dict to send to the TradeINterface API
accountDict = {}
accountDict['consumer_key'] = consumerKey
accountDict['consumer_secret'] = consumerSecret
accountKeys = {'production': accountDict}

if clOptions.sandBox:
   sandBox = 1

# Set the proper consumer keys, sandbox or live
if sandBox:
   consumerKey = sandConsumerKey
   consumerSecret = sandConsumerSecret
   accountDict['consumer_key'] = consumerKey
   accountDict['consumer_secret'] = consumerSecret
   accountKeys = {'sandbox': accountDict}
   print ("Sandbox account is true: " + str(sandBox))
else:
   print ("Live account: Sandbox value: " + str(sandBox))

if clOptions.autoConnect:
   print ("browserPath " + str(browserPath))

   ti = TradeInterface(accountKeys, False, browserPath) 

   # Try to reconnect using saved tokens

   with open(oauthKeysPath, 'r') as reader:
      oaLines = reader.readlines()

   oauth_token = oaLines[0].replace("\n", "")
   oauth_token_secret = oaLines[1].replace("\n", "")
   
   staticTokens = {}
   staticTokens['oauth_token'] = oauth_token
   staticTokens['oauth_token_secret'] = oauth_token_secret
   
   print("staticTokens: " + str(staticTokens))

   tokens = {}   
   if not ti.reconnect(staticTokens):   
      tokens = ti.connect() 
      with open(oauthKeysPath, 'w') as writer:
         writer.write(tokens['oauth_token'] + "\n")
         writer.write(tokens['oauth_token_secret'] + "\n")
   
      print("Generated token/secret:")
      print(tokens['oauth_token'])
      print(tokens['oauth_token_secret'])
   else:
      print("Static token/secret:")
      print(staticTokens['oauth_token'])
      print(staticTokens['oauth_token_secret'])

   # To choose which account to trade uncomment below line
   #ti.select_account()
   ti.select_daytrade_account()
   cash, margin = ti.get_account_balance()
   print ("cash " + str(cash))
   print ("margin " + str(margin))
   
   print ("TQQQ price " + str(ti.get_current_price("TQQQ")))

else:
   oauth = pyetrade.ETradeOAuth(consumerKey, consumerSecret)
   
   # Use the printed URL
   URL = oauth.get_request_token()
   
   #os.system('open -a safari ' + URL)
   
   print("\n" + URL + "\n")
   
   verifierCode = input("Enter verification code: ")
   tokens = oauth.get_access_token(verifierCode)
   
   print("Generated token/secret:")
   print(tokens['oauth_token'])
   print(tokens['oauth_token_secret'])
   
   with open(oauthKeysPath, 'w') as writer:
      writer.write(tokens['oauth_token'] + "\n")
      writer.write(tokens['oauth_token_secret'] + "\n")

exit(0)
