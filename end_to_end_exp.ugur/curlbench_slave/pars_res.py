#!/usr/bin/python
import sys
import getopt
import subprocess
import os
import shutil
import time

if len(sys.argv) != 2:
	print ("Usage: ./res_parser.py <folder name>")
	
pr_fol = os.getcwd()
pr_fol = pr_fol + "/results/" + sys.argv[1]
iteration = 10 # number of simulation we re-do
out_file = open ("tmp_res_out.txt", 'w')
res_out = [] 
for i in range(iteration):
	res_out.append([])
for fi in os.listdir(pr_fol):
	for i in range(iteration):
		starter = "output-"+str(i+1)+"-"
		if fi.startswith(starter):
			file_path = pr_fol + "/" + fi
			with open (file_path, 'r') as f_hndl:
				for line in f_hndl:
					if line.startswith("\r"):
						f_res = line.split("\r")
						raw_data =  f_res[-1].split()
						raw_data = raw_data[6]
						BW = raw_data.split("M")
						print BW[0]
						res_out[i].append(BW[0])
						
print res_out
print len(res_out)
print len(res_out[0])
for j in range(len(res_out[0])):
	out_file.write("\n")
	for i in range(iteration):	
		if len(res_out[i]) !=0:
			out_file.write(str(res_out[i][j])+ " ")
		
out_file.close()
			
