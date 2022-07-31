#!/bin/bash

## Find the best algo's across all days

function init {

   #wp="/Users/tsk/w/lplTrade"
   wp=$(pwd)
   
   $HOME/bin/lplt.sh
   . $wp/scripts/db.sh

   day=$1
   algo=$2
   sym=$3
   debug=$4
   dontStopDB=$5
   
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   today=$(date "+%Y%m%d")
   
   tmpFile=$(getRandomTmpFile)
   
   syms=$sym
   if [[ $day == "all" ]] && [[ $sym == "all" ]]; then
      syms=$(getAllSyms "all")
   elif [[ $day != "all" ]] && [[ $sym == "all" ]]; then
      syms=$(getAllSyms $day)
   fi
   
   if [[ -n $debug ]]; then echo syms: $syms; fi
   if [[ -z $syms ]]; then echo sym is empty!; exit 1 ; fi
   if [[ -z $algo ]]; then echo Need algo; exit 1; fi
      
   eq="="
   echo $algo | grep "%" > /dev/null
   if [[ $? == 0 ]]; then eq="like"; fi

   days=$day
   if [[ $day == "all" ]]; then
      days=$(getAllDays $sym)
   fi
      
   if [[ -f $tmpFile ]]; then rm -f $tmpFile ; fi
   if [[ -z $days ]]; then echo day is empty!; exit 1 ; fi
   
   algoCtr=0
   algoModCtr=0
}

init $1 $2 $3 $4 $5

if [[ -n $debug ]]; then
   echo Deleting data from DB: ${days} sym: $syms algo: ${algo}...
fi

for db in $days; do
   if [[ ! -f "$dbDir/${db}/log" ]]; then 
      if [[ -n $debug ]]; then
         echo $db DB log file missing! skipping...
      fi
      continue
   fi
   
   isDBRunning $db
   if (( $? == 1 )); then
      port=$(getRunningPort $db)
      if [[ -n $debug ]]; then
         echo running port: $port for db $db
      fi
      dbWasRunning=1
   else
      port=$(getNextPort)
      startDB $db $port > $tmpFile 2>&1
      if [[ -n $debug ]]; then cat $tmpFile; fi
      if [[ $? != 0 ]]; then
         echo Unable to start DB $db
      fi
   fi

   cl=$(getCL $port "algos")
   clO=$(getCLO $port "algos")
      
   for s in $(echo $syms); do
      $cl "delete from algoData where sym = '${s}' and algo $eq '${algo}'"
      if [[ -n $debug ]]; then
         echo $clO "\"delete from algoData where sym = '${s}' and algo $eq '${algo}'\""
      fi
      
      if [[ -s $tmpFile ]]; then
         algoCtr=$((algoCtr + 1))
         cat $tmpFile >> ${tmpFileSort}_${s}
      fi
      
      $cl "delete from algoModData where sym = '${s}' and algo $eq '${algo}'"
      if [[ -n $debug ]]; then
         echo $clO "\"delete from algoModData where sym = '${s}' and algo $eq '${algo}'\""
      fi
      if [[ -s $tmpFile ]]; then
         algoModCtr=$((algoModCtr + 1))         
         cat $tmpFile >> ${tmpFileSort}_${s}
      fi
   done
   if [[ -z $dontStopDB ]]; then
      if (( ! dbWasRunning )); then
         if [[ -n $debug ]]; then echo Stopping DB $port; fi
         dbStop.sh $db > $tmpFile 2>&1
         if [[ -n $debug ]]; then cat $tmpFile; fi
         dbWasRunning=0
      fi
   fi
done      

exit 0