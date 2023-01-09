#!/bin/bash

## Update the profile. Run the trading program

dt=""
algo=""
stock=""
debug=""

dt=$1
algo=$2
stock=$3
debug=$4

numOfAlgosToVerify=7

wp=$(pwd)

#if [[ -n $pf ]]; then
#   ${wp}/scripts/modProfiles.sh test
#fi

$HOME/bin/lplt.sh

#host=$(hostname -s)

activateDir="/lplW2"

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

dayProvided=0

if [[ -z $dt ]]; then
   days=`for d in $(ls test); do if [[ -f "test/${d}/bc/active${stock}.bc" ]]; then echo $d;fi;done`
else
   dayProvided=1
   days=$dt
fi

numDays=0
numDays=$(echo $days | tr -cd ' ' | wc -c)

if [[ -z $stock ]]; then
   echo Not all required args passed in, 3 required date algo stock
   exit 1
fi

if [[ -z $algo ]]; then
   if [[ ! -f "totalResults/${stock}.tr" ]]; then
      echo Results dont exist for totalResults/${stock}.tr. exiting...
      exit 1
   fi
   echo Finding best algos to run from totalResults/${stock}.tr
   algos=$(grep "BP" totalResults/${stock}.tr | awk '{print $2}' | head -${numOfAlgosToVerify})
   bestAlgo=$(grep "BA" totalResults/${stock}.tr | awk '{print $3}')
   algos="${bestAlgo} ${algos}"
else
   algos=$algo   
fi

set -m

outFile="/tmp/out${stock}.ot"
dirty=""

volDate=20201118

for algo in $algos; do
   a=$algo
   
   gainFile="${wp}/totalResults/${stock}_${algo}.gn"

   if [[ -f $gainFile ]]; then
      rm -f $gainFile
   fi
   
   for day in $days; do
      
      trap - SIGINT
            
#      fnd=$(echo "$day < $volDate" | bc)
#
#      if echo $a | grep -q "AV" || echo $a | grep -q "AL" ; then
#         if [[ $fnd -eq 1 ]] ; then
#            dirty="yesIAm"
#            #echo Found volume in $a. Restricting testing range to $volDate. Skipping ${day}...
#            continue
#         fi
#      fi

      if [[ ! -s "${wp}/test/${day}/bc/active${stock}.bc" ]] || [[ ! -s "${wp}/test/${day}/prices/active${stock}.pr" ]]; then
         continue
      fi
      
      ${py3} ${wp}/bin/profileGenerator.py -d $day -a $algo -s $stock > /dev/null 2>&1
      
      #${py3} ${wp}/bin/lpltSlave.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json -w test/${day} -o -d -s $stock > $outFile 2>/dev/null

      if [[ $debug == "d" ]]; then
         echo debug set
         ${py3} ${wp}/bin/lpltSlave.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json_${stock} -w test/${day} -o -d -s $stock > $outFile
      else
         ${py3} ${wp}/bin/lpltSlave.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json_${stock} -w test/${day} -o -s $stock > $outFile
         
      fi
      
      value=$(cat $outFile | grep "Total Gain" | tail -1 | awk '{print $4}')
      echo $value on $day >> $gainFile
      echo $value on $day
   done

   if (( dayProvided == 1 )); then
      if [[ $dirty -ne "yesIam" ]]; then
         echo Cant run algo: $a before $volDate
         exit 1
      fi
   fi

   if [[ ! -f $gainFile ]]; then
      echo Error check the CL dam it. exiting...
      exit 1
   fi

   losers=$(grep \- $gainFile | wc -l  | awk '{print $1}')
   winners=$(grep -v \- $gainFile | wc -l | awk '{print $1}')
   total=$(echo "scale=2 ; $winners + $losers" | bc)
   
   winPct=$(echo "scale=2 ; $winners / $total * 100" | bc)
   
   amt=$(awk '{s+=$1} END {print s}' $gainFile)
   amt=$(echo $amt | sed "/.*e-*/d")
   dotFound=$(echo $amt | grep \\.)
   if [[ -z $dotFound ]]; then
      amt=${amt}.0
   fi
   numDays=$(cat $gainFile | wc -l | awk '{print $1}')
   echo "Gain: \$ ${amt}" "in ${numDays} days with algo $a" >> $gainFile
   echo $stock Gain: \$ ${amt} Win %: $winPct in $numDays days with algo $a
done

exit 0

