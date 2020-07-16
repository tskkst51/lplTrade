#!/bin/bash

## Detect the status of lplTrade and restart if not running

# Command to kill all processes:
# kill $(ps | grep lplt.py|awk '{printf $1 " " }')

wp=$(pwd)

lpltPath=$wp
lpltPath+="/bin/lplt.py"

if [[ ! -e $lpltPath ]]; then
   echo $lpltPath not found!
   exit 1
fi

host=$(hostname -s)

if [[ $host -eq "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

activateCmd=$(dirname $wp)
activateCmd+=$activateDir
activateCmd+="/bin/activate"

py3=$(dirname $wp)
py3+=$activateDir
py3+="/bin/python3"

stocksPath=$wp
stocksPath+="/profiles/stocks.txt"

echo $activateCmd
echo $lpltPath
echo $py3
echo $stocksPath

echo Running lplt against the following symbols...
cat $stocksPath

#activate=$(. $activateCmd) || echo activation failed

. $activateCmd || echo activation failed 

# Execute script to populate source library path
$HOME/bin/lplt.sh
dt=$(date "+%Y%m%d")

while true ; do
   
   # Open the stock path and launch the trading program against all stocks
   while read stock; do      
            
      log=$wp
      log+="/logs/TEMPP_"
      log+=$stock
      log+="_"
      log+=$dt
      
      cmd="$py3 $lpltPath -r -s $stock -c $HOME/profiles/et.json -p $wp/profiles/active.json"
      
      program=lplt.py
      
      ps | grep $program | grep $stock | grep -qv grep
      
      if [ $? == 0 ]; then
        sleep 3
        continue
      fi
      
      echo Re-starting $stock $(date) ...
      
      # Resume running the program from disk
      $cmd >> $log &
   done < $stocksPath
done

exit 0

