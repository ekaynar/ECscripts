#!/bin/bash


# Bring in other script files
myPath="${BASH_SOURCE%/*}"
if [[ ! -d "$myPath" ]]; then
    myPath="$PWD"
fi

# Variables
source "$myPath/vars.shinc"


# Split files to distribute across workers

lines="$(wc $fname | awk '{print $1}')" &&
splitSize=$((lines / (workers+1)+1))

echo "Spliting Files"
split -l $splitSize $fname part
i=0
for entry in "."/part*
do

   files[$i]="$entry"
    (( i++ ))
done

echo ${files[1]}


# Copy Files into worker nodes
echo "Copying Files"
for i in  $(seq 0 $workers)
do
   echo ${workerIP[$i]}
	scp -r ${files[$i]} root@${workerIP[$i]}:$path/${files[$i]}
done

for i in  $(seq 0 $workers)
do
	ssh  root@${workerIP[$i]} "$path/2upload.py $path/${files[$i]}" &

done

wait
