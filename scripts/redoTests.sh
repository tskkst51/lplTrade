#!/bin/bash

## redoTests.sh
## Redo tests, results and best Algos. Resume where left off

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

init $1 $2

for stock in $stocks; do

   #echo stock $stock

   if [[ -z $stockCL ]]; then
      if skipStocks $stock; then
         echo skipped stock ${stock}...
         continue
      fi
   fi
       
   echo processing stock ${stock}...
   
   exitFiles="${wp}/exitResults/${stock}*"
   reFiles="${wp}/totalResults/${stock}\.*"
   bestFiles="${wp}/bestAlgos/${stock}\.*"
   
   if [[ -z $noTest ]]; then
      rm $exitFiles || echo exit results dont exist 
   fi
   
   rm $reFiles || echo exit total results dont exist
   rm $bestFiles || echo exit best algo results dont exist
   
   echo $stock >> $log

   if [[ -z $noTest ]]; then
      echo Running tests for ${stock}...
      test.sh "" "" $stock || echo failed running tests
   fi
   
   echo Running results for ${stock}...
   results.sh $stock || echo failed running results
   
   echo Running best algos for ${stock}...
   findBestAlgos.sh $stock || echo failed running best algos 
done

exit 0

