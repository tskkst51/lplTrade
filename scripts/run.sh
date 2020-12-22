#!/bin/bash

## Update the profile. Run the trading program


day=""
algo=""
stock=""

day=$1
algo=$2
stock=$3

wp=$(pwd)

$HOME/bin/lplt.sh

host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

if [[ ! -d "test/${day}" ]]; then
   echo test directory not found $day
   exit 1
fi

if [[ -z $stock ]]; then
   echo stock not provided on CL
   exit 1
fi

if [[ -z $algo ]]; then
   echo algorithm not provided on CL. e.g: TB2_HL_HS_AL_OB2_OS2_CB2_CS2
   exit 1
fi

${py3} ${wp}/bin/profileGenerator.py -d $day -a $algo

${py3} ${wp}/bin/lplt.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json -w test/${day} -o -d -s $stock > out

tail -50 out

exit 0

