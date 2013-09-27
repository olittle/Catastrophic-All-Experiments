#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Cost.generator.py
#
# Purpose :
#
# Creation Date : 31-07-2013
#
# Last Modified : Wed 31 Jul 2013 10:48:33 AM PDT
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
        
    data = open("Member.Cost")
    fout = open("final.Member.Cost", "w")
    for line in data:
        value = line.split("\n")[0].split("\t")
        m = int(value[0])
       
        fout.write(str(index_mem[m]) + "\t" + value[1] + "\n")

    fout.close() 
   
