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


fname =  open(sys.argv[1],"r")
outRT="nc"
warmup=8000
out=open(outRT,"w")
lenght = sum(1 for line in open(sys.argv[1]))

for line in fname:
    value = line.split("\t")
    jobid=value[0].split("-")[2].split(".")[0].split("job")[1]
    if(int(jobid)>=int(warmup)):
        out.write(line)

fname.close()
out.close()

