#!/bin/bash

. $LPLT/scripts/db.sh

day=$1

isDBRunning $day
if [[ $? == 0 ]]; then
   port=$(getNextPort)
   echo Starting DB $day
   startDB $day $port || exit 1
else
   port=$(getRunningPort $day)
fi

echo port $port

exit 0