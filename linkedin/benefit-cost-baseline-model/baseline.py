#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : main.py
#
# Purpose : The main module for algorithm to calculate the absolute cost / benefits of members / companies 
#
# Creation Date : 27-06-2013
#
# Last Modified : Thu 26 Sep 2013 03:17:41 PM CDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from LoadData import LoadData
from Test import Test
import sys
import numpy as np

if __name__ == "__main__":

    fout = open("b-c.baseline.results.txt", "w")  
    # Read Data 
    user_bias, job_bias, Similarity, action, test_sim, test_action = LoadData()
    
    print len(user_bias), len(job_bias), len(Similarity), len(test_sim) 
    
    best = 0 
    params = (0,0)
    for lambda_job in range(10, 101, 5):
        for lambda_mem in range(10, 101, 5):
            print lambda_job, lambda_mem
            

            user_score = {}
            job_score = {}
            
            for u in user_bias:
                user_score[u] = float(user_bias[u][0]) / (float(user_bias[u][1]) + lambda_mem)
            for j in job_bias:
                job_score[j] = float(job_bias[j][0]) / (float(job_bias[j][1]) + lambda_job)

            AUC, AUPR, Pre_1, Pre_3, Pre_10,  NDCG_1, NDCG_3, NDCG_10 = Test(user_score, job_score, test_sim, test_action)
            print AUPR 
            if best < AUPR:
                best = AUPR
                params = (lambda_job, lambda_mem) 
                
            fout.write(str(lambda_job) + "\t" + str(lambda_mem) + "\t" + str(AUC) + "\t" + str(AUPR) + "\t" + str(Pre_1) + "\t" + str(Pre_3) + "\t" + str(Pre_10) + "\t" + str(NDCG_1) + "\t" + str(NDCG_3) + "\t" + str(NDCG_10) + "\n") 
        
    lambda_job = params[0]
    lambda_mem = params[1] 
    AUC, AUPR, Pre_1, Pre_3, Pre_10,  NDCG_1, NDCG_3, NDCG_10 = Test(user_score, job_score, test_sim, test_action)
    print lambda_job, lambda_mem
    print AUC, AUPR, Pre_1, Pre_3, Pre_10,  NDCG_1, NDCG_3, NDCG_10 
    
    fout.close() 
