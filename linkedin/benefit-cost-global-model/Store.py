#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Store.pyx
#
# Purpose :
#
# Creation Date : 28-06-2013
#
# Last Modified : Sun 22 Sep 2013 12:23:50 PM CDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
def Store(Cost_array, Benefit_array, Member_array, k, dataset, f):
    
    cost_fout = open(str(f) + "/Member.Cost" , "w") 
    for memId in range(len(Cost_array)):
        cost_fout.write(str(memId) + "\t" + str(Cost_array[memId]) + "\n")
    
    bene_fout = open(str(f) + "/Job.Benefit.Matrix" , "w") 
    for jobId in range(len(Benefit_array)):
        bene_fout.write(str(jobId) + "\t")
        for j in range(f):
            bene_fout.write(str(Benefit_array[jobId][j]) + " ") 
        bene_fout.write("\n")
    
    cost_fout.close()
    
    bene_fout = open(str(f) + "/Member.Benefit.Matrix", "w") 
    for memId in range(len(Member_array)):
        bene_fout.write(str(memId) + "\t")
        for j in range(f):
            bene_fout.write(str(Member_array[memId][j]) + " ") 
        bene_fout.write("\n")

    bene_fout.close() 
