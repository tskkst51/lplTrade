import pyetrade
import os
import io
import time
import json
from optparse import OptionParser

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse Command Line Options

parser = OptionParser()

parser.add_option("-c"	, "--profileConnectPath", dest="profileConnectPath",
	help="write report to FILE", metavar="FILE")

(clOptions, args) = parser.parse_args()

print ("Getting connection profile from :" + clOptions.profileConnectPath + "\n")

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

# Set the proper consumer keys, sandbox or live
live = True
if c["profileConnectET"]["live"] == "False":
   live = False

if not live:
   consumerKey = sandConsumerKey
   consumerSecret = sandConsumerSecret

print ("Live account: " + str(live))

oauth = pyetrade.ETradeOAuth(consumerKey, consumerSecret)

# Use the printed URL
URL = oauth.get_request_token()

#os.system('open -a safari ' + URL)

print("\n" + URL + "\n")

verifierCode = input("Enter verification code: ")
tokens = oauth.get_access_token(verifierCode)

print ("\nconsumerKey:" + consumerKey)
print ("consumerSecret:" + consumerSecret)
print(tokens)

with open(oauthKeysPath, 'w') as writer:
   writer.write(tokens['oauth_token'] + "\n")
   writer.write(tokens['oauth_token_secret'] + "\n")

exit()
