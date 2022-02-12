#!/bin/bash

## remove n lines in bc files

prices=""
numLinesToKeep=""

date=$1
numLinesToKeep=$2
prices=$3

#dir=$1

wp=$(pwd)

#dt=$(date "+%m%d%Y")
dt=$(date "+%Y%m%d")

if [[ -z $numLinesToKeep ]]; then
   echo need numLinesToKeep
   exit 1
fi


testPaths=$(ls "test/${date}/bc")  
if [[ -n $prices ]]; then
   testPaths=$(ls "test/${date}/prices")
   cd test/${date}/prices || exit 1
else
   cd test/${date}/bc || exit 1
fi

echo $testPaths


path="${wp}/test/${date}/bc"

for bChart in $testPaths; do
#   testPaths="${dir}/${testPath}/bc"
#   bcFiles=$(ls $testPaths) 
   #for f in $bcFiles; do
      #echo Modifying ${testPaths}/${f}...
      echo Modifying ${bChart}...
      cp ${path}/${bChart} ${path}/${bChart}.tmp
      head -n ${numLinesToKeep} ${path}/${bChart} > ${path}/${bChart}.tmp
      mv ${path}/${bChart}.tmp ${path}/${bChart}
   #done
done

cd $wp

exit 0

