#!/bin/bash


# Bring in other script files
myPath="${BASH_SOURCE%/*}"
if [[ ! -d "$myPath" ]]; then
    myPath="$PWD"
fi



# Variables
source "$myPath/vars.shinc"

ddF=$size
ddF+="M"
#create fileV
dd if=/dev/zero of=$ddF  bs=1M  count=$size &&
echo "file is created"

# Get RGW credentials
rgwKEY=$(radosgw-admin user info --uid=$rgwUSER | grep secret_key | tail -1 | awk '{print $2}' | sed 's/"//g')


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


echo "Running Upload Script"
for i in  $(seq 0 $workers)
do
	ssh  root@${workerIP[$i]} "cd $path && $path/upload.py $path/${files[$i]} $rgwURL $rgwKEY $size" &

done

wait
