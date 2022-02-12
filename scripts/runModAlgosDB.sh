#!/bin/bash
 
function init {

   day=$1
   sym=$2
   
   $HOME/bin/lplt.sh

   . $HOME/profiles/db.sh

   #xattr -d com.apple.quarantine scripts/* > /dev/null 2>&1
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   run="${wp}/scripts/run.sh"

   testDir="test"
   numRows=10
   
   today=$(date "+%Y%m%d")
      
   tmpFile=$(getTmpFile $sym)
   
   stocksNotProvided=""
   
   if [[ -n $sym ]]; then
      syms=$sym 
   else
      stocksNotProvided="yes"  
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

algoModifiers=(
"RV"
"IR4"
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
"TR_QP_DB"
"RV_TR_DB"
"RV_AV_DB"
"RV_AL_DB"
"RV_QP_DB"
"HM_TR_DB"
"HM_AV_DB"
"HM_QP_DB"
"IT_QL_DB"
"IT_QP_DB"
"TR_IR4"
"TR_TS"
"TR_QP"
"QP_IR4"
"RV_TR"
"RV_AV"
"RV_AL"
"RV_QP"
"HM_TR"
"HM_AV"
"HM_AL"
"HM_QP"
"IT_QL"
"IT_QP"
"IT_TS"
"AO_AC"
"QP_PM"
"AV_TS"
"AL_TS"
)

init $1 $2

numModifiers=${#algoModifiers[@]}
numModTests=$(echo "$(($numModifiers * $dbNumModTestRows))")

#totNumModTests=$(expr $dbNumModTestRows * $numModifiers)

# Make sure test DB is up and running
isDBRunning $day
if [[ $? == 0 ]]; then
   port=$(getNextPort)
   echo Starting DB $day
   startDB $day $port || exit 1
else
   port=$(getRunningPort $day)
fi

# Make sure master DB is up and running
isDBRunning "master"
if [[ $? == 0 ]]; then
   masterPort=$(getNextPort)
   echo Starting DB master
   startDB "master" $masterPort
else
   masterPort=$(getRunningPort "master")
fi

# Take the best 10 algos for today and attach modifier algo and run for today 

cl=$(getCL $port $dbName)

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
for day in $days; do
   
   echo Running $dbAlgoModTestName for $day

   if [[ -n $stocksNotProvided ]]; then
      syms=$($cl "select distinct sym from algoData order by sym asc")
      
      if (( $? != 0 )); then
         echo "psql failed to get data items"
         exit $rv
      fi
   fi

   echo Symbols being tested:
   echo $syms
      
   for sym in $syms; do
      
      # check if mod tests are complete and skip
      count=$($cl "SELECT count(algo) FROM algoModData where sym = '${sym}'")
            
      modTestsRan=$($cl "select count(algo) from algoModData where sym = '${sym}'")            
      
      if (( $modTestsRan >= $numModTests )); then
         echo $day ${sym} COMPLETE! ${modTestsRan} ran out of max  $numModTests
         continue
      fi
      
      algos=$($cl "select algo from algoData where sym = '${sym}' order by gain,winpct asc" | tail -${numRows})
            
      echo Running algos for ${sym}...
      for a in $algos; do echo $a; done
      
      if (( $? != 0 )); then
         echo "psql failed to get data items"
         exit 1
      fi
               
      for algo in ${algos}; do
         for mod in ${algoModifiers[*]}; do
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
      

            algoDB=$(modAlgosCaseAlreadyRan $port $sym $modifiedAlgo)
            
            if [[ $algoDB == $modifiedAlgo ]]; then
               echo $day $sym $modifiedAlgo skipping...
               continue
            fi 
                        
            ${py3} ${wp}/bin/profileGenerator.py -d $day -a $modifiedAlgo
            
            cmd="${py3} ${wp}/bin/lpltSlave.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json -w test/${day} -o -d -s $sym"
            
            $cmd > /tmp/out 2>&1
            
            gain=$(tail -1 ${wp}/test/${day}/logs/active${sym}.ls | awk '{print $4}')
            winPct=$(tail -1 ${wp}/test/${day}/logs/active${sym}.ls | awk '{print $5}'| sed "s/%//")
            if [[ -z $gain ]]; then
               gain=0
               winPct=0
            fi
            
            echo $day $sym \$${gain} ${winPct}% $modifiedAlgo
   
            $cl "INSERT INTO algoModData (sym, algo, gain, winPct) VALUES ('${sym}', '${modifiedAlgo}', '${gain}', '${winPct}')"
            
            if (( $? != 0 )); then
               echo "psql failed duplicate"
            fi
         done
      done
   done
   
#   $cl "INSERT INTO algoModData (sym, algo, gain, winPct) VALUES ('${sym}', '${modifiedAlgo}', '${gain}', '${winPct}')"
#   
#   if (( $? != 0 )); then
#      echo "psql failed duplicate"
#   fi
done

exit 0