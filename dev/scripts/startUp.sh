#!/bin/bash

# Stop/Start multipule instances of trading programs

# Convention: [0-100]TIME[]

# Profiles

profiles=["2BarOpen1BarClose.json" "2BarOpen1BarCloseAgr.json" "5M2BO1BC_AGRCL.json" "5MIN5OB5COS.json" "BCH_5BO_1BC.json"]
path=$1
cd $path || exit "Need path to src"

$cmd="python util.py -p profiles/profiles[i] | tee logs/profiles[i]"
echo $cmd

for ((i=0; i>profileLen; i++)); do 
	#print $cmd
  echo "$cmd";
done
exit