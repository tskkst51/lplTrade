#!/bin/bash

## RUn the test program over all test directories

args=" "
algo=""
stock=""
doVol=""
modProfiles=""
testPath=""

loc=$1
algo=$2
stock=$3
doVol=$4
modProfiles=$5
testPath=$6

wp=$(pwd)

testCmd="${wp}/bin/test.py"

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
elif [[ $host == "tmm" ]]; then
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

if [[ -n $modProfiles ]]; then
   ${wp}/scripts/modProfiles.sh $testPath
fi

testPaths=$(ls ${testPath}/${loc})

# Do volume algos after 11182020
testResults="${wp}/resultsTest"

if [[ ! -d $testResults ]]; then
   mkdir $testResults
fi

#   "HS,IT"

if [[ -n $algo ]]; then
   algos=($algo)
else
   if [[ -n $doVol ]]; then
      algos=(
      # DON"T CHANGE ORDER!!!!
      "HL_QM_AL"
      "HS_QM_AL"
      "HI_QM_AL"
      "LO_QM_AL"
      "OC_QM_AL"
      "EO_EC_QM_AL"
      "HL_HS_QM_AL"
      "HL_HI_QM_AL"
      "HL_LO_QM_AL"
      )        
   else
      algos=(
      "HL_QM"
      "HS_QM"
      "HI_QM"
      "LO_QM"
      "OC_QM"
      "OO_QM"
      "CC_QM"
      "PL_QM"
      "EO_EC_QM"
      "HL_HS_QM"
      "HL_HI_QM"
      "HL_LO_QM"
      )
   fi  
fi

#volDate=20201117
newPaths=""

if [[ -n $loc ]]; then
   testPaths=$loc
fi


if [[ -n $stock ]]; then
   stockCL="-s $stock"
else
   # Get stock from profile
   stock=$(grep \"stock\" "${wp}/${testPath}/${loc}/profiles/active.json" \
      | uniq | awk -F\" '{print $4}')
fi

set -m

# Copy all the new code into place
$HOME/bin/lplt.sh

for datePath in $testPaths; do
   
   echo $datePath
   
   trap - SIGINT
      
   # No bar charts exist, skip
   if [[ -z $loc ]]; then
      #echo "${wp}/${testPath}/${datePath}/bc/active${stock}.bc"
      #echo "${wp}/${testPath}/${datePath}/prices/active${stock}.pr"

      if [[ ! -s "${wp}/${testPath}/${datePath}/bc/active${stock}.bc" ]]; then
         echo
         echo $stock BAR chart for $datePath not found. Skipping...
         continue
      fi
      if [[ ! -s "${wp}/${testPath}/${datePath}/prices/active${stock}.pr" ]]; then
         echo
         echo $stock PRICE chart for $datePath not found. Skipping...
         continue
      fi
   fi
  
   log="${testResults}/${datePath}_testOut_${dt}"
   
   resultsPath="resultsTest/${datePath}"
   
   # Squirrel away the results in $resultsPath
   if [[ ! -d $resultsPath ]]; then
      echo Creating results path: ${resultsPath}...
      mkdir $resultsPath || exit 1
   fi
   
   for a in ${algos[*]}; do
      algoOpt="-a ${a}"
      a=$(echo $a | sed 's/,/_/g')
      
      date=$(basename $datePath)      
      
      if [[ -n $algo ]]; then
         p="exitResults/${stock}_${a}.ex"
      else
         p="exitResults/${stock}_TB3_${a}_OB3_OS3_CB2_CS2.ex"
         
      fi
#echo p $p
      # Already ran, skip
      grep -q $date $p > /dev/null 2>&1
      if (( $? == 0 )); then
         echo ALGO $a already ran against $stock for ${date}. Skipping...
         echo p $p
         echo
         continue
      fi

      numStocks=0
      ctr=0
      
      if [[ -z $stock ]]; then
         stocks=$(grep stocks ${wp}/${testPath}/${datePath}/profiles/active.json | \
            awk -F\" '{print $4}')
         numStocks=$(echo $stocks | awk -F, '{print NF}')

         lastStock=$(echo $stocks | awk -F, -v ns="$numStocks" '{print $ns}')
         firstStock=$(echo $stocks | awk -F, '{print $1}')
   
         p="exitResults/${lastStock}_TB3_${a}_OB3_OS3_CB2_CS2.ex"
#echo p $p
         # Already ran, skip
         grep -q $date $p > /dev/null 2>&1
         if (( $? == 0 )); then
            #echo ALGO $a already ran against $lastStock for ${date}. Skipping...
            echo ALGO $a already ran against $firstStock for ${date}. Skipping...
            echo p $p
            echo
            continue
         fi
      fi

      echo Testing ${datePath} $algoOpt ...

      cmd="$py3 $testCmd $algoOpt $stockCL -c $HOME/profiles/et.json -w ${wp}/${testPath}/${datePath} -p ${wp}/${testPath}/${datePath}/profiles/active.json"
      
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

