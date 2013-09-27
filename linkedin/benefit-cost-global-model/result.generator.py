#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : result.generator.py
#
# Purpose :
#
# Creation Date : 31-07-2013
#
# Last Modified : Wed 31 Jul 2013 09:22:34 AM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
import numpy as np 
#import matplotlib.pyplot as plt 

# Test the data based on Cost and Benefits 
if __name__ == "__main__":

    job_index = {}
    mem_index = {}
    
    index_job = {}
    index_mem = {} 
    
    data = open("job.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        job_index[int(value[1])] = int(value[0])
        index_job[int(value[0])] = int(value[1]) 

    data = open("mem.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        mem_index[int(value[1])] = int(value[0])
        index_mem[int(value[0])] = int(value[1]) 
        
    data = open("test.result.20")
    fout = open("final.result", "w")
    for line in data:
        value = line.split("\n")[0].split("\t")
        c = int(value[0])
        m = index_mem[int(value[1])]
        j = index_job[int(value[2])]
       
        fout.write(value[0] + "\t" + str(m) + "\t" + str(j) + "\t" + value[3] + "\t" + value[4] + "\n")

    fout.close() 
   
