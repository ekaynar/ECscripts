#!/usr/bin/python

#This trace recievs the job file and the # of client as an input
#Make sure about the bucket names for master and the slave - They should be different as we do not wanna read the same file
#Make sure that the correct RGW (Vanilla vs. RGWCache) is installed

import sys
import getopt
import subprocess
import os
import shutil
import time 
import bnch_cfg
import urllib3
import threading
import time
import os.path
import socket
import thread


time_hndl = open("start_time.txt", "w")
token = ""

def usage():
    print ("usage: ./bnch_master.py <job_file> <client_cnt>")

def get_token():
    while(1):
    	_token = subprocess.Popen(["swift -A http://%s:%d/auth/1.0 -U %s:swift -K %s auth | grep AUTH_rgwtk | awk -F = '{print $2'}" %(bnch_cfg.L1_rgwaddr, bnch_cfg.L1_rgwport, bnch_cfg.swiftuser,bnch_cfg.key)], shell=True, stdout=subprocess.PIPE).communicate()[0]
	if _token != "":
		return _token
	time.sleep(5)

class serverThread (threading.Thread):
    def __init__(self, threadID,  lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.lock = lock
    def run(self):
        print "Starting thread " + self.threadID
        sendReqPacket(self.lock)
        print "Exiting thread " + self.threadID


def on_new_client(c , addr, threadLock):
	global start_cntr
	global time_hndl
	ter_flg  = 0
	while True:
	#	threadLock.acquire()
		if ter_flg == 0 and len(curl_tasks) < ((task_cntr *2 )/ 3):
			st_time = time.strftime("%H:%M:%S")
			print "Warming up time finished..... Start time: ", (time.strftime("%H:%M:%S")), task_cntr, "---  ", len(curl_tasks), " ", str(st_time)  ,"\n"
			time_hndl.write("Start time: " + str(st_time) +  ",    all tasks, remaning tasks:   " + str(task_cntr) + " ," + str(len(curl_tasks)) +  "\n")
			time_hndl.close()
			ter_flg = 1
	#	threadLock.release()
		#else:
		#	 print "time ----------------------------------------------------: ", str(len(curl_tasks)), "\n"
#		print 'Got connection from', addr
   		data = c.recv(9)
#        	print "------------------------------", data
        	if data == "Need more":
            		threadLock.acquire()
            		if len(curl_tasks) > 0:
                		x = curl_tasks.pop(0)
                		c.send('%s %s %s %s %s ' %(x.bucket_name, x.dataset_name, x.obj_name, x.job_id, x.req_num))
                		threadLock.release()
            		else:
                		c.send("empty")
				print "Sending empty.....................\n"
				c.close()
                		threadLock.release()
                		break 
		elif data == "start":
			threadLock.acquire()
			start_cntr += 1
			threadLock.release()
			while start_cntr < client_cnt:
				continue
			c.send("initiate")	
		else:
            		c.close()
          		break
		
def sendReqPacket(threadLock):
    global terminate_flg 
    s = socket.socket()         # Create a socket object
    s.bind((bnch_cfg.master_ip, bnch_cfg.master_port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    if client_cnt == 0:
	print "No clients idenified..."
	while wrkng_curl_th_cnt < bnch_cfg.mapper_cnt:
		continue
	time.sleep(5)
	start_cnd.acquire()
	start_cnd.notifyAll()
	start_cnd.release()
    else:
    	while True:
	    if terminate_flg == 1:
		break
	    c, addr = s.accept()     # Establish connection with client.
	    thread.start_new_thread(on_new_client,(c,addr, threadLock))
	    if start_cntr == client_cnt :	
		start_cnd.acquire()
            	start_cnd.notifyAll() 
        	start_cnd.release()

class runCurlThread (threading.Thread):
    def __init__(self, threadID,  lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
	self.lock = lock
    def run(self):
        print "Starting thread" + self.threadID
        ssh_runCurl(self.lock)
        print "Exiting thread" + self.threadID

def ssh_runCurl(threadLock):
   global token
   global terminate_flg
   global wrkng_curl_th_cnt
#   global time_hndl
   token = get_token().replace("\n","")
#   print token
   wrking_curtl_th_lck.acquire()
   wrkng_curl_th_cnt += 1
   wrking_curtl_th_lck.release()
   start_cnd.acquire()
   start_cnd.wait()	
   start_cnd.release()
   while(True):
	threadLock.acquire()
        if len(curl_tasks) > 0:
        	x = curl_tasks.pop(0)
        else:
		threadLock.release()
		terminate_flg = 1
		print "***************************", terminate_flg, "\n"
		end_time = time.strftime("%H:%M:%S")
#		time_hndl.write("Stop time: " + str(end_time))
	#	time_hndl.close()
           	break
        threadLock.release()
	start_t = time.time()
	#local_p = subprocess.Popen(["curl -i http://%s:%d/swift/v1/%s/%s/%s -X GET -H \"X-Auth-Token: %s \" -o /dev/null 2>&1 | tee %soutput-%s-%s.txt" %(bnch_cfg.L1_rgwaddr, bnch_cfg.L1_rgwport, x.bucket_name, x.dataset_name, x.obj_name, token, bnch_cfg.m_res_fldr, x.dataset_name, x.obj_name)], shell=True)

#	local_p = subprocess.Popen(["curl -w \'\ntime_namelookup=%%{time_namelookup}\ntime_appconnect=%%{time_appconnect}\ntime_connect=%%{time_connect}\ntime_redirect=%%{time_redirect}\ntime_pretransfer=%%{time_pretransfer}\ntime_starttransfer=%%{time_starttransfer}\ntime_total=%%{time_total}\n\n\' -i http://%s:%d/swift/v1/%s/%s -X GET -H \"X-Auth-Token: %s \" -o /dev/null 2>&1 | tee %soutput-%s.txt" %(bnch_cfg.L1_rgwaddr, bnch_cfg.L1_rgwport, x.bucket_name, x.obj_name, token, bnch_cfg.m_res_fldr, x.obj_name)], shell=True)
	#local_p = subprocess.Popen(["curl -w \'\ntime_total=%%{time_total}\' -i http://%s:%d/swift/v1/%s/%s -X GET -H \"X-Auth-Token: %s\" -o /dev/null 2>&1 | tee %soutput-%s-%s.txt" %(bnch_cfg.L1_rgwaddr, bnch_cfg.L1_rgwport, x.bucket_name, x.obj_name, token, bnch_cfg.m_res_fldr, x.obj_name, x.job_id)], shell=True)
	local_p = subprocess.Popen(["curl -w \'\ntime_total=%%{time_total}\n\' -i http://%s:%d/swift/v1/%s/%s -X GET -H \"X-Auth-Token: %s\" -o /dev/null 2>&1 | tee %soutput-%s-%s.txt" %(bnch_cfg.L1_rgwaddr, bnch_cfg.L1_rgwport, x.bucket_name, x.obj_name, token, bnch_cfg.m_res_fldr, x.obj_name, x.job_id)], shell=True)
	local_p.wait()
	end_t = time.time()
	dur = str(end_t - start_t)
	f_stat = open ("%s%s-%s.txt" %(bnch_cfg.m_res_fldr, x.job_id, x.obj_name), "a+") 
	f_stat.write(str(x.req_num)+"\t"+ str(start_t) + "\t" + str(end_t) + "\t" + dur +"\n") 	    

class curl_pack:
    def __init__(self, bucket_name, dataset_name, obj_name, job_id, req_num):
	self.obj_name = obj_name
	self.bucket_name = bucket_name
        self.dataset_name = dataset_name
	self.job_id  = job_id
	self.req_num = req_num

global terminate_flg
terminate_flg = 0
start_cnd = threading.Condition()
start_cntr = 0;
client_cnt = 0
curl_tasks = []
wrkng_curl_th_cnt = 0
wrking_curtl_th_lck = threading.Lock()
task_cntr = 0

print len(curl_tasks)

def drop_ceph_MOC_dram():
    print ("Clearing MOC ceph cluster buffer cache...")
    sshProcess = subprocess.Popen(["ssh -A %s@%s" %(bnch_cfg.MOC_usr, bnch_cfg.MOC_addr)],
                    shell=True, stdin=subprocess.PIPE, stdout = subprocess.PIPE,
                    universal_newlines=True, bufsize=0)
    sshProcess.stdin.write("./ceph_drop_dram.sh \n")
    sshProcess.stdin.write("echo Done \n")
    sshProcess.stdin.close()
    for line in iter(sshProcess.stdout.readline, ''):
        if line.startswith("Done") == 1:
            sshProcess.stdout.close()
            print ("CEPH DRAM cleared!")
	    break

def read_job(file_path):
    global task_cntr
    in_file = open(file_path, "r")
    in_file_content = in_file.readlines()
    for line in in_file_content:
	line_split = line.split(' ')
#	print line_split
	curl_tasks.append(curl_pack(line_split[0],"", line_split[1],line_split[2], line_split[3]))	
	#curl_tasks.append(curl_pack(line_split[0], line_split[1], line_split[2], line_split[3], int(line_split[4])))	
	task_cntr += 1
    in_file.close()	

def main(argv):
    if len(sys.argv) != 3:
	print "usage: ./bnch_master.py <job_file> <client_cnt>"
	exit(0)
    global client_cnt
    job_file = sys.argv[1] 
    client_cnt  = int(sys.argv[2])
    read_job(job_file)
    #drop_ceph_MOC_dram()
#    exit(0)

    threadLock = threading.Lock()
    th_server = serverThread("server", threadLock)
    thread_pool = [] 
    for i in range(bnch_cfg.mapper_cnt):
    	th_worker = runCurlThread(str(i), threadLock)
	thread_pool.append(th_worker)
    th_server.start()
    for i in range(bnch_cfg.mapper_cnt):
	thread_pool[i].start()

print "Exiting Main Thread"


if __name__ == "__main__":
    main(sys.argv[1:])
