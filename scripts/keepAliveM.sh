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
#cmd="$py3 $lpltMaster -d -r -c $HOME/profiles/et.json -p $wp/profiles/active.json"

ps | grep $program | grep -qv grep

if [ $? == 0 ]; then
  sleep 2
  continue
fi

echo Starting $cmd $(date) ...

# Resume running the program from disk if program exits a non 0
$HOME/bin/lplt.sh
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
echo timeNow $timeNow
echo exitTime $exitTime

#if [[ "$timeNow" > "$exitTime" ]]; then
#   echo Exiting... Time is after Market exit time: $(date)
#   
#   # Sleep so the other git command can push its content
#   sleep 60
#
#   # Move data to test directory
#   testDir="${wp}/test/${dt}"        
#   echo $testDir
#   
#   mkdir $testDir || echo Unable to make directory $testDir
#   mv "prices" $testDir || echo Unable to move prices directory to $testDir
#   mv "bc" $testDir || echo Unable to move bc directory to $testDir
#   mv "logs" $testDir || echo Unable to move logs directory to $testDir
#   mv "debug" $testDir || echo Unable to move debug directory to $testDir
#   rm ${testDir}/logs/output_${dt} || echo Unable to remove output file output_${dt}
#   mkdir ${testDir}/results || echo Unable to mkdir ${testDir}/results
#   #mkdir -p ${testDir}/profiles/saved || echo Unable to mkdir ${testDir}/profiles/saved
#   #cp profiles/saved/* ${testDir}/profiles/saved || echo Unable to copy profiles
#   #cp profiles/* ${testDir}/profiles || echo Unable to copy profiles
#   cp ${testDir}/profiles/good  ${testDir}/profiles/active.json || echo Unable to copy active.json
#   mkdir "prices" "bc" "logs" "debug"  || echo Unable to mkdir "prices" "bc" "logs"
#   tarNm="${dt}mm.tar"
#   tar -cf $tarNm ${testDir} || echo Unable to tar test dir $dt
#   gzip $tarNm || echo Unable to gzip $tarNm
#   #mkdir archives || echo Unable to make Archives dir
#   mv "${tarNm}.gz" ../lpltArchives || echo Unable to mv archive to archives
#   cd ../lpltArchives
#   git pull
#   git add "${tarNm}.gz"
#   git commit -am "${tarNm}.gz"
#   git push
#   cd $wd
#   
#   # Execute the tests
#   #echo Running ${wp}/scripts/test.sh $dt
#   #${wp}/scripts/test.sh $dt
#fi

exit 0

