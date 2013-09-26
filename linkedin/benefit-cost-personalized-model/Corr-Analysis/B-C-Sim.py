#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : B-C-Sim.py
#
# Purpose : The correlation between (B - C, Sim), and (B, Sim) 
#
# Creation Date : 29-07-2013
#
# Last Modified : Mon 29 Jul 2013 04:22:35 PM PDT
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
    Cost = {} 

    f = len(open("../Job.Benefit.Matrix").readlines()[0].split("\n")[0].split()) - 1
    
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

    Cost_file = open("../Member.Cost")
    for line in Cost_file:
        value = line.split("\n")[0].split() 
        memId = int(value[0])
        cost = float(value[1])
        Cost[memId] = cost 

    data = open("../input.txt")

    Data = [] 

    for line in data:
        if line[0] != 't':
            continue 

        value = line.split("\n")[0].split("\t")
        memId = int(value[2]) 
        jobId = int(value[3]) 
        score = float(value[4]) 
        if not (memId in mem_index and jobId in job_index):
            continue 
       
        memId = mem_index[memId]
        jobId = job_index[jobId] 
        
        y1 = np.dot(Benefit[jobId], Member[memId]) 
        y2 = y1 - Cost[memId]
        Data.append([score, y1, y2]) 
    
    Data = np.array(Data) 

    data_size = len(Data) 
    Sample_Index = np.random.randint(0, data_size, 10000)
    
    SampleData = Data[Sample_Index] 
    
    cor_1, p_1 = pearsonr(Data[:, 0], Data[:, 1])
    cor_2, p_2 = pearsonr(Data[:, 0], Data[:, 2])

    plt.scatter(SampleData[:, 0], SampleData[:, 1], label = 'Benefit \nCor = ' + str(round(cor_1, 3)) + "\np-value = " + str(p_1)  , s=0.5, c='r')

    plt.legend(loc="upper left")
    plt.xlabel("(Member, Job) content similarity (logistic regression)")
    plt.ylabel("(Member, Job) Benefit Score") 
    
    plt.savefig("Benefit-Similarity.png")
   
    plt.clf()

    plt.scatter(SampleData[:, 0], SampleData[:, 2], label = 'Benefit - Cost \nCor = ' + str(round(cor_2, 3)) + "\np-value = " + str(p_2)  , s=0.5, c='r')
    plt.legend(loc="upper left")
    plt.xlabel("(Member, Job) content similarity (logistic regression)")
    plt.ylabel("(Member, Job) Benefit Score - (Member) Cost")

    plt.savefig("Benefit-Cost-Similarity.png") 


