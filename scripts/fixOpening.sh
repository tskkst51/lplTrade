#!/bin/bash

## fix the open of the first line of BC with DC 

dir=$1

wp=$(pwd)

dt=$(date "+%Y%m%d")

testPaths=$(ls ${dir}/*/bc/*bc)
testPricePaths=$(ls ${dir}/*/bc/*bc)

for testPath in $testPaths; do
   
   day=$(echo $testPath | awk -F/ '{print $2}')
   stock=$(echo $testPath | awk -F/ '{print $4}'  | awk -F. '{print $1}'| sed "s/active//")
   origOpenValue=$(head -1 $testPath | awk -F, '{print $3'})
   pricesPath="${dir}/${day}/prices/active${stock}.pr"
   head -1 $testPath
   head -1 $pricesPath
   echo origOpenValue $origOpenValue
   echo testPath $testPath
   echo day $day
   echo stock $stock
   
   bcPath=$(dirname $testPath)
   bcName=$(basename $testPath)
   
   newPath="${bcPath}/${bcName}.new"
   echo newPath $newPath
   
   openValue=$(head -1 ${pricesPath} | awk -F, '{print $3'})
   
   echo openValue $openValue
   
   newLine=$(head -1 $testPath | sed "s/${origOpenValue}/${openValue}/")
   echo newLine $newLine
      
   echo $newLine > $newPath
   
   numLines=$(wc -l $testPath | awk '{print $1}')
   echo numLines $numLines
   
   numLines=$(echo "scale=2 ; $numLines - 1" | bc)

   echo numLines $numLines
   tail -${numLines} $testPath >> $newPath
   mv $newPath $testPath || exit 1      
done

exit 0

