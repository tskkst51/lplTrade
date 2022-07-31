# Cleanup all the DC's of symbols that do not exist anymore before DAY

day=$1

if [[ -z $day ]]; then 
   echo need date e.g. 20220304
   exit 1
fi

testDir="test"
days=$(ls test)

cd dc || echo cant cd to dc

for f in $(ls | grep -E ".dc"); do 
   stock=$(echo $f | cut -d\. -f1)
   if [[ $(tail -1 $f |cut -f9 -d,) < $day ]]; then 
      gp=$(echo $f | sed "s/.dc/.gp/")
      tail -1 $f
      echo removing $f $gp
      rm $gp || echo cant remove $gp
      rm $f || echo cant remove $f
      # Remove test data
      for day in $days; do
         echo $day $stock
         if [[ -f "../${testDir}/${day}/bc/active${stock}.bc" ]]; then
            echo moving "../${testDir}/${day}/bc/active${stock}.bc" to tmp
            mkdir -p "../tmp/${day}/bc"
            mv  "../${testDir}/${day}/bc/active${stock}.bc ../tmp/${day}/bc" || echo cant remove ${stock}.bc
            echo moving "../${testDir}/${day}/prices/active${stock}.pr" to tmp
            mkdir -p "../tmp/${day}/prices"
            mv "../${testDir}/${day}/prices/active${stock}.pr ../tmp/${day}/prices" || echo cant remove ${stock}.pr
         fi
      done
   fi
done

exit 0