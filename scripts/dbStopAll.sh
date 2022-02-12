#!/bin/bash

. $HOME/profiles/db.sh

runningDBs=$(getAllRunningDBs)

echo $runningDBs

for db in $runningDBs; do
   pg_ctl -D $db stop
done

exit 0