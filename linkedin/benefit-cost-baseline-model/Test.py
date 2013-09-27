#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Test.pyx
#
# Purpose :
#
# Creation Date : 28-06-2013
#
# Last Modified : Fri 27 Sep 2013 09:13:17 AM CDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
import numpy as np 
#import matplotlib.pyplot as plt
from math import * 

# Test the data based on Cost and Benefits 
def Test(user_score, job_score, test_sim, test_action):
    Data = []
    
    for (mem, job) in test_sim:
        score = test_sim[(mem, job)] + job_score[job] - user_score[mem] 
        Data.append([test_action[(mem, job)], score]) 

    Data = np.array(Data) 

    DataLen = len(Data) - 1
    total = len(Data) 
    Data = Data[DataLen - Data[:, 1].argsort()]
    
    P = (Data[:, 0] < 1).sum() 
    N = total - P 

    
################################### AUC #######################################
    TP = 0 
    FP = 0
    TPR = 0 
    FPR = 0
    TPR_last = 0 
    FPR_last = 0 
    AUC = 0 

    for i in range(total):
        if Data[i][0] <= 1:
            TP += 1
        else:
            FP += 1

        TPR = float(TP) / float(P)
        FPR = float(FP) / float(N) 
        AUC += 0.5 * (FPR - FPR_last) * (TPR + TPR_last) 

        TPR_last = TPR
        FPR_last = FPR

################################### AUPR #######################################

    relevant = 0 
    retrieved = 0
    Pre = 0
    Pre_last = 0 
    Rec = 0 
    Rec_last = 0 
    AUPR = 0 

    for i in range(total):
        if Data[i][0] <= 0:
            relevant += 1
        retrieved += 1 

        Pre = float(relevant) / float(retrieved)
        Rec = float(relevant) / float(P) 
        AUPR += 0.5 * (Rec - Rec_last) * (Pre + Pre_last) 

        Pre_last = Pre
        Rec_last = Rec

################################### Precision @ 1 ######################################

    k = 1
    correct = 0 
    for i in range(k):
        if i > total:
            break 
        if Data[i][0] < 1:
            correct += 1
    Pre_1 = float(correct) / float(i+1) 

################################### Precision @ 3 ######################################

    k = 3 
    correct = 0 
    for i in range(k):
        if i > total:
            break 
        if Data[i][0] < 1:
            correct += 1
    Pre_3 = float(correct) / float(i+1) 
        

################################### Precision @ 10 ######################################

    k = 10 
    correct = 0 
    for i in range(k):
        if i > total:
            break 
        if Data[i][0] < 1:
            correct += 1
    Pre_10 = float(correct) / float(i+1) 


################################### NDCG @ 1 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
   
    k = 1 
    DCG = 0 
    IDCG = 0 
    for i in range(k):
        if i > total:
            break
    
        if Data[i][0] < 1:
            DCG += log(2) / log(i + 2)  
        
    x = P
    if P > k:
        x = k 
    for i in range(x):
        IDCG += log(2) / log(i + 2) 
    
    NDCG_1 = DCG / IDCG


################################### NDCG @ 3 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
   
    k = 3 
    DCG = 0 
    IDCG = 0 
    for i in range(k):
        if i > total:
            break
    
        if Data[i][0] < 1:
            DCG += log(2) / log(i + 2)  
        
    x = P
    if P > k:
        x = k 
    for i in range(x):
        IDCG += log(2) / log(i + 2) 
    
    NDCG_3 = DCG / IDCG 


################################### NDCG @ 10 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
   
    k = 10 
    DCG = 0 
    IDCG = 0 
    for i in range(k):
        if i > total:
            break
    
        if Data[i][0] < 1:
            DCG += log(2) / log(i + 2)  
        
    x = P
    if P > k:
        x = k 
    for i in range(x):
        IDCG += log(2) / log(i + 2) 
    
    NDCG_10 = DCG / IDCG 
    
    return AUC, AUPR, Pre_1, Pre_3, Pre_10,  NDCG_1, NDCG_3, NDCG_10
