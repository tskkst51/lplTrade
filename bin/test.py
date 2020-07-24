import json
import os
import time
import simplejson
import lplTrade as lpl
from optparse import OptionParser
from pathlib import Path
import subprocess
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test all lplTrade profile combinations. Output best combinations

# Create dict of all default 

parser = OptionParser()

parser.add_option("-p"  , "--profileTradeDataPath", dest="profileTradeDataPath",
   help="profile template", metavar="FILE")

parser.add_option("-w", "--workPath", type="string",
   action="store", dest="workPath", default=False,
   help="work directory. default lplTrade...")

parser.add_option("-s", "--stock", type="string",
   action="store", dest="stock", default=False,
   help="stock to bua/selly: AAPL")
         
(clOptions, args) = parser.parse_args()

if workPath:
   os.chdir(workPath)
else:
   exit()

tm = lpl.Time()

# Get trading elements
with open(clOptions.profileTradeDataPath) as jsonData:
   d = json.load(jsonData)

openBuyBars = [2,3,4,5]
openSellBars = [2,3,4,5]
closeBuyBars = [2,3,4,5]
closeSellBars = [2,3,4,5]
timeBar = [1,2,3,4,5]
aggressiveOpen = [0,1]
aggressiveClose = [0,1]
doHiLoSeq = [0,1]
doExecuteOnOpen = [0,1]
doTrends = [0,1]
doQuickProfit = [0,1]
doRangeTradeBars = [0,1]
doOpensCloses = [0,1]
doExecuteOnClose = [0,1]
doHiLoOnClose = [0,1]
doHiLoOnOpen = [0,1]
doReversalPattern = [0,1]
doQuickReversal = [0,1]
doReverseBuySell = [0,1]
doDynamic = [0,1]
doOnlySells = [0,1]
doOnlyBuys = [0,1]
useAvgBarLimits = [0,1]
usePricesFromFile = 1
write1_5MinData = 1
resume = 1
tradingDelayBars = range(2,20)
quickProfitMax = [0,1]
waitForNextBar = [0,1]
profitPctTrigger = [0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002]
quitMaxProfit = [0,1]
bearTrendValue = [1.5,1.6,1.7,1.8,1.9]
bullTrendValue = [3.5,3.4,3.3,3.2,3.1]
shortTrendBars = [6,8,10,12]
midTrendBars = [12,16,20,24]
longTrendBars = [18,24,30,36]
megaTrendBars = [24,32,40,48]

dumpedProfilePath = profileTradeDataPath

# Set  and dump back out to temp file. return temp file
with open(dumpedProfilePath, 'w') as fp:
    json.dump(d, fp, indent=2)

# Create one profile file, changing values defined above. 
# Execute lpltTrade with a the same profile file with varying values.
# Save the profile values the high, low, last prices and the dates they happened
# iterate over all values to find the most favorable WOW

# Execute shell sript to populate site path with latest code
runPath = os.getcwd()
home = str(Path.home())

shellCmd = home + "/bin/lplt.sh"
pid = subprocess.Popen([sys.executable, shellCmd])

progPath = home + "/w/gitWS/lplTrade/bin/lplt.py"
connectionPath = home + "/profiles/et.json"
profilePath = runPath + dumpedProfilePath


progOPtions = " -o -m"

# pid = subprocess.Popen([sys.executable, "longtask.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


python3 bin/lplt.py -c ~/profiles/et.json -d -o -s QQQ -p profiles/active.json -w test/2020072

cmd = ""



