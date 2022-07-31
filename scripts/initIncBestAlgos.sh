#!/bin/bash

## Use the *.in (the initial best algo file incrementally to find the 
## best based off last trading day. Use this every day for testing

function init {

   wp="/Users/tsk/w/lplTrade"

   . ${wp}/scripts/db.sh
   
   $HOME/bin/lplt.sh

   sym=$1
   ss=$2
   debug=$3

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
      
   if [[ -z $sym ]]; then echo Need SYM; exit 1 ; fi
   if [[ -z $ss ]]; then ss=$initNumBestAlgos ; fi
   if [[ -n $debug ]] && [[ $debug != "d" ]]; then debug=""; fi
}

init $1 $2 $3

if [[ -n $debug ]]; then
   echo Incrementing best algos for sym ${sym}...
fi

tmpFile=$(getRandomTmpFile)
tmpFile2=$(getRandomTmpFile)

if [[ ! -f "${bestAlgosDir}/${sym}${inEx}" ]]; then 
   echo Exiting ${0}... No init file found for $sym
   exit 1
fi

rm -f ${tmpFile}_${sym}
rm -f $tmpFile2

for algo in $(tail -n $ss "${bestAlgosDir}/${sym}${inEx}" | awk '{print $13}' ); do
   run.sh "" $algo $sym | grep Gain >> ${tmpFile}_${sym}
   tail -1 ${tmpFile}_${sym}
done


# Only overwrite the .in file if the new results out perform the algos in the 
# current in file.
sort -n -k4,4 ${tmpFile}_${sym} | tail -1 > $tmpFile2

if [[ -n $debug ]]; then tail -5 $tmpFile2; fi

bestOld=$(awk '{print $4}' "${bestAlgosDir}/${sym}${inEx}" | tail -n 1)
bestNew=$(awk '{print $4}' $tmpFile2 | tail -n 1)

if [[ $bestNew > $bestOld ]]; then
   sort -n -k4,4 ${tmpFile}_${sym} > "${bestAlgosDir}/${sym}${inEx}"
   echo Got a new best algo value:
   echo old: $bestOld
   echo new: $bestNew
else
   echo No new best algo with another day of test data:
   echo old: $bestOld
   echo new: $bestNew
   exit 1
fi

if [[ -n $debug ]]; then echo Adding $ss algos to "${bestAlgosDir}/${sym}${bsEx}" file; fi

tail -n $ss "${bestAlgosDir}/${sym}${inEx}" >> "${bestAlgosDir}/${sym}${bsEx}" 

exit 0