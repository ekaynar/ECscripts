import numpy as np
import matplotlib.pyplot as plt
import time
import sys


data = np.genfromtxt("th.csv", delimiter=',' ,skip_header=0, names=['a', 'b' ,'c','d' ,'e','f','g'])


minor_ticks = np.arange(0, 2501, 250)
major_ticks = np.arange(0, 2501, 500)

N=3
ind = np.arange(N)  # the x locations for the groups
width = 0.15       # the width of the bars

fig = plt.figure(figsize=(6,4))
ax1 = fig.add_subplot(111)

#Grid
ax1.grid(True)
#ax1.yaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
ax1.xaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
ax1.set_axisbelow(True)

#(158, 154, 200), "ppurple1"
#@map color 30 to (117, 107, 177), "ppurple2"
#@map color 31 to (84, 39, 143), "ppurple3"
##9E9AC8
color0="#cbc9e2"
color1="#54278f"
color2="#9e9ac8"
color3="#6a51a3"


##Max bar
#ax1.text(3, 5150, "Max SSD Bandwidth", fontsize=18,color="black")
#plt.axhline(y=5000, xmin=0, xmax=8,color="black",linestyle='--',linewidth=2,hold=None)

print data['b']
# Drawing Bars
ax1.bar(ind +width, data['b'], width , color='#cbc9e2', label='EC',align='center',edgecolor='none')
ax1.bar(ind +(width*2) , data['c'], width, color='#9E9AC8', label='EC with cache',align='center',edgecolor="none")
ax1.bar(ind +(width*3) , data['d'], width, color='#756BB1', label='3xRep ',align='center',edgecolor='none')
ax1.bar(ind +(width*4) , data['e'], width, color='#6a51a3', label='3xRep with cache',align='center',edgecolor='none')

labels = [item.get_text() for item in ax1.get_yticklabels()]
labels=[]
ax1.set_yticklabels(labels)

labels2 = [item.get_text() for item in ax1.get_yminorticklabels()]
labels2=['', '','30','','50' ,'','75']
ax1.set_yticklabels(labels2,minor=True)

## Puttin Axes..etc
plt.ylim([0,20])
#plt.xlim([0,4])
plt.tick_params(axis='both', which='major', labelsize=12 , top='off' ,right='off')
plt.tick_params(axis='both', which='minor', labelsize=12, top='off', right='off')

#Axes Labels
plt.ylabel('Throughput (MB/sec)',  fontsize=14)
plt.xlabel('Hit Ratio (%)',  fontsize=14)

#Legend
leg=plt.legend(fontsize=10, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
#leg=plt.legend( loc="upper left", ncol=1, borderaxespad=0., fontsize=18)

plt.xticks(ind + (width*2+width/2), ( '30','50','75','8','16','32'))
#plt.yticks('1','1.5','2','2.5','3','3.5','4','4.5','5','5.5')

plt.subplots_adjust(left=0.16, bottom=0.21, right=0.84, top=0.73 , wspace=0.2 ,hspace=0.2 )
plt.savefig("overhead_scale.png",bbox_inches='tight')
plt.savefig("overhead_scale.eps",bbox_inches='tight')
plt.show()

