#!/bin/bash

## use the latest active.json profile to replace all others 
## minus the stocks line

dir=$1

wp=$(pwd)


testPaths=$(ls $dir)  

profile="profiles/active.json"

for testPath in $testPaths; do
   testPaths="${dir}/${testPath}/profiles"
   cp $profile "${dir}/${testPath}/profiles" || cant cp profile to test path $testPath && echo modified $testPath with $profile
done

exit 0

