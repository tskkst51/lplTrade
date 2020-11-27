#!/bin/bash

## use the latest active.json profile to replace all others 
## minus the stocks line

dir=$1

wp=$(pwd)

dt=$(date "+%m%d%Y")
  
testPaths=$(ls $dir)  

template="/tmp/template.json"

grep -v "stocks" profiles/active.json > $template

stockVar="\"stocks\": \""
stockVarEnd="\","
echo $stockVar

for testPath in $testPaths; do
   bcPaths="${dir}/${testPath}/bc"
   testPaths="${dir}/${testPath}/profiles"
   
   profileFiles=$(ls $testPaths) 
   echo $profileFiles
   
   for f in $testPaths; do
      echo Modifying ${bcPaths}...
      cd ${bcPaths}
      
      stocks=$(ls -l | awk '{print $10}' | sed 's/[a-z]*//' | sed 's/\..*//' | tr '\n' ','| sed 's/,$//' | sed 's/^,//')
      
      line=${stockVar}${stocks}${stockVarEnd}
      
      echo $line

      cd $wp
      
      for t in $profileFiles; do
         echo $t
         echo Modifying ${f}/${t}...
         stocksLine=${line}
         echo $stocksLine
         
         echo ${f}/${t}
         
         rm -f ${f}/${t} 
         head -6 $template > ${f}/${t}
         printf "%s%s" "    " $stocksLine >> ${f}/${t}
         echo >> ${f}/${t}
         tail -86 $template >> ${f}/${t}
         cat ${f}/${t}
         cat ${f}/${t} >> /tmp/results
      done   
   done 
   
done

exit 0

