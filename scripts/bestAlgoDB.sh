#!/bin/bash

## Find the best algo's across all days

function init {

   #wp="/Users/tsk/w/lplTrade"
   wp=$(pwd)

   . ${wp}/scripts/db.sh
   
   $HOME/bin/lplt.sh

   sym=$1
   ss=$2
   debug=$3
   
   syms=$sym
   if [[ $sym == "all" ]]; then 
      syms=$(getBestSymsFile); 
   else
      syms=$sym
      #syms=$(getPartBestSymsFile $sym)
   fi
   
   #elif [[ $sym == "all" ]]; then syms=$(getBestSymsFile); fi
   
   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
      
   if [[ -n $debug ]]; then echo syms: $syms; fi
   if [[ -f $tmpFile ]]; then rm -f $tmpFile ; fi
   if [[ -n $ss ]]; then dbNumModTestRows=$ss ; fi
   
}

init $1 $2 $3

if [[ -n $debug ]]; then
   echo Getting data for ${syms}...
fi

for s in $syms; do
   echo Running best algos for ${s}...
   
   tmpFile=$(getRandomTmpFile)
   tmpFile2=$(getRandomTmpFile)

   cmd="${wp}/scripts/getDBVal.sh all TB% $s "
   
   if [[ -n $debug ]] && [[ -n $ss ]]; then
      cmd="$cmd $ss d"   
   elif [[ -n $debug ]]; then
      cmd="$cmd d"
   elif [[ -n $ss ]]; then
      cmd="$cmd $ss"
   fi
   
   echo $cmd

   $cmd >> $tmpFile
   
#      if [[ -n $ss ]]; then
#         gv all TB% $s "d" $ss >> $tmpFile
#      else
#         gv all TB% $s "d" >> $tmpFile
#      fi
#   else
#      gv all TB% $s >> $tmpFile
#   fi
      
   if [[ ! -f $tmpFile ]]; then echo No data found in the DBs for ${s}, skipping...; continue; fi
   
   if [[ -f "$bestAlgosDir/${s}.ds" ]]; then
      mv "$bestAlgosDir/${s}.ds" "$bestAlgosDir/${s}.bak.ds"
   fi
   
   for algo in $(awk -F\| '{print $2}' $tmpFile); do
      #if [[ -n $debug ]]; then echo Running algo $algo; fi
      #echo Running algo $algo
      run.sh "" $algo $s | grep Gain >> $tmpFile2
      tail -1 $tmpFile2
   done
   
   sort -n -k4,4 $tmpFile2 > "$bestAlgosDir/${s}.ds"
   tail -n $dbNumBestRows "$bestAlgosDir/${s}.ds"
done

exit 0