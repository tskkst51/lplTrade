#!/bin/bash

## Iterate over the exitResults dir and keep results in totalResults dir for 
## premarket usage for finding best algo.

# Format of totalResults file:
# BA: Best algo found for all dates based on $ amount won
# BD: Best algo for the day based on $ amount won
# BT: Algo and time bar found the most 
# BP: Best algo percentage over time 
#   AAPL.tr:
#     TYPE DATE     ALGO                       PCT AMT  DAYS
#     BA   10292020 TB3_HS_QM_OB2_OS2_CB3_CS3  70% 3.05 77
#     BD   12222020 TB2_HS_QM_OB1_OS1_CB3_CS3  75% 1.25 1
#                                             BEST TIME BAR DAYS
#     BT   "      " HS_QM                     TB5           33
#                                             % WIN DAYS
#     BP   "      " HS_QM                     75 %   77
 
function init {

   wp=$(pwd)
   

   testDir="test"
   numRows=10

   dates=$(ls $testDir | awk '{print $1}')
   
   today=$(date "+%Y%m%d")
   
   cd $exDir || exit 1
   
   stock=$1
      
   host=$(hostname -s|awk '{print $1}')
   
   tmpFile="/tmp/${stock}.rs"
   tmpFile2="/tmp/${stock}2.rs"
   tmpFile3="/tmp/${stock}3.rs"
   tmpFile4="/tmp/${stock}4.rs"
   tmpFile5="/tmp/${stock}5.rs"
   resultsPath="${resultsDir}/${stock}.tr"

   files="${stock}_TB1_*ex"
   files2="${stock}_TB2_*ex"
   files3="${stock}_TB3_*ex"
   files4="${stock}_TB4_*ex"
   files5="${stock}_TB5_*ex"

   if [[ -z $stock ]]; then
      echo Must have a stock to iterate over!
      exit 1
   fi
   
   if [[ -f $tmpFile ]]; then
      rm -f $tmpFile
   fi
   
   if [[ -f $tmpFile2 ]]; then
      rm -f $tmpFile2
   fi
   
   if [[ -f $tmpFile3 ]]; then
      rm -f $tmpFile3
   fi
   
   if [[ -f $tmpFile4 ]]; then
      rm -f $tmpFile4
   fi
   
   if [[ -f $tmpFile5 ]]; then
      rm -f $tmpFile5
   fi
   
   if [[ -f $resultsPath ]]; then
      rm -f $resultsPath
   fi

   activateDir="/lplW2"

}

algoModifiers=(
"RV"
"IR"
"TR"
"AV" # avg vol close
"AL" # vol > last bar close
"VI" # avg vol open
"LI" # vol > last bar open
"QP"
"HM"
"SS"
"QL"
"DB"
"AO"
"AC"
"IT" # In position tracking
"PM" # Price movement
"TS" # Trailing stop
)

init $1

# Take the best 10 algos for today and attach modifier algo and run for today 

if [[ -z $stock ]]; then
   psql algos -q -o $tmpFile -t -c '\a' '-c select sym from algoData where liveDate=${day} order by sym asc';
   stocks=$(cat $tmpFile)
fi
   
echo $stocks

for day in $dates; do
   for stock in $stocks; do
      

   psql algos -o $tmpFile -c '\a' '-c select algo from algoData where sym=${stock} and liveDate=${day} order by winpct,gain asc';
   
   topTen=$(cat $tmpFile)

   
   if (( $? -ne 0 )); then
      echo "psql failed to get data items"
   fi
   
   tail -n $numRows $tmpFile | awk -F| 
   for ff in $files $files2 $files3 $files4 $files5; do
      echo $ff
      #$(grep -q $day $files)
      $(grep -q $day $ff)
      if (( $? == 1 )); then
         #echo Skipping ${day}. No results found
         continue
      fi
      
      if [[ ! -f $ff ]]; then
         #echo Skipping ${day}. No results found
         continue
      fi
   
      #echo day $day
      #echo files $files
      
      # Find best result given the algo on specific date
      
      #find . -type f -exec grep -l 'pattern' {} +
   
      algoPctAmt=$(grep $day $ff | sort -n -k 4 | tail -1 | awk '{print $6, $5, $4}')
      days="1"
      resultType="BD"
      resultStrBD="${resultType} ${day} ${algoPctAmt} ${days}"
      
      echo $resultStrBD | sort -n -k 5 >> $tmpFile
   done
done
exit 1

# Find the algo that appears the most in the results file
for a in ${algos[*]}; do
   algoCount=$(grep -c $a $tmpFile)
   echo "${a} ${algoCount}" >> $tmpFile2
done

bestAlgoCount=$(sort -r -n -k 2 $tmpFile2 | awk '{print $1, $2}' | head -1)
bestAlgo=$(sort -r -n -k 2 $tmpFile2 | awk '{print $1}' | head -1)

tb1=$(grep "TB1" $tmpFile | wc -l)
echo "TB1 ${tb1}" >> $tmpFile3
tb2=$(grep "TB2" $tmpFile | wc -l)
echo "TB2 ${tb2}" >> $tmpFile3
tb3=$(grep "TB3" $tmpFile | wc -l)
echo "TB3 ${tb3}" >> $tmpFile3
tb4=$(grep "TB4" $tmpFile | wc -l)
echo "TB4 ${tb4}" >> $tmpFile3
tb5=$(grep "TB5" $tmpFile | wc -l)
echo "TB5 ${tb5}" >> $tmpFile3

bTBCount=$(sort -r -n -k 2 $tmpFile3 | head -3)
bestTB=$(echo $bTBCount | awk '{print $1}' | head -1)
sortTBAlgo="${bestTB}_${bestAlgo}"
resultStrBT="BT ${bestAlgoCount} ${bTBCount}"

# Find total amt and pct won for all days
files="${stock}_TB*"
dayAmtPctAlgo=$(sort -n -k 4 $files | tail -1 | awk '{print $1, $6, $5, $4}')
winningAlgo=$(sort -n -k 4  $files | tail -1 | awk '{print $6}')
winningAlgoFile="${stock}_${winningAlgo}.ex"

days=$(cat $winningAlgoFile | wc -l)
resultType="BA"
resultStrBA="${resultType} ${dayAmtPctAlgo} ${days}"

# store total results
echo $resultStrBA > $resultsPath

grep $sortTBAlgo $tmpFile | sort -k 3 | sort -n -r -k 5 > $tmpFile4
grep -v $sortTBAlgo $tmpFile | sort -k 3 | sort -n -r -k 5 >> $tmpFile4

for path in ${files}; do
   losers=$(grep \- $path | wc -l  | awk '{print $1}')
   winners=$(grep -v \- $path | wc -l | awk '{print $1}')
   total=$(echo "scale=2 ; $winners + $losers" | bc)
   winPct=$(echo "scale=2 ; $winners / $total * 100" | bc)
   amt=$(awk '{s+=$4} END {print s}' $path)
   pathNoExt=$(echo $path | awk -F. '{print $1}')
   pathNoExt=$(echo $pathNoExt | sed "s/${stock}_//")
   echo BP $pathNoExt $winPct % $amt $total days >> $tmpFile5
done

#sort -r -n -k 5,5 -k 3,3 $tmpFile5 >> $resultsPath
sort -r -n -k 5,5 -k 6,6 -k 3,3 $tmpFile5 >> $resultsPath

cat $tmpFile4 >> $resultsPath
echo $resultStrBT >> $resultsPath

cat $resultsPath
#sort -n -k 3 $resultsPath

exit 0

