#!/bin/bash

## use the latest active.json profile to replace all others 
## minus the stocks line

dir=$1

wp=$(pwd)

#dt=$(date "+%m%d%Y")
dt=$(date "+%Y%m%d")

testPaths=$(ls $dir)  

for testPath in $testPaths; do
   testPaths="${dir}/${testPath}/profiles"
   echo Copying profiles/active.json to ${testPaths}
   cp profiles/active.json $testPaths
done

exit 0

