#!/bin/bash

## Copy file to targets

function init {

   wp=$(pwd)
   
   . ${wp}/scripts/db.sh

   path=$1
   systems=$2
   user=$3
   
   if [[ -z $user ]]; then user=$defaultUser; fi
   if [[ -z $systems ]]; then systems=$allSystems; fi
}

init $1 $2 $3

echo copying $path to:
for s in $(echo $systems); do
   echo $s
   if [[ $s == $activeLiveHost ]]; then scpUser=$liveHostUser; else scpUser=$user; fi
   scp $path "${scpUser}@${s}:${wp}/${path}" || echo Cant scp to $s
done

exit 0