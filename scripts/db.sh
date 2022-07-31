# ENV file for DB operations
wp="$(echo $HOME)/w/lplTrade"

dbDir="db"
dbMasterName="master"
dbName="algos"
dbToken="bin/postgres"
bestAlgosDir="${wp}/bestAlgos"
dbStartingPort="6000"
dbAlgoModTestName="Algo Modifiers Test"
dbAlgoTestName="Algo Test(s)"

dbNumTestRows=625
dbNumModTestRows=5
dbMaxModTestRows=10
dbNumBestRows=5
dbNumBestAlgos=100
initNumBestAlgos=25

dbTmpFile="/tmp/db_"
tmpFileSyms="/tmp/allSymbols"
testDir="test"
inEx=".in"
bsEx=".bs"

run="scripts/runDB.sh"
postGresPath="/Applications/Postgres.app/Contents/Versions/14/bin"

testDBAlgos="HL_TG_QM HS_HL_TG_QM BL_QM HL_QM HS_QM HI_QM LO_QM OC_QM OO_QM CC_QM PL_QM EO_EC_QM HS_HL_QM HI_HL_QM LO_HL_QM"

testModDBAlgos="DU2 DU3 DU4 DU5 DU6 RV IR TR AV AL VI LI AV_VI AL_LI QP HM SS QL DB AO AC IT PM TS UA WT UA_WT TR_QP_DB TR_QP_QL_DB RV_TR_DB RV_AV_DB RV_AL_DB RV_QP_DB RV_QP_QL_DB HM_TR_DB HM_AV_DB HM_QP_QL_DB IT_QL_DB IT_QP_QL_DB TR_IR TR_TS TR_QP TR_QP_QL QP_IR QP_QL_IR RV_TR RV_AV RV_AL RV_QP RV_QP_QL HM_TR HM_AV HM_AL HM_QP HM_QP_QL IT_QL IT_QP IT_QP_QL IT_TS AO_AC QP_PM QP_QL_PM AV_TS AL_TS AV_IT AL_IT AV_UA AL_UA QP_QL"

today=$(date "+%Y%m%d")

keepToken="keepAliveDB"

allSystems="ML-C02C8546LVDL.local mm.local mmT.local"
devSystem="ML-C02DW7S9ML7H.local"
testSystems="mm.local mmT.local"

activeLiveHost="ML-C02C8546LVDL"

lpltArchiveSystem="mm.local"
dbArchiveSystem="mmT.local"

liveHostUser="tknitter"
defaultUser="tsk"

testProgram="keepAliveDb.sh"

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
function getNextPort {

   randomNum=$((RANDOM%100))  
   randomNum=$((RANDOM%100))

   newPort=$(expr $randomNum + $dbStartingPort)
   
   echo $newPort
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
   
   echo "psql $db -q -p $port -t -c \a -c "
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getCLO {

   port=$1
   db=$2
   
#   if [[ -n $dbPort ]]; then
#      echo dbPort set $dbPort
#      port=$dbPort
#   fi
   
   echo "psql $db -q -p $port -t -c "
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getCLf {

   port=$1
   db=$2
   
   if [[ -n $dbPort ]]; then
      echo dbPort set $dbPort
      port=$dbPort
   fi
   
   echo "psql $db -q -p $port -t -o $tmpFile -c "
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
      
   "${postGresPath}/pg_ctl" -D ${dbPath} -o "-p ${port}" -l $logPath start
   
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
