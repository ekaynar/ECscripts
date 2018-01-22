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
* end (directory)



USAGE:
* Edit 'vars.shinc' for your environment (SlaveIPs & jobs)
* run './end_mas.sh'  <-- run the test and record results
* run './postporcess.sh <Filename>'    <-- collect and parse results
                                           ';

