#!/bin/bash

## Detect the status of lplTrade and restart if not running

# Set 
# Configure cron to Wait 10 seconds before checking

lpltPath=$HOME/git/lplTrade
runPath=$HOME/git/venv/bin

py3=$runPath/python3

activate=$(. $runPath/activate) || echo activation failed
shScript=$HOME/bin/lplt.sh
cmd="$py3 $lpltPath/bin/lplt.py -r -c $HOME/profiles/et.json -p $lpltPath/profiles/active.json"

echo $shScript
$shScript

while true ; do
  echo $cmd
  program=lplt.py

  ps | grep -q $program | grep -v grep

  if [ $? == 0 ]; then
     sleep 5
     continue
  fi

  echo Starting lplt...

  # Make sure latest code is in place
  $HOME/bin/lplt.sh

  # Resume running the program from disk
  $py3 $lpltPath/bin/lplt.py -r -c $HOME/profiles/et.json -p $lpltPath/profiles/active.json

done

exit 0

