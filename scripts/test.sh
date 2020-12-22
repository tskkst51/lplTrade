#!/bin/bash

## RUn the test program over all test directories

args=" "
algo=""
stock=""

loc=$1
algo=$2
stock=$3

wp=$(pwd)

testCmd="${wp}/bin/test.py"

if [[ ! -e $testCmd ]]; then
   echo $testCmd not found!
   exit 1
fi

host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

activateCmd=$(dirname $wp)
activateCmd+="${activateDir}/bin/activate"

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

# Execute script to populate source library path

dt=$(date "+%m%d%Y")

testPaths=$(ls test)

# Do volume algos after 11182020
testResults="${wp}/resultsTest"

if [[ ! -d $testResults ]]; then
   mkdir $testResults
fi

#   "HS,IT"

if [[ -n $algo ]]; then
   algos=($algo)
else
   algos=(
   "HL,QM"
   "HS,QM"
   "HL,AL,QM"
   "HS,AL,QM"
   "HS,HL,AL,QM"
   "EO,EC,AL,QM"
   )
fi

volDate=11182020
newPaths=""

# if the algo has AV or AL restrict dates to the initial volume date and later

if echo $algos | grep -q "AV"  ||  echo $algos | grep -q "AL" ; then
   echo Found volume in $algos. Restricting testing range to $volDate

   for path in $testPaths; do
      if [[ ${path:0:1} -eq 0 ]]; then
         continue
      fi
      if (( path >= volDate )); then
         newPaths="$newPaths $path"
      fi  
   done
   
   if [[ -n $newPaths ]]; then
      testPaths=$newPaths
   fi
fi

if [[ -n $loc ]]; then
   testPaths=$loc
fi


if [[ -n $stock ]]; then
   stockCL="-s $stock" 
fi

set -m

for testPath in $testPaths; do
   
   trap - SIGINT
   
   log="${testResults}/${testPath}_testOut_${dt}"
   
   resultsPath="resultsTest/${testPath}"
   testPath="test/${testPath}"
   
   echo Testing ${testPath}...
   
   echo Creating results path: ${resultsPath}...

   # Squirrel away the results in $resultsPath
   if [[ ! -d $resultsPath ]]; then
      mkdir $resultsPath || exit 1
   fi
   
   for a in ${algos[*]}; do
      algoOpt="-a ${a}"
      
      cmd="$py3 $testCmd $algoOpt $stockCL -c $HOME/profiles/et.json -w ${wp}/${testPath} -p ${wp}/${testPath}/profiles/active.json"
      
      $HOME/bin/lplt.sh

      echo "command: ${cmd}"

      $cmd 
      
      a=$(echo $a | sed 's/,/_/g')
            
      algoPath="${resultsPath}/${stock}_${a}_${dt}"

      echo Results Path ${algoPath}...

      if [[ -d $algoPath ]]; then
         rm -fr $algoPath || exit 1
      fi
      
      mkdir $algoPath || exit 1
      
      # Move results to results path
      mv ${testPath}/profiles/saved $algoPath
      mv ${testPath}/logs $algoPath
      
      mkdir ${testPath}/profiles/saved
      mkdir ${testPath}/logs
      
   done      
done

exit 0

