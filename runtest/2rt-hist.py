from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import pandas as pd

def draw(argv):

    fd = open(sys.argv[1], 'r')
    next(fd)
    time=[]
    perc=[]
    sample=[]
    tail=0
    tail99=0
    limit= int(sys.argv[2])
    count=0
    samps=0
    for line in fd:
         count+=1
         value = line.split(",")
   #      print value[0], value[1], value[2]
         time.append(value[0])
         sample.append(int(value[1]))
         samps+=int(value[1])
         perc.append(float(value[2].replace("%\n","")))
         if (float(value[2].replace("%\n","")) <= 90.0):
            tail = count
         if (float(value[2].replace("%\n","")) <= 99.0):
            tail99=count
         if (count*10>=800):
            break
         if (count*10 >= limit) and (count%20==0):
            break
        
    print count , tail
    fd.close()
    print samps
    y_pos = np.arange(len(sample))
    df = pd.DataFrame({"range": time,"sample": sample, "perc": perc})
    fig = plt.figure(figsize=(12,6))
    ax1 = fig.add_subplot(111)
    ax1 = df['sample'].plot(kind="bar", label='read', edgecolor = "none")
    plt.ylabel('Sample Count',  fontsize=20)
    plt.xlabel('ms',  fontsize=20)
       
    ax2 = ax1.twinx()
    ax2.plot(ax1.get_xticks(), df['perc'], label='CDF',marker='o',markeredgecolor='none', c='red', linewidth=2)
    plt.axvline(x=tail, ymin=0, ymax=1.02*df["sample"].max(), hold=None, color='black')
    plt.axvline(x=tail99, ymin=0, ymax=1.02*df["sample"].max(), hold=None, color='black')
    
    xlabels=[]
    locations=[]
    for i in range(0,len(time),10):
        xlabels.append(time[i])
        locations.append(i)
    print xlabels
    xticks_major = np.arange(len(time), step=10)
    ax1.set_xticks(xticks_major)
    ax2.set_xticks(xticks_major)
    ax1.set_xticklabels(xlabels,minor=False)
    ax2.set_xticklabels(xlabels,minor=False)

    ax1.set_ylim(0,1.02*df["sample"].max())
    ax2.set_ylim(0,1.05*df["perc"].max())
    ax1.set_xlim(0,count)
    ax2.set_xlim(0,count)
    plt.ylabel('Cummulative Percentage (%)',  fontsize=20)
    ax1.grid(True)
    
    lines1,l1=ax1.get_legend_handles_labels()
    lines2, l2=ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, l1 + l2, loc=4)
    ax1.tick_params(axis='both', which='major', labelsize=18 , top='off')
    ax2.tick_params(axis='both', which='major', labelsize=18 , top='off')
#    x =len(time)-tail
    ax2.annotate('90th\npercentile', xy=(tail, 90),xycoords='data', xytext=(tail+5, 80),
            arrowprops=dict(facecolor='black',width=2, shrink=0.05),
             horizontalalignment='left', verticalalignment='top',
            )
    ax2.annotate('99th\npercentile', xy=(tail99, 99),xycoords='data', xytext=(tail99+5, 90),
            arrowprops=dict(facecolor='black',width=2, shrink=0.05),
             horizontalalignment='left',verticalalignment='top'
            )
    ax2 = plt.gca() # grab the current axis
    locations.append(tail)
    locations.append(tail99)
    xlabels.append(time[tail])
    xlabels.append(time[tail99])
    ax2.set_xticks(locations) # choose which x locations to have ticks
    ax2.set_xticklabels(xlabels) # set the labels to display at those ticks
    plt.subplots_adjust(left=0.10, bottom=0.28, right=0.91, top=0.93 , wspace=0.2 ,hspace=0.2 )
    plt.savefig(sys.argv[1]+".png",bbox_inches='tight')
    plt.savefig(sys.argv[1]+".eps",bbox_inches='tight')
#    plt.title('EC(6,3) Replication')
    plt.show()


if __name__ == "__main__":
    draw(sys.argv[1:])

