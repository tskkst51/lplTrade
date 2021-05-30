#!/bin/bash

## Update the profile. Run the trading program live

stock=""
algo=""
workPath=""

stock=$1
algo=$2
workPath=$3

wp=$(pwd)

$HOME/bin/lplt.sh

lpltPath="$HOME/w/lplTrade"

host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
elif [[ $host == "Mac-mini" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

py3=$(dirname $lpltPath)
py3+="${activateDir}/bin/python3"

if [[ -n $workPath ]]; then
   echo changing to workpath $workPath
   cd $workPath || exit 1
fi

echo stock $stock
echo algo $algo
echo offLine $offLine

if [[ -z $stock ]]; then
   echo stock not provided on CL
   exit 1
fi

if [[ -n $stock ]]; then
   profilePath="${wp}/profiles/active.json_${stock}"
else
   profilePath="${wp}/profiles/active.json"
fi

if [[ -z $algo ]]; then
   echo algo not provided on CL
   exit 1
else
   algos=$algo   
fi

set -m

outFile="/tmp/out${stock}.ot"
dirty=""

for algo in $algos; do
   a=$algo
   
   ${py3} ${lpltPath}/bin/profileGenerator.py -d "" -a $algo -s $stock || echo Fainle profile generator
   
   cmd="${py3} ${lpltPath}/bin/lpltSlave.py -d -c $HOME/profiles/et.json -p $profilePath -l -s $stock"

#   if [[ -n $workPath ]]; then
#      ${py3} ${lpltPath}/bin/profileGenerator.py -d $workPath -a $algo || echo Fainle profile generator
#      cmd="${py3} ${lpltPath}/bin/lpltSlave.py -w ${wp} -c $HOME/profiles/et.json -p ${workPath}/profiles/active.json -l -o -s $stock"
#   else
#      ${py3} ${lpltPath}/bin/profileGenerator.py -d "" -a $algo || echo Fainle profile generator
#      cmd="${py3} ${lpltPath}/bin/lpltSlave.py -c $HOME/profiles/et.json -p ${wp}/profiles/active.json -l -s $stock"
#   fi
      
   echo $cmd
   $cmd
done

exit 0

