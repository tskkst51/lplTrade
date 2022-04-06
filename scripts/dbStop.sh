#!/bin/bash

. $LPLT/scripts/db.sh

runningDBs="db/${1}"

if [[ -z $1 ]]; then
   runningDBs=$(getAllRunningDBs)
fi

for db in $runningDBs; do
   pg_ctl -D $db stop
done

exit 0