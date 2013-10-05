#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : main.py
#
# Purpose : The main module for algorithm to calculate the absolute cost / benefits of members / companies 
#
# Creation Date : 27-06-2013
#
# Last Modified : Tue 01 Oct 2013 10:24:21 PM CDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from LoadData import LoadData
from Store import Store
from Test import Test
from time import time 
import sys

from scipy.sparse import lil_matrix, csr_matrix, csc_matrix 
from multiprocessing import Process, Value, Array

import threading 

from lr_solver_BC import lr_solver_BC
from lr_solver_MC import lr_solver_MC
import numpy as np

import os 

Member_Job_List = {}

Member_Job_Score = {} 

Cost = {}

Cost_Prior = {} 

Benefit = {}
graph = set() 

if __name__ == "__main__":

    dataset = sys.argv[1] 
    f = 1
    try:
        outLoop = int(sys.argv[2])
    except:
        outLoop = 100
    
    os.system("mkdir "+ dataset) 

    start = time()  
    Cost_array, Cost_Prior_array, Benefit_array, Member_array, TestData, TupleSet_array, Pos_array, Neg_array = LoadData(dataset)

    Tuple_len = len(TupleSet_array) 
    Pos_len = len(Pos_array) 
    Neg_len = len(Neg_array)

    memCnt = len(Member_array) 
    jobCnt = len(Benefit_array) 
    print memCnt, jobCnt 
    
    print Tuple_len, Pos_len, Neg_len
    
    gTupleCnt = Tuple_len + Pos_len + Neg_len 
    
    print "Tuple Count", gTupleCnt
    print time() - start    
    start = time() 
    trainSize = gTupleCnt
    b = np.zeros((trainSize, 1), dtype = float)
    print time() - start 
    start = time() 

    trIndex = 0 
    # Input the tuple data
    for i in range(Tuple_len):
        iTuple = TupleSet_array[i]  
        sim_1 = iTuple[4]
        sim_2 = iTuple[5]
        
        b[trIndex, 0] = sim_1 - sim_2 
        trIndex += 1 
    print sim_1, sim_2
    
    # Input the Pos data
    for i in range(Pos_len):
        iTuple = Pos_array[i]  
        sim_1 = iTuple[3]
        
        b[trIndex, 0] = sim_1 
        trIndex += 1 

    # Input the Neg data 
    for i in range(Neg_len):
        iTuple = Neg_array[i]  
        sim_2 = iTuple[3]
        
        b[trIndex, 0] = - sim_2 
        trIndex += 1 
   
    print trIndex
    
    A_BC_x = np.array([])
    A_BC_y = np.array([]) 

    for k in range(f):
        A_BC_x = np.concatenate((A_BC_x, TupleSet_array[:, 0], TupleSet_array[:, 0], Pos_array[:, 0], Neg_array[:, 0]))
        A_BC_y = np.concatenate((A_BC_y, TupleSet_array[:, 2] * f + k, TupleSet_array[:, 3] * f + k, Pos_array[:, 2] * f + k, Neg_array[:, 2] * f + k))
        
    A_BC_x = np.concatenate((A_BC_x, Pos_array[:, 0]))
    A_BC_y = np.concatenate((A_BC_y, Pos_array[:, 1] + jobCnt * f))
        
    A_BC_x = np.concatenate((A_BC_x, Neg_array[:, 0]))
    A_BC_y = np.concatenate((A_BC_y, Neg_array[:, 1] + jobCnt * f))
    
    A_MC_x = np.array([])
    A_MC_y = np.array([]) 

    for k in range(f):
        A_MC_x = np.concatenate((A_MC_x, TupleSet_array[:, 0], Pos_array[:, 0], Neg_array[:, 0]))
        A_MC_y = np.concatenate((A_MC_y, TupleSet_array[:, 1] * f + k, Pos_array[:, 1] * f + k, Neg_array[:, 1] * f + k))

    A_MC_x = np.concatenate((A_MC_x, Pos_array[:, 0]))
    A_MC_y = np.concatenate((A_MC_y, Pos_array[:, 1] + memCnt * f))
        
    A_MC_x = np.concatenate((A_MC_x, Neg_array[:, 0]))
    A_MC_y = np.concatenate((A_MC_y, Neg_array[:, 1] + memCnt * f))
    
    print time() - start
    
    TupleSet_array = np.array(TupleSet_array[:, :4], dtype = int) 
    Pos_array = np.array(Pos_array[:, :3], dtype = int) 
    Neg_array = np.array(Neg_array[:, :3], dtype = int) 
    
    #OptChecker(TupleSet_array, Pos_array, Neg_array, A_MC_x, A_MC_y, A_BC_x, A_BC_y,  Cost_array, Benefit_array, Member_array, b, Cost_Prior_array, TupleSet_score_array, Pos_score_array, Neg_score_array, f)
   
    # Training The Model 
    vUpdate = 3000

    uCnt = -1 

    # Temp Cost and Benefits for parallelism

    print "start training ..............................."
    timeout = open( dataset + "/time.record.txt", "w")
    begin_time = time()
    timeout.close() 

    Best_AUPR = 0 
    fout = open(dataset + "/AUC.result.txt", "w")
    fout.close() 

    while vUpdate > 100 and uCnt < outLoop:
        
        uCnt += 1

        p_array = {}
        
        innerUpdate = 300 

        Benefit_array, Cost_array, update1 = lr_solver_BC(TupleSet_array, Pos_array, Neg_array, Cost_array, Benefit_array, Member_array, b, A_BC_x, A_BC_y, innerUpdate)
       
        print "Update ", uCnt, update1
        
        newAUC_score, Accuracy, Pre_1, Pre_3, NDCG_1, NDCG_3 = Test(Cost_array, Benefit_array, Member_array, uCnt, dataset, "test", f, TestData)
        timeout = open(dataset + "/time.record.txt", "a")  

        timeout.write(str(time() - begin_time) + "\t" + str(newAUC_score) + "\t" + str(Accuracy) + "\t" + str(Pre_1) + "\t" + str(Pre_3) + "\t" + str(NDCG_1) + "\t" + str(NDCG_3) + "\n")

        timeout.close()

        if newAUC_score > Best_AUPR:
            Best_AUPR = newAUC_score
            
            if uCnt > 0:
                p_store.join() 
            p_store = Process(target = Store, args = (Cost_array, Benefit_array, Member_array, uCnt, dataset, f))
            p_store.start()

        fout = open(dataset + "/AUC.result.txt", "a")
        fout.write(str(uCnt) + "\t" + str(newAUC_score)  + "\t" + str(Accuracy) + "\t" + str(Pre_1) + "\t" + str(Pre_3) + "\t" + str(NDCG_1) + "\t" + str(NDCG_3) + "\n")

    print "new AUC score, AUC = ", Best_AUPR

