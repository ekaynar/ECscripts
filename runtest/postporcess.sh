#!/bin/bash


# Bring in other script files
myPath="${BASH_SOURCE%/*}"
if [[ ! -d "$myPath" ]]; then
    myPath="$PWD" 
fi

repo="/tmp/final_res"
# Variables
source "$myPath/vars.shinc"


echo "Copying Files from Remote Clients" &&
for i in  $(seq 0 $slaves)
do
	ssh root@${slaveIP[$i]} "mv $bnchPATH/results $bnchPATH/$1.${slaveIP[$i]}" &&
	ssh root@${slaveIP[$i]} "mkdir $bnchPATH/results" 

	echo ""	
done



for i in  $(seq 0 $slaves)
do
        scp -r root@${slaveIP[$i]}:$bnchPATH/$1.${slaveIP[$i]} $repo/ &

done
wait


echo "Parsing Result Files" &&
for i in  $(seq 0 $slaves)
do
	echo $i
	./parser.py $repo/$1.${slaveIP[$i]}/	&&
	cat tmp_res_out.txt  >> $1.res
done


echo "Extract RT and Throughput" &&
./extract.py $1.res

