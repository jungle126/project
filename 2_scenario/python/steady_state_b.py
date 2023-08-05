#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os
import NC_X
from scipy import optimize
import move as mv
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


DataPath = '../out/'
FigurePath = '../Fig/'

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
X = []
#abstract data
for i in range(File_number):
    Dc_Dp_mean,Dc[i],Dp[i],Dc_Dp[i] = NC_X.coculateC_DcDp_func(DataPath, DataName[i])
    conc[i],conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName[i])
    BC_conc.append(BC_conc_sum)
    X.append(int(DataName[i][-6:-3]))
X=[i-1 for i in X] #from 1 to 239

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
                if (j * bin_gap)< Dp[k][i] <= (j * bin_gap + bin_gap) and Dc_min <= Dc[k][i] < Dc_max:
                    nDp[k][j] += conc[k][i]
    return nDp
nDp = [[] for i in range(File_number)]

nDp = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=0,Dc_max=10000)

#do move average

nDp_mv = list(map(list, zip(*nDp)))
for n in range(len(nDp_mv)):
    nDp_mv[n] = mv.smoothmoveavg(nDp_mv[n],24,'valid')
nDp_mv = list(map(list, zip(*nDp_mv)))
X1 = mv.smoothmoveavg(X,24,'valid')
X1 = [i-0.5 for i in X1]

print(X)
print(X1)
#  nomal fun
def nDp_to_filtered_nD(nDp):
    norm_nDp = nDp
    for i in range(len(nDp)):
        time_i_nDp_sum = sum(nDp[i])
        for j in range(len(nDp[i])):
            nDp[i][j] = nDp[i][j]/time_i_nDp_sum 
    return nDp

# do normal
norm_nDp = nDp_to_filtered_nD(nDp)
norm_nDp_mv = nDp_to_filtered_nD(nDp_mv)
print(sum(norm_nDp[0])) #validation
print(sum(norm_nDp_mv[0]))


#do ln
n_DP_ln = [[] for i in range(len(norm_nDp))]
for i in range(len(norm_nDp)):
    n_DP_ln[i] = list(map(logF, norm_nDp[i]))

n_DP_ln_mv = [[] for i in range(len(norm_nDp_mv))]
for i in range(len(norm_nDp_mv)):
    n_DP_ln_mv[i] = list(map(logF, norm_nDp_mv[i]))



#do filter n>0 and dp>=140
filtered_X_Dp = [[] for i in range(len(n_DP_ln))]
filtered_nDp = [[] for i in range(len(n_DP_ln))]
for n in range(len(n_DP_ln)):
    filtered_X_Dp[n] = [i for i, j in zip(x,n_DP_ln[n]) if j < 0 and i>=140]
    filtered_nDp[n] = [j for i, j in zip(x,n_DP_ln[n]) if j < 0 and i>=140]

filtered_X_Dp_mv = [[] for i in range(len(n_DP_ln_mv))]
filtered_nDp_mv = [[] for i in range(len(n_DP_ln_mv))]
for n in range(len(n_DP_ln_mv)):
    filtered_X_Dp_mv[n] = [i for i, j in zip(x,n_DP_ln_mv[n]) if j < 0 and i>=140]
    filtered_nDp_mv[n] = [j for i, j in zip(x,n_DP_ln_mv[n]) if j < 0 and i>=140]


#coculate B and K
k = [[] for i in range(len(norm_nDp))]
b = [[] for i in range(len(norm_nDp))]
for i in range(len(norm_nDp)):
    k[i],b[i] = optimize.curve_fit(f_1,filtered_X_Dp[i],filtered_nDp[i])[0]

k_mv = [[] for i in range(len(norm_nDp_mv))]
b_mv = [[] for i in range(len(norm_nDp_mv))]
for i in range(len(norm_nDp_mv)):
    k_mv[i],b_mv[i] = optimize.curve_fit(f_1,filtered_X_Dp_mv[i],filtered_nDp_mv[i])[0]
print(max(k))
print(min(k))
#print(X_mark)
#exit()
#plot1
FigureName = 'steady_state_b'
fig, ax = plt.subplots(figsize=(7, 3),constrained_layout=False)
fig.subplots_adjust(bottom=0.2)
ax.plot(X, k , color='#0452d7',label = 'Before SMA')
ax.plot(X1, k_mv , color='#0452d7',linestyle='--',alpha=0.6,label = 'After SMA')
#ax.scatter(X2, [i*0.03-0.03 for i in sigma_mean_k],color = 'black',s=1, label = 'Degree of dispersion')
#ax.plot(X,[-0.0285 for i in range(len(X))],linewidth=0.5,color = 'red')
#ax.text(200,-0.0270,'Value = 5%',fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.legend(loc='upper right',fontsize=8,frameon=False)#,bbox_to_anchor = (1,0.5))
ax.set_title('(b)', fontsize = 12 ,loc = 'left')
ax.set_xlabel('Time of simulation(h)', fontsize=12)
ax.set_ylabel(r"Slope of BC size distribution", fontsize=12)
#ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.set_xlim([-5,245])
ax.set_ylim([-0.03,0])
ax.set_yticks([-0.03, -0.02,-0.01,0])
#ax.set_yticklabels([-10, -8,-6, -4, -2])
ax.set_xticks([24*i for i in range(11)])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
fig.savefig(FigurePath+FigureName,dpi=1000)


