#!/bin/bash

function init {

   . $LPLT/scripts/db.sh

   day=""
   algo=""
   stock=""
   
   day=$1
   algo=$2
   stock=$3
   testPath=$4   

   algoProvided=0
   stockProvided=0
   
   wp=$LPLT

   if [[ -z $day ]]; then
      echo ERROR: Must have a day to test on
      exit 1
   fi
   
   #echo $1 $2 $3
   
   testCmd="${wp}/bin/test.py"
   
   if [[ ! -e $testCmd ]]; then
      echo $testCmd not found!
      exit 1
   fi

   if [[ -n $testPath ]]; then
      testPath=$testPath
   else
      testPath=$testDir
   fi
      
   activateDir="/lplW2"
   
   activateCmd=$(dirname $wp)
   activateCmd+="${activateDir}/bin/activate"
   
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   # Execute script to populate source library path
   
   dt=$(date "+%Y%m%d")
   
   doResults=0
   
   pl=""
   dbDir="db"
   dbName="algos"
   dbToken="Applications/Postgres.app"
   dbKey="20"
   
   #${wp}/scripts/modProfiles.sh $testPath > /dev/null 2>&1
}

function populateTestDir {
   # Populate from the archives
   if [[ ! -d "${testPath}/${day}" ]]; then
      cd ../lpltArchives || exit 1
      git pull
      tar -zxf "${day}.tar.gz"
      mv "Users/tsk/git/lplTrade/test/${day}" ../lplTrade/${testPath}
      rm -fr Users
      cd ../lplTrade
      doResults=1
      #${wp}/scripts/modProfiles.sh $testPath
   fi
}

function initAlgos {

#testPaths=$(ls ${testPath})

testPaths="${testPath}/${day}"

if [[ -n $algo ]] && [[ $algo != "none" ]]; then
   algos=$algo
   algoProvided=1
else
   algos="HL_QM HS_QM HI_QM LO_QM OC_QM OO_QM CC_QM PL_QM EO_EC_QM HS_HL_QM HI_HL_QM LO_HL_QM"
fi
}

function initStocks {

   if [[ -n $stock ]]; then
      stockCL="-s $stock"
      stockProvided=1

   else
      stocks=$(ls "${testPath}/${day}/bc" | awk -F\. '{print $1}'|sed "s/active//")
      #stocks=$(grep stocks ${wp}/${testPath}/${datePath}/profiles/active.json | \
      #   awk -F\" '{print $4}')
      for s in ${stocks[*]}; do
         stock=$s
         echo stock $stock
         break
      done
      numStocks=$(echo $stocks | awk -F" " '{print NF}')
      #echo stocks $stocks
      #echo numStocks $numStocks
   fi
}


#~~~~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

init "$1" "$2" "$3" "$4"
initAlgos

i=0
for a in ${algos}; do i=$((i+1)); done
echo Running $i $dbAlgoTestName for ${day}...
for a in ${algos}; do echo $a; done

isDBRunning $day
if [[ $? == 0 ]]; then
   port=$(getNextPort)
   echo Starting DB $day
   startDB $day $port
else
   port=$(getRunningPort $day)
fi

cd $LPLT || exit 1

#volDate=20201117

initStocks

set -m

for datePath in $testPaths; do
      
   trap - SIGINT
      
   # No bar charts exist, skip
   if [[ -z $day ]]; then
      if [[ ! -s "${wp}/${testPath}/${datePath}/bc/active${stock}.bc" ]]; then
         echo
         echo $stock BAR chart for $datePath not found. Skipping...
         continue
      fi
      if [[ ! -s "${wp}/${testPath}/${datePath}/prices/active${stock}.pr" ]]; then
         echo
         echo $stock PRICE chart for $datePath not found. Skipping...
         continue
      fi
   fi
   
   for a in $(echo ${algos}); do
      algoOpt="-a ${a}"
      
      a=$(echo $a | sed 's/,/_/g')
      
      day=$(basename $datePath)      
      
      numStocks=0
      ctr=0
      
      if [[ -z $stock ]]; then
         echo numStocks $numStocks
      fi

      echo Testing $day $stock $a ...

      cmd="$py3 $testCmd $algoOpt $stockCL -c $HOME/profiles/et.json -w ${wp}/${datePath} -p ${wp}/${datePath}/profiles/active.json"
      
      #echo "command: ${cmd}"

      $cmd 
   done      
done

if (( stockProvided )); then
   scripts/testModsDB.sh $day $stock
   #scripts/dbBest.sh $day $stock
else
   scripts/testModsDB.sh $day
fi

#pg_ctl -D ${dbDir}/${day} stop

exit 0

