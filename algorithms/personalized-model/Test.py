#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Test.pyx
#
# Purpose :
#
# Creation Date : 28-06-2013
#
# Last Modified : Fri 27 Sep 2013 09:56:54 AM CDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
import numpy as np 
#import matplotlib.pyplot as plt 

# Test the data based on Cost and Benefits 
def Test(Cost_array, Benefit_array, Member_array, K, dataset, tType , f, TestData):
    
    job_index = {}
    mem_index = {}

    data = open(str(f) + "/job.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        job_index[int(value[1])] = int(value[0]) 

    data = open(str(f) + "/mem.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        mem_index[int(value[1])] = int(value[0]) 
    
    Original = {} 
    Result = {}
   
    fout = open(str(f) + "/test.result." + str(K), "w")

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
#            newScore[index, 0] = beta[0] * vSc - 100 * Cost[memId] + 100 * Benefit[jobId]
        Score[index, 0] = vSc
        newScore[index, 1] = vCla
        Score[index, 1] = vCla
        index += 1
        fout.write(str(vCla) + "\t" + str(memId) + "\t" + str(jobId) + "\t" + str(vSc) + "\t" + str(newScore[index - 1, 0]) + "\n") 
    fout.close() 

    tRrd = index

    print "TestData Size", index 

# Rank Score
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
     
    N_F1 = 0 
    O_F1 = 0 
    TP = 0 
    
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

        AUC_x.append(Rcl)
        AUC_y.append(Pre)

        newAUC_x.append(new_Rcl)
        newAUC_y.append(new_Pre)

        AUC_score += 0.5 * (lp + Pre) * (Rcl - lr)
        lp = Pre
        lr = Rcl
        
        old_f1 = 2 * lp * lr / ( lp + lr) 
        if old_f1 > O_F1:
            O_F1 = old_f1 

        newAUC_score += 0.5 * (lnp + new_Pre) * (new_Rcl - lnr)
        lnp = new_Pre
        lnr = new_Rcl
        
        new_f1 = (2 * new_Pre * new_Rcl) / (new_Pre + new_Rcl)
        if new_f1 > N_F1:
            N_F1 = new_f1
    
    print "Original Similarity, AUC = ", AUC_score, O_F1
    print "new AUC score, AUC = ", newAUC_score, N_F1
    
    testfile = open(str(f) + "/test." + dataset + "." + str(f), "a") 
    testfile.write(str(AUC_score) + "\t" + str(newAUC_score) + "\t" + str(O_F1) + "\t" + str(N_F1) + "\n")
    testfile.close() 
    
    return newAUC_score



