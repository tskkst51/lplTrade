#!/bin/bash

## Detect the status of lplTradea(or the command passed in and restart it 
## if it needs to be restarted.

# Set 
# Configure cron to Wait 10 seconds before checking

user=tsk
userPath=$(echo ~)
lpltPath=$userPath/w/gitWS/lplTrade
runPath=$userPath/w/gitWS/lplW/bin

py3=$runPath/python3

activate=$(. $HOME/w/gitWS/lplW/bin/activate) || echo activation failed
CMD="$py3 $lpltPath/bin/lplt.py -o -r -c $userPath/profiles/et.json -p $lpltPath/profiles/active.json"

while true ; do
  echo $CMD
  PROGRAM=lplt.py

  RUNNING=$(ps | grep $PROGRAM | grep -v grep) 

  echo $RUNNING
  if $RUNNING; then
     sleep 5
     continue
  fi

  # Resume running the program from disk
  $($py3 $lpltPath/bin/lplt.py -o -r -c $userPath/profiles/et.json -p $lpltPath/profiles/active.json > $lpltPath/logs/tempp)

done

exit 0

