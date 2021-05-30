#!/bin/bash

## Detect the status of the command passed in and restart it if it is not running
## Requires command to be in $PATH

cmd=$1

if [[ -z $cmd ]]; then
   echo Need a command to monitor!
   exit 1
fi

# Command to kill all processes:
# kill $(ps | grep lplt.py|awk '{printf $1 " " }')

wp=$(pwd)

#cmdPath="${wp}/bin/${cmd}"
#
#if [[ ! -e $cmdPath ]]; then
#   echo $cmdPath not found!
#   exit 1
#fi

dt=$(date "+%Y%m%d")

log="/tmp/${cmd}_${dt}.log"

while true ; do
   timeNow=$(date "+%H%M%S")
      
   #echo cmd $cmd
   
   ps -ef | grep $cmd | grep -v "grep" | grep -qv "keepAlive"
   retVal=$?
   
   #ps -ef | grep $cmd | grep -v "grep" | grep -v "keepAlive"

   #echo retVal $retVal
   
   if [[ $retVal == 0 ]]; then
     sleep 10
     echo $cmd is running...
     continue
   fi
   
   echo $cmd is NOT running...
   echo Re-starting $cmd date ...
   
   # Resume running the program from disk if program exits a non 0
   $cmd >> $log &
done

exit 0

