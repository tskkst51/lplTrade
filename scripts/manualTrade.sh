#!/bin/bash
 
function init {

   sym=""
   limit=""

   sym=$1
   action=$2
   limit=$3
   validated=0
   
   wp="/Users/tsk/w/lplTrade"
   
   . $wp/scripts/db.sh

   wp=$(pwd)

   if [[ -z $sym ]]; then
      echo Must provide symbol!
      exit 1
   fi
   
   if [[ -z $action ]]; then
      echo Must provide action!
      exit 1
   fi

   if [[ ! -f ${manualOverideDir}/${sym}${manualOverideEx} ]]; then
      echo no overide file exists!
      echo ${manualOverideDir}/${sym}${manualOverideEx}  
      exit 1
   fi
}

init $1 $2 $3

# Update manual overide file with action

#for a in $(echo ${overideModes}); do
#   if [[ $a == $action ]]; then
#      validated=1
#   fi
#done

if [[ -n $limit ]]; then action="$action $limit"; fi

echo -n $action > ${manualOverideDir}/${sym}${manualOverideEx}
sync;sync
cat ${manualOverideDir}/${sym}${manualOverideEx}

exit 0