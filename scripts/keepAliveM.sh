#!/bin/bash

## Detect the status of lplTrade amster and restart if not running

# Command to kill all processes:
# kill $(ps | grep lplt.py|awk '{printf $1 " " }')

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

if [[ $host == "ML-C02C8546LVDL" ]] || [[ $host == "mm" ]] || [[ $host == "tmm" ]]; then
   activateDir="/lplW"
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

retCode=0

function endIt {
   if [[ $1 == 0 ]]; then  
      echo
   fi
}
      
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
#$cmd >> $log
retCode=$?
   
sleep 1

# Exit when time is after 4pm
timeNow=$(date "+%H%M%S")

#if [[ "$retCode" == "3" ]]; then
   
#   echo Exiting... Return code is 3. Normal exitting. $(date)


# Kill all process and exit
#kill $(ps | grep $program | awk '{printf $1 " " }')
#echo timeNow $timeNow
#echo exitTime $exitTime
#
#if [[ "$timeNow" > "$exitTime" ]]; then

if [[ -z $offLine ]]; then
   
   echo Exiting... Time is after Market exit time: $(date)
   echo Waiting to archive results...
   
   # Sleep so the other git command can push its content
   sleep 180

   cd ../lpltArchives || echo cant cd to ../lpltArchives
   
   git pull
   
   # Move data to test directory
   
   testDir="${wp}/test/${dt}"
   tar -zxf "${dt}.tar.gz" || echo cant unarchive
   
   mv "Users/tsk/git/lplTrade/test/${dt}" "../lplTrade/test"
   rm -fr "Users"
   
   cd $wp || echo cant cd to $wp

   if [[ -d $testDir ]]; then
      # Merge results with existing results
      exitingMCharts=$(ls ${testDir}/bc)
      
      echo Merging results...
      
      for mChart in $(ls "${wp}/bc"); do
         if [[ -f ${testDir}/bc/${mChart} ]]; then
            echo ${testDir}/bc/${mChart} exists, skipping...
            continue
         fi
         
         echo copying $mChart
         
         cp "${wp}/bc/${mChart}" "${testDir}/bc" || echo cant copy $mChart to "${testDir}/bc"
         prices=$(echo $mChart | sed "s/bc/pr/")
         
         echo copying $prices
         cp "${wp}/prices/${prices}" "${testDir}/prices" || echo cant copy $prices to "${testDir}/prices"
         debugFile=$(echo $mChart | sed "s/bc/ds/")
         
         echo copying $debugFile
         if [[ -f "${wp}/debug/${debugFile}" ]]; then
            cp "${wp}/debug/${debugFile}" "${testDir}/debug" || echo cant copy $debugFile to "${testDir}/debug"
         fi
         
         logFile=$(echo $mChart | sed "s/bc/ls/")
         echo copying $logFile
         if [[ -f "${wp}/debug/${logFile}" ]]; then
            cp "${wp}/logs/${logFile}" "${testDir}/debug" || echo cant copy $logFile to "${testDir}/logs"
         fi
         
         echo copying profiles...
         if [[ ! -d "${testDir}/profiles" ]]; then
            mkdir "${testDir}/profiles"
            cp "${wp}/profiles/active.json" "${testDir}/profiles" || echo cant copy active.json to "${testDir}/profiles"
         fi
      done

      tarNm="${dt}all.tar"
      tar -cf $tarNm "test/${dt}" || echo Unable to tar test dir $dt
      gzip $tarNm || echo Unable to gzip $tarNm
      mv "${tarNm}.gz" ../lpltArchives || echo Unable to mv archive to archives
      
      cd ../lpltArchives || echo cant cd to ../lpltArchives
   
      git add "${tarNm}.gz"
      git commit -am "${tarNm}.gz"
      git push
      echo results archived
         
      #rm -fr "debug/*" "logs/*" "bc/*" "prices/*"

      pwd

      cd $wp || echo cant cd to $wp

      #${wp}/scripts/modProfiles.sh "test"
      #${wp}/scripts/keepAliveM.sh off $dt
      
      scripts/modProfiles.sh "test"
      scripts/keepAliveM.sh off $dt
   else
      cd "test"
      tar -xvf "../lpltArchives/${dt}.tar.gz"
      cd $wp
      
#      mkdir $testDir || echo Unable to make directory $testDir
#      mv "prices" $testDir || echo Unable to move prices directory to $testDir
#      mv "bc" $testDir || echo Unable to move bc directory to $testDir
#      mv "logs" $testDir || echo Unable to move logs directory to $testDir
#      mv "debug" $testDir || echo Unable to move debug directory to $testDir
#      rm -f ${testDir}/debug/* || echo Unable to remove ${testDir}/debug directory contents
#      rm -f ${testDir}/logs/*log || echo Unable to remove ${testDir}/logs/ directory contents
#      #rm ${testDir}/logs/output_${dt} || echo Unable to remove output file output_${dt}
#      mkdir ${testDir}/results || echo Unable to mkdir ${testDir}/results
#      mkdir ${testDir}/profiles || echo Unable to mkdir ${testDir}/profiles
#      cp profiles/*  ${testDir}/profiles || echo Unable to copy profiles
#      mkdir "prices" "bc" "logs" "debug"  || echo Unable to mkdir "prices" "bc" "logs"
            
      # Execute the tests
      #echo Running ${wp}/scripts/test.sh $dt
      #${wp}/scripts/test.sh $dt
   fi
   

fi

exit 0

