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
   
   dbName=$1
   
   tmpFile="/tmp/tmp.rd"

   if [[ -n $dbName ]]; then
      dbNames=$dbName
   else
      dbNames=$(ls $testDir | awk '{print $1}')
   fi
      
   if [[ -f $tmpFile ]]; then
      rm -f $tmpFile
   fi
   
   dbInitFile="/tmp/dbInit"
}

function createDBSeedFile {

if [[ $dbName != "master" ]]; then

cat<<EOF > $dbInitFile
CREATE TABLE algoData (
    sym         varchar(10),
    day    varchar(10),
    algo        varchar(64),
    gain        numeric NOT NULL,
    winPct      numeric NOT NULL,
    CONSTRAINT symAlgo PRIMARY KEY(day,sym,algo)
);

CREATE TABLE algoModData (
    sym         varchar(10),
    day    varchar(10),
    algo        varchar(64),
    gain        numeric NOT NULL,
    winPct      numeric NOT NULL,
    CONSTRAINT symModAlgo PRIMARY KEY(day,sym,algo)
);

CREATE TABLE algoBestData (
    sym         varchar(10),
    days   text,
    algo        varchar(64),
    gain        numeric NOT NULL,
    totalGain   numeric NOT NULL,
    totalWinPct numeric NOT NULL,
    totalDays   integer NOT NULL,
    CONSTRAINT bestAlgos PRIMARY KEY(sym,algo)
);
EOF
}
else
   
cat<<EOF > $dbInitFile
CREATE TABLE master (
    sym         varchar(10),
    day         text,
    status      varchar(20),
    bestAlgo    varchar(64),
    liveAlgo    varchar(64),
    liveGain    numeric NOT NULL
    CHECK(status='live' OR status='liveComplete' OR status='test' OR status='testComplete' OR status='modTest' OR status='modTestComplete' OR status='bestTest' OR status='bestTestComplete'),
    CONSTRAINT symDayStatus PRIMARY KEY(sym,day,status)
);

CREATE TABLE algoBestData (
    sym         varchar(10),
    day         text,
    algo        varchar(64),
    gain        numeric NOT NULL,
    totalGain   numeric NOT NULL,
    totalWinPct numeric NOT NULL,
    totalDays   integer NOT NULL
);
EOF
fi
}

init $1

for dbName in $dbNames; do
   
   dbDir="db/${dbName}"
   log="db/${dbName}/log"
   
   if [[ ! -f $log ]]; then
      mkdir $dbDir
      
      initdb -D $dbDir || echo here1
      
      #pg_ctl -D db/${dbName} stop
      sleep 3
      echo pg_ctl -D $dbDir -l $log start
      pg_ctl -D $dbDir -l $log start || echo here2
      
      createdb algos || echo here3
      createDBSeedFile || echo here4
      psql -f $dbInitFile algos || echo here5
   else
      pg_ctl -D db/${dbName} -l $log start || echo here6
   fi
   
done