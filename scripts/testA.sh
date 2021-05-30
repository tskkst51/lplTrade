#!/bin/bash

## RUn the test program over all test directories

args=" "
algo=""
stock=""
testPath=""

loc=$1
algo=$2
stock=$3
testPath=$4

wp=$(pwd)

testCmd="${wp}/bin/testA.py"

if [[ ! -e $testCmd ]]; then
   echo $testCmd not found!
   exit 1
fi

if [[ -z $testPath ]]; then
   testPath="test"
fi

host=$(hostname -s)

if [[ $host == "ML-C02C8546LVDL" ]]; then
   activateDir="/lplW"
else
   activateDir="/venv" 
fi

activateCmd=$(dirname $wp)
activateCmd+="${activateDir}/bin/activate"

py3=$(dirname $wp)
py3+="${activateDir}/bin/python3"

# Execute script to populate source library path

dt=$(date "+%Y%m%d")

doResults=0
if [[ -n $loc ]]; then
      if [[ ! -d "${testPath}/${loc}" ]]; then
      cd ../lpltArchives || exit 1
      git pull
      cd ../lplTrade/${testPath} || exit 1
      tar -xf "../../lpltArchives/${dt}.tar.gz"
      cd ../${testPath}
      mv "Users/tsk/git/lplTrade/${testPath}/${loc}" .
      rm -fr Users
      cd ..
      doResults=1
      ${wp}/scripts/modProfiles.sh $testPath
   fi
fi

testPaths=$(ls $testPath)

testResults="${wp}/resultsTest"

if [[ ! -d $testResults ]]; then
   mkdir $testResults
fi

#   "HS,IT"

if [[ -n $algo ]]; then
   algos=($algo)
else
   algos=(
   "HL_QM"
   "HS_QM"
   "HI_QM"
   "LO_QM"
   "OC_QM"
   "EO_EC_QM"
   "HL_HS_QM"
   "HL_HI_QM"
   "HL_LO_QM"
   "HL_AL_QM"
   "HS_AL_QM"
   "HI_AL_QM"
   "LO_AL_QM"
   "HL_HS_AL_QM"
   "HL_HI_AL_QM"
   "HL_LO_AL_QM"
   "EO_EC_AL_QM"
   )        
fi

newPaths=""

if [[ -n $loc ]]; then
   testPaths=$loc
fi


if [[ -n $stock ]]; then
   stockCL="-s $stock" 
fi

set -m

# Copy all the new code into place
$HOME/bin/lplt.sh

for datePath in $testPaths; do
   
   trap - SIGINT
      
   # No bar charts exist, skip
   if [[ -z $loc ]]; then
      if [[ ! -s "${wp}/${testPath}/${datePath}/bc/active${stock}.bc" ]] || [[ ! -s "${wp}/${testPath}/${datePath}/prices/active${stock}.pr" ]]; then
         echo
         echo $stock bar chart for $testPath not found. Skipping...
         continue
      fi
   fi
   
   log="${testResults}/${datePath}_testOut_${dt}"
   
   resultsPath="resultsTest/${datePath}"
   testPath="${testPath}/${datePath}"
   
   # Squirrel away the results in $resultsPath
   if [[ ! -d $resultsPath ]]; then
      echo Creating results path: ${resultsPath}...
      mkdir $resultsPath || exit 1
   fi
   
   for a in ${algos[*]}; do
      
      algoOpt="-a ${a}"

      a=$(echo $a | sed 's/,/_/g')

      # if the algo has AV or AL restrict dates to the initial volume date and later
      
      date=$(basename $datePath)      
      
      echo "date:" $date

      # Already ran, skip
      p="exitResults/${stock}_TB5_${a}_OB*"
      
      echo algo: $a
      
      grep -q $date $p > /dev/null 2>&1
      if (( $? == 0 )); then
         echo algo $a already ran against $stock for ${date}. Skipping...
         continue
      fi
      
      echo
      echo Testing ${datePath}...

#      if echo $a | grep -q "AV" || echo $a | grep -q "AL" ; then
#         if [[ $fnd -eq 1 ]] ; then
#            echo Found volume in $a. Restricting testing range to $volDate. Skipping ${date}...
#            continue
#         fi
#      fi

      cmd="$py3 $testCmd $algoOpt $stockCL -c $HOME/profiles/et.json -w ${wp}/${testPath} -p ${wp}/${testPath}/profiles/active.json"
      
      echo "command: ${cmd}"

      $cmd 
                  
      algoPath="${resultsPath}/${stock}_${a}_${dt}"

      echo Results Path ${algoPath}...

      if [[ -d $algoPath ]]; then
         rm -fr $algoPath || exit 1
      fi
      
      mkdir $algoPath || exit 1
      mv ${testPath}/logs $algoPath
      mkdir ${testPath}/logs
      
   done      
done

#if (( doResults == 1 )); then
#   stocks=($(grep stocks "test/${loc}/profiles/active.json"))
#   for stock in $stocks; do
#       scripts/results.sh $stock
#   done
#fi

exit 0

