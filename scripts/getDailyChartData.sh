#!/bin/bash

wp="/Users/tsk/w/lplTrade"
tmpFile="/tmp/removeFiles.$$"

removeOldData=$1
debug=$2

cd $wp

lpltPath="${wp}/bin/lpltMaster.py"

if [[ ! -e $lpltPath ]]; then
   echo $lpltPath not found!
   exit 1
fi

host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
elif [[ $host == "mm" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

# Execute script to populate source library path
$HOME/bin/lplt.sh

cmd="${py3} $lpltPath -i -c ${HOME}/profiles/et.json -p ${wp}/profiles/active.json"

dt=$(date "+%Y%m%H%M")

echo $cmd

# Run twice to get em all. some aren't updated close to midnight

if [[ -z $removeOldData ]]; then
   $cmd  >> logs/dailyCharts.${dt}
   ret=$?
   echo return code: $rt
fi

if [[ -n $removeOldData ]]; then
   # Remove bad data
   token=$(tail -1 dc/TQQQ.dc | awk -F\, '{print $9}')
   stocks=$(ls -l dc/*dc|awk '{print $9}'|awk -F\/ '{print $2}'|sed "s/\.dc//")
   echo stocks $stocks
   echo token $token
   echo debug $debug

   if [[ -n $debug ]]; then echo DATA BEING SHOWN NOT DELETED!; fi

   for stock in $stocks; do
      #echo stock $stock
      newToken=$(tail -1 "dc/${stock}.dc" | awk -F\, '{print $9}')
   
      if [[ $newToken != $token ]] && [[ $newToken != "" ]]; then
         #if [[ ${stock} == "FB" ]]; then continue; fi
         echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         echo Removing old data from stock $stock
         echo time stamp on file $token
         echo last recorded time from file $newToken
         if [[ -n $debug ]]; then
            find ./dc -type f -name "${stock}.dc" -exec echo {} \;
            find ./dc -type f -name "${stock}.gp" -exec echo {} \;
            find ./test -type f -name active${stock}.pr -exec echo {} \;
            find ./test -type f -name active${stock}.bc -exec echo {} \;
            find ./test -type f -name active${stock}.ls -exec echo {} \;
            find ./test -type f -name active${stock}.log -exec echo {} \;
            find ./test -type f -name active${stock}.ds -exec echo {} \;
            find ./test -type f -name active${stock}.dm -exec echo {} \;
         else         
            find ./dc -type f -name ${stock}.dc -exec echo {} \; >> $tmpFile
            find ./dc -type f -name ${stock}.gp -exec echo {} \; >> $tmpFile
            find ./test -type f -name active${stock}.pr -exec echo {} \; >> $tmpFile
            find ./test -type f -name active${stock}.bc -exec echo {} \; >> $tmpFile
            find ./test -type f -name active${stock}.ls -exec echo {} \; >> $tmpFile
            find ./test -type f -name active${stock}.log -exec echo {} \; >> $tmpFile
            find ./test -type f -name active${stock}.ds -exec echo {} \; >> $tmpFile
            find ./test -type f -name active${stock}.dm -exec echo {} \; >> $tmpFile
            echo Files are not removed but are in $tmpFile
         fi
         
      else
         echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         echo Not removing data from stock $stock
         echo time stamp on file $token
         echo last recorded time from file $newToken
      fi      
   done
 fi
exit 0
