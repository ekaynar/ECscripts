# Scripts for Testing Erasure Coding Performance on CEPH

Scripts for automation of I/O workload.

FILE INVENTORY:
* vars.shinc - global variables
* runtest (directory)
  * end_mas.sh - script which is run Curl Benchmark on Given Nodes
  * postporcess.sh - script which collect the results of Curl Benchmark from slave nodes
  * parser.py - script which parse the results of curl benchmark 
  * extract.py - script which extracts latency and throughput .csv files
  * ./RTFilePlotter.py - script which generates RT graph.
* end_to_end_exp.ugur (directory)
  * curlbench_master (directory for master)
   * bnch_master.py - script which run the master benchmark
   * bnch_cfg.py - benchmark config files
   * results (directory) - which is used for storing results
  * curlbench_slave (directory for slave)



USAGE:
* Edit 'vars.shinc' for your environment (SlaveIPs & jobs)
* run './end_mas.sh'  <-- run the test and record results
* run './postporcess.sh <Filename>'    <-- collect and parse results      

* Edit 'bnch_cfg.py' for your environment
* run './bnch_master.py <job_file> <client_count>'  <-- run master benchmark
