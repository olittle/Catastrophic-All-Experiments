#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : C-Apply.py
#
# Purpose : Correlation between Cost and apply behavior  
#
# Creation Date : 29-07-2013
#
# Last Modified : Mon 29 Jul 2013 06:22:48 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import matplotlib.pyplot as plt
import numpy as np 
from scipy.stats import pearsonr 

if __name__ == "__main__":
    
    mem_index = {}

    data = open("../mem.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        mem_index[int(value[1])] = int(value[0]) 

    Cost = {} 
    Apply = {} 
    Total = {} 

    Cost_file = open("../Member.Cost")
    for line in Cost_file:
        value = line.split("\n")[0].split() 
        memId = int(value[0])
        cost = float(value[1])
        Cost[memId] = cost
        Apply[memId] = 0 
        Total[memId] = 0 
    
    valueset = set() 

    data = open("../input.txt")
    for line in data:
        if line[0] != "t":
            continue 
        value = line.split("\n")[0].split("\t")
        vClass = int(value[1]) 
        memId = int(value[2])
        if not memId in mem_index:
            continue
        memId = mem_index[memId]
        
        if vClass == 0:
            Apply[memId] += 1
        Total[memId] += 1

    

    Data = [] 

    for memId in Cost:

        Data.append([Cost[memId], Apply[memId], float(Apply[memId]) / float(Total[memId])])  

    Data = np.array(Data) 

    
    cor_1, p_1 = pearsonr(Data[:, 0], Data[:, 1])
    cor_2, p_2 = pearsonr(Data[:, 0], Data[:, 2])
    
    print cor_1, p_1
    print cor_2, p_2

    

