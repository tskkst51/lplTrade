#!/bin/bash

## Find the best algo's across all days

function init {

   $HOME/bin/lplt.sh
   . $LPLT/scripts/db.sh

   sym=$1
   
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   numRows=10
   dbWasRunning=0

   today=$(date "+%Y%m%d")
   
   tmpFile=$(getTmpFile $sym)

   if [[ -n $sym ]]; then
      syms=$sym 
   else
      stocksNotProvided="yes"  
   fi
   
   if [[ -f $tmpFile ]]; then
      rm -f $tmpFile
   fi
}

init $1

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

   cl=$(getCL $port $db)
   
   algoMods=$($cl "select algo,gain,winpct from algoModData where sym = '${sym}' order by gain,winpct desc" | tail -n "-${dbNumBestRows}")

   algos=$($cl "select algo,gain,winpct from algoData where sym = '${sym}' order by gain,winpct desc" | tail -n "-${dbNumBestRows}")

echo algos $algos 
echo algoMods $algoMods 
   for a in $algos $algoMods; do
      # if any algos have a gain of 0 ignore
      gain=$(echo $a | awk -F\| '{print $3}')
      if (( gain == 0 )); then
         continue
      fi
      # Store in tmp file for later processing
      echo "${db}|${a}" >> "${tmpFile}"
   done
   if (( ! dbWasRunning )); then
      echo Gathering data from $db for $sym complete!
      echo Stopping DB $port
      dbStop.sh $db || exit 1
      dbWasRunning=0
   fi
done

for dayAlgo in $(cat $tmpFile | awk -F\| 'BEGIN{OFS=FS} {print $1,$2}'); do
   day=$(echo $dayAlgo | cut -f1 -d\|)
   algo=$(echo $dayAlgo | cut -f2 -d\|)
   
   symExistsForDay $day $sym
   if (( $? != 0 )); then
      echo $day $sym ${algo}...
      if [[ -f bestAlgos/${sym}.allDB ]]; then
         mv bestAlgos/${sym}.allDB historyBestAlgos
      fi
      $run "" $algo $sym >> bestAlgos/${sym}.allDB
      tail -n 5 bestAlgos/${sym}.allDB | grep Gain
   fi
done

grep Gain bestAlgos/${sym}.allDB | sort -n -k4,4 -k7,7 > bestAlgos/${sym}.bsDB

exit 0