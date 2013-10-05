#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : History-Benefit.py
#
# Purpose : Caculate the correlation between past applied jobs 
#
# Creation Date : 30-07-2013
#
# Last Modified : Tue 30 Jul 2013 05:15:25 PM PDT
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


    f = len(open("../Job.Benefit.Matrix").readlines()[0].split("\n")[0].split()) - 1
    
    Data = []

    Benefit_file = open("../Job.Benefit.Matrix")
    for line in Benefit_file:
        value = line.split("\n")[0].split()
        jobId = int(value[0]) 
        feature = np.zeros(f) 
        for i in range(f):
            feature[i] = float(value[i + 1]) 
        Benefit[jobId] = feature

    Member_file = open("../Member.Benefit.Matrix")
    for line in Member_file:
        value = line.split("\n")[0].split()
        memId = int(value[0]) 
        feature = np.zeros(f) 
        for i in range(f):
            feature[i] = float(value[i + 1]) 
        Member[memId] = feature

    data = open("jj-score")

    for line in data:
        value = line.split("\n")[0].split("\t")
        memId = int(value[0]) 
        jobId = int(value[1]) 

        if not (memId in mem_index and jobId in job_index):
            continue 
        
        xscore = float(value[2]) 
        score = float(value[3])
       
        memId = mem_index[memId]
        jobId = job_index[jobId] 
        
        y1 = np.dot(Benefit[jobId], Member[memId])

        Data.append([xscore, score, y1]) 

    Data = np.array(Data)
    print Data.shape

    cor_1, p_1 = pearsonr(Data[:, 0], Data[:, 1])
    cor_2, p_2 = pearsonr(Data[:, 0], Data[:, 2])
    
    print cor_1, p_1
    print cor_2, p_2

    
