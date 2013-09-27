#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : draw.py
#
# Purpose :
#
# Creation Date : 01-08-2013
#
# Last Modified : Thu 01 Aug 2013 08:57:11 AM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
import numpy as np 
#import matplotlib.pyplot as plt 

# Test the data based on Cost and Benefits 
def draw(f):

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

    Cost_array = np.zeros(len(mem_index)) 
    data = open("Member.Cost")
    for line in data:
        value = line.split()
        index = int(value[0]) 
        cost = float(value[1]) 
        Cost_array[index] = cost 

    Member_array = np.zeros((len(mem_index), f) )
    data = open("Member.Benefit.Matrix") 
    for line in data:
        value = line.split("\n")[0].split("\t")
        index = int(value[0])
        vec = value[1].split() 
        for i in range(len(value)):
            Member_array[index][i] = float(vec[i])

    Benefit_array = np.zeros((len(job_index), f))
    data = open("Job.Benefit.Matrix") 
    for line in data:
        value = line.split("\n")[0].split("\t")
        index = int(value[0])
        vec = value[1].split() 
        for i in range(len(value)):
            Benefit_array[index][i] = float(vec[i])


    data = open("input.txt")
    TestData = []
    for line in data:
        if line[0] != "c":
            continue 
        value = line.split("\n")[0].split("\t") 
        try:
            vClass = int(value[1])
            memId = mem_index[int(value[2])]
            jobId = job_index[int(value[3])]
            score = float(value[4])
            TestData.append([vClass, memId, jobId, score])

        except:
            pass

    Original = {} 
    Result = {}
   
    Score = np.zeros((len(TestData), 2))
    newScore = np.zeros((len(TestData), 2))

    index = 0
    tPos = 0
    tRrd = 0
    class_threshold = 1 

    for i in range(len(TestData)):
        vCla = TestData[i][0]
        memId = TestData[i][1]
        jobId = TestData[i][2] 
        vSc = TestData[i][3]

        if vCla < class_threshold:
            tPos += 1
        try:
            newScore[index, 0] =  vSc - Cost_array[memId] + np.dot( Benefit_array[jobId], Member_array[memId])
        except:
            print Cost_array[memId]
            print Benefit_array[jobId]
            print Member_array[memId]
            exit(1) 
        Score[index, 0] = vSc
        newScore[index, 1] = vCla
        Score[index, 1] = vCla
        index += 1

    tRrd = index

    print "TestData Size", index 

    newScore = sorted(newScore, key=lambda x:x[0], reverse = True)
    Score = sorted(Score, key=lambda x:x[0], reverse = True)

    newAUC_x = []
    newAUC_y = []

    AUC_x = []
    AUC_y = []

    newAUC_score = 0
    AUC_score = 0

    Pre = 0
    new_Pre = 0
    Rcl = 0
    new_Rcl = 0
    new_cPos = 0
    cPos = 0
    new_cPos = 0
    cTotal = 0
    lp = 0  
    lr = 0 
    lnp = 0 
    lnr = 0 

   # Study the orginal score and plot
    fout = open("AUC.Matrix.Factorization", "w") 

    for i in range(tRrd):
        cTotal += 1
        if Score[i][1] < class_threshold:
            cPos += 1
        if newScore[i][1] < class_threshold:
            new_cPos += 1

        Pre = float(cPos) / float(cTotal)
        Rcl = float(cPos) / float(tPos)

        new_Pre = float(new_cPos) / float(cTotal)
        new_Rcl = float(new_cPos) / float(tPos)
        
        fout.write(str(new_Pre) + "\t" + str(new_Rcl) + "\n")
        AUC_x.append(Rcl)
        AUC_y.append(Pre)

        newAUC_x.append(new_Rcl)
        newAUC_y.append(new_Pre)

        AUC_score += 0.5 * (lp + Pre) * (Rcl - lr)
        lp = Pre
        lr = Rcl

        newAUC_score += 0.5 * (lnp + new_Pre) * (new_Rcl - lnr)
        lnp = new_Pre
        lnr = new_Rcl
    
    fout.close() 

    print "Original Similarity, AUC = ", AUC_score
    print "new AUC score, AUC = ", newAUC_score
    
    return newAUC_score

if __name__ == "__main__":
    draw(50)

