# ENV file for DB operations
wp="$(echo $HOME)/w/lplTrade"

time=$1
day=$(date "+%Y%m%d")

if [[ -z $time ]]; then time="160500"; fi
   
while [[ 1 ]]; do
   sleep 10
   now=$(date "+%H%M%S")
   echo now: $now
   echo time: $time
   letsGo=$(echo "$now > $time" | bc)
   if (( $letsGo == 1 )); then
      echo Starting tests at $day $time
      keepAliveDB.sh $day
      break
   fi
done