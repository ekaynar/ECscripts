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
        print ("Usage: ./parser.py <folder name>")
	exit(0)

pr_fol = os.getcwd()
pr_fol = pr_fol +"/"+ sys.argv[1]
pr_fol =  sys.argv[1]
out_file = open ("tmp_res_out.txt", 'w')
res_out = []
for fi in os.listdir(pr_fol):
	BW=latency=""
	starter = "output-"
        if fi.startswith(starter):	
		file_path = pr_fol + "/" + fi
		with open (file_path, 'r') as f_hndl:
			for line in f_hndl:
				 if line.startswith("\r"):
					f_res = line.split("\r")
                                        try:
						raw_data =  f_res[-1].split()
                #                        	print raw_data,"\t",fi
						raw_data = raw_data[6]
						if "M" in raw_data:
							BW = raw_data.split("M")[0]
							BW=float(BW)*1024
						else:
							BW = raw_data.split("k")[0]
					except IndexError:
                                                raw_data = 0
						BW = 0
				 if line.startswith("time_total"):
					latency=line.split("=")[1]
				 else:
					latency=str(0)+"\n"
		out_file.write(fi+"\t"+ str(raw_data)+"\t"+str(BW)+"\t"+str(latency))


out_file.close()
exit(0)

