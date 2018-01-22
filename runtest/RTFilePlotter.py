#!/usr/bin/python
import sys
import datetime as dt
import csv
import numpy as np
import matplotlib.pyplot as plt
def create_files(argv):
	label, lat, per = [],[],[]
	counter=0
	with open(sys.argv[1],'r') as csvfile:
    		plots = csv.reader(csvfile, delimiter=',')
    		for row in plots:
			 label.append(row[0])
			 lat.append(int(row[1]))	
			 per.append(row[2])
			 if(float(row[2]) <= 0.90):
			 	x90=counter

			 if(float(row[2]) <= 0.95):
			 	x95=counter
			 if(float(row[2]) <= 0.99):
			 	x99=counter
			 counter+=1
	N = len(lat)
	x = range(N)
	width = 1/1.5
	fig = plt.figure(figsize=(18,6))
	ax1 = fig.add_subplot(111)
	cdf_ax = ax1.twinx()
	ax1.yaxis.grid(True)
	ax1.xaxis.grid(True)
	ax1.yaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
	ax1.xaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
	ax1.set_axisbelow(True)
	
	ax1.bar(x, lat, color='b', label='64K')
	cdf_ax.plot(per,color="r", label="CDF", marker="o")
	plt.tick_params(axis='both', which='major', labelsize=18)
	plt.tick_params(axis='both', which='minor', labelsize=18)
	plt.ylabel('Throughput (op/s)',  fontsize=20)
	plt.xlabel('Time (sec)',  fontsize=20)
	plt.axvline(x=x90, color='g', linestyle='--')
	plt.axvline(x=x95, color='r', linestyle='--')
	plt.axvline(x=x99, color='purple', linestyle='--')

	plt.xlim([0,80])
	leg=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0., fontsize=19)
	plt.subplots_adjust(left=0.12,bottom=0.18, right=0.9, top=0.85, wspace=0.2,hspace=0.2)
	plt.savefig(sys.argv[1]+'.pdf', format='pdf', dpi=1000)
	plt.savefig(sys.argv[1]+'.eps', format='eps', dpi=1000)
	plt.show()


if __name__ == "__main__":
	create_files(sys.argv[1:])
