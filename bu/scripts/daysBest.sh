#!/bin/bash

## daysBest.sh
## rank stocks in order of $$'s won per days / num of days
##   and a score. Score closest to 1 is best
## ZY $10 / 5 days = $2 per day
## ZY score: $2 * 5 / 13.50 = 0.740740740740741
## AMZN: $8.07 * 92 = 742 
## AMZN score: $8.07 * 92 / last = 0.222021531100478
## "AMZN $8.07 92 days last price 3343.63"

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
   
   magicNumFlag="yes"
   
   tail -q -n 1 bestAlgos/*.bs| awk '{print $1, $4, $9}' | sed "/.*e-*/d" | sed "/Gain\:/d" | sed "/[a-z].*/d" > $stkpriceDayFile
   
}

init $1 $2

for token in $(cat $stkpriceDayFile); do

   if [[ $token =~ [A-Z]\.* ]]; then
      stock=$token
      continue
   fi
   
   if [[ $token =~ .*\..* ]]; then
      price=$token
      continue
   fi
   
   days=$token
   
   echo $stock $price $days >> /tmp/tt
   
   if [[ $days != 0 ]]; then
      perDayPrice=$(echo "scale=2 ; $price / $days" | bc -l)
   fi
   
   lastPrice=""
   magicNum="YoU sHoUlDn'T SeE ThIs"
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
   
   if [[ -n $magicNumFlag ]]; then
      if [[ $days != 0 ]]; then
         magicNum=$(echo "scale=3 ; $perDayPrice / $lastPrice * $days" | bc)
         # magicNum=$(echo "scale=3 ; $perDayPrice * $days / $lastPrice" | bc)
      else
         continue
      fi
   fi
   echo $stock $perDayPrice $days $lastPrice $magicNum >> $ppdOut
   echo $stock $perDayPrice $days $lastPrice $magicNum
   
done

sort -r -n  -k 5,5 -k 2,2 $ppdOut > "daysBest/daysBest.mn.${dt}"
sort -r -n -k 2,2 $ppdOut > "daysBest/daysBest.db.${dt}"

rm -f daysBest/latest || echo cant remove daysBest/latest
rm -f daysBest/latestMN || echo cant remove daysBest/latestMN

ln -s "daysBest.db.${dt}" "daysBest/latest"
ln -s "daysBest.mn.${dt}" "daysBest/latestMN"

exit 0

