#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Test.pyx
#
# Purpose :
#
# Creation Date : 28-06-2013
#
# Last Modified : Mon 30 Sep 2013 08:11:42 PM CDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
import numpy as np
from math  import * 
#import matplotlib.pyplot as plt 

# Test the data based on Cost and Benefits 
def Test(Cost_array, Benefit_array, Member_array, K, dataset, tType , f, TestData):
    
    job_index = {}
    mem_index = {}

    data = open(dataset + "/job.index.txt")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        job_index[int(value[1])] = int(value[0]) 

    data = open(dataset + "/mem.index.txt")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        mem_index[int(value[1])] = int(value[0]) 
    
    Original = {} 
    Result = {}
    
    threshold = 1
    
    os.system("mkdir " + dataset + "/tmp/")
    fout = open(dataset + "/tmp/test.result." + str(K) + ".txt", "w")

    Score = np.zeros((len(TestData), 2))
    newScore = np.zeros((len(TestData), 2))

    index = 0
    tPos = 0
    tRrd = 0
    class_threshold = 1 
    
    Per_Data = {} 

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

        if memId not in Per_Data:
            Per_Data[memId] = []
        Per_Data[memId].append([vCla, newScore[index - 1, 0]])

    fout.close() 

    for mem in Per_Data:
        Per_Data[mem] = np.array(Per_Data[mem]) 
        if len(Per_Data[mem]) > 1:
            Per_Data[mem] = Per_Data[mem][len(Per_Data[mem]) - 1 - Per_Data[mem][:, 1].argsort()]
    
    Score = np.array(Score) 
    newScore = np.array(newScore) 
    np.random.shuffle(Score)
    np.random.shuffle(newScore)
    

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

        newAUC_score += 0.5 * (lnp + new_Pre) * (new_Rcl - lnr)
        lnp = new_Pre
        lnr = new_Rcl
    
    print "Original Similarity, AUPR = ", AUC_score
    print "new AUPR score, AUPR = ", newAUC_score
    
################################### Precision @ 1 ######################################

    k = 1
    Pre_1_array = [] 
    for mem in Per_Data:
        correct = 0
        for i in range(k):
            if i >= len(Per_Data[mem]):
                break 
            if Per_Data[mem][i, 0]  < threshold:
                correct += 1
        Pre_1_array.append(float(correct) / float(k)) 
    Pre_1_array = np.array(Pre_1_array) 
    Pre_1 = np.mean(Pre_1_array) 
    del Pre_1_array
    
################################### Precision @ 3 ######################################

    k = 3
    correct = 0
    Pre_3_array = [] 
    for mem in Per_Data:
        correct = 0
        for i in range(k):
            if i >= len(Per_Data[mem]):
                break 
            if Per_Data[mem][i, 0]  < threshold:
                correct += 1
        Pre_3_array.append(float(correct) / float(k)) 
    Pre_3_array = np.array(Pre_3_array) 
    Pre_3 = np.mean(Pre_3_array) 
    del Pre_3_array

################################### NDCG @ 1 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
   
    k = 1 
    NDCG_1_array = [] 
    
    for mem in Per_Data:
        DCG = 0 
        IDCG = 0
        for i in range(k):
            if i >= len(Per_Data[mem]):
                break
            if Per_Data[mem][i][0]  < threshold:
                DCG += log(2) / log(i + 2)  
        x = (Per_Data[mem][:, 0]  < threshold).sum()
        
        if x == 0 and Per_Data[mem][0, 0] < 0:
            continue
        if x == 0 and Per_Data[mem][0, 0] >= 0:
            NDCG_1_array.append(0)
            continue
        
        if x > k:
            x = k 
        for i in range(x):
            IDCG += log(2) / log(i + 2)
        NDCG_1_array.append(DCG / IDCG) 
    
    NDCG_1_array = np.array(NDCG_1_array) 
    NDCG_1 = np.mean(NDCG_1_array) 
    del NDCG_1_array
    
################################### NDCG @ 3 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
    k = 3 
    NDCG_3_array = [] 
    
    for mem in Per_Data:
        DCG = 0 
        IDCG = 0
        for i in range(k):
            if i >= len(Per_Data[mem]):
                break
            if Per_Data[mem][i][0]  < threshold:
                DCG += log(2) / log(i + 2)  
        x = (Per_Data[mem][:, 0]  < threshold).sum()
        if x == 0 and Per_Data[mem][0, 0] < 0:
            continue
        if x == 0 and Per_Data[mem][0, 0] >= 0:
            NDCG_3_array.append(0)
            continue 

        if x > k:
            x = k 
        for i in range(x):
            IDCG += log(2) / log(i + 2)
        NDCG_3_array.append(DCG / IDCG) 
    
    NDCG_3_array = np.array(NDCG_3_array) 
    NDCG_3 = np.mean(NDCG_3_array) 
    del NDCG_3_array

################################### classification @ 3  ######################################
    
    k = 3
    correct = 0
    Accuracy_array = [] 
    for mem in Per_Data:
        correct = 0
        for i in range(len(Per_Data[mem])):
            if Per_Data[mem][i, 0]  < threshold and Per_Data[mem][i, 1] >= 0 :
                correct += 1
            elif Per_Data[mem][i, 0]  >= threshold and Per_Data[mem][i, 1] < 0 :
                correct += 1
        Accuracy_array.append(float(correct) / float(len(Per_Data[mem]))) 
    Accuracy_array = np.array(Accuracy_array) 
    Accuracy = np.mean(Accuracy_array) 
    del Accuracy_array 
    
    print  newAUC_score, Accuracy, Pre_1, Pre_3, NDCG_1, NDCG_3
    return newAUC_score, Accuracy, Pre_1, Pre_3, NDCG_1, NDCG_3
