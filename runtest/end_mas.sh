#!/bin/bash


# Bring in other script files
myPath="${BASH_SOURCE%/*}"
if [[ ! -d "$myPath" ]]; then
    myPath="$PWD" 
fi

# Variables
source "$myPath/vars.shinc"



for i in  $(seq 0 $slaves)
do
	#echo ${slaveIP[$i]}
	#echo ${jobs[$i]}
	ssh root@${slaveIP[$i]} "$bnchPATH/bnch_master.py $bnchPATH/${jobs[$i]} 0" &
#	ssh  root@${workerIP[$i]} "$path/upload.py $path/${files[$i]}" &

done

wait

