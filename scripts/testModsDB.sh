#!/bin/bash
 
function init {

   day=""
   sym=""

   day=$1
   sym=$2
   
   $HOME/bin/lplt.sh

   wp="/Users/tsk/w/lplTrade"
   
   . $wp/scripts/db.sh

   #xattr -d com.apple.quarantine scripts/* > /dev/null 2>&1
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   run="${wp}/scripts/run.sh"
   
   today=$(date "+%Y%m%d")
      
   tmpFile=$(getTmpFile $sym)
      
   symProvided=0
   
   if [[ -n $sym ]]; then
      syms=$sym 
      symProvided=1
   fi

   if [[ -n $day ]]; then
      days=$day
   else
      days=$(ls $testDir | awk '{print $1}')
   fi
   
   if [[ -f $tmpFile ]]; then
      rm -f $tmpFile
   fi
}

init $1 $2

numModifiers=$(echo $testModDBAlgos | tr -cd ' ' | wc -c)
numModifiers=$(echo "$(($numModifiers + 1))")
numModTests=$(echo "$(($numModifiers * $dbMaxModTestRows))")

# Make sure test DB is up and running
isDBRunning $day
if [[ $? == 0 ]]; then
   port=$(getNextPort)
   echo Starting DB $day
   startDB $day $port || exit 1
else
   port=$(getRunningPort $day)
fi

echo PORT $port

# Make sure master DB is up and running
#isDBRunning "master"
#if [[ $? == 0 ]]; then
#   masterPort=$(getNextPort)
#   echo Starting DB master
#   startDB "master" $masterPort
#else
#   masterPort=$(getRunningPort "master")
#fi

# Take the best 10 algos for today and attach modifier algo and run for today 

cl=$(getCL $port $dbName)

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
for day in $days; do
   
   echo Running $dbAlgoModTestName for $day
   
   if (( ! symProvided )); then
      syms=$($cl "select distinct sym from algoData order by sym asc")
      #syms=$(runSQL $cl "select distinct sym from algoData order by sym asc")
      
      if (( $? != 0 )); then
         echo "psql failed to get data items"
         exit $rv
      fi
   fi

   echo Symbols being tested: $syms
      
   for sym in $syms; do
      
      # check if mod tests are complete and skip
      #count=$($cl "SELECT count(algo) FROM algoModData where sym = '${sym}'")
      modTestsRan=0      
      modTestsRan=$($cl "select count(algo) from algoModData where sym = '${sym}'")            
      
      if (( $modTestsRan >= $numModTests )); then
         echo $day ${sym} COMPLETE! ${modTestsRan} ran out of max  $numModTests
         continue
      fi
      
      echo Detected $modTestsRan ran out of max $numModTests
      
      algos=$($cl "select algo from algoData where sym = '${sym}' order by gain,winpct asc" | tail -${dbMaxModTestRows})
            
      echo Running algos for ${sym}...
      for a in $algos; do echo $a; done
      
      if (( $? != 0 )); then
         echo "psql failed to get data items"
         exit 1
      fi
               
      for algo in ${algos}; do
         for mod in $testModDBAlgos; do
            modifiedAlgo="${algo}_${mod}"

            # Get number of decision bars and add range value to IR
            tbv=$(echo $modifiedAlgo | awk -F_ '{print $1}' | sed 's/TB//')
         
            if (( tbv == 1 )); then 
               mtbv="5"
               dtbv="30"
            elif (( tbv == 2 )); then 
               mtbv="4"
               dtbv="15"
            elif (( tbv == 3 )); then 
               mtbv="3"
               dtbv="10"
            elif (( tbv == 4 )); then 
               mtbv="2"
               dtbv="8"
            elif (( tbv == 5 )); then 
               mtbv="1"
               dtbv="6"
            fi
            
            ctbv=${mod: -2}
      
            if [[ $ctbv == "IR" ]]; then
               aMod=${modifiedAlgo}${mtbv} 
               modifiedAlgo=$aMod
            elif [[ $ctbv == "DB" ]]; then
               aMod=${modifiedAlgo}${dtbv} 
               modifiedAlgo=$aMod
            else
               modifiedAlgo="${algo}_${mod}"
            fi
      
            algoDB=$(modAlgosCaseAlreadyRan $sym $modifiedAlgo $day)
            
            if [[ $algoDB == $modifiedAlgo ]]; then
               echo $day $sym $modifiedAlgo skipping...
               continue
            fi 
                        
            ${py3} ${wp}/bin/profileGenerator.py -d $day -a $modifiedAlgo -s $sym
            
            cmd="${py3} ${wp}/bin/lpltSlave.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json_${sym} -w test/${day} -o -d -s $sym"
            
            $cmd > /tmp/out 2>&1
            
            gain=$(tail -1 ${wp}/test/${day}/logs/active${sym}.ls | awk '{print $4}')
            winPct=$(tail -1 ${wp}/test/${day}/logs/active${sym}.ls | awk '{print $5}'| sed "s/%//")
            if [[ -z $gain ]] || [[ $gain == "" ]] || [[ $gain == " " ]]; then
               gain=0
            fi
            
            if [[ -z $winPct ]] || [[ $winPct == "" ]] || [[ $winPct == " " ]]; then
               winPct=0
            fi
            
            echo $day $sym \$${gain} ${winPct}% $modifiedAlgo
                        
            $cl "INSERT INTO algoModData (sym, algo, gain, winPct) VALUES ('${sym}', '${modifiedAlgo}', '${gain}', '${winPct}')"

         done
      done
   done
done

exit 0