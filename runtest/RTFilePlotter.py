#!/usr/bin/python
import sys
import matplotlib.ticker as ticker
import datetime as dt
import csv
import numpy as np
import matplotlib.pyplot as plt
def create_files(argv):
    label, lat, per = [],[],[]
    counter=0
    name=sys.argv[1].split(".")[0]
    if(sys.argv[2]=="ec"):
	t = "EC(6,3)"
    else:
	t="3xRep"
    if (sys.argv[3]=="cache"):
	c= " with Cache"
    else:
	c=""
    with open(sys.argv[1],'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
            # val=row[0].split("-")
            # l = str(float(val[0])/1000)+"-"+str(float(val[1])/1000)
            # label.append(l)
             label.append(row[0])
             lat.append(int(row[1]))    
             per.append(float(row[2])*100)
             if(float(row[2]) <= 0.90):
                x90=counter

             if(float(row[2]) <= 0.95):
                x95=counter
             if(float(row[2]) <= 0.99):
                x99=counter
             counter+=1
    N = len(lat)
    #print N
    x = range(N)
    fig = plt.figure(figsize=(5,5))
    ax1 = fig.add_subplot(111)
    plt.ylabel('Request Count',  fontsize=14)
    plt.xlabel('Time (ms)',  fontsize=14)
    #ax1.bar(x, lat, color='#00008B', label=t+c)
    ax1.bar(x, lat, color='b', label="RT",edgecolor = "none")
    #ax1.bar(x, lat, color='b', label=t+c,edgecolor = "none")
    cdf_ax = ax1.twinx()

    # Grid
    ax1.grid(True)
    ax1.yaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
    ax1.xaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
    ax1.set_axisbelow(True)
  
 
    cdf_ax.plot(x,per,color="#FF8C00", label="CDF", marker="o",markeredgecolor="none")
   # cdf_ax.plot(per,color="#00008B", label="CDF", marker="o")
    cdf_ax.set_ylim(0,110)
    ax1.tick_params(axis='both', which='major', labelsize=13 , top='off')
    cdf_ax.tick_params(axis='both', which='major', labelsize=13 , top='off')
    plt.ylabel('Cummulative Percentage (%)',  fontsize=14)
    plt.title(t, fontsize=16)

    plt.axvline(x=x90, color='black', linestyle='--')
#    plt.axvline(x=x95, color='r', linestyle='--')
    plt.axvline(x=x99, color='black', linestyle='--')

    # Y-Label
    ylabels=[]
    a=ax1.get_yticks().tolist()
    for i in a:
        ylabels.append(str(int(i/1000))+"K")
    ylabels[0]=""
    ax1.set_yticklabels(ylabels)
    
    # X-Label
    xlabels=[]
    locations=[]
    for i in range(0,N,2):
        xlabels.append(label[i])
        locations.append(i)

    xticks_major = np.arange(len(label), step=2)
    ax1.set_xticks(xticks_major)
    #cdf_ax.set_xticks(xticks_major)
    ax1.set_xticklabels(xlabels,minor=False,rotation=90)
    #cdf_ax.set_xticklabels(xlabels,minor=False,rotation=90)



    # Legends
    lines1,l1=ax1.get_legend_handles_labels()
    lines2, l2=cdf_ax.get_legend_handles_labels()
#    cdf_ax.legend(lines1 + lines2, l1 + l2,fontsize=14, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)   
    cdf_ax.legend(lines1 + lines2, l1 + l2,fontsize=11, loc=4)
  #  plt.axis('equal')
    plt.xticks(rotation=90)


    plt.xlim([0,14])
#    lo = ax1.get_xlim()
#    lo2 = cdf_ax.get_xlim()
#    f = lambda x : lo2[0]+(x-lo[0])/(lo[1]-lo[0])*(lo2[1]-lo2[0])
#    ticks = f(ax1.get_xticks())
#    cdf_ax.xaxis.set_major_locator(ticker.FixedLocator(ticks))
#
    plt.rc('font', family='serif')
    plt.subplots_adjust(left=0.18, bottom=0.38, right=0.81, top=0.87 , wspace=0.2 ,hspace=0.2 )
    #plt.subplots_adjust(left=0.10, bottom=0.28, right=0.91, top=0.93 , wspace=0.2 ,hspace=0.2 )
    plt.savefig(name+".pdf",bbox_inches='tight')
    plt.savefig(name+".eps",bbox_inches='tight')
    plt.show()


if __name__ == "__main__":

   if len(sys.argv) != 4:
   	print ("Usage: ./RTFilePlotter.py <file name> <ec/rep> <cache>")
        exit(0)
   create_files(sys.argv[1:])
