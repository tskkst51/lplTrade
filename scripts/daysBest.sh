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

   wp=$(pwd)

   . ${wp}/scripts/db.sh

   ex=$1
   
   if [[ -z $ex ]]; then
      ex="in"
   fi
   
   echo Using bestAlgo extension: $ex
   
   dt=$(date "+%Y%m%d")

   ppdOut="/tmp/perDayPrice"
   stkpriceDayFile="/tmp/stkpriceDayFile"
   
   rm -f $ppdOut
   
   wp=$(pwd)
   
   bestFiles=$(getRandomTmpFile)
   stkpriceDayFile=$(getRandomTmpFile)
   
   magicNumFlag="yes"
   
   ls bestAlgos/*.${ex}| grep -v -e "[0-9]" >> $bestFiles
   
   #cat $bestFiles
   #exit 1
   
   for b in $(cat $bestFiles); do
      tail -q -n 1 $b | awk '{print $1, $4, $9}' | sed "/.*e-*/d" | sed "/Gain\:/d" | sed "/[a-z].*/d" >> $stkpriceDayFile
   done
   
   minPrice=0.0
   minPrice=$(grep minStockPrice $liveConfig | awk -F\" '{print $4}')

}

init $1

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
         
   if [[ -z $lastPrice ]]; then
      # look for last price in minute charts
      minuteChart=$(ls test/*/bc/*${stock}.bc|awk -F, 'END{print}')
      if [[ -n $minuteChart ]]; then
         lastPrice=$(tail -1 $minuteChart |awk -F, '{print $4}')
      else
         echo minuteChart $minuteChart does not exist

      fi
   fi

   if [[ $(echo "$lastPrice < $minPrice" | bc) == 1 ]]; then
      echo ${stock} excluded. Price $lastPrice is less than $minPrice
      continue
   fi

   if [[ -n $magicNumFlag ]]; then
      if [[ $days != 0 ]]; then
         magicNum=$(echo "scale=3 ; $perDayPrice / $lastPrice * $days" | bc)
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

