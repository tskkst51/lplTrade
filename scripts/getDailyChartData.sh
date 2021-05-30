#!/bin/bash

## Detect the status of lplTrade and restart if not running

# Command to kill all processes:
# kill $(ps | grep lplt.py|awk '{printf $1 " " }')

wp=$(pwd)

lpltPath="${wp}/bin/lpltMaster.py"

if [[ ! -e $lpltPath ]]; then
   echo $lpltPath not found!
   exit 1
fi

startTime="000028"
#startTime="130100"
host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
elif [[ $host == "Mac-mini" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

activateCmd=$(dirname $wp)
activateCmd+=$activateDir
activateCmd+="/bin/activate"

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

#. $activateCmd || echo activation failed 

# Execute script to populate source library path
$HOME/bin/lplt.sh

cmd="${py3} bin/lpltMaster.py -d -i -c $HOME/profiles/et.json -p $HOME/w/gitWS/lplTrade/profiles/active.json"

while [[ "$(date "+%H%M%S")" > "$startTime" ]]; do
   echo "sleeping $(date "+%H%M%S") > $startTime"
   sleep 20
done

dt=$(date "+%Y%H%M")

echo $cmd

# Run twice to get em all. some aren't updated close to midnight
#$cmd
$cmd > logs/dailyCharts.${dt} 2>&1
$cmd >> logs/dailyCharts.${dt} 2>&1

exit 0

