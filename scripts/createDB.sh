#!/bin/bash
 
function init {

   $HOME/bin/lplt.sh

   #xattr -d com.apple.quarantine scripts/* > /dev/null 2>&1
   wp=$(pwd)

   activateDir="/lplW2"
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   testDir="test"
   
   today=$(date "+%Y%m%d")
   
   #cd $exDir || exit 1
   
   day=$1
   
   tmpFile="/tmp/tmp.rd"

   if [[ -n $day ]]; then
      days=$day
   else
      days=$(ls $testDir | awk '{print $1}')
   fi
   
   if [[ -f $tmpFile ]]; then
      rm -f $tmpFile
   fi
   
   dbInitFile="/tmp/dbInit"
      
   . $LPLT/scripts/db.sh
}

function createDBSeedFile {

cat<<EOF > $dbInitFile
CREATE TABLE algoData (
    sym         varchar(10),
    algo        varchar(64),
    gain        numeric NOT NULL,
    winPct      numeric NOT NULL,
    CONSTRAINT symAlgo PRIMARY KEY(sym,algo)
);

CREATE TABLE algoModData (
    sym         varchar(10),
    algo        varchar(64),
    gain        numeric NOT NULL,
    winPct      numeric NOT NULL,
    CONSTRAINT symModAlgo PRIMARY KEY(sym,algo)
);


EOF
}

#CREATE TABLE algoBestData (
#    sym         varchar(10),
#    days        text,
#    algo        varchar(64),
#    gain        numeric NOT NULL,
#    totalGain   numeric NOT NULL,
#    totalWinPct numeric NOT NULL,
#    totalDays   integer NOT NULL,
#);

init $1

for day in $days; do
   isDBRunning $day
   if [[ $? != 0 ]]; then
      echo DB $day is already running...
      exit 0
   fi
   
   isDBCreated $day
   if [[ $? != 0 ]]; then
      echo DB $day already exists...
      exit 0
   fi
      
   rm -fr db/${day} || exit 1
   mkdir db/${day} || exit 1
   
   echo DB $day does not exist. Creating...
   
   port=$(getNextPort)
   
   echo Using port ${port}...
   
   log="db/${day}/log"
         
   initdb -D "db/${day}"
   createDBSeedFile
   startDB $day $port
   if [[ $? != 0 ]]; then
      echo ERROR starting DB $day
   fi
   createdb -p $port algos 
   psql -f $dbInitFile -p $port algos
   
done

exit 0