#!/usr/bin/env python

import argparse
import subprocess 
import shlex
import re
import os
import time

parser = argparse.ArgumentParser(description='Get hardware performance counter statistics for fft implementation for powers of 2 up to n threads and save to output file.')

parser.add_argument('--threads','-t', dest='NumThreads', type=int, 
                    help='up to number of threads to run (Default 128)',
                    default=128)
parser.add_argument('events', type=str,
                    help='comma seperated list of perf events to take')
parser.add_argument('--input','-i', dest='input', type=str, 
                    help='input data to run with (Default native)',
                    default='native')
parser.add_argument('--directory','-d', dest='parsecmgmt_dir', type=str,
                    help='location of parsecmgmt tool (Default ./parsec-3.0/bin/parsecmgmt)', 
                    default='./parsec-3.0/bin/parsecmgmt')

args = parser.parse_args()

events_no_duplicates = ','.join(set(args.events.split(',')))

path = 'perf stat -e {0} -x, {1} -a run -p splash2x.fft -i {2}'.format(events_no_duplicates,args.parsecmgmt_dir,args.input)
cmd_list = shlex.split(path)


## threadsToRun must be power of 2
threadsToRun = []
i = 0
while True:
    powVal = 2**i
    if powVal <= args.NumThreads:
        threadsToRun.append(powVal)
        i = i + 1
    else:
        break


if not os.path.exists('./output'):
    os.makedirs('./output')
       
timestr = time.strftime("%Y%m%d_%H%M%S")
file_name = './output/output_{0}.txt'.format(timestr)

out_file = open(file_name, "w")

regex = re.compile('real\s+(\d+)m(\d+\.\d+)s')

for x in threadsToRun:
	
    cmd_list.extend(['-n',str(x)])
  
    proc = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate() #perf stats piped to stderr, fft output piped to stdout
    out_file.write('{0},threads\n'.format(x))
    out_file.write(error)

    #search output stream for real time statistics, convert to seconds and write to file   
    m = regex.search(output)
    if m:
        out_file.write('{0},real-time-secs\n'.format(int(m.group(1))*60 + float(m.group(2))))
    
out_file.close()




