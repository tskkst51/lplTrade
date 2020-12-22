## Take algo string and write a profile from it

# TB2_HS_IT_OB1_OS1_CB3_CS3

import json
from optparse import OptionParser
import lplTrade as lpl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseCL():

   parser = OptionParser()
      
   parser.add_option("-d", "--day", type="string",
      action="store", dest="day", default=False,
      help="day: 1112202020 ")
   
   parser.add_option("-a", "--algo", type="string",
      action="store", dest="algo", default=False,
      help="algo: TB2_HS_IT_OB1_OS1_CB3_CS3 ")
      
   return parser

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def readProfile(profilePath):

   with open(profilePath) as jsonData:
      d = json.load(jsonData)

   return d

#~~~~~~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parser = parseCL()
(clOpts, args) = parser.parse_args()
algo = clOpts.algo

profilePath="test/" + str(clOpts.day) + "/" + "profiles/active.json"

d = readProfile(profilePath)

pf = lpl.Profile(d)
      
b, m, bar = algo.rpartition("TB")
pf.setAlgoValues(d, algo, bar[0], "")

b, m, bar = algo.rpartition("OB")
pf.setOpenBuyValue(d, bar[0], "")

b, m, bar = algo.rpartition("OS")
pf.setOpenSellValue(d, bar[0], "")

b, m, bar = algo.rpartition("CB")
pf.setCloseBuyValue(d, bar[0], "")

b, m, bar = algo.rpartition("CS")
pf.setCloseSellValue(d, bar[0], "")

exit(pf.writeProfile(profilePath, d))


