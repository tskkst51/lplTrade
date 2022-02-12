#!/bin/bash

## Find the best algo's across all days

function init {

   . $HOME/profiles/db.sh

   sym=$1
   
   $HOME/bin/lplt.sh

   . $HOME/profiles/db.sh

   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   numRows=10
   
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

for db in $(ls db | grep "20"); do
   echo $db
   isDBRunning $db
   if [[ $? == 0 ]]; then
      port=$(getNextPort)
      echo Starting DB $db
      startDB $db $port
   else
      port=$(getRunningPort $day)
   fi

   cl=$(getCL $port $dbName)
   
   algos=$($cl "select algo,gain,winpct from algoModData where sym = '${sym}' order  by gain,winpct desc" | tail -n "-${dbNumBestRows}")

   for a in $algos; do
      echo $a
      # Store in tmp file for later processing
      echo $a >> "${tmpFile}"
   done
   
   dbStop.sh $db || exit 1
   
done

#sort -r -t "|" -n -k2,2  "${tmpFile}"

for algo in $(cat $tmpFile | awk -F\| '{print $1}'); do
   #$run "" $algo $stock >> bestAlgos/${stock}.all
   $run "" $algo $sym

done


exit 0