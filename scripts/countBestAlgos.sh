#!/bin/bash

## Find the best algo's across all days

function init {

   #wp="/Users/tsk/w/lplTrade"
   wp=$(pwd)

   . ${wp}/scripts/db.sh
   
   $HOME/bin/lplt.sh

   sym=$1
   sortPct=$2
   
   syms=$sym
   if [[ $sym == "all" ]]; then 
      syms=$(getBestSymsFile); 
   else
      syms=$sym
   fi
      
   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
      
   sortCol="4,4 -k7,7"

   if [[ -n $debug ]]; then echo syms: $syms; fi
   if [[ -f $tmpFile ]]; then rm -f $tmpFile ; fi
   if [[ -n $ss ]]; then dbNumModTestRows=$ss ; fi
   if [[ -n $sortPct ]] && [[ $sortPct == "a" ]]; then sortCol="14,14 -k7,7" ; fi
   if [[ -n $sortPct ]] && [[ $sortPct == "p" ]]; then sortCol="7,7 -k4,4" ; fi
   
   
}

init $1 $2 $3

if [[ -n $debug ]]; then
   echo Counting successful algos ${syms}...
fi

tmpFile=$(getRandomTmpFile)
tmpFile2=$(getRandomTmpFile)

for s in $syms; do
   for a in $testModDBAlgos; do      
      grep "_${a}" "bestAlgos/${s}.ds" | grep -v -e "-" | awk '{print $4, $7, $9}' > "${tmpFile}_${a}"
      grep "_${a}" "bestAlgos/${s}.ds" | awk '{print $4, $7, $9}' > "${tmpFile}_${a}_all"
   done
done

for a in $testModDBAlgos; do
   if [[ ! -s "${tmpFile}_${a}" ]]; then continue; fi
   totPrice=$(awk '{s+=$1} END {print s}' "${tmpFile}_${a}")
   totPriceAll=$(awk '{s+=$1} END {print s}' "${tmpFile}_${a}_all")
   numPrices=$(tail -n 1 "${tmpFile}_${a}" | awk '{print $3}')
   numWins=$(wc -l "${tmpFile}_${a}" | awk '{print $1}')
   numPct=$(awk '{s+=$2} END {print s}' "${tmpFile}_${a}")
   avgPrice=$(echo "scale=2 ; $totPrice / $numWins" | bc)
   avgPriceAll=$(echo "scale=2 ; $totPriceAll / $numWins" | bc)
   avgPct=$(echo "scale=2 ; $numPct / $numWins" | bc)
   echo $a avg gain: $avgPrice avg % $avgPct in $numPrices days avg gain all: $avgPriceAll >> $tmpFile2
done

sort -n -k${sortCol} $tmpFile2
#rm $tmpFile $tmpFile2

exit 0