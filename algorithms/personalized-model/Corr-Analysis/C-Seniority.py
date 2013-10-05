#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : C-Seniority.py
#
# Purpose : The correlation between Cost and Seniority Score 
#
# Creation Date : 29-07-2013
#
# Last Modified : Mon 29 Jul 2013 05:00:43 PM PDT
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
    Seniority = {} 

    Cost_file = open("../Member.Cost")
    for line in Cost_file:
        value = line.split("\n")[0].split() 
        memId = int(value[0])
        cost = float(value[1])
        Cost[memId] = cost 
        Seniority[memId] = 0 
    
    valueset = set() 

    data = open("../input.txt")
    for line in data:
        if line[0] != "s":
            continue 
        value = line.split("\n")[0].split("\t")
        memId = int(value[1])
        if not memId in mem_index:
            continue
        memId = mem_index[memId]

        score = int(value[2])
        Seniority[memId] = score 
        valueset.add(score) 

    valueset.add(0)

    coeff = [] 

    dist = {}
    for v in valueset:
        dist[v] = [] 

    for memId in Cost:
        dist[Seniority[memId]].append(Cost[memId])
        coeff.append([Cost[memId], Seniority[memId]]) 


    Data = []
    for v in valueset:
        dist[v] = np.array(dist[v])
        Data.append([v, np.median(dist[v]), np.percentile(dist[v], 0.25), np.percentile(dist[v], 0.75)])
        
    coeff = np.array(coeff)
    
    cor, p = pearsonr(coeff[:, 0], coeff[:, 1])
    
    print cor, p
   
    Data = np.array(Data) 
    print Data.shape
    plt.errorbar(Data[:, 0], Data[:, 1], yerr=[Data[:, 2], Data[:, 3]], fmt='.-', label = "Corr = " + str(round(cor, 3)) + "\np-value = " + str(round(p, 3)))
    plt.xlim(-1, 12)
    plt.ylim(-5, 5)
    plt.legend(loc = "best")
    plt.xlabel("Senority Score")
    plt.ylabel("Cost score calculated ")
    plt.savefig("Cost-Seniority.png")


    cor, p = pearsonr(1.0 / (1.0 + np.exp(0.5 * (1 - coeff[:, 0]))) - 0.5, coeff[:, 1])
    print cor, p
