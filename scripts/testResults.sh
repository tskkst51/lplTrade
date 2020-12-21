#!/bin/bash

## Run the allTest.sh program and iterate its results

wp=$(pwd)

testCmd="${wp}/bin/test.py"

if [[ ! -e $testPath ]]; then
   echo $testPath not found!
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

echo "Paths:"
echo $activateCmd
echo $testPath
echo $py3
echo $stocksPath
echo

. $activateCmd || echo activation failed 

# Execute script to populate source library path
$HOME/bin/lplt.sh

dt=$(date "+%d%m%Y")

testPaths=$(ls test)  

log="${wp}/testOut_${dt}"

for testDir in $testPaths; do
   testPath="test/${testDir}"
   echo $testPath
   
   cmd="$py3 $testCmd -c $HOME/profiles/et.json -w $testPath -p ${testPath}/profiles/active.json"
      
   $HOME/bin/sh
   $cmd >> $l

done

exit 0

