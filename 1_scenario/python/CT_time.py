#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os
import NC_X
from scipy import optimize
import csv
font_manager.fontManager.addfont('/data/home/zzy/.fonts/ARIAL.TTF')
plt.rcParams['font.sans-serif']= 'ARIAL'

#f_1
def f_1(x,A,B):
    return A * x + B
#log func
def logF(va):
    if va == 0:
        return 0
    else:
        return math.log(va)
#caculate mean_CT
def caculate_mean_CT(Dp_list,Dc_list,Conc_list):
    Sum_CT = 0
    Sum_CT_conc = 0
    for i in range(len(Dp_list)):
        if Dc_list[i]>0:
            Sum_CT += (Dp_list[i] - Dc_list[i])*Conc_list[i]
            Sum_CT_conc += Conc_list[i]
    mean_CT = Sum_CT/Sum_CT_conc
    return mean_CT
    

DataPath = '../Data/'
DataName = 'Dp_Dc_Conc.csv'
FigurePath = '../Fig/'

Dp_Dc_Conc = []
#Read
with open(DataPath+DataName, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        float_row = [float(x) for x in row]
        Dp_Dc_Conc.append(float_row)
print('validation of list_len')
print(len(Dp_Dc_Conc))
Dp = Dp_Dc_Conc[:240]
Dc = Dp_Dc_Conc[240:480]
conc = Dp_Dc_Conc[480:]
print(len(Dp))
print(len(Dc))
print(len(conc))
print()
File_number = len(Dp)



CT = []
for i in range(len(Dc)):
    mean_CT = caculate_mean_CT(Dp[i],Dc[i],conc[i])
    CT.append(mean_CT)
X = [i+1 for i in range(len(CT))]
#draw code
FigureName1 = 'CT_time'
fig, ax = plt.subplots(figsize=(7, 3),constrained_layout=False)
fig.subplots_adjust(bottom=0.2)
ax.plot(X,CT ,color='red',label = 'k-value method')
ax.set_title(r'(a)', fontsize = 12 ,loc = 'left')
ax.set_xlabel('Time of simulation(h)', fontsize=12)
ax.set_ylabel(r'$\overline{CT}$',fontsize=12)
ax.set_xlim([-5,245])
#ax.set_ylim([0,50])
#ax.set_yticks([0,10,20,30,40,50])
ax.set_xticks([24*i for i in range(11)])
#ax.set_xticklabels(['7/'+str(19+i) for i in range(11)])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
fig.savefig(FigurePath+FigureName1,dpi=1000)

exit()
