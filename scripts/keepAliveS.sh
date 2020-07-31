#!/bin/bash

## Detect the status of lplTrade and restart if not running

# Command to kill all processes:
# kill $(ps | grep lplt.py|awk '{printf $1 " " }')

wp=$(pwd)

lpltPath="${wp}/bin/lpltS.py"

if [[ ! -e $lpltPath ]]; then
   echo $lpltPath not found!
   exit 1
fi

exitTime="160000"
host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

activateCmd=$(dirname $wp)
activateCmd+=$activateDir
activateCmd+="/bin/activate"

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

stocksPath="${wp}/profiles/stocks.txt"

echo "Paths:"
echo $activateCmd
echo $lpltPath
echo $py3
echo $stocksPath
echo

echo Running lplt against the following symbols...
cat $stocksPath
echo

. $activateCmd || echo activation failed 

# Execute script to populate source library path
$HOME/bin/lplt.sh
dt=$(date "+%Y%m%d")

while true ; do
      
   # Exit when time is after 4pm
   timeNow=$(date "+%H%M%S")
   
   if [[ "$timeNow" > "$exitTime" ]]; then
      echo Exiting... Time is after 4PM: $(date)
      
      # Kill all process and exit
      kill $(ps | grep lplt.py | awk '{printf $1 " " }')
      
      # Move data to test directory
      testDir="${wp}/test/${dt}"         
      echo $testDir
      
      mkdir $testDir || echo Unable to make directory $testDir
      mv "prices" $testDir || echo Unable to move prices directory to $testDir
      mv "bc" $testDir || echo Unable to move bc directory to $testDir
      mv "logs" $testDir || echo Unable to move logs directory to $testDir
      mv "debug" $testDir || echo Unable to move debug directory to $testDir
      mkdir "prices" "bc" "logs"  || echo Unable to mkdir "prices" "bc" "logs"
      tar -cf ${testDir}.tar ${testDir} || echo Unable to tar test dir $testDir
      gzip ${testDir}.tar || echo Unable to gzip ${testDir}.tar
      exit 0
   fi
   
   log="${wp}/logs/TEMPP_${dt}"
   
   cmd="$py3 $lpltPath -r -c $HOME/profiles/et.json -p $wp/profiles/active.json"
   
   program=lplt.py
   
   ps | grep $program | grep $stock | grep -qv grep
   
   if [ $? == 0 ]; then
     sleep 3
     continue
   fi
   
   echo Re-starting $stock $(date) ...
   
   # Resume running the program from disk if program exits a non 0
   $cmd >> $log &
done

exit 0

