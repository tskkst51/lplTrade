#!/bin/bash

## ReRun tests. Use when algo has changed due to a bug.
## e.g. dv DATE %ALGO% SYM
##

wp="/Users/tsk/w/lplTrade"
cd $wp || exit 1

sym=$1
numTests=$2
d=$3

if [[ -z $sym ]]; then
   echo no SYM provided.
   exit 1
fi

if [[ -n $d ]]; then
   d=1.
fi

numProcesses=10

if [[ -z $numTests ]]; then
   numTests=20
fi

ctr=0
pdCtr=""
rm -f "/tmp/reRun*"

echo Running tests for $sym

for d in $(ls test/*/bc/active${sym}.bc | awk -F\/ '{print $2}'|sort -r|head -${numTests}); do

   if [[ ! -f db/${d}/log ]]; then continue; fi

   ctr=$((ctr+1))
   if (( d )); then 
      echo  "keepAliveDB.sh $d $sym 1>/tmp/reRun.txt 2>&1 &"
   fi
   # Start the processes in parallel...
   keepAliveDB.sh $d $sym 1>>/tmp/reRun_${ctr}.txt 2>&1 &
   #keepAliveDB.sh $d $sym 1>/dev/null 2>&1 &
   pdCtr="$pdCtr $!"
   echo pid started $!
   mod=$(echo "$ctr % $numProcesses" | bc)
   echo mod $mod
   if [[ $mod == 0 ]]; then
      pd=
      echo "in $ctr % $numTests"
      for pd in $pdCtr; do
         # Wait for processes to finish...
         echo waiting for pid $pd to finish...
         wait $pd
         if [[ $? != 0 ]]; then
            echo error pid $pd
         else
            echo "   ending pid $pd"
         fi
      done
   fi
done


echo "All tests completed... "
#echo "Running initAllAlgos... "
${wp}/scripts/initAllAlgos.sh $sym

exit 0