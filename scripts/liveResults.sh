#!/bin/bash

## Run the test trading program with the results from a days test results to find the best

dt=""
lplt=""

dt=$1
lplt=$2

#wp=$(pwd)
wp="/Users/tsk/w/lplTrade"

#$HOME/bin/lplt.sh

host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
elif [[ $host == "mm" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"


if [[ -z $dt ]]; then
   day=$(date "+%Y%m%d")
else
   day=$dt
fi

outFile="docs/postResults.po"

bcPath="test/${day}/bc"
bestPath="bestAlgos"
tgtPath="daysBest/postResults${day}.po"
orderPath="test/${day}/logs/stockOrder.ll"

stocks=$(ls $bcPath | sed "s/active//" | sed "s/\.bc//")

if [[ -z $stocks ]]; then
   echo $dt doesnt exist
   exit 1 
fi
tmpPath="/tmp/db"

rm -f $tgtPath $tmpPath

for stock in $stocks; do
   # Skip if 0 length file
   if [[ ! -s "${bcPath}/active${stock}.bc" ]]; then
      continue
   fi
   
   algo="\"\""
   
   if [[ -f "${bestPath}/${stock}.bs" ]]; then
      algo=$(tail -1 ${bestPath}/${stock}.bs | awk '{print $13}')
   else
      # Default found in preMarket.py: defaultAlgorithm
      algo="TB1_HS_QM_OB2_OS2_CB3_CS3_DB30_IT_TS"
   fi
   
   order=$(grep $stock $orderPath | awk '{print $2}')
   
   if [[ -n $lplt ]]; then
      #run.sh $day $algo $stock "lplt" | sed '/^[0-9].*/d; /^\-.*/d; /^on.*/d' >> $tgtPath
      runRes=$(run.sh $day $algo $stock "lplt" | sed '/^[0-9].*/d; /^\-.*/d; /^on.*/d')
   else
      #run.sh $day $algo $stock | sed '/^[0-9].*/d; /^\-.*/d; /^on.*/d' >> $tgtPath
      runRes=$(run.sh $day $algo $stock | sed '/^[0-9].*/d; /^\-.*/d; /^on.*/d')
   fi
   echo $runRes $order >> $tgtPath
done

sort -n -k4,4 $tgtPath > $tmpPath
mv $tmpPath $tgtPath || cant move $tgtPath

totalWon=$(awk '{s+=$4} END {print s}' $tgtPath)
numStocks=$(wc -l $tgtPath | awk '{print $1}')

echo Days gain with $numStocks stocks: $totalWon >> $tgtPath
echo Days gain with $numStocks stocks: $totalWon

exit 0

