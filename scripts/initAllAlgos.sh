#!/bin/bash

## Initialize the best algo's across one day. This runs the exhaustive bestAllDBs.sh

function init {

   #wp="/Users/tsk/w/lplTrade"
   wp=$(pwd)

   . ${wp}/scripts/db.sh
   
   $HOME/bin/lplt.sh

   incDBNum=0
   reduceNumDBs=""
   
   sym=$1
   ss=$2
   debug=$3
   reduceNumDBs=$4
   overideInits=$5

   syms=$(getAllSyms "all")
   
   if [[ $sym != "" ]]; then 
      syms=$sym
   fi

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
      
   if [[ -z $ss ]]; then ss=$dbNumModTestRows ; fi
   if [[ $overideInits != "o" ]]; then overideInits="" ; fi
   if [[ -n $reduceNumDBs ]]; then incDBNum=$reduceNumDBs; else incDBNum=$incDBNums ; fi
   if [[ -n $debug ]] && [[ $debug != "d" ]]; then debug="n"; fi
   
   echo day $day
   echo ss $ss
   echo overideInits $overideInits
   echo syms $syms
   echo debug $debug
   echo incDBNum $incDBNum
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
         echo removing ${s}${inEx} 
         rm ${bestAlgosDir}/${s}${inEx}
         #continue
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

days=$(getAllDays $sym)
ctr=0

# Only run on the last $reduceNumDBs days
if (( incDBNum > 0 )); then
   numDays=$(echo $days | tr -cd ' ' | wc -c)
   loopCtr=$(echo "$numDays - $incDBNum + 1" | bc)
   for d in $(echo $days); do
      # Skip total - n
      ctr=$(echo "$(($ctr + 1))")
      if (( ctr <= loopCtr )); then
         if [[ -n $debug ]]; then echo skipping $d; fi
         continue
      fi
      newDays="$newDays $d"
   done
   days=$newDays
fi

if [[ -n $debug ]]; then echo Running days: $days; fi


for t in $(echo "1 3 5"); do
   #for a in $testModDBAlgos; do
      for s in $(echo $syms); do
         #echo Running all best algos for ${s}...
         
         #pattern="TB${t}%_${a}"
         pattern="TB${t}%"
         
         for b in $(echo "DB IR"); do
            echo $a | grep -q $b
            if [[ $? == 0 ]]; then
               pattern="TB${t}%_${a}%"
               break
            fi
         done
         
         echo DB search pattern: $pattern $s

         #cmd="${wp}/scripts/getDBVal.sh all $pattern $s $ss"
         cmd="${wp}/scripts/getDBVal.sh all $pattern $s $ss $incDBNum $debug p dontStopDB"
         cmd2="${wp}/scripts/getDBVal.sh all $pattern $s $ss $incDBNum $debug w dontStopDB"

         if [[ $debug == "d" ]]; then echo $cmd; echo $cmd2; fi
         
         # Ignore any results that were negative
         res=$($cmd)
         res2=$($cmd2)
         if [[ $debug == "d" ]]; then echo res $res; echo res2 $res2; fi

         for r in $(echo $res $res2); do
            echo $r | grep \|TB
            if [[ $? == 1 ]]; then
               continue
            fi
            if [[ $debug == "d" ]]; then echo "res $r >> $tmpFile2"; fi
            echo $r >> $tmpFile2
         done
#         tail -${ss} $tmpFile2 >> $tmpFile
#         rm -f $tmpFile2
#         tmpFile2=$(getRandomTmpFile)
         
         #$cmd >> $tmpFile
      done
   #done
done

if [[ ! -f $tmpFile2 ]]; then 
   echo No data found in the DBs for ${s}, exiting...
   exit 1
fi

if [[ -f "$bestAlgosDir/${s}.in" ]]; then
   mv "$bestAlgosDir/${s}.in" "$bestAlgosDir/${s}.$$.in"
fi

if [[ -f "$bestAlgosDir/${s}.pc" ]]; then
   mv "$bestAlgosDir/${s}.pc" "$bestAlgosDir/${s}.$$.pc"
fi

#rm -f ${tmpFile2}_*

# Get rid of dups
sort -u -t\| -k3,3 $tmpFile2 >> $tmpFile
rm -f $tmpFile2

tmpFile2=$(getRandomTmpFile)

echo Running $(wc -l $tmpFile) algos
for line in $(cat $tmpFile); do
   s=$(echo $line | awk -F\| '{print $1}')
   a=$(echo $line | awk -F\| '{print $2}')
#   for d in echo $days; do
#      run.sh $d $a $s | grep Gain >> ${tmpFile2}_${s}
#   done

   # Do we run all days or just 10 or so?
   run.sh \\"$days\\" $a $s | grep Gain >> ${tmpFile2}_${s}
   #run.sh "" $a $s | grep Gain >> ${tmpFile2}_${s}
   tail -1 ${tmpFile2}_${s}
   
   # Add DU, DL and AS to all algos
   for aa in $(echo $addedAlgos); do
      if $(echo $a | grep -q $aa); then
         if [[ -n $debug ]]; then echo $aa found in $a skipping...; fi
         continue
      fi
      
      ab=${a}_${aa}
      if [[ -n $debug ]]; then echo Running $ab $aa; fi
      if [[ -n $debug ]]; then echo Run cmd redirecting to ${tmpFile2}_${s}; fi
      run.sh \\"$days\\" $ab $s | grep Gain >> ${tmpFile2}_${s}
      tail -1 ${tmpFile2}_${s}
      #run.sh "" $a $s | grep Gain >> ${tmpFile2}_${s}
   done
done

for s in $(echo $syms); do
   echo Creating $bestAlgosDir/${s} in and pc files...
   sort -n -k4,4 -k7,7 ${tmpFile2}_${s} > "$bestAlgosDir/${s}.in"
   sort -n -k9,9 -k7,7 -k4,4 ${tmpFile2}_${s} > "$bestAlgosDir/${s}.pc"
   #sort -n -k4,4 ${tmpFile2}_${s} > "$bestAlgosDir/${s}.in"
   echo Best based on price...
   tail -n $dbNumBestRows "$bestAlgosDir/${s}.in"
   echo Best based on percent...
   tail -n $dbNumBestRows "$bestAlgosDir/${s}.pc"
   rm -f ${tmpFile2}_${s}
done

#${wp}/scripts/dbStopAll.sh

exit 0
