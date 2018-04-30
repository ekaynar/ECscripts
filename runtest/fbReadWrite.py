#!/usr/bin/python
import sys
import datetime as dt
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


def create_files(argv):
    label, lat, per = [],[],[]
    counter=0
    name=sys.argv[1].split(".")[0]
    #df = pd.read_csv(sys.argv[1], usecols=['ratio','rep','ec6','ec10'])
    df = pd.read_csv(sys.argv[1], usecols=['ratio','fb75'])
    w1,w2,w3=[],[],[]   
    for i in  df['fb75']: 
    	w1.append(i)
    	w2.append(i/2)
    	w3.append(i*31.05/160.21)

    print w1
    print w2
    print w3

    for i in range(len(w1)):
		if float(w1[i]) < 1:
			w1[i] = (float(1)/float(w1[i]))*-1+2
    
    for i in range(len(w2)):
		if float(w2[i]) < 1:
			w2[i] = (float(1)/float(w2[i]))*-1+2

    for i in range(len(w3)):
		if float(w3[i]) < 1:
			w3[i] = (float(1)/float(w3[i]))*-1+2


    fig = plt.figure(figsize=(3.5,3.5))
    ax1 = fig.add_subplot(111)
    plt.xlabel('Cache_Size',  fontsize=13)
    plt.ylabel('Read/Write Ratio',  fontsize=13)
   # plt.title("Network Load", fontsize=13)
    #ax1.plot(df['fb75'], color='b', marker='o',markeredgecolor=None,label='FB-(5:1)')
    #ax1.plot(df['fb75']/2,  color='g', marker='^',markeredgecolor=None,label='FB-(2.5:1)')
    #ax1.plot(df['fb75']*31.05/160.21,  color='magenta', marker='^',markeredgecolor=None,label='FB-(1:1)')
    ax1.plot(w1, color='b', marker='o',markeredgecolor=None,label='FB-(5:1)')
    ax1.plot(w2,  color='g', marker='^',markeredgecolor=None,label='FB-(2.5:1)')
    ax1.plot(w3,  color='magenta', marker='^',markeredgecolor=None,label='FB-(1:1)')
    plt.axhline(y=1,color='brown',lw=1.2)
#    ax1.plot(df['ec10'],  color='magenta', marker='s',markeredgecolor=None,label='EC(10,4)')

#    minor_ticks = np.arange(0, 10000, 500)
    #Grid
 #   ax1.set_yticks(minor_ticks, minor=True)
    ax1.yaxis.grid(which='minor', alpha=0.5)
    ax1.yaxis.grid(True)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
    ax1.xaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
    ax1.set_axisbelow(True)
#    ax1.set_xscale('log')
    
    xticks_major = np.arange(0,31, step=4)
    yticks_major = np.arange(-5,8, step=2)
    ax1.set_xticks(xticks_major)
    ax1.set_yticks(yticks_major)
    #ax1.set_xticklabels(df['ratio'],minor=False)
    xlabs = [float(i)/100 for i in range(0,30,4)]
    ax1.set_xticklabels(xlabs)
    ylabs=["1:7","1:5","1:3","1:1","3:1","5:1","7:1"]
    ax1.set_yticklabels(ylabs)
    plt.xticks(rotation=45)
    # Legends
    plt.legend(loc=1,fontsize=9)
#    ymax=3500
    plt.ylim([-5,7])
    plt.xlim([0,31])
    #plt.xticks(rotation=90)
    plt.subplots_adjust(left=0.20, bottom=0.38, right=0.89, top=0.87 , wspace=0.2 ,hspace=0.2 )
    plt.savefig(name+".pdf",bbox_inches='tight')
    plt.savefig(name+".eps",bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    create_files(sys.argv[1:])
