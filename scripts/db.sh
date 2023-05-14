# ENV file for DB operations
wp="$(echo $HOME)/w/lplTrade"

absTestDir="${wp}/test"
manualOverideDir="${wp}/manualOveride"
manualOverideEx=".mo"
testDir="test"
dbDir="db"
dbMasterName="master"
dbName="algos"
dbToken="bin/postgres"
bestAlgosDir="${wp}/bestAlgos"
dbStartingPort="6000"
dbAlgoModTestName="Algo Modifiers Test"
dbAlgoTestName="Algo Test(s)"

dbNumTestRows=625
dbMaxModTestRows=13
dbNumBestRows=5
dbNumBestAlgos=100
initNumBestAlgos=25
numTestStocks=13

seqAlgos=11

# The total number of hi/lo tests are 5**5*3 = 9375
# The total number of seq tests are 4**4*3 = 768

# 18 standard tests
# seq tests = seqAlgos * 768
# hi/lo tests = testDBAlgos - seqAlgos * 9375

# testModDBAlgos 72
# numStandardTests 17
# numModTests 1224
# 20210816 TME COMPLETE! 1306 ran out of max 1224


# This is used for restricting the number of DB's/test days used for 
# finding the best Algo.
maxNumDays=20

# Used for reducing the number of DB's searched
incDBNums=20

# Sample size of DB query result
dbNumModTestRows=5


dbTmpFile="/tmp/db_"
tmpFileSyms="/tmp/allSymbols"
inEx=".in"
bsEx=".bs"

run="scripts/runDB.sh"
postGresPath="/Applications/Postgres.app/Contents/Versions/14/bin"

testDBAlgos="LS_QM LH_QM SH_QM HL_TG_QM BL_QM HL_QM HS_QM HI_QM LO_QM OC_QM OO_QM CC_QM PL_QM EO_EC_QM HS_HL_QM HI_HL_QM LO_HL_QM"

# Tests for testDB.sh
testDBAlgosAS="AS_LS_QM AS_LH_QM AS_SH_QM AS_HL_TG_QM AS_HS_HL_TG_QM AS_BL_QM AS_HL_QM AS_HS_QM AS_HI_QM AS_LO_QM AS_OC_QM AS_OO_QM AS_CC_QM AS_PL_QM AS_EO_EC_QM AS_HS_HL_QM AS_HI_HL_QM AS_LO_HL_QM NL_QM"

# Tests for testModsDB.sh
testModDBAlgos="OT OT_AS DU8_AS DU8_IT DU8_IT_AS AS IT_AS AS_DB AS_UA DU8_DL2 DU6_DL2 DU4 DU6 DU8 DU4_UA DU6_UA DU6_UA DU6_AV DU6_AL DU6_AV_AL RV SR IR TR AV AL VI VI_AS LI LI_AS AV_VI AL_LI QP HM SS QL DB AO AC IT PM TS UA WT UA_WT TR_QP_DB RV_TR_DB RV_AV_DB RV_AL_DB RV_QP_DB HM_TR_DB HM_AV_DB TR_IR TR_TS TR_QP QP_IR RV_TR RV_AV RV_AL RV_QP HM_TR HM_AV HM_AL HM_QP IT_QP IT_TS AO_AC QP_PM AV_TS AL_TS AV_IT AL_IT AV_UA AL_UA AV_AL_UA QP_QL"

# Used now in initBestAlgos.sh
addedAlgos="DU8 DU8_DL2 AS UA"

# Removed DL1 11/15/22

incAlgos="DU8_DL2 AV AL UA TG DU8_AV_DL2 DU8_AL_DL2 DU8_UA_DL2 DU8_UA_AV_DL2"

today=$(date "+%Y%m%d")

keepToken="keepAliveDB"

allSystems="mm.local mmT.local"
#allSystems="ML-C02C8546LVDL.local mm.local mmT.local"
#allSystems="mmT.local"
devSystem="ML-C02DW7S9ML7H.local"
testSystems="mm.local mmT.local"
remoteTestSystems="mmT.local"

activeLiveHost="ML-C02C8546LVDL"

lpltArchiveSystem="mm.local"
liveSystem="mm"
dbArchiveSystem="mmT.local"

liveHostUser="tknitter"
defaultUser="tsk"

testProgram="keepAliveDb.sh"

liveConfig="profiles/active.json"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getTmpFile {
   
   sym=$1
   
   tmpFile="${tmpFile}${sym}"
   
   echo $tmpFile
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getRandomTmpFile {

   echo "${dbTmpFile}${RANDOM}"
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function rmRandomTmpFiles {
      
   rm -f ${dbTmpFile}*
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getTotalAlgoModRows {
   
   sym=$1
   
   tmpFile="${tmpFile}_${sym}"
   
   echo $tmpFile
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function isPortInUse {

	port=$1
	
   runningPorts=$(ps -ef | grep $dbToken | awk '{print $12}')

	echo $runningPorts | grep -q $port
	
	if (( $? == 0 )); then
		return 1
	fi
	
	return 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function isDBCreated {

   db=$1

   if [[ -f "${dbDir}/${db}/log" ]]; then
      return 1
   fi
   return 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function isDBRunning {

   db=$1

   dbStr=""
   dbStr=$(ps -ef | grep "$dbToken" | grep "${dbDir}/${db}" | awk '{print $10}')

   if [[ -n $dbStr ]]; then
      return 1
   fi
   
   return 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getNextPort {

   randomNum=$((RANDOM%100))  

   newPort=$(expr $randomNum + $dbStartingPort)

   isPortInUse $newPort   
   if (( $? == 1 )); then
		while true; do
   		randomNum=$((RANDOM%100))  
			newPort=$(expr $randomNum + $dbStartingPort)
			isPortInUse $newPort
			if (( $? == 0 )); then break; fi
		done
	fi
	
   echo $newPort
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getKeepAliveDay {

   day=$1

   dayTesting=""
   runningLive=""
   
   dayTesting=$(ps -ef | grep "$keepToken" | grep -v grep | awk '{print $10}')
   runningLive=$(ps -ef | grep "$keepToken" | grep -v grep)

   if [[ -n $dayTesting ]]; then
      echo $dayTesting
   elif [[ -n $runningLive ]]; then
      # Could be running live
      echo $today
   fi
   
   echo ""
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getAllRunningDBs {

   dbStr=""
   dbStr=$(ps -ef | grep "$dbToken" | awk '{print $10}')

   if [[ -n $dbStr ]]; then
      echo ""
   fi
   
   echo $dbStr
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getRunningPort {

   db=$1

   port=""
   port=$(ps -ef | grep $dbToken | grep "${dbDir}/$db" | awk '{print $12}')
   
   if [[ -n $port ]]; then
      echo $port | awk '{print $1}'
      return
   fi
   
   echo 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getCL {

   port=$1
   db=$2
   
#   if [[ -n $dbPort ]]; then
#      echo dbPort set $dbPort
#      port=$dbPort
#   fi
   
   echo "$postGresPath/psql $db -q -p $port -t -c \a -c "
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getCLO {

   port=$1
   db=$2
   
#   if [[ -n $dbPort ]]; then
#      echo dbPort set $dbPort
#      port=$dbPort
#   fi
   
   echo "$postGresPath/psql $db -q -p $port -t -c "
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getCLf {

   port=$1
   db=$2
   
   if [[ -n $dbPort ]]; then
      echo dbPort set $dbPort
      port=$dbPort
   fi
   
   echo "$postGresPath/psql $db -q -p $port -t -o $tmpFile -c "
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function modAlgosCaseAlreadyRan {

   sym=$1
   algo=$2
   
   algo=$($cl "select algo from algoModData where sym = '${sym}' and algo = '${algo}'")
      
   echo $algo
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function modAlgoPurposesAlreadyRan {

   sym=$1
   day=$2
   
   status=$(runSQL $cl "select status from $dbMasterName where sym = '${sym}' and day = '${day}'" $day)
   
   echo $status
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function modAlgosAlreadyRan {

   sym=$1
   day=$2
   
   status=$(runSQL $cl "select status from $dbMasterName where sym = '${sym}' and day = '${day}'")
   
   echo $status
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function runSQL {

   cmd=$1
      
   status=$($cmd)
   
   echo $status
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function startDB {
   
   db=$1
   port=$2
      
   dbPath="${dbDir}/${db}"
   logPath="${dbPath}/log"
      
   pg_ctl -D ${dbPath} -o "-p ${port}" -l $logPath start
   
   return $?
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function symExistsForDay {

   day=$1
   sym=$2
   
   if [[ -f "${testDir}/${day}/bc/active${sym}.bc" ]]; then
      return 1
   fi
   
   return 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getPartBestSymsFile {

   regEx=$1
   
   bestSyms="AAPL BABA TSLA"
   
   # Use the bestAlgo files as seeds. filter out a portion based on regEx
   bestAlgoSeed="${wp}/daysBest/latest"

   bestSyms=$(grep -E $regEx $bestAlgoSeed | awk '{print $1}')

   #bestSyms=$(head -n ${dbNumBestAlgos} $bestAlgoSeed | awk '{print $1}')
   
   echo $bestSyms
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getBestSymsFile {

   bestSyms="AAPL BABA TSLA"
   
   # Use the bestAlgo files as seeds.
   bestAlgoSeed="${wp}/daysBest/latest"
   bestSyms=$(head -n ${dbNumBestAlgos} $bestAlgoSeed | awk '{print $1}')
   
   echo $bestSyms
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getAllSyms {
   
   day=$1
   
   rm -f $tmpFileSyms

   if [[ $day == "all" ]]; then
      for s in $(ls test); do 
         ls "test/${s}/bc" | sed "s/active//" | sed "s/\.bc//" >> $tmpFileSyms;
      done  
   else
      ls "test/${day}/bc" | sed "s/active//" | sed "s/\.bc//" > $tmpFileSyms;
   fi
   
   allSyms=$(sort -u $tmpFileSyms)
   
   echo $allSyms
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getAllDays {
   
   sym=$1

   dbs=`for d in $(ls test); do if [[ -f "test/${d}/bc/active${sym}.bc" ]]; then echo $d;fi;done`

   echo $dbs
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function removeDupsFromAlgoStr {
   
   s=$1

   str=$(echo $s | sed "s/_/ /g")

   fs=""
   ctr=0
   for t in $(echo $str); do 
      if [[ "$fs" == *"$t"* ]]; then
         continue
      fi
      if (( ctr == 0 )); then
         fs=$t
         ctr=$((ctr+1))
         continue
      fi
      fs="${fs}_${t}" 
   done

   echo $fs
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function killRunningScript {
   
   script=$1

   thisPID=$$
      
   pids=$(ps -ef|grep $script |grep -v grep| awk '{print $2}')
   
   numPids=$(echo $pids | tr -cd ' ' | wc -c)
   
   if (( $numPids == 1 )); then return 0; fi
      
   for p in $(echo $pids); do
      eq=$(echo "$p == $thisPID" | bc)
      if (( $eq == 1 )); then continue; fi
      echo killing test scripts $p
      kill $p
   done
   
   kill $(ps -ef |grep "test"|grep -v grep|awk '{print $2}')
   
   return 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function numOfTestDays {
   
   sym=$1
   
   cwd=$(pwd)
   
   cd $absTestDir || echo cant cd to $absTestDir
   
   numDays=$(find . -name "active${sym}.pr" -print | wc -l)
   
   cd $cwd || echo cant cd to $cwd
   
   echo $numDays
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function numOfBestAlgoDays {
   
   sym=$1
   
   days=0
   
   #if [[ -s "${bestAlgosDir}/${sym}.bs" ]]; then
   if [[ -s "${bestAlgosDir}/${sym}.in" ]]; then
      days=$(tail -1 "${bestAlgosDir}/${sym}.in" | awk '{print $9}')
   fi
   
   echo $days
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getLastNDays {
   
   sym=$1
   range=$2
         
   days=$(getAllDays $sym)

   totalNumDays=$(echo $days | grep -o ' ' | wc -l)
   totalNumDays=$(echo "$totalNumDays + 1" | bc)

   if (( $totalNumDays > $range )); then
     # Reduce the set
      firstDay=$(echo "$totalNumDays - $range + 1" | bc)
      days=$(echo $days | cut -f${firstDay}-${totalNumDays} -d' ')
   fi
 
   echo $days  
}
