#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Cost.dist.py
#
# Purpose :
#
# Creation Date : 31-07-2013
#
# Last Modified : Wed 31 Jul 2013 07:59:22 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

# Get the Distribution of Cost value 

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


data = open("../final.Member.Cost")
x = []
for line in data:
    value = line.split("\n")[0].split("\t")
    
    x.append(float(value[1])) 

x = np.array(x) 

mean = np.average(x)
median = np.median(x) 

n, bins, patches = plt.hist(x, 100,  facecolor='green', alpha=0.75, label = 'mean = ' + str(round(mean, 3)) + "\nmedian = " + str(round(median, 3)))

# add a 'best fit' line

plt.xlabel('Cost Value of Members')
plt.ylabel('Members Count')
plt.legend(loc='best')
#plt.axis([40, 160, 0, 0.03])
plt.grid(True)

plt.show()

