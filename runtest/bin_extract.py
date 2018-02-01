#!/usr/bin/python
import collections
import sys
import itertools
import getopt
import subprocess
import os
import shutil
import time
import glob
import os
import numpy as np


if len(sys.argv) != 3:
        print ("Usage: ./bin_extract <folder name> <bin_size>")
	exit(0)


lat2,dat,perc,binarray=[],[],[],[]
binsize=int(sys.argv[2])
name=sys.argv[1].split(".")[0]

fname =  open(sys.argv[1],"r")
outRT=name+"-RT.csv"
warmup=20000


lenght = sum(1 for line in open(sys.argv[1]))
lenght-=warmup
for i in range(1000):
	lat2.append(int(0))
for line in fname:
	value = line.split("\t")
	jobid=value[0].split("-")[2].split(".")[0].split("job")[1]
	if(int(jobid)>=int(warmup)):
		latency=float(value[3].split("\n")[0])
		dat.append(latency*1000)		
fname.close()
#
fname= open(outRT, "w")
for i in range(binsize,len(dat),binsize):
	binarray.append(float(i))

bins = np.array(binarray)
data = np.array(dat)
inds = np.digitize(data, bins,right=False)
#
counter=collections.Counter(inds)
count=0
sum2=0

for i in range(int(1000)):
	sum2 += counter[i]/float(lenght)
	perc.append(sum2)

for i in range(len(lat2)):

        line= str(int(count))+"-"+str(int(count+float(binsize))) +","+str(int(counter[i])) +","+ str(perc[i])+"\n"
        fname.write(line)
        count+=float(binsize)
#	print str(count)+"-"+str(count+float(binsize)/100), str(int(counter[i])),str(perc[i])
fname.close()


exit(0)

