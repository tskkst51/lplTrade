#!/bin/bash

## daysBest.sh
## rank stocks in order of $$'s won per days / num of days
## ZY $10 / 5 days = $2 per day
## ZY score: $2 * 5 10


function skipStocks {
   
   skipStocks=$(cat $log)

   for stk in $skipStocks; do
      if [[ $1 == $stk ]]; then
         return 0
      fi
   done
   
   return 1
}
  
function init {

   dt=$(date "+%Y%m%d")

   ppdOut="/tmp/perDayPrice"
   stkpriceDayFile="/tmp/stkpriceDayFile"
   
   rm -f $ppdOut
   
   wp=$(pwd)
   
   tail -q -n 1 bestAlgos/*.bs| awk '{print $1, $4, $9}' | sed "/.*e-*/d" | sed "/Gain\:/d" | sed "/[a-z].*/d" > $stkpriceDayFile
   
}

init $1 $2

for line in $(cat $stkpriceDayFile); do

   if [[ $line =~ [A-Z]\.* ]]; then
      stock=$line
      continue
   fi
   if [[ $line =~ .*\..* ]]; then
      price=$line
      continue
   fi
   
   days=$line
   
   if [[ $days != 0 ]]; then
      perDayPrice=$(echo "scale=2 ; $price / $days" | bc -l)
   fi
   
   lastPrice=""
   if [[ -f "dc/${stock}.dc" ]]; then
      lastPrice=$(tail -1 "dc/${stock}.dc" | awk -F, '{print $4}') 2>/dev/null
   fi

   #echo lastPrice $lastPrice
   
   if [[ -z $lastPrice ]]; then
      # look for last price in minute charts
      minChart=$(ls test/*/bc/*${stock}.bc|awk -F, 'END{print}')
      if [[ -n $minChart ]]; then
         lastPrice=$(tail -1 $minChart |awk -F, '{print $4}')
      else
         echo minChart $minChart does not exist

      fi
   fi
   echo $stock $perDayPrice $days $lastPrice >> $ppdOut
   echo $stock $perDayPrice $days $lastPrice
   
done

sort -n -k 2,2 $ppdOut > "daysBest/daysBest.db.${dt}"
exit 0

