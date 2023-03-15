#!/bin/bash

## Find the best algo's across all days

function init {

   #wp="/Users/tsk/w/lplTrade"
   wp=$(pwd)
   
   $HOME/bin/lplt.sh
   . $wp/scripts/db.sh

   reduceSearchDBs=0
   
   day=$1
   algo=$2
   sym=$3
   ss=$4
   reduceSearchDBs=$5
   debug=$6
   sortPct=$7
   dontStopDB=$8
   
   searchAllDays=0
   
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   numRows=10
   dbWasRunning=0
   
   #tmpFile=$(getTmpFile $sym)
   #tmpFileSort=$(getTmpFile "sort")

   tmpFile=$(getRandomTmpFile)
   tmpFileSort=$(getRandomTmpFile)      
   
   if [[ -n $debug ]] && [[ $debug != "d" ]]; then debug=""; fi
#   if [[ -n $reduceSearchDBs ]] && [[ $reduceSearchDBs != "r" ]]; then reduceSearchDBs=""; fi
   if [[ -z $sym ]]; then echo sym is empty!; exit 1 ; fi
   if [[ -z $algo ]]; then echo Need algo; exit 1; fi
   if [[ -n $ss ]]; then dbNumModTestRows=$ss; fi
   if [[ -n $sortPct ]] && [[ $sortPct = "p" ]]; then sortPct="p"; else sortPct="w"; fi

   syms=$sym
   if [[ $day == "all" ]] && [[ $sym == "all" ]]; then
      syms=$(getAllSyms "all")
   elif [[ $day != "all" ]] && [[ $sym == "all" ]]; then
      syms=$(getAllSyms $day)
   fi

   eq="="
   echo $algo | grep "%" > /dev/null
   if [[ $? == 0 ]]; then eq="like"; fi

   days=$day   
   if [[ -n $debug ]]; then
      echo syms $syms
      echo algo $algo
      echo ss $ss
      echo reduceSearchDBs $reduceSearchDBs
   fi
   
   if [[ $day == "all" ]]; then
      days=$(getAllDays $sym)
      searchAllDays=1
      if [[ -n $reduceSearchDBs ]]; then
         # reduce the set of DB's to search
         ctr=0
         numDBs=$(echo $days | tr -cd ' ' | wc -c)
         loopCtr=$(echo "$numDBs - $reduceSearchDBs + 1" | bc)
         if [[ -n $debug ]]; then echo numDBs $numDBs; fi
         if [[ -n $debug ]]; then echo loopCtr $loopCtr; fi
         for d in $(echo $days); do
            # Skip total - n
            ctr=$(echo "$(($ctr + 1))")
            if (( ctr <= loopCtr )); then
               if [[ -n $debug ]]; then echo skipping $d; fi
               continue
            fi
            newDays="$newDays $d"
         done
         days=$newDays
         echo Using only the last $reduceSearchDBs days: $days
      fi
   fi
   
   if [[ -f $tmpFile ]]; then rm -f $tmpFile ; fi
   if [[ -z $days ]]; then echo day is empty!; exit 1 ; fi
   
   sortDB="order by gain,winpct desc"
   sortF="-k4,4 -k7,7"
   if [[ $sortPct == "p" ]]; then 
      sortDB="order by winpct,gain asc"
      sortF="-k7,7 -k4,4"
   fi
   algoCtr=0
   algoModCtr=0
   
   #dbStopAll.sh
}

init $1 $2 $3 $4 $5 $6 $7 $8

# Get the 10 best algoMods populate file

if [[ -n $debug ]]; then
   echo Getting data from DB: ${days} sym: $syms algo: ${algo}...
fi

for db in $days; do
   if [[ ! -f "$dbDir/${db}/log" ]]; then 
      if [[ -n $debug ]]; then
         echo $db DB log file missing! skipping...
      fi
      continue
   fi
   
  # Skip todays DB in case were running live and to predict better for next day
   if [[ $db == $today ]]; then continue; fi

   # Skip a DB that is being tested
   testDay=$(getKeepAliveDay)
   if [[ $db == $testDay ]]; then 
      echo DB $testDay is being tested or running live, skipping...
      continue
   fi
   
   isDBRunning $db
   if (( $? == 1 )); then
      port=$(getRunningPort $db)
      if [[ -n $debug ]]; then
         echo running port: $port for db $db
      fi
      dbWasRunning=1
   else
      port=$(getNextPort)
      startDB $db $port > $tmpFile 2>&1
      if [[ -n $debug ]]; then cat $tmpFile; fi
      if [[ $? != 0 ]]; then
         echo Unable to start DB $db
      fi
   fi

   if [[ -n $debug ]]; then
      echo $db
   fi
   

   cl=$(getCL $port "algos")
   clO=$(getCLO $port "algos")
      
   for s in $(echo $syms); do
      $cl "select sym, algo, gain, winpct from algoData where sym = '${s}' and algo $eq '${algo}' $sortDB" | tail -n $dbNumModTestRows > $tmpFile
      if [[ $? != 0 ]]; then echo No DB for $s on $db; fi
      if [[ -n $debug ]]; then
         echo $clO "\"select sym, algo, gain, winpct from algoData where sym = '${s}' and algo $eq '${algo}' $sortDB\""
      fi
      
      if [[ -s $tmpFile ]]; then
         if [[ -n $debug ]]; then
            echo $db >> ${tmpFileSort}_${s}
         fi
         algoCtr=$((algoCtr + 1))
         cat $tmpFile >> ${tmpFileSort}_${s}
      fi
      
      rm -f $tmpFile

      $cl "select sym, algo, gain, winpct from algoModData where sym = '${s}' and algo $eq '${algo}' $sortDB" | tail -n $dbNumModTestRows > $tmpFile
      if [[ $? != 0 ]]; then echo No DB for $s on $db; fi
      if [[ -n $debug ]]; then
         echo $clO "\"select sym, algo, gain, winpct from algoModData where sym = '${s}' and algo $eq '${algo}' $sortDB\""
      fi
      if [[ -s $tmpFile ]]; then
         if (( searchAllDays == 1 )); then echo $db; fi

         algoModCtr=$((algoModCtr + 1))         
         cat $tmpFile >> ${tmpFileSort}_${s}
      fi
      rm -f $tmpFile
   done

   if [[ -z $dontStopDB ]]; then
      if (( ! dbWasRunning )); then
         if [[ -n $debug ]]; then echo Stopping DB $port; fi
         dbStop.sh $db > $tmpFile 2>&1
         if [[ -n $debug ]]; then cat $tmpFile; fi
         dbWasRunning=0
      fi
   fi
done      

if (( searchAllDays == 1 )); then
   echo found pattern $algo in standard algo: $algoCtr mod: $algoModCtr
fi

rm -f $tmpFile

if [[ -n $debug ]]; then
   echo $algoCtr "DB's processed"
fi

if [[ $day != "all" ]] && [[ $sym != "all" ]]; then
   if [[ -f ${tmpFileSort}_${sym} ]]; then
      sort -t\| -n `echo $sortF` ${tmpFileSort}_${sym}
   fi
fi

if [[ $sym == "all" ]]; then
   for s in $syms; do
      if [[ -f ${tmpFileSort}_${s} ]]; then
         #cat ${tmpFileSort}_${s} >> $tmpFile
         tail -n $numRows ${tmpFileSort}_${s} >> $tmpFile
      fi
   done
   if [[ -f $tmpFile ]]; then sort -t\| -n `echo $sortF` $tmpFile; fi
   #cat $tmpFile
fi

if [[ $day == "all" ]]; then
   for s in $syms; do
      if [[ -f ${tmpFileSort}_${s} ]]; then
         sort -t\| -n `echo $sortF` ${tmpFileSort}_${s}
      fi
      #cat ${tmpFileSort}_${s}
   done
fi
   
#   winTot=$(awk -F\| '{print $3}' ${tmpFileSort}_${sym} | awk '{s+=$1} END {print s}')
#   pctTot=$(awk -F\| '{print $4}' ${tmpFileSort}_${sym} | awk '{s+=$1} END {print s}')
#   numEntries=$(expr $algoModCtr + $algoCtr)
#   echo $algoModCtr
#   echo $algoCtr
#   echo $numEntries
#   cat ${tmpFileSort}_${sym}
#   sort -u -t\| -n `echo $sortF` ${tmpFileSort}_${sym}
#   avgPrice=$(echo "scale=2; $winTot / $numEntries" | bc)
#   avgPct=$(echo "scale=2; $pctTot / $numEntries" | bc)
   #echo Days: $numEntries Average total $: $avgPrice Average %: $avgPct

exit 0