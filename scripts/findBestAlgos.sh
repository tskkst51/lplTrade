#!/bin/bash

## Iterate over the totalResults/results.tr file add algo modifiers to find best producing Algo

function init {

   wp=$(pwd)
   
   run="scripts/run.sh"
   resultsDir="totalResults"
   testDir="test"

   dates=$(ls $testDir | awk '{print $1}')
   
   stock=$1
   algoOveride=$2
   modProfiles=$3
   
   host=$(hostname -s)
   if [[ $host == "ML-C02C8546LVDL" ]]; then
      activateDir="/lplW"
   else
      activateDir="/venv" 
   fi

   resultsPath="${resultsDir}/${stock}.tr"
   
   if [[ -z $stock ]]; then
      echo Must have a stock to iterate over!
      exit 1
   fi
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

algoModifiersCombined=(
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
"TR_IR"
"TR_TS"
"TR_QP"
"QP_IR"
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

init $1 $2 $3

if [[ -n $algoOveride ]]; then
   echo algoOR $algoOveride
fi

if [[ -n $modProfiles ]]; then
   ${wp}/scripts/modProfiles.sh test
fi

# Get the top 4 Algo from the results file
if [[ ! -s $resultsPath ]]; then
   echo Results path $resultsPath not found
   exit 1
fi

if [[ -z $algoOveride ]]; then
   # Remove the gain file if we are doing a run across all algos
   rm -f bestAlgos/${stock}.gn || cant remove gain file!!
fi

# Top 4 standard algos found to be the best
#algos=$(head -5 $resultsPath | grep BP | awk '{print $2}' | sed "s/${stock}_//")
algos=$(head -5 $resultsPath | grep BP | awk '{print $2}')

# and the best 
algoBest=$(head -1 $resultsPath | grep BA | awk '{print $3}')

algos="$algos $algoBest"

echo algos remove me $algos

# Run the original once for a baseline
for algo in $algos; do
   #echo Running algo $algo against $stock
   $run "" $algo $stock >> bestAlgos/${stock}.all
   tail bestAlgos/${stock}.all | grep "Gain" | sed "s/\$//" | sed "/.*e-*/d" >> bestAlgos/${stock}.gn
   tail -1 bestAlgos/${stock}.all
   break
done

# Add the algo modifiers to the algo and run the test.sh program
for algo in $algos; do
   
   # Get number of decision bars and add range value to IR
   tbv=$(echo $algo | awk -F_ '{print $1}' | sed 's/TB//')

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
   
   # Run modifiers combined
   for aMod in ${algoModifiersCombined[*]}; do
      
      if [[ -n $algoOveride ]]; then
         if ! $(echo $aMod | grep -q $algoOveride); then
            echo Skipping $aMod
            continue 
         fi
      fi
      
      ctbv=${aMod: -2}

      if [[ $ctbv == "IR" ]]; then
         aMod=${aMod}${mtbv} 
      elif [[ $ctbv == "DB" ]]; then
         aMod=${aMod}${dtbv} 
      fi

      modAlgo="${algo}_${aMod}"
      
      #echo Running algo $modAlgo against $stock
      $run "" $modAlgo $stock > bestAlgos/${stock}.all
      #tail bestAlgos/${stock}.all | grep "Gain" | sed "s/\$//" | sed "/.*e-*/d" >> bestAlgos/${stock}.gn
      tail bestAlgos/${stock}.all | grep "Gain" | sed "/.*e-*/d" >> bestAlgos/${stock}.gn
      tail -1 bestAlgos/${stock}.all
   done
   
   # Run all modifiers individually
   for aMod in ${algoModifiers[*]}; do

      if [[ -n $algoOveride ]]; then
         if ! $(echo $aMod | grep -q $algoOveride); then
            echo Skipping $aMod
            continue 
         fi
      fi

      if [[ $aMod == "IR" ]]; then
         aMod=${aMod}${mtbv} 
      elif [[ $aMod == "DB" ]]; then
         aMod=${aMod}${dtbv} 
      fi

      modAlgo="${algo}_${aMod}"
      
      #echo Running algo $modAlgo against $stock
      $run "" $modAlgo $stock > bestAlgos/${stock}.all
      #tail bestAlgos/${stock}.all | grep "Gain" | sed "s/\$//" | sed "/.*e-*/d" >> bestAlgos/${stock}.gn
      tail bestAlgos/${stock}.all | grep "Gain" | sed "/.*e-*/d" >> bestAlgos/${stock}.gn
      tail -1 bestAlgos/${stock}.all
   done
   
done



if [[ -f bestAlgos/${stock}.bs ]]; then
   dt=$(date "+%Y%m%d")
   mv bestAlgos/${stock}.bs historyBestAlgos/${stock}_${dt}.bo
fi

# Ordered by days data, %, price gained
#sort -n -k9,9 -k7,7 -k4,4 bestAlgos/${stock}.gn  | sed "/.*e-*/d" | sed -E 's/\$ ([0-9]) /\$ \1.0 /' > bestAlgos/${stock}.bs

# Ordered by days data, price gained, %
sort -n -k9,9 -k4,4 -k7,7 bestAlgos/${stock}.gn  | sed "/.*e-*/d" | sed -E 's/\$ ([0-9]) /\$ \1.0 /' > bestAlgos/${stock}.bs

exit 0

