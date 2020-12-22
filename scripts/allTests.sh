#!/bin/bash

## Run the test script for each date

loc=""
algo=""
stock=""
report=""

loc=$1
algo=$2
stock=$3
report=$4

wp=$(pwd)

testCmd="${wp}/scripts/test.sh "

host=$(hostname -s)

dt=$(date "+%H%M_%m%d%Y")

testPaths=$(ls test) 

#   "HL,HS,QM,VM" 
#   "EO,EC,QM,VM"
#   "EO,EC,QM,VM,PT,HM,RV"
#   "HS,IT"

if [[ -n $algo ]]; then
   algos=($algo)
else
   algos=(
   "HS,AV,QM"
   "HS,AL,QM"
   "HS,AL,AV,QM"
   "HS,HL,AV,QM"
   "HS,HL,AL,QM"
   "EO,EC,AV,QM"
   )
fi

set -m

if [[ -z $report ]]; then
   testPaths=$loc
   for algo in $algos; do
      for testPath in $testPaths; do
         
         trap - SIGINT
         a=$(echo $algo | sed 's/,/_/g')
      
         logFile="${testResults}/${testPath}/${stock}_${a}_${dt}/out.log"
         #testIt="${testCmd} ${testPath} ${algo} ${stock} > $logFile 2>&1"
         
         testIt="${testCmd} ${testPath} ${algo} ${stock}"
      
         echo Testing ${testIt}...
         
         $testIt
      done
   done
fi

# Parse the results and try to find winning algos

if [[ -n $algo ]]; then
   path="${wp}/exitResults/${stock}*${algo}*"
else
   path="${wp}/exitResults/${stock}_TB*"
fi

exitPaths=$(ls $path) 

totalResults="${wp}/totalResults"

testResults="${wp}/resultsTest"

if [[ ! -d $testResults ]]; then
   mkdir $testResults
fi

if [[ ! -d $totalResults ]]; then
   mkdir $totalResults
fi

for exitPath in $exitPaths; do   
   
   algo=$(awk '{print $6}' $exitPath | head -1)

   lastP=$(awk '{print $3}' $exitPath | head -1)
   
   days=$(wc -l $exitPath | awk '{print $1}')
   price=$(awk '{s+=$4} END {print s}' $exitPath)
   pctWinsDay=$(awk '{s+=$5} END {print s}' $exitPath)
      
   losses=$(grep \- $exitPath | wc -l | awk '{print $1}')
   wins=$(grep -v \- $exitPath | wc -l | awk '{print $1}')
   
   if (( wins > losses  )); then
      algosWon=$(echo "scale=2 ; $pctWinsDay / $days * 100" | bc)
   else
      algosWon=$(echo "scale=2 ; $pctWinsDay / $days * 100" | bc)      
   fi
   
   winLossMsg="win %"

   if (( losses == 0 )); then
      winLossPct="100"
   elif (( wins == 0 )); then
      winLossPct="0"
   else
      winLossPct=$(echo "scale=2 ; $wins / $days * 100" | bc)
   fi
   
   echo "$stock $lastP $algo \$ $price in $days days $winLossMsg $winLossPct "
   echo $stock $lastP $algo \$ $price in $days days $winLossMsg $winLossPct >> ${totalResults}/${stock}_${dt}
done

exit 0

