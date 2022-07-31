#!/bin/bash

## Initialize the best algo's across one day. This runs the exhaustive bestAllDBs.sh

function init {

   #wp="/Users/tsk/w/lplTrade"
   wp=$(pwd)

   . ${wp}/scripts/db.sh
   
   $HOME/bin/lplt.sh

   day=$1
   ss=$2
   sym=$3
   overideInits=$4
   debug=$5

   syms=$(getAllSyms $day)
   
   if [[ $sym != "" ]]; then 
      syms=$sym
   fi

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
      
   if [[ -z $ss ]]; then ss=$dbNumModTestRows ; fi
   if [[ $overideInits != "o" ]]; then overideInits="" ; fi
   if [[ -n $debug ]] && [[ $debug != "d" ]]; then debug=""; fi
   
   echo day $day
   echo ss $ss
   echo overideInits $overideInits
   echo syms $syms
   echo debug $debug
}

init $1 $2 $3 $4 $5

if [[ -n $debug ]]; then
   echo Initializing best algos for all syms on ${day}...
fi

tmpFile=$(getRandomTmpFile)
tmpFile2=$(getRandomTmpFile)

symsPurged=""

# Purge syms if init file already exists
if [[ $overideInits == "o" ]]; then
   for s in $syms; do
      if [[ -f "${bestAlgosDir}/${s}${inEx}" ]]; then
         echo skipping ${s}${inEx} 
         continue
      fi
      symsPurged="$symsPurged ${s}"
   done
   syms=$symsPurged
fi

echo syms after purge $syms
#exit 1

for s in $syms; do
   touch "${bestAlgosDir}/${s}${inEx}" || echo cant create "${bestAlgosDir}/${s}${inEx}"
done

for t in $(echo "1 3 5"); do
   for a in $testModDBAlgos; do
      for s in $(echo $syms); do
         #echo Running all best algos for ${s}...
         
         pattern="TB${t}%_${a}"
         
         for b in $(echo "DB IR"); do
            echo $a | grep -q $b
            if [[ $? == 0 ]]; then
               pattern="TB${t}%_${a}%"
               break
            fi
         done
         
         echo DB search pattern: $pattern $s

         #cmd="${wp}/scripts/getDBVal.sh all $pattern $s $ss n d"
         cmd="${wp}/scripts/getDBVal.sh all $pattern $s $ss"
                  
         #echo $cmd
         
         # Ignore any results that were negative
         res=$($cmd)
         for r in $(echo $res); do
            echo $r | grep -q "-"
            if [[ $? == 0 ]]; then
               continue
            fi
            echo $r >> $tmpFile2
         done
         tail -${ss} $tmpFile2 >> $tmpFile
         rm -f $tmpFile2
         tmpFile2=$(getRandomTmpFile)
         #$cmd >> $tmpFile
      done
   done
done

if [[ ! -f $tmpFile ]]; then 
   echo No data found in the DBs for ${s}, exiting...
   exit 1
fi

if [[ -f "$bestAlgosDir/${s}.in" ]]; then
   mv "$bestAlgosDir/${s}.in" "$bestAlgosDir/${s}.$$.in"
fi

rm -f ${tmpFile2}_*
tmpFile2=$(getRandomTmpFile)
cat $tmpFile

for line in $(cat $tmpFile); do
   a=$(echo $line | awk -F\| '{print $2}')
   s=$(echo $line | awk -F\| '{print $1}')
   run.sh "" $a $s | grep Gain >> ${tmpFile2}_${s}
   tail -1 ${tmpFile2}_${s} >> "/tmp/${s}.inTmp"
   tail -1 ${tmpFile2}_${s}
done

for s in $(echo $syms); do
   sort -n -k4,4 "/tmp/${s}.inTmp" > "$bestAlgosDir/${s}.in"
   #sort -n -k4,4 ${tmpFile2}_${s} > "$bestAlgosDir/${s}.in"
   tail -n $dbNumBestRows "$bestAlgosDir/${s}.in"
   rm -f "/tmp/${s}.inTmp"
done

#${wp}/scripts/dbStopAll.sh

exit 0