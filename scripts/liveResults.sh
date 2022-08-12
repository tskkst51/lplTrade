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

if [[ -f $tgtPath ]]; then mv $tgtPath ${tgtPath}.$$; fi

rm -f $tmpPath

for stock in $stocks; do
   # Skip if 0 length file
   if [[ ! -s "${bcPath}/active${stock}.bc" ]]; then
      continue
   fi
   
   algo="\"\""
   
   if [[ -f "${bestPath}/${stock}.bs" ]]; then
      algo=$(tail -1 ${bestPath}/${stock}.bs | awk '{print $13}')
   else
      # Default found in active.json
      algo=$(grep defaultAlgoStr profiles/active.json | awk '{print $2}' | sed "s/,//" | sed "s/\"//g")
   fi
   
   if [[ -f $orderPath ]]; then
      order=$(grep $stock $orderPath | awk '{print $2}')
   fi
   
   if [[ -n $lplt ]]; then
      runRes=$(run.sh $day $algo $stock "lplt" | sed '/^[0-9].*/d; /^\-.*/d; /^on.*/d')
   else
      runRes=$(run.sh $day $algo $stock | sed '/^[0-9].*/d; /^\-.*/d; /^on.*/d')
   fi
   echo $runRes $order >> $tgtPath
done

sort -n -k4,4 $tgtPath > $tmpPath
mv $tmpPath $tgtPath || cant move $tgtPath

totalWon=$(awk '{s+=$4} END {print s}' $tgtPath)
numStocks=$(wc -l $tgtPath | awk '{print $1}')

echo Days gain with $numStocks stocks: $totalWon $dt >> $tgtPath
echo Days gain with $numStocks stocks: $totalWon $dt

exit 0

