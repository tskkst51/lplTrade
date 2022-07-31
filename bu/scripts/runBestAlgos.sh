#!/bin/bash
 
function init {

   $HOME/bin/lplt.sh

   #xattr -d com.apple.quarantine scripts/* > /dev/null 2>&1
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   run="${wp}/scripts/run.sh"

   testDir="test"
   numRows=10
   
   today=$(date "+%Y%m%d")
   
   stock=$1
   
   tmpFile="/tmp/tmp.rd"
   resultsPath="${resultsDir}/${stock}.tr"

   if [[ -n $stock ]]; then
      stocks=$stock 
   else
      stocksNotProvided="yes"  
   fi

   days=$(ls $testDir | awk '{print $1}')
   
   if [[ -f $tmpFile ]]; then
      rm -f $tmpFile
   fi
   
   pl="psql algos -q -o $tmpFile -t -c '\a' -c "
   plN="psql algos -q -t -c '\a' -c "
}

init $1

# Take the best $numRows algos for all days and run for all days 

echo $days
for day in $days; do
      if [[ -n $stocksNotProvided ]]; then
         stocks=$("${pln} select distinct sym from algoModData where liveDate = '${day}' order by sym asc")
         #stocks=$(cat $tmpFile)
      fi
      
      if (( $? != 0 )); then
         echo "psql failed to get data items"
         exit 1
      fi

   for stock in $stocks; do
      
      "${pl} select algo from algoData where liveDate = '${day}' and sym = '${stock}' order by gain,winpct asc";
      
      if (( $? != 0 )); then
         echo "psql failed to get data items"
         exit 1
      fi
   
      algos=$(tail -n $numRows $tmpFile)
   
      #echo $algos
         
      for algo in ${algos}; do
         for mod in ${algoModifiers[*]}; do
   #         if [[ $mod == "IR" ]]; then
   #            mod="${mod}4"
   #         fi
            testAlgo="${algo}_${mod}"
   
            "${pCmd} select sym from algoModData where sym = '${stock}' and liveDate = '${day}' and algo = '${testAlgo}'"
   
            if [[ -s $tmpFile ]]; then
               echo skipping $day $stock $testAlgo already ran
               continue
            fi
   
            #$run $day $testAlgo $stock >> ${cwd}/bestAlgos/${stock}.all
            
            ${py3} ${wp}/bin/profileGenerator.py -d $day -a $testAlgo
            
            cmd="${py3} ${wp}/bin/lpltSlave.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json -w test/${day} -o -d -s $stock"
            
            $cmd > /tmp/out 2>&1
            
            gain=$(tail -1 ${wp}/test/${day}/logs/active${stock}.ls | awk '{print $4}')
            winPct=$(tail -1 ${wp}/test/${day}/logs/active${stock}.ls | awk '{print $5}'| sed "s/%//")
            
            if [[ -z $gain ]]; then
               gain=0
               winPct=0
            fi
            
            echo $day $stock gain: \$${gain} ${winPct}% $testAlgo
   
            "${pCmd} INSERT INTO algoModData (sym, liveDate, algo, gain, winPct) VALUES ('${stock}', '${day}', '${testAlgo}', '${gain}', '${winPct}')"
            if (( $? == 1 )); then
               echo "psql failed duplicate"
            fi
         done
      done
   done   
done

exit 0




         # Get NUMROWS of best gain and %,
         # run the best against all other days
         
         "${pCmd} select * from algoModData where liveDate = '${day}' and sym = '${stock}' and liveDate = '${day}' order by gain,winpct"
         if (( $? != 0 )); then
            echo "psql failed..."
         fi

         if [[ -f $tmpFile ]]; then
            dbValues=$(tail -${numRows} | awk '{print}')
         fi
         
#         for dbv in $dbValues; do
#         
#         done

