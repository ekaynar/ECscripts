#!/usr/bin/python
import getopt
import sys
import subprocess
from subprocess import call
from multiprocessing.dummy import Pool as ThreadPool
import collections
import os
import time
import os.path

dict={}
rgwURL=""
rgwKEY=""
objSize=""
filenames=[]
sizes=[]

def swift(file,lenght):
	print file
	command ="cp "+objSize+"M "+ file
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
#	with open(file, 'wb') as fout:
#        	fout.write(os.urandom(int(lenght)))
	command= "swift -A http://"+rgwURL+"/auth/1.0 -U johndoe:swift -K "+rgwKEY+" upload sort128G1 "+ file
#	print command
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	os.remove(file)
#	print file
def product_helper(args):
	return swift(*args)

def calculateParallel(key,size):
	pool = ThreadPool(2)
	job_args = [(item_a, size[i]) for i, item_a in enumerate(key)]
	results = pool.map(product_helper,job_args)


def upload(argv):
	fd = open(sys.argv[1], 'r')
	#hash={}
	count =1

        for line in fd:
                value = line.split(" ")
		if line not in dict:
			dict[value[1]]=value[2].replace('\n','')
			filenames.append(value[1])
			sizes.append(dict[value[1]])
			print value[1],value[2]
		count+=1
#		if count==20:
#			break;
        fd.close()

	calculateParallel(filenames,sizes)

if __name__ == "__main__":
	rgwURL=sys.argv[2]
	rgwKEY=sys.argv[3]
	objSize=sys.argv[4]
	upload(sys.argv[1:])
