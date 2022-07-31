#!/bin/bash

## Update the profile. Run the trading program live

stock=""
algo=""
testDate=""

stock=$1
algo=$2
testDate=$3

wp=$(pwd)

$HOME/bin/lplt.sh

lpltPath=""

host=$(hostname -s)

activateDir="${HOME}/w/lplW"
lpltPath="${HOME}/w/lplTrade"

py3="${activateDir}/bin/python3"

if [[ -n $testDate ]]; then
   workPath="test/${testDate}"
fi

echo stock $stock
echo algo $algo

if [[ -z $stock ]]; then
   echo stock not provided on CL
   exit 1
fi

if [[ -n $stock ]]; then
   #cp ${wp}/profiles/active.json ${wp}/profiles/active.json_${stock}
   profilePath="${wp}/profiles/active.json_${stock}"
   if [[ -f $profilePath ]]; then
      rm -f $profilePath
   fi
else
   if [[ -n $testDate ]]; then
      profilePath="${workPath}/profiles/active.json"
   else
      profilePath="${wp}/profiles/active.json"
   fi
fi

if [[ -n $algo ]]; then
   algos=$algo   
fi

set -m

outFile="/tmp/out${stock}.ot"
dirty=""
if [[ -n $testDate ]]; then
   if [[ -z $algo ]]; then
      algos=(
      # DON"T CHANGE ORDER!!!!
      "HL_QM_AL"
      "HS_QM_AL"
      "HI_QM_AL"
      "LO_QM_AL"
      "OC_QM_AL"
      "EO_EC_QM_AL"
      "HL_HS_QM_AL"
      "HL_HI_QM_AL"
      "HL_LO_QM_AL"
   
      "HL_QM"
      "HS_QM"
      "HI_QM"
      "LO_QM"
      "OC_QM"
      "OO_QM"
      "CC_QM"
      "PL_QM"
      "EO_EC_QM"
      "HL_HS_QM"
      "HL_HI_QM"
      "HL_LO_QM"
      )
   fi
fi

for algo in $algos; do
   a=$algo
      
   # Write algo string to log (.ls) file
   log="logs/active${stock}.ls"
   if [[ -n $testDate ]]; then
      log="test/testDate/${log}"
      ${py3} ${lpltPath}/bin/profileGenerator.py -d $testDate -a $algo -s $stock || echo Fainle profile generator
      cmd="${py3} ${lpltPath}/bin/lpltSlave.py -w $workPath -c $HOME/profiles/et.json -p $profilePath -o -d -s $stock"
   else # LIVE
      ${py3} ${lpltPath}/bin/profileGenerator.py -d "" -a $algo -s $stock || echo Fainle profile generator
      cmd="${py3} ${lpltPath}/bin/lpltSlave.py -c $HOME/profiles/et.json -p $profilePath -d -l -s $stock"
   fi
   
   echo $algo >> $log
   
   echo $cmd
   $cmd
done

exit 0

