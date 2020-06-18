#!/bin/bash

## Detect the status of lplTradea(or the command passed in and restart it 
## if it needs to be restarted.

# Set 
# Configure cron to Wait 10 seconds before checking

user="tsk"
userPath=$(echo ~)
lpltPath="$userPath/git/lplTrade


# Resume running the program from disk
CMD="py3 $lplyPath/bin/lplt.py -r -c $userPath/profiles/et.json -p $lpltPath/profiles/active.json"

PROGRAM=basename$($CMD)

RUNNING=$(ps | grep $PROGRAM | grep -v grep) || exit 1

if $RUNNING; then
   exit 0
fi

#$(CMD) || exit 1
echo "TESTING CRON" > /tmp/test

exit 0

