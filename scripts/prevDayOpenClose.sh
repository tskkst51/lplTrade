#!/bin/bash

function init {

   . $LPLT/scripts/db.sh

   sym=""
   
   sym=$1

   if [[ -z $sym ]]; then
      echo need symbol!
      exit 1
   fi
   
   wp=$LPLT

   activateDir="/lplW2"
   
   activateCmd=$(dirname $wp)
   activateCmd+="${activateDir}/bin/activate"
   
   py3=$(dirname $wp)
   py3+="${activateDir}/bin/python3"
   
   # Execute script to populate source library path
   
   dt=$(date "+%Y%m%d")
}


#~~~~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

init "$1"

openedUp=0
openedDown=0
dif=0
prevDay=down=up=0
ctr=0
totGain=0
gain=0
winUp=winDown=0
for l in $(cat "dc/${sym}.dc"); do
   ctr=$((ctr + 1))
   if (( $prevDay != 0)); then
      open=$(echo $l | awk -F, '{print $3}')
      dif=$(echo "scale=2 ; $prevClose - $open" | bc)
      dif=$(echo "scale=2 ; $dif > 0" | bc)

      if (( dif > 0 ));then
         down=1
      else
         up=1
      fi
      
      if (( prevClosedDown == 1 )) && (( up == 1 )); then
         openedUp=$((openedUp + 1))
         winUp=1
      elif (( prevClosedUp == 1 )) && (( down == 1 )); then
         openedDown=$((openedDown + 1))
         winDown=1
      fi
      prevDay=0
      prevClosedDown=0
      prevClosedUp=0
   else
      prevOpen=$(echo $l | awk -F, '{print $3}')
      prevClose=$(echo $l | awk -F, '{print $4}')
      
      prevDif=$(echo "scale=2 ; $prevOpen - $prevClose" | bc)
      prevDif=$(echo "scale=2 ; $prevDif > 0" | bc)
      
      if (( prevDif > 0 ));then
         prevClosedDown=1
      else
         prevClosedUp=1
      fi
      prevDay=1
      winUp=0
      winDown=0
      up=0
      down=0
   fi
   
   if (( prevDay == 0));then   
#      echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#      echo prevOpen $prevOpen prevClose $prevClose prevDif $prevDif
#      echo open $open close $close dif $dif
#      echo openedDown $openedDown 
#      echo openedUp $openedUp 
#      echo winDown $winDown winUp $winUp
      
      if (( winDown == 1)); then
         gain=$(echo "$prevClose - $open" | bc)
         #echo H1
      elif (( winUp == 1)); then
         gain=$(echo "$open - $prevClose" | bc)
         #echo H2
      elif (( down == 0)); then
         gain=$(echo "$prevClose - $open" | bc)
         #echo H3
      elif (( up == 0)); then
         gain=$(echo "$open - $prevClose" | bc)
         #echo H4
      fi
      totGain=$(echo "$totGain + $gain" | bc)

      #echo gain $gain      
      #echo totGain $totGain
      
   fi
done

ctr=$(echo "scale=2 ; $ctr / 2" | bc)

opendUpWhenDown=$(echo "scale=2 ; $openedUp + $openedUp" | bc)

pctWin=$(echo "scale=2 ; $opendUpWhenDown / $ctr" | bc)
echo $sym win "$(echo "scale=2 ; $pctWin * 100" | bc)" % \$ ${totGain} /year
#echo $sym win "$(echo "scale=2 ; $pctWin * 100" | bc)"% \$${totGain}/year

exit 0

