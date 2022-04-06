#!/bin/bash

## Detect the status of lplTrade amster and restart if not running

# Command to kill all processes:
# kill $(ps | grep lplt.py|awk '{printf $1 " " }')

function init {

   . $LPLT/scripts/db.sh

   ulimit -n 10000
   
   wp=$(pwd)
   
   day=$1
   stock=$2

   if [[ -z $1 ]]; then
      day=""
   fi
   
   lpltMaster="${wp}/bin/lpltMaster.py"
   
   if [[ ! -e $lpltMaster ]]; then
      echo $lpltMaster not found!
      exit 1
   fi
   
   host=$(hostname -s)
   
   liveHost=""
   
   activateDir="/lplW2"
 
   if [[ $host == "mm" ]]; then
      liveHost="yes"
   fi
   
   activateCmd=$(dirname $wp)
   activateCmd+=$activateDir
   activateCmd+="/bin/activate"
   
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
#   echo "Paths:"
#   echo $activateCmd
#   echo $lpltMaster
#   echo $py3
#   echo
   
   . $activateCmd || echo activation failed 
   
   # Execute script to populate source library path
   $HOME/bin/lplt.sh
   
   dt=$(date "+%Y%m%d")
   
   program="lpltMaster.py"
   testDir="${wp}/test/${dt}"
   log="${wp}/logs/liveDebugLog_${dt}.oo"
   cmd="$py3 $lpltMaster -d -c $HOME/profiles/et.json -p $wp/profiles/active.json"

}   

function cleanup {
   
   # Remove debug data 
   rm -f "test/${dt}/logs/*" || echo cant remove log files
   rm -f "test/${dt}/debug/*" || echo cant remove debug files
}

function moveDBtoTestSystem {
   
   gzNm="${1}.gz"
   
   cd "${wp}/db" || echo cant cd to db
   
   tar -zcf $gzNm $dt || echo cant tar $gzNm || echo cant tar $dt
   scp $gzNm  "mmT.local:${LPLT}/dbArchive" || echo cant scp $gzNm
   
   cd $wp || echo cant cd to $wp
}

function endIt {
   if [[ $1 == 0 ]]; then  
      echo
   fi
}

function pushData {
   
   tarFile=$1

   cd ${wp}/../lpltArchives || echo cant cd to ../lpltArchives

   git add "${tarFile}.gz"
   git commit -am "${tarFile}.gz"
   git push || echo cant archive results!

   cd $wp || echo cant cd to $wp
}

function pullSlaveData {

   if [[ -d "test/${dt}" ]]; then
      return
   fi

   cd ${wp}/../lpltArchives || echo cant cd to ../lpltArchives
   git pull || echo cant pull data for $dt
   cd $wp || echo cant cd to $wp
}

function tallyLiveResults {

   dtt=$1
   out="${wp}/docs/stats"
   
   cd "test/${dtt}" || echo cant cd to test $dtt
   
   echo >> $out
   echo Live results on ${dtt} >> $out
   echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" >> $out
   tail -1 logs/*ls >> $out
   echo Total Gain/Loss: >> $out   
   tail -1 logs/*ls|awk '{s+=$4} END {print s}' >> $out
   
   cd $wp || echo cant cd to $wp
}

function moveDataToTest {
   
   tarNm=$1

   cd "test" || echo cant cd to test dir
   
   echo $tarNm
   echo $dt
   
   tar -cf "${tarNm}" "${dt}" || echo Unable to tar test dir $tarNm
   gzip ${tarNm} || echo Unable to gzip $tarNm   
   mv ${tarNm}.gz ${wp}/../lpltArchives || echo Unable to mv "${tarNm}.gz" to ${wp}/lpltArchives
   
   cd $wp || echo cant cd to $wp
}

function moveDataToArchive {
   
   tarNm=$1

   cd "test" || echo cant cd to test dir
   
   tar -cf "${tarNm}" "${dt}" || echo Unable to tar test dir $tarNm
   gzip ${tarNm} || echo Unable to gzip $tarNm   
   mv ${tarNm}.gz ${wp}/../lpltArchives || echo Unable to mv "${tarNm}.gz" to ${wp}/lpltArchives
   
   cd $wp || echo cant cd to $wp
}

function createSlaveTestData {
   
   if [[ ! -d $testDir ]]; then
      mkdir $testDir || echo Unable to make directory $testDir
   fi
   mv "prices" $testDir || echo Unable to move prices directory to $testDir
   mv "bc" $testDir || echo Unable to move bc directory to $testDir
   mv "logs" $testDir || echo Unable to move logs directory to $testDir
   mv "debug" $testDir || echo Unable to move debug directory to $testDir
   rm -f "${testDir}/debug/*dm" || echo Unable to remove ${testDir}/debug directory contents
   rm -f "${testDir}/logs/*log" || echo Unable to remove ${testDir}/logs/ directory contents
   #rm ${testDir}/logs/output_${dt} || echo Unable to remove output file output_${dt}
   mkdir ${testDir}/results || echo Unable to mkdir ${testDir}/results
   mkdir ${testDir}/profiles || echo Unable to mkdir ${testDir}/profiles
   cp profiles/*  ${testDir}/profiles || echo Unable to copy profiles
   mkdir "prices" "bc" "logs" "debug"  || echo Unable to mkdir "prices" "bc" "logs"
}

function mergeMasterSlaveData {
   
   if [[ -d $testDir ]]; then

      # Merge results with existing results
      exitingMCharts=$(ls ${testDir}/bc)
      
      echo Merging results...
      
      echo Copying profiles...
      
      if [[ ! -d "${testDir}/profiles" ]]; then
         mkdir "${testDir}/profiles"
         cp "${wp}/profiles/active.json" "${testDir}/profiles" || echo cant copy active.json to "${testDir}/profiles"
      fi
   
      for mChart in $(ls "${wp}/bc"); do
         if [[ -f ${testDir}/bc/${mChart} ]]; then
            echo ${testDir}/bc/${mChart} exists, skipping...
            continue
         fi
         
         echo Copying $mChart
         
         cp "${wp}/bc/${mChart}" "${testDir}/bc" || echo cant copy $mChart to "${testDir}/bc"
         prices=$(echo $mChart | sed "s/bc/pr/")
         
         echo Copying $prices
         cp "${wp}/prices/${prices}" "${testDir}/prices" || echo cant copy $prices to "${testDir}/prices"
         debugFile=$(echo $mChart | sed "s/bc/ds/")
         
         echo Copying $debugFile
         if [[ -f "${wp}/debug/${debugFile}" ]]; then
            cp "${wp}/debug/${debugFile}" "${testDir}/debug" || echo cant copy $debugFile to "${testDir}/debug"
         fi
         
         logFile=$(echo $mChart | sed "s/bc/ls/")
         origFile=$(echo $mChart | sed "s/ls/or_ls")
         
         echo Copying $logFile
         if [[ -f "${wp}/logs/${logFile}" ]]; then
            cp "${wp}/logs/${logFile}" "${testDir}/logs/${origFile}" || echo cant copy $logFile to "${testDir}/logs/${origFile}"
            cp "${wp}/logs/orderFile.ll" "${testDir}/logs" || echo cant copy orderFile.ll to "${testDir}/logs"
         fi
      done
   else
      mkdir $testDir || echo cant make $testDir
      mkdir ${testDir}/profiles || echo cant make ${testDir}/profiles
      mv prices bc logs debug $testDir || echo cant move live data to $testDir
      mkdir prices bc logs debug || echo cant mkdir prices bc logs debug
      cp profiles/* ${testDir}/profiles || echo cant copy profiles to $testDir
   fi
   
   #rm -fr "debug/*" "logs/*" "bc/*" "prices/*"
}

function initSlaveTestData {
      
   # Move data to test directory
   
   if [[ -d "test/${dt}" ]]; then
      return
   fi
      
   cd ${wp}/../lpltArchives || echo cant cd to ../lpltArchives
   
   tar -zxf "${dt}.tar.gz" || echo cant unarchive "${dt}.tar.gz"
   tar -zxf "${dt}all.tar.gz" || echo cant unarchive "${dt}all.tar.gz"
   mv ${dt} "../lplTrade/test"
   
   cd $wp || echo cant cd to $wp
}

function initDB {

   db=$1
   
   isDBCreated $db
   if [[ $? == 0 ]]; then # No
      port=$(getNextPort)
      scripts/createDB.sh $db
      if [[ $? != 0 ]]; then
         echo Unable to create DB $db
      fi
   else # Yes
      isDBRunning $db
      if [[ $? == 0 ]]; then
         port=$(getNextPort)
         echo Starting DB ${db}...
         startDB $db $port
      fi
   fi
  
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

init $1 $2

if [[ -n $liveHost ]] && [[ -z $day ]]; then
   initDB $dt
else
   initDB $day
fi

# Check if a rogue program is running. kill it if it is
ps | grep $program | grep -qv grep

if [ $? == 0 ]; then
   kill $(ps | grep $program | awk '{printf $1 " " }')
fi

if [[ -n $day ]]; then
   testDay=$day
   offLine="yes"
   scripts/modProfiles.sh "test" > /dev/null 2>&1

   cmd="$py3 $lpltMaster -w "${wp}/test/${testDay}" -o -d -c $HOME/profiles/et.json -p ${wp}/test/${testDay}/profiles/active.json"

   if [[ -n $stock ]]; then
      cmd="$py3 $lpltMaster -w "${wp}/test/${testDay}" -o -d -c $HOME/profiles/et.json -p ${wp}/test/${testDay}/profiles/active.json -s $stock"
       
   fi
fi

echo Starting $cmd $(date) ...

$cmd
#echo log: $log
#$cmd > $log

if [[ $? != 0 ]]; then
   echo lpltMaster exited with non 0. Quitting... 
   exit 1
fi

waiting=0

if [[ -n $liveHost ]] && [[ -z $day ]]; then

   # Archive data
   echo Waiting $waiting seconds to archive results...
   sleep $waiting
      
   tarNm="${dt}.tar"

   createSlaveTestData   
   moveDataToArchive $tarNm
   pushData $tarNm
   scripts/liveResults.sh $dt
   tallyLiveResults $dt

   # Run tests twice...
   scripts/keepAliveDB.sh $dt
   scripts/keepAliveDB.sh $dt

   moveDBtoTestSystem $tarNm
   
   cleanup
   
   # Copy DB to test system
   #scp -r "db/${dt}" ${testSystem}/${dbPath} || echo cannot copy DB $dt to $testSystem

   #cd $wp || echo cant cd to $wp
   
   # Gather live results. modify test profiles. Run tests. collate results
   #scripts/daysBest.sh
   #scripts/runModAlgosDB.sh $dt

else # Run tests on test system
   echo Do nothing now
   #pullSlaveData
   #initSlaveTestData

   #scripts/modProfiles.sh "test" > /dev/null 2>&1
   #   if [[ -n $sym ]]; then
   #      scripts/bestDB.sh $sym
   #   fi
   #   mergeMasterSlaveData
   
   #   tarNm="${dt}.tar"
   #
   #   moveDataToArchive $tarNm
   #   pushData $tarNm
fi

exit 0

