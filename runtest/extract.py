#!/usr/bin/python
import sys
import getopt
import subprocess
import os
import shutil
import time
import glob
import os



if len(sys.argv) != 2:
        print ("Usage: ./extract <folder name>")
	exit(0)


fname =  open(sys.argv[1],"r")
lat = []
b_size=1
outfile=sys.argv[1]+"rt.hist.csv"
lenght = sum(1 for line in open(sys.argv[1]))
for i in range(1000):
	lat.append(int(0))
for line in fname:
	value = line.split("\t")
	latency=float(value[3].split("\n")[0])
	lat[int(latency)]+=1
		
per=[]
sum2=0
for i in lat:
	sum2 += float(i)/float(lenght)
	per.append(sum2)

fname.close()
fname= open(outfile, "w")
count=0
for i in range(len(lat)):
	line= str(count)+"-"+str(count+1) +","+str(int(lat[i])) +","+ str(per[i])+"\n"
	fname.write(line)
	count+=1
fname.close()
print lat
exit(0)

