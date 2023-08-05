#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os
import NC_X
from scipy import optimize

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


DataPath = '../2_scenario/out/'
FigurePath = '../Figure/'

#Read data
lists = [] #save dataname
for file in os.listdir(DataPath):
        #print(file)
   if os.path.splitext(file)[1].lower() in '.nc':
            lists.append(file)
lists = sorted(lists,key=lambda keys:[ord(i) for i in keys],reverse=False)
listtime = [i+1 for i in range(240)]
DataName = lists[1:]
File_number = len(DataName)
#
Dc = [[] for i in range(File_number)]
Dp = [[] for i in range(File_number)]
Dc_Dp = [[] for i in range(File_number)]
conc = [[] for i in range(File_number)]
BC_conc = []
#abstract data
for i in range(File_number):
    Dc_Dp_mean,Dc[i],Dp[i],Dc_Dp[i] = NC_X.coculateC_DcDp_func(DataPath, DataName[i])
    conc[i],conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName[i])
    BC_conc.append(BC_conc_sum)
bin_gap=10
n_bin=60
#data cut
x = [i * bin_gap for i in range(n_bin)] # x,Dp from 0 to (Dp_max//50+1)*50 sep = 50    [0, 10, 20, ..., 300 ]   len = index +
def filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min,Dc_max):
    nDp = [[] for i in range(File_number)]
    for k in range(File_number):
        nDp[k] = [0 for i in range(n_bin)]
        for i in range(len(Dp[k])):
            for j in range(n_bin):
                if (j * bin_gap)< Dp[k][i]<= (j * bin_gap + bin_gap) and Dc_min < Dc[k][i] <= Dc_max:
                    nDp[k][j] += conc[k][i]
    return nDp
nDp = [[] for i in range(File_number)]

nDp = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=0,Dc_max=10000)

list_nDp = []
# time cut time = 18:00 ,13
list_nDp = nDp[13]
BC_conc_SUM2 = sum(list_nDp) # do Sum n[dp]
norm_nDp = [list_nDp[i]/BC_conc_SUM2 for i in range(len(list_nDp))] #do normalized process

print(sum(norm_nDp)) #validation
#exit()
n_DP_ln = list(map(logF, norm_nDp)) #log process

filtered_X_Dp = [i for i, j in zip(x,n_DP_ln) if j < 0] # do filter n>0 and Dp>=140nm
filtered_nDp = [j for i, j in zip(x,n_DP_ln) if j < 0]

#coculate B and K
k,b=optimize.curve_fit(f_1,filtered_X_Dp,filtered_nDp)[0]
#data: y=kx+b

x1 = np.arange(0,600,0.01)
y1 = x1*k+b
sum_upper=0
sum_lower=0
mean_filtered_nDp = sum(filtered_nDp)/len(filtered_nDp)
for i in range(len(filtered_X_Dp)):
    yi = filtered_nDp[i]
    yi_pred = filtered_X_Dp[i]*k+b
    y_mean = mean_filtered_nDp
    upper = (yi_pred-yi)**2
    lower = (yi-y_mean)**2
    sum_upper+= upper
    sum_lower+= lower
R_2 = 1-sum_upper/sum_lower
print('R2:',end='')
print(R_2)
#plot1
FigureName = 'Figure4_b'
fig, ax = plt.subplots(figsize=(5,5),constrained_layout=False)
ax.scatter(filtered_X_Dp, filtered_nDp, s=5, color='red', alpha=0.8) #,label = 'shell')
ax.plot(x1,y1,color = 'black',linestyle = '--')
ax.set_title('(b)', fontsize = 12 ,loc = 'left')
ax.set_ylabel( r'ln(n($\mathrm{D_p}$))', fontsize=12,labelpad = 0)
ax.set_xlabel(r'$\mathrm{D_p}$(nm)', fontsize=12,labelpad = 0)
ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
#ax.text(520,-4,'$\mathrm{R^2}$ = '+str(abs(round(R_2,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')

ax.set_xlim([140,600])
ax.set_ylim([-16,-0])
ax.set_yticks([-16,-12,-8,-4,0])
#ax.set_yticklabels([-10, -8,-6, -4, -2])
ax.set_xticks([150,300,450,600])
#ax.set_xticklabels([150,300,450,600])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
#ax.autoscale(tight=True)
#plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
#fig.savefig(FigurePath + FigureName+'.pdf')
fig.savefig(FigurePath+FigureName,dpi=1000)

