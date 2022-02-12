#!/bin/bash

## redoTests.sh
## Redo tests using parallel mode
  
function init {

   stockCL=noTest=""
   
   wp=$(pwd)
   
   # Only do tests for stocks before 20210810
   startDt="20210810"
   dt=$(date "+%Y%m%d")
   days=$(echo $dt - $startDt | bc -l)
   
   stockCL=$1
   noTest=$2
   
   
   log="docs/processedStocks"
   
   cd bestAlgos
   if [[ -z $stockCL ]]; then
      stocks=$(find . -mtime +${days} -ls|grep "bs$"|awk '{print $11}'|sed "s/\.\///"|sed "s/\.bs//"|sort -r)
   else
      stocks=$stockCL
   fi

   cd ..
}

#init $1 $2

days=$(ls test)

for day in $days; do
   scripts/keepAliveM.sh $day
done

exit 0

