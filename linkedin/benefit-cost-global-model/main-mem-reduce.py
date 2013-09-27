#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : main.py
#
# Purpose : The main module for algorithm to calculate the absolute cost / benefits of members / companies 
#
# Creation Date : 27-06-2013
#
# Last Modified : Thu 26 Sep 2013 01:41:21 PM CDT
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

# Member - Job Relationship Data 
# 0 positive
# 1 view 
# 2 impressed
# 3 deleted 

Member_Job_List = {}

# Member - Job Sample Index 
# Given a sample number, return the type of data 

# 0 positive - null
# 1 positive - view 
# 2 positive - impressed
# 3 positive - deleted 
# 4 view - impressed 
# 5 view - deleted 
# 6 impressed - deleted 
# 7 null - deleted 

# Member - Job Similarity Score 
Member_Job_Score = {} 

# Member Cost Value 
Cost = {}

# Member Cost Value prior 
Cost_Prior = {} 

# Job Benefit Value 
Benefit = {}
graph = set() 

if __name__ == "__main__":

    dataset = "cs" 
    f = int(sys.argv[1]) 
    inLoop = int(sys.argv[2])
    outLoop = int(sys.argv[3]) 
    
    os.system("mkdir "+ str(f)) 

    # Read Data 
    start = time()  
    Cost_array, Cost_Prior_array, Benefit_array, Member_array, TestData, TupleSet_array, Pos_array, Neg_array = LoadData(dataset, f)

    Tuple_len = len(TupleSet_array) 
    Pos_len = len(Pos_array) 
    Neg_len = len(Neg_array)

    memCnt = len(Member_array) 
    jobCnt = len(Benefit_array) 
    print memCnt, jobCnt 
    
    print Tuple_len, Pos_len, Neg_len
    exit(1) 
    
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
    #exit(1) 
   
    # Training The Model 
    vUpdate = 3000

    uCnt = -1 

    # Temp Cost and Benefits for parallelism

    print "start training ..............................."
    timeout = open( str(f) + "/time.record", "w")
    begin_time = time()
    timeout.close() 

    Best_AUPR = 0 
    fout = open(str(f) + "/AUC.result", "w")
    fout.close() 

    while vUpdate > 100 and uCnt < outLoop:
        
        uCnt += 1

        p_array = {}
        
        innerUpdate = inLoop 

        Benefit_array, Cost_array, update1 = lr_solver_BC(TupleSet_array, Pos_array, Neg_array, Cost_array, Benefit_array, Member_array, b, A_BC_x, A_BC_y, innerUpdate)
        Member_array, Cost_array, update2 = lr_solver_MC(TupleSet_array, Pos_array, Neg_array, Cost_array, Benefit_array, Member_array, b, Cost_Prior_array, A_MC_x, A_MC_y, innerUpdate)
       
        print "Update ", uCnt, update1, update2
        
        newAUC_score = Test(Cost_array, Benefit_array, Member_array, uCnt, dataset, "test", f, TestData)
        timeout = open(str(f) + "/time.record", "a")    
        timeout.write(str(time() - begin_time) + "\t" + str(newAUC_score) + "\n")
        timeout.close()

        if newAUC_score > Best_AUPR:
            Best_AUPR = newAUC_score
            #Store(Cost_array, Benefit_array, Member_array, uCnt, dataset, f)
            if uCnt > 0:
                p_store.join() 
            p_store = Process(target = Store, args = (Cost_array, Benefit_array, Member_array, uCnt, dataset, f))
            p_store.start()

        fout = open(str(f) + "/AUC.result", "a")
        fout.write(str(uCnt) + "\t" + str(newAUC_score) + "\n") 

    print "new AUC score, AUC = ", Best_AUPR

