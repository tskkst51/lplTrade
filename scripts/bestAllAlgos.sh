#!/bin/bash

## Find the best algo's across all days

function init {

   #wp="/Users/tsk/w/lplTrade"
   wp=$(pwd)

   . ${wp}/scripts/db.sh
   
   $HOME/bin/lplt.sh

   sym=$1
   ss=$2
   debug=$3
   
   syms=$sym
   if [[ $sym == "all" ]]; then 
      syms=$(getBestSymsFile); 
   else
      syms=$sym
   fi
      
   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
      
   if [[ -n $debug ]] && [[ $debug != "d" ]]; then debug=""; fi
   if [[ -f $tmpFile ]]; then rm -f $tmpFile ; fi
   if [[ -n $ss ]]; then dbNumModTestRows=$ss ; fi
   
}

init $1 $2 $3

if [[ -n $debug ]]; then
   echo Getting data for ${syms}...
fi

tmpFile=$(getRandomTmpFile)
tmpFile2=$(getRandomTmpFile)

testDBAlgos=$testModDBAlgos

for t in $(echo "1 3 5"); do
   for a in $testDBAlgos; do
      for s in $syms; do
         #echo Running all best algos for ${s}...
         
         pattern="TB${t}%_${a}"
         
         for b in $(echo "DB IR"); do
            echo $a | grep -q $b
            if [[ $? == 0 ]]; then
               pattern="TB${t}%_${a}%"
               break
            fi
         done
         
         echo DB search pattern: $pattern

         cmd="${wp}/scripts/getDBVal.sh all $pattern $s "
         
         if [[ -n $ss ]]; then
            cmd="$cmd $ss"   
         else
            cmd="$cmd $dbNumModTestRows"
         fi
         
         if [[ -n $debug ]]; then
            cmd="$cmd d"
         else
            cmd="$cmd n"
         fi
         
         cmd="$cmd dontStopDB"
         echo $cmd

         # Ignore any results that were negative
         res=$($cmd)
         for r in $(echo $res); do
            echo $r | grep -q "-"
            if [[ $? == 0 ]]; then
               continue
            fi
            echo $r >> $tmpFile
         done
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

for algo in $(awk -F\| '{print $2}' $tmpFile); do
   #if [[ -n $debug ]]; then echo Running algo $algo; fi
   #echo Running algo $algo
   run.sh "" $algo $s | grep Gain >> $tmpFile2
   tail -1 $tmpFile2
done

sort -n -k4,4 $tmpFile2 > "$bestAlgosDir/${s}.in"
tail -n $dbNumBestRows "$bestAlgosDir/${s}.in"

exit 0