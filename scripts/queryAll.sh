#!/bin/bash

## Find the best algo's across all days

function init {

   $HOME/bin/lplt.sh
   . $LPLT/scripts/db.sh

   sym=$1
   algo=$2
   
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   numRows=10
   dbWasRunning=0

   today=$(date "+%Y%m%d")
   
   tmpFile=$(getTmpFile $sym)

   if [[ -z $sym ]] || [[ -z $algo ]]; then
      echo need sym and algo 
      exit 1 
   fi
   
#   if [[ -z $algo ]]; then
#      echo need algo
#      exit 1 
#   fi
      
   if [[ -f $tmpFile ]]; then
      rm -f $tmpFile
   fi
}

init $1 $2

# Get the 10 best algoMods populate file

echo Gathering algo data across all dates...

for db in $(ls db | grep "20"); do
   isDBRunning $db
   if (( $? == 1 )); then
      port=$(getRunningPort $db)
      echo running port: $port
      dbWasRunning=1
   else
      port=$(getNextPort)
      startDB $db $port
      if [[ $? != 0 ]]; then
         echo Unable to start DB $db
      fi
   fi

   cl=$(getCL $port $dbName)
   
   algoMods=$($cl "select algo,gain,winpct from algoModData where sym = '${sym}' and algo = '${algo}' order by gain,winpct desc")

   algos=$($cl "select algo,gain,winpct from algoData where sym = '${sym}' and algo = '${algo}' order by gain,winpct desc")

   echo $db $algos >> $tmpFile
   echo $db $algoMods >> $tmpFile
   
   echo algoMods $algoMods
   echo algos $algos
   
#   for a in $algos $algoMods; do
#      # if any algos have a gain of 0 ignore
#      gain=$(echo $a | awk -F\| '{print $3}')
#      if (( gain == 0 )); then
#         continue
#      fi
#      # Store in tmp file for later processing
#      echo "${db}|${a}" >> "${tmpFile}"
#   done
#   if (( ! dbWasRunning )); then
#      echo Gathering data from $db for $sym complete!
#      echo Stopping DB $port
#      dbStop.sh $db || exit 1
#      dbWasRunning=0
#   fi
done

