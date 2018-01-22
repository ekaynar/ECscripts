#!/usr/bin/python

#Make sure about the data-set

import sys
import getopt
import subprocess
import os
import shutil
import time 
import bnch_cfg

token=""

def usage():
    print ("usage: ")

def get_token():
    while(1):
        _token = subprocess.Popen(["swift -A http://%s:%d/auth/1.0 -U %s:swift -K %s auth | grep AUTH_rgwtk | awk -F = '{print $2'}" %(bnch_cfg.L1_rgwaddr, bnch_cfg.L1_rgwport, bnch_cfg.swiftuser, bnch_cfg.key)], shell=True, stdout=subprocess.PIPE).communicate()[0]
        if _token != "":
                return _token
        time.sleep(10)

def do_slave (iters, cur_i, count):
    procs = []
    token = get_token()
    for i in range(1, count+1):
      procs.append(subprocess.Popen(["curl -i http://%s:%d/swift/v1/%s/%s%d -X GET -H \"X-Auth-Token: %s \" -o /dev/null 2>&1 | tee %soutput-%d-%d-%d.txt" %(bnch_cfg.L1_rgwaddr, bnch_cfg.L1_rgwport, bnch_cfg.bucket_name, bnch_cfg.obj_name, i, token, bnch_cfg.logloc, iters, cur_i, i)], shell=True))
    exit_code = [p.wait() for p in procs]

def run(test, iters, count, cur_it):
    print(token)
    if test == 'L1': #L1
        output = hit_L1(iters, count)
    if test == 'L2': #L2
        output = hit_L2(iters, count)
    if test == 'CR_L1': #Cache Tiering Ceph DRAM when a single cache server is used 
        output = do_CR(iters, count, "L1")
    if test == 'CH_L1': #Cache Tiering Ceph HDD when a single cache server is used
        output = do_CH(iters, count, "L1")
    if test == 'CR_L2': #Cache Tiering Ceph DRAM in distributed mode
        output = do_CR(iters, count, "L2")
    if test == 'CH_L2': #Cache Tiering Ceph HDD in distributed mode
        output = do_CH(iters, count, "L2")
    if test == 'CR_VN': #Vanilla Ceph DRAM
        output = do_CR(iters, count, "VN")
    if test == 'CH_VN': #Vanilla Ceph HDD
        do_CH(iters, count, "VN")
    if test == 'by_remote': #runnig slave
	do_slave(iters, cur_it, count)

def main(argv):
    try:
       opts, args = getopt.getopt(argv, "ht:i:c:o:u:m:", ["test=", "iter=", "count=", "logfile=", "user=", "cur_iter="]);
    except getopt.GetoptError:
       usage();
       exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ('-t', "--test"):
            test = arg 
        elif opt in ('-i', "--iter"):
            iters = int(arg)
        elif opt in ('-c', "--count"):
	    count = int(arg)
        elif opt in ('-m', "--cur_iter"):
            cur_it = int(arg)
        elif opt in ('-o', "--logfile"):
            lf = arg
	elif opt in ('-u', "--user"):
            MOC_usr = arg
    run(test, iters, count, cur_it)

if __name__ == "__main__":
    main(sys.argv[1:])
