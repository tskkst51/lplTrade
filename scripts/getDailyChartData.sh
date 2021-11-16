#!/bin/bash

wp="/Users/tsk/w/lplTrade"

cd $wp

lpltPath="${wp}/bin/lpltMaster.py"

if [[ ! -e $lpltPath ]]; then
   echo $lpltPath not found!
   exit 1
fi

host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
elif [[ $host == "mm" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

# Execute script to populate source library path
$HOME/bin/lplt.sh

cmd="${py3} $lpltPath -i -c ${HOME}/profiles/et.json -p ${wp}/profiles/active.json"

dt=$(date "+%Y%m%H%M")

echo $cmd

# Run twice to get em all. some aren't updated close to midnight
#$cmd
$cmd > logs/dailyCharts.${dt} 2>&1
echo $dt 1 >> logs/dailyCharts.${dt}
sleep 10
$cmd >> logs/dailyCharts.${dt} 2>&1
echo $dt 2 >> logs/dailyCharts.${dt}
sleep 10
$cmd >> logs/dailyCharts.${dt} 2>&1
ret=$?
echo $dt 3 >> logs/dailyCharts.${dt}

if [[ $ret != 0 ]]; then
   echo exit code is not 0
   echo exit code is not 0 >> logs/dailyCharts.${dt}
   exit 0
   
# Remove bad data
token=$(tail -1 dc/TQQQ.dc | awk -F\, '{print $9}')
stocks=$(ls -l dc/*dc|awk '{print $9}'|awk -F\/ '{print $2}'|sed "s/\.dc//")
echo stocks $stocks
echo token $token
for stock in $stocks; do
   #echo stock $stock
   newToken=$(tail -1 "dc/${stock}.dc" | awk -F\, '{print $9}')
   if [[ $newToken != $token ]]; then
      echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      echo removing bad data from stock $stock
      echo stock $stock
      echo token $token
      echo newToken $newToken
      rm -f "dc/${stock}.dc" "dc/${stock}.gp"
      rm -fr "exitResults/${stock}\*"
      rm -fr "totalResults/${stock}\*"
      rm -fr test/\*/bc/\*${stock}\*
      rm -fr test/\*/prices/\*${stock}\*
      rm -fr test/\*/logs/\*${stock}\*
   fi
done

exit 0

