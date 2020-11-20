#!/bin/bash

## Use first column of data and add a 3rd colum
## add 4th column

dir=$1

wp=$(pwd)

dt=$(date "+%m%d%Y")
  
testPaths=$(ls $dir)  

for testPath in $testPaths; do
   testPaths="${dir}/${testPath}/prices"
   priceFiles=$(ls $testPaths) 
   for f in $priceFiles; do
      echo Modifying ${testPaths}/${f}...
      awk -v FS=',' '{print $1, $2, $3, $4, $4}' ${testPaths}/${f}  | sed 's/ /,/g' > ${testPaths}/${f}_${dt}
      echo Moving ${testPaths}/${f} ${testPaths}/${f}_${dt} ${testPaths}/${f} ...
      mv ${testPaths}/${f}_${dt} ${testPaths}/${f}
   done
done

exit 0

