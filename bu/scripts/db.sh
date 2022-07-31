# ENV file for DB operations
dbDir="db"
dbMasterName="master"
dbName="algos"
dbToken="bin/postgres"
dbStartingPort="6000"
dbAlgoModTestName="Algo Modifiers Test"
dbAlgoTestName="Algo Test(s)"

dbNumTestRows=625
dbNumModTestRows=10
dbNumBestRows=5

tmpFile="/tmp/db_"
testDir="test"

run="scripts/runDB.sh"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function getTmpFile {
   
   sym=$1
   
   tmpFile="${tmpFile}${sym}"
   
   echo $tmpFile
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
