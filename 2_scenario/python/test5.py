#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k 
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os
import NC_X
import move as mv
from scipy import optimize
import scienceplots
#f_1
def f_1(x,A,B):
    return A * x + B
#log func
def logF(va):
    if va == 0:
        return 0
    else:
        return math.log(va)

DataPath = '/data/home/zzy/CHI_PartMC/baselineR5/out/'
FigurePath = DataPath
lists = []
for file in os.listdir(DataPath):
        #print(file)
   if os.path.splitext(file)[1].lower() in '.nc':
            lists.append(file)
lists = sorted(lists,key=lambda keys:[ord(i) for i in keys],reverse=False)
listtime = [i+1 for i in range(240)]
DataName = lists[1:]

Dc = [[] for i in range(240)]
Dp = [[] for i in range(240)]
Dc_Dp = [[] for i in range(240)]
conc = [[] for i in range(240)]
y = [[] for i in range(240)] #save dp
nDc = [[] for i in range(240)]
#abstract data
for i in range(240):
    Dc_Dp_mean,Dc[i],Dp[i],Dc_Dp[i] = NC_X.coculateC_DcDp_func(DataPath, DataName[i])
    conc[i],conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName[i])


#data cut
x = [i * 10 for i in range(50)] # x,Dp from 0 to (Dp_max//50+1)*50 sep = 50    [0, 10, 20, ..., 300 ]   len = index +
for k in range(240):
    y[k] = [0 for i in range(50)]
    nDc[k] = [0 for i in range(50)]
    for i in range(len(Dp[k])):
        for j in range(50):
#            if Dp[k][i] >= (j * 10) and Dp[k][i] <= (j * 10 + 10) and 175>Dc[k][i]>45:
#            if Dp[k][i] >= (j * 10) and Dp[k][i] <= (j * 10 + 10):
            if Dp[k][i] > (j * 10) and Dp[k][i] <= (j * 10 + 10) and Dc[k][i]  > 0:
                y[k][j] += conc[k][i]
            if Dc[k][i] > (j * 10) and Dc[k][i] <= (j * 10 + 10):
                nDc[k][j] += conc[k][i]
list_nDP = []
list_nDc = []
# time add
y = list(map(list, zip(*y)))#转置，使行为Dp，原先是时间
for i in range(len(y)):
    list_nDP.append(y[i][13])
n_DP_ln = list(map(logF, list_nDP))
nDc = list(map(list, zip(*nDc)))
for i in range(len(nDc)):
    list_nDc.append(nDc[i][13])
n_Dc_ln = list(map(logF, list_nDc))
#coculate B and K
k,b=optimize.curve_fit(f_1,x[10:],n_DP_ln[10:])[0]

#data: y=kx+b
x1 = np.arange(50,490,0.01)
y1 = x1*k+b 

#point
filtered_X_Dp = [i for i, j in zip(x,n_DP_ln) if j > 0.1]
filtered_nDp = [j for j in n_DP_ln if j > 0.1]

filtered_X_Dc = [i for i, j in zip(x,n_Dc_ln) if j > 0.1]
filtered_nDc = [j for j in n_Dc_ln if j > 0.1]
#plot
FigureName = '1800hmoveln'
pparam = dict(xlabel = '$\mathrm{D_p}$ (nm)',ylabel = r"$\mathrm{ln(n(D_p))}$")
with plt.style.context(['science']):
    fig, ax = plt.subplots(figsize=(3.2, 3))
    ax.scatter(filtered_X_Dc, filtered_nDc, s=15, color = 'black',alpha =0.5,label = 'BC-core')
    ax.scatter(filtered_X_Dp, filtered_nDp, s=25, color='#219ebc', alpha=0.6,label = 'shell')
    ax.plot(x1,y1,color = 'red',linestyle = '--')
    ax.text(400,18,'k='+str(round(k,3)),fontsize=9,horizontalalignment='center', verticalalignment='center') 
    ax.set_xlim([0,500])
    ax.set_ylim([0,30])
    ax.set_yticks([0, 5, 10, 15, 20, 25,30])
    ax.set_yticklabels([0,5,10,15,20,25,30])
    ax.set_xticks([0,100,200,300,400,500])
    ax.set_xticklabels([0,100,200,300,400,500])
#    ax.autoscale(tight=True)
    ax.set(**pparam)
    plt.legend(loc='lower left',fontsize=6.5,frameon=False)#,bbox_to_anchor = (1,0.5))
    fig.savefig(FigurePath + FigureName+'.pdf')
    fig.savefig(FigurePath+FigureName,dpi=500)


