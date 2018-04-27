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
    df = pd.read_csv(sys.argv[1], usecols=['name','count'])
    
    fig = plt.figure(figsize=(3.5,3.5))
    ax1 = fig.add_subplot(111)
    plt.xlabel('Cache_Size',  fontsize=13)
    plt.ylabel('Read/Write Ratio',  fontsize=13)
    #ax1.plot(df['count'], color='b', marker='o',markeredgecolor=None,label='FB-(5:1)')
    ax1.plot(df['count'], color='b',label='FB-(5:1)')

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
    
  #  print df['ratio']
    #xticks_major = np.arange(len(label), step=5)
    #ax1.set_xticks(xticks_major)
   # ax1.set_xticklabels(df['ratio'],minor=False)
   # xlabs = [float(i)/100.0 for i in range(0,30,4)]
   # ax1.set_xticklabels(xlabs)

    # Legends
    plt.legend(loc=1,fontsize=11)
#    ymax=3500
    plt.xlim([-0.05,1200])
    #plt.xticks(rotation=90)
    plt.subplots_adjust(left=0.14, bottom=0.38, right=0.89, top=0.87 , wspace=0.2 ,hspace=0.2 )
    plt.savefig(name+".pdf",bbox_inches='tight')
    plt.savefig(name+".eps",bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    create_files(sys.argv[1:])
