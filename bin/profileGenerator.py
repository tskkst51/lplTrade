## Take algo string and write a profile from it

# TB2_HS_IT_OB1_OS1_CB3_CS3

import json
from optparse import OptionParser
import lplTrade as lpl
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseCL():

   parser = OptionParser()
      
   parser.add_option("-d", "--day", type="string",
      action="store", dest="day", default=False,
      help="day: 1112202020 ")
   
   parser.add_option("-a", "--algo", type="string",
      action="store", dest="algo", default=False,
      help="algo: TB2_HS_IT_OB1_OS1_CB3_CS3 ")
      
   parser.add_option("-s", "--stock", type="string",
      action="store", dest="stock", default=False,
      help="stock: AAPL ")
      
   return parser

#~~~~~~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

day = ""
parser = parseCL()
(clOpts, args) = parser.parse_args()
algo = clOpts.algo
day = clOpts.day
stock = clOpts.stock

profilePath = "profiles/active.json"

#if day == "":
#   profilePath = "profiles/active.json"
#else:
#   #profilePath = day + "/" + "profiles/active.json"
#   profilePath = "test/" + day + "/" + "profiles/active.json"
#   #profilePath = os.getcwd() + "/test/" + day + "/" + "profiles/active.json"

pf = lpl.Profile()

d = pf.readProfile(profilePath)

pf.initProfile(d)
      
b, m, bar = algo.rpartition("TB")
pf.setAlgoValues(d, algo, bar[0], "")
#print ("bar " + str(bar))

b, m, bar = algo.rpartition("OB")
pf.setOpenBuyValue(d, bar[0], "")
#print ("bar " + str(bar))

b, m, bar = algo.rpartition("OS")
pf.setOpenSellValue(d, bar[0], "")
#print ("bar " + str(bar))

b, m, bar = algo.rpartition("CB")
pf.setCloseBuyValue(d, bar[0], "")
#print ("bar " + str(bar))

b, m, bar = algo.rpartition("CS")
pf.setCloseSellValue(d, bar[0], "")
#print ("bar " + str(bar))

if "DB" in algo:
   b, m, bar = algo.rpartition("DB")
   bars, m, e = bar.partition("_")
   pf.setTradingDelayBars(d, bars, "")

exit(pf.writeProfile(profilePath, d, stock))


