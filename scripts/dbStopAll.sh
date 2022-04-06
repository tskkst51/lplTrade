#!/bin/bash

. scripts/db.sh

runningDBs=$(getAllRunningDBs)

echo $runningDBs

for db in $runningDBs; do
   if [[ $db == "/usr/local/var/postgres" ]]; then
      continue
   fi
   pg_ctl -D $db stop
done

exit 0