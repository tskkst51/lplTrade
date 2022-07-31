#!/bin/bash

wp="/Users/tsk/w/lplTrade"
.  ${wp}/scripts/db.sh

cd $wp || echo cant cd to wp

runningDBs="db/${1}"

if [[ -z $1 ]]; then
   runningDBs=$(getAllRunningDBs)
fi

for db in $runningDBs; do
   pg_ctl -D $db stop
done

exit 0