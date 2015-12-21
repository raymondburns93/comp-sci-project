#!/usr/bin/env python

from __future__ import division
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse
from collections import defaultdict
import os
import re

'''
Parse script arguments and validate.
'''

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

parser = argparse.ArgumentParser(description='Plots graphical representations of fft statistics for hardware counter events')

parser.add_argument('input_file', 
                    help='Input file containing parseable statistics',
                    metavar="FILE", type=lambda x: is_valid_file(parser, x))

args = parser.parse_args()

'''
Parse input file and add event statistics to dictionary
'''

d = defaultdict(list)

with open(args.input_file) as f:
    for line in f:	
        currentline = re.split(',+|\s+', line.rstrip("\n"))

        try:
    	    val = float(currentline[0])
        except ValueError:
            continue;
       
        d[currentline[1]].append(val)
        
base = os.path.basename(args.input_file)
out_dir = './output_plots/{0}'.format(os.path.splitext(base)[0])

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

threads = d.get("threads")
del d["threads"] #no longer required


'''
Calculate Events Per Second 
'''
tmp_dict = dict()
real_time = d.get("real-time-secs")
for key,value in d.iteritems():
    if key == "real-time-secs": 
        continue
    event_per_sec = [round(a/b) for a, b in zip(value,real_time)]
    event_name = '{0}-per-sec'.format(key)
    tmp_dict[event_name] = event_per_sec

d.update(tmp_dict)


'''
Parse raw-code-translations file so that raw event codes can be given a descriptive name if known.
Builds a dictionary of known events 
'''

codetranslations = dict()

with open('raw-code-translation.txt') as f:
    for line in f:
        currentline = line.rstrip("\n").split(",")
        codetranslations[currentline[0]] = currentline[1].strip()

'''
Create plot and save as png file to output_dir for each event statistic found in input_file.
Gives plot descriptive event name if contained within dictionary of known events.
'''

plt.figure(figsize=(10,10))
regex = re.compile('(r[0-9a-fA-F]+).*')

for key,value in d.iteritems():
  
    ylabel = plotname = key   
    
    #check whether key is a raw code and if so, attempt to retrieve a descriptive name from the translation dict
    rawcode = regex.match(key)
    if rawcode:
        translation = codetranslations.get(rawcode.group(1))
        if translation:
            ylabel = '{0} ({1})'.format(key,translation)
            plotname = '{0}-{1}'.format(key,translation) 
    
    plt.plot(threads,value)
    plt.xlabel('number of threads')
    plt.xticks(threads)
    plt.ylabel('number of {0}'.format(ylabel))
    ax = plt.gca()
    ax.yaxis.major.formatter._useMathText = True
    ax.set_xscale('log',basex=2)
    ax.set_xlim(xmin=1)
    plt.title('statistics for {0}'.format(ylabel))
    plt.grid(True)
    plt.savefig('{0}/{1}.png'.format(out_dir,plotname))
    plt.clf() #clears figure







