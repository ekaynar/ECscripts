import sys
import numpy as np
import operator
import pandas as pd
from collections import deque
from lru import LRU
import ConfigParser
import logging
##############################################################
## GLobal Variables
#-----------------------------
key=[]
dict={}
osize=[]
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
log_file = config.get('My Section', 'log_file')
logging.basicConfig(filename=log_file,level=logging.DEBUG)


## Parsing the input file
## Get object ID,size and calculate footprint of
## input data for calculating the cache size, 
#----------------------------------------------
def parse(fname):
        fd = open(fname, 'r')
        hit=miss=0
	counter=0
	for line in fd:
		counter+=1
                value = line.split(" ")
                key1 = value[2]
                key.append(key1)
		osize.append(int(64))
                if key1 not in dict:
                        dict[key1]=1
			miss+=1
		else:
			hit+=1
        fd.close()
	dict.clear()
	logging.info("Hit " + str(hit))
	logging.info("Miss " + str(miss))
	print hit, miss

def lru2(new_list):
        size = avail= 115*1024*4
        hashmap={}
        hit=miss=0
	avail=int(avail)
        cache = LRU(82170872)
        for i in range(len(new_list)):
                if new_list[i] in hashmap:
                        hit+=1
                        cache[new_list[i]]=osize[i]
                else:
                        miss +=1
                        if (int(osize[i]) <= avail):
                                cache[new_list[i]]="1"
                                hashmap[new_list[i]]=int(osize[i])
                                avail -= int(osize[i])
                        else:
                                while(int(osize[i]) > avail):
                                        id = cache.peek_last_item()[0]
                                        avail+=int(hashmap[id])
                                        del cache[id]
                                        del hashmap[id]
                                hashmap[new_list[i]]=osize[i]
                                cache[new_list[i]]="1"
                                avail -= int(osize[i])
	print "lru2",hit, miss

def lru(new_list):
	hit=miss=0
	cache = LRU(1840*4)
	for i in range(len(new_list)):
		if new_list[i] in cache:
			hit+=1
			cache[new_list[i]]="1"
		else:
			miss +=1
			cache[new_list[i]]="1"
	#print hit, "," , miss
	hitratio=float(hit)/float(hit+miss)
	#print "hitratio",hitratio
#	if (float(hitratio) > float(0.75)):
#		print hit, "," , miss
#		print "hitratio",hitratio
		
	return hitratio
	
if __name__ == "__main__":

## Load the configuration filec
#------------------------------
	input_file = config.get('My Section', 'input_file')	

## Parsing the Input File
	logging.info('**************************')
	logging.info('Parsing ' + str(input_file))
	parse(input_file)

## Running Single Level Cache
	for i in range(5500000,22717987,1000):
		new_list = key[i:i+400000]
		r=lru(new_list)
		if (float(r) > float(0.36)):
		
			print "--------------"
			print "line:",i ," : ", i+400000
			print r	
		if(float(r) >float(0.38)):
			break;
   	
