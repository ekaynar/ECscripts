#!/usr/bin/python
import getopt
import sys
import getopt
import random
import subprocess
import operator
dict={}
#f_name="files"
#f_job_name="jobs"

def create_files(argv):
	fd = open(sys.argv[1], 'r')
	out = open(sys.argv[2], 'w')
	out2 = open(sys.argv[3], 'w')
	filename=0
	jcount=0
	sume=0
	bucket=0
        for line in fd:
                value = line.split(" ")
		key=value[2]
		length =value[2].split("length=")[1].replace("\n","")
		length =16777216
		if key not in dict:
			dict[key]=filename
			sume+=int(length)
			#files = "sort128G "+"inputPath"+str(bucket)+" "+"file"+str(filename)+" "+str(length) +" \n"
			files = "sort128G1 "+"file"+str(filename)+" "+str(length) +" \n"
			out.write(files)
			filename+=1
		#req = "sort128G "+"inputPath"+str(bucket)+" file"+str(dict[key]) +" "+"job"+str(jcount)+" "+str(1)+" \n"
		req = "sort128G1 "+"file"+str(dict[key]) +" "+"job"+str(jcount)+" "+str(1)+" \n"
		out2.write(req)
		jcount+=1

		if filename%625 ==0:
			bucket+=1


	print len(dict)
	print filename
	print sume
        fd.close()
        out.close()
        out2.close()



if __name__ == "__main__":
	if len(sys.argv) != 4:
	        print ("Usage: ./create_files <trace file>  <uniqfiles> <jobfiles>")
		exit(0)

	create_files(sys.argv[1:])
