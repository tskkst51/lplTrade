#!/bin/bash

## RUn the test program over all test directories

args=" "
algo=""
stock=""

loc=$1
algo=$2
stock=$3

args=$algo

if [[ -n $3 ]]; then
   args+=" ${stock}"   
fi

echo $args

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
testResults="${wp}/resultsTest"

if [[ -n $loc ]]; then
   testPaths=$loc
fi

if [[ ! -d $testResults ]]; then
   mkdir $testResults
fi

# Removed doTR_RBS_ABL_RT
algos="doTrendsdoRT doTrendsdoQPdoRT"

if [[ -n $algo ]]; then
   algos=$algo
fi

for testPath in $testPaths; do
   log="${testResults}/${testPath}_testOut_${dt}"
   
   testPath="test/${testPath}"
   
   echo Testing ${testPath}...
   
   cmd="$py3 $testCmd $args -f -c $HOME/profiles/et.json -w ${wp}/${testPath} -p ${wp}/${testPath}/profiles/active.json"

   if [[ -n $aglo ]]; then
      for algo in $algos; do
         cmd="$py3 $testCmd -a $algo -c $HOME/profiles/et.json -w ${wp}/${testPath} -p ${wp}/${testPath}/profiles/active.json"
         
         $HOME/bin/lplt.sh
         $cmd
      done

   else
      echo "command: ${cmd}"
   
      $HOME/bin/lplt.sh
      $cmd
      
   fi
      
done

exit 0

