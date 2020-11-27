#!/bin/bash

## use the latest active.json profile to replace all others 
## minus the stocks line

dir=$1

wp=$(pwd)

dt=$(date "+%m%d%Y")
  
testPaths=$(ls $dir)  

cp profiles/active.json /tmp/template.json || exit 1

template="/tmp/template.json"

grep -v "stocks" profiles/active.json > $template

for testPath in $testPaths; do
   testPaths="${dir}/${testPath}/profiles"
   profileFiles=$(ls $testPaths) 
   for f in $profileFiles; do
      echo Modifying ${testPaths}/${f}...
      numLines=$(wc -l ${testPaths}/${f} | awk '{print $1}')
      numLines=$(expr $numLines - 1)
      numLines="-"${numLines}
      echo $numLines
      stocksLine=$(grep "stocks" ${testPaths}/${f})
      echo $stocksLine

      rm -f ${testPaths}/${f} 
      head -6 $template > ${testPaths}/${f}
      echo $stocksLine >> ${testPaths}/${f}
      tail $numLines $template >> ${testPaths}/${f}
      cat ${testPaths}/${f}
      #cat ${testPaths}/${f} >> /tmp/results
   done
done

exit 0

