#!/bin/bash

wp="/Users/tsk/w/lplTrade"
.  ${wp}/scripts/db.sh

runningDBs=$(getAllRunningDBs)

echo $runningDBs

for db in $runningDBs; do
   if [[ $db == "/usr/local/var/postgres" ]]; then
      continue
   fi
   echo $db | grep -q $today
   if [[ $? == 0 ]]; then
      echo Skipping live DB $db
      continue
   fi
   pg_ctl -D $db stop
done

exit 0