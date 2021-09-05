#!/bin/bash

## Detect the status of lplTrade amster and restart if not running

# Command to kill all processes:
# kill $(ps | grep lplt.py|awk '{printf $1 " " }')

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

   cd ${wp}/../lpltArchives || echo cant cd to ../lpltArchives
   git pull || echo cant pull data for $dt
   cd $wp || echo cant cd to $wp
}

function moveDataToArchive {
   
   tarNm=$1

   cd "test" || echo cant cd to test dir
   
   echo $tarNm
   echo $dt
   
   tar -cf "${tarNm}" "${dt}" || echo Unable to tar test dir $tarNm
   gzip ${tarNm} || echo Unable to gzip $tarNm   
   mv ${tarNm}.gz ${wp}/../lpltArchives || echo Unable to mv "${tarNm}.gz" to ${wp}/lpltArchives
   
   cd $wp || echo cant cd to $wp
}

function createSlaveTestData {
   
   if [[ ! -d $testDir ]]; then
      mkdir $testDir || echo Unable to make directory $testDir
      mv "prices" $testDir || echo Unable to move prices directory to $testDir
      mv "bc" $testDir || echo Unable to move bc directory to $testDir
      mv "logs" $testDir || echo Unable to move logs directory to $testDir
      mv "debug" $testDir || echo Unable to move debug directory to $testDir
      rm -f ${testDir}/debug/* || echo Unable to remove ${testDir}/debug directory contents
      rm -f ${testDir}/logs/*log || echo Unable to remove ${testDir}/logs/ directory contents
      #rm ${testDir}/logs/output_${dt} || echo Unable to remove output file output_${dt}
      mkdir ${testDir}/results || echo Unable to mkdir ${testDir}/results
      mkdir ${testDir}/profiles || echo Unable to mkdir ${testDir}/profiles
      cp profiles/*  ${testDir}/profiles || echo Unable to copy profiles
      mkdir "prices" "bc" "logs" "debug"  || echo Unable to mkdir "prices" "bc" "logs"
   fi
}

function mergeMasterSlaveDate {
   
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
         
         echo Copying $logFile
         if [[ -f "${wp}/debug/${logFile}" ]]; then
            cp "${wp}/logs/${logFile}" "${testDir}/debug" || echo cant copy $logFile to "${testDir}/logs"
         fi
      done
   fi
   
   #rm -fr "debug/*" "logs/*" "bc/*" "prices/*"
}

function initSlaveTestData {
      
   # Move data to test directory
   
   cd ${wp}/../lpltArchives || echo cant cd to ../lpltArchives
   
   tar -zxf "${dt}.tar.gz" || echo cant unarchive
   mv ${dt} "../lplTrade/test"
   
   cd $wp || echo cant cd to $wp
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ulimit -n 10000

wp=$(pwd)

offLine=$1
day=$2

lpltMaster="${wp}/bin/lpltMaster.py"

if [[ ! -e $lpltMaster ]]; then
   echo $lpltMaster not found!
   exit 1
fi

#exitTime="160001"
exitTime="155951"

host=$(hostname -s)

testHost=""

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
elif [[ $host == "mm" ]]; then
   activateDir="/lplW2"
   testHost="yes"
else
   activateDir="/venv"
fi

activateCmd=$(dirname $wp)
activateCmd+=$activateDir
activateCmd+="/bin/activate"

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

echo "Paths:"
echo $activateCmd
echo $lpltMaster
echo $py3
echo

. $activateCmd || echo activation failed 

# Execute script to populate source library path
$HOME/bin/lplt.sh

dt=$(date "+%Y%m%d")

program="lpltMaster.py"

# Check if a rogue program is running. kill it if it is
ps | grep $program | grep -qv grep

if [ $? == 0 ]; then
   kill $(ps | grep $program | awk '{printf $1 " " }')
fi

testDir="${wp}/test/${dt}"

retCode=0

log="${wp}/logs/output_${dt}"

cmd="$py3 $lpltMaster -d -c $HOME/profiles/et.json -p $wp/profiles/active.json"

if [[ -n $offLine ]]; then
   if [[ -n $day ]]; then
      testDay=$day
   fi
   cmd="$py3 $lpltMaster -w "${wp}/test/${testDay}" -o -d -c $HOME/profiles/et.json -p ${wp}/test/${testDay}/profiles/active.json"
fi

ps | grep $program | grep -qv grep

if [ $? == 0 ]; then
  sleep 2
  continue
fi

echo Starting $cmd $(date) ...

#$HOME/bin/lplt.sh
$cmd
#$cmd > $log
retCode=$?
   
sleep 1
waiting=5

# Exit when time is after 4pm
timeNow=$(date "+%H%M%S")

echo Exiting... Time is after Market exit time: $timeNow

if [[ -z $offLine ]]; then
   if [[ -n $testHost ]]; then

      # Archive data
      echo Waiting $waiting to archive results...
      sleep $waiting
         
      tarNm="${dt}all.tar"

      pullSlaveData
      initSlaveTestData
      mergeMasterSlaveDate
      moveDataToArchive $tarNm
      pushData $tarNm
      
      # Run tests...
      cd $wp || echo cant cd to $wp
      scripts/modProfiles.sh "test"
      scripts/keepAliveM.sh off $dt
      scripts/daysBest.sh

   else # Archive slave
      
      tarNm="${dt}.tar"

      createSlaveTestData
      moveDataToArchive $tarNm
      pushData $tarNm

   fi
fi

exit 0

