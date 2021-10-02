#!/bin/bash

## Push all code and data to n num of slaves

function init {

   wp=$(pwd)
   
   run="scripts/run.sh"
   resultsDir="totalResults"
   testDir="test"

   dates=$(ls $testDir | awk '{print $1}')
   
   stock=$1
   modProfiles=$2
   
   host=$(hostname -s)
   if [[ $host == "ML-C02C8546LVDL" ]]; then
      activateDir="w/gitWS/lplTrade"
   elif [[ $host == "mm" ]]; then
      activateDir="/lplW2"
   else
      activateDir="git/lplTrade"
   fi

   tgtPath="${HOME}/${activateDir}"
   
   slave1=""
}

