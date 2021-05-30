#!/bin/bash

## use the latest active.json profile to replace all others 
## minus the stocks line

dir=$1

wp=$(pwd)

#dt=$(date "+%m%d%Y")
dt=$(date "+%Y%m%d")

testPaths=$(ls $dir)  

cp profiles/active.json /tmp/template.json || exit 1

template="/tmp/template.json"

totalTemplateLines=$(wc -l $template | awk '{print $1}')
endLines=$(expr $totalTemplateLines - 7)

grep -v "stocks" profiles/active.json > $template

for testPath in $testPaths; do
   testPaths="${dir}/${testPath}/profiles"
   profileFiles=$(ls $testPaths) 
   for f in $profileFiles; do
      if [[ -d ${testPaths}/${f} ]]; then
         continue
      fi
      
      if [[ "${testPaths}/${f}" != "${testPaths}/active.json" ]]; then
         continue
      fi
      
      echo Modifying ${testPaths}/${f}...
      numLines="-"${endLines}
      stocksLine=$(grep "stocks" ${testPaths}/${f})
      
      #echo $stocksLine

      rm -f ${testPaths}/${f} 
      head -6 $template > ${testPaths}/${f}
      echo $stocksLine >> ${testPaths}/${f}
      tail $numLines $template >> ${testPaths}/${f}
      #cat ${testPaths}/${f}
      #cat ${testPaths}/${f} >> /tmp/results
   done
done

exit 0

