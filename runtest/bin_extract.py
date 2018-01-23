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


if len(sys.argv) != 2:
        print ("Usage: ./bin_extract <folder name>")
	exit(0)


lat2,dat,perc,binarray=[],[],[],[]
binsize=25
name=sys.argv[1]+str(binsize)+"bin."

fname =  open(sys.argv[1],"r")
out_file = open (name+"latency", 'w')
outRT=name+"rt.hist.csv"
warmup=20000

lenght = sum(1 for line in open(sys.argv[1]))
for i in range(1000):
	lat2.append(int(0))
for line in fname:
	value = line.split("\t")
	jobid=value[0].split("-")[2].split(".")[0].split("job")[1]
	if(int(jobid)>=int(warmup)):
		latency=float(value[3].split("\n")[0])
		dat.append(latency)		

fname.close()

fname= open(outRT, "w")
for i in range(0,len(dat),binsize):
	binarray.append(float(i)/100)

bins = np.array(binarray)
data = np.array(dat)
inds = np.digitize(data, bins,right=True)

counter=collections.Counter(inds)
count=0
sum2=0
for i in range(int(1000/(float(binsize)/100))):
	sum2 += counter[i]/float(lenght)
	perc.append(sum2)


for i in range(len(lat2)):
        line= str(count)+"-"+str(count+float(binsize)/100) +","+str(int(counter[i])) +","+ str(perc[i])+"\n"
        fname.write(line)
        count+=float(binsize)/100
#	print str(count)+"-"+str(count+float(binsize)/100), str(int(counter[i])),str(perc[i])
fname.close()


exit(0)

