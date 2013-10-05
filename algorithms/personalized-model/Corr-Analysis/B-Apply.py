#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : B-Apply.py
#
# Purpose : How to understand Benefit score 
#
# Creation Date : 29-07-2013
#
# Last Modified : Wed 31 Jul 2013 07:54:08 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import pearsonr 

if __name__ == "__main__":

    job_index = {}
    mem_index = {}

    data = open("../job.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        job_index[int(value[1])] = int(value[0]) 

    data = open("../mem.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        mem_index[int(value[1])] = int(value[0]) 
    
    Member = {}
    Benefit = {}

    Apply = {}
    Total = {}
    Score = {} 

    f = len(open("../Job.Benefit.Matrix").readlines()[0].split("\n")[0].split()) - 1
    
    Benefit_file = open("../Job.Benefit.Matrix")
    for line in Benefit_file:
        value = line.split("\n")[0].split()
        jobId = int(value[0]) 
        feature = np.zeros(f) 
        for i in range(f):
            feature[i] = float(value[i + 1]) 
        Benefit[jobId] = feature
        Apply[jobId] = 0 
        Total[jobId] = 0
        Score[jobId] = [] 

    Member_file = open("../Member.Benefit.Matrix")
    for line in Member_file:
        value = line.split("\n")[0].split()
        memId = int(value[0]) 
        feature = np.zeros(f) 
        for i in range(f):
            feature[i] = float(value[i + 1]) 
        Member[memId] = feature

    data = open("../input.txt")


    for line in data:
        if line[0] != 't':
            continue 

        value = line.split("\n")[0].split("\t")
        vClass = int(value[1]) 
        memId = int(value[2]) 
        jobId = int(value[3]) 
        score = float(value[4]) 
        if not (memId in mem_index and jobId in job_index and score > 0.9):
            continue 
       
        memId = mem_index[memId]
        jobId = job_index[jobId] 
        
        y1 = np.dot(Benefit[jobId], Member[memId])
        Score[jobId].append(y1) 
        if vClass == 0:
            Apply[jobId] += 1
        Total[jobId] += 1

    Data = [] 
    
    for jobId in Score:
        if Total[jobId] == 0:
            continue
        Score[jobId] = np.array(Score[jobId])
        avg = np.mean(Score[jobId]) 

        Data.append([avg, Apply[jobId], float(Apply[jobId]) / float(Total[jobId])])

    Data = np.array(Data) 

    cor_1, p_1 = pearsonr(Data[:, 0], Data[:, 1])
    cor_2, p_2 = pearsonr(Data[:, 0], Data[:, 2])
    
    print cor_1, p_1
    print cor_2, p_2

    
    plt.scatter(Data[:, 0], Data[:, 2], s=0.5, c = 'r', label = "cor = " + str(round(cor_2,3)) + "\np-value = 0") 
    plt.xlabel("Benefits") 
    plt.ylabel("probability to be applied")
    
    plt.legend(loc="lower right")
    
    plt.show() 

