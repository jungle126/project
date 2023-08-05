#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k 
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import os
import NC_X
import move as mv
from scipy import optimize
import scienceplots

# 设置服务器上 ARIA 字体的路径
#font_path = '/data/home/zzy/.fonts/ARIAL.TTF'
#my_font = fm.FontProperties(fname=font_path)
#mpl.rcParams['font.family'] = 'sans-serif'
#mpl.rcParams['font.sans-serif'] = [my_font.get_name()]
#mpl.rcParams['axes.unicode_minus'] = False
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
BC_conc = []
#abstract data
for i in range(240):
    Dc_Dp_mean,Dc[i],Dp[i],Dc_Dp[i] = NC_X.coculateC_DcDp_func(DataPath, DataName[i])
    conc[i],conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName[i])
    BC_conc.append(BC_conc_sum)
bin_gap=10
n_bin=60
#data cut
x = [i * bin_gap for i in range(n_bin)] # x,Dp from 0 to (Dp_max//50+1)*50 sep = 50    [0, 10, 20, ..., 300 ]   len = index +
for k in range(240):
    y[k] = [0 for i in range(n_bin)]
    nDc[k] = [0 for i in range(n_bin)]
    for i in range(len(Dp[k])):
        for j in range(n_bin):
#            if Dp[k][i] >= (j * 10) and Dp[k][i] <= (j * 10 + 10) and 175>Dc[k][i]>45:
#            if Dp[k][i] >= (j * 10) and Dp[k][i] <= (j * 10 + 10):
            if Dp[k][i] > (j * 10) and Dp[k][i] <= (j * 10 + 10) and Dc[k][i]  > 0:
                y[k][j] += conc[k][i]
            if Dc[k][i] > (j * 10) and Dc[k][i] <= (j * 10 + 10):
                nDc[k][j] += conc[k][i]
list_nDP = []
list_nDc = []
# time add
timeafter=96
BC_conc_SUM =sum(BC_conc[timeafter:])
y = list(map(list, zip(*y)))#转置，使行为Dp，原先是时间
for i in range(len(y)):
    list_nDP.append(sum(y[i][timeafter:]))
BC_conc_SUM2 = sum(list_nDP)
norm_nDp = [list_nDP[i]/BC_conc_SUM2 for i in range(len(list_nDP))]
print(sum(norm_nDp))
n_DP_ln = list(map(logF, norm_nDp))
filtered_X_Dp = [i for i, j in zip(x,n_DP_ln) if j < 0 and i>=140]
filtered_nDp = [j for i, j in zip(x,n_DP_ln) if j < 0 and i>=140]

#coculate B and K
k,b=optimize.curve_fit(f_1,filtered_X_Dp,filtered_nDp)[0]
###code
#data: y=kx+b
x1 = np.arange(140,600,0.01)
y1 = x1*k+b 
#plot
FigureName = 'aft_96hmoveln_norn'
pparam = dict(xlabel = '$\mathrm{D_p}$ (nm)',ylabel = r"$\mathrm{ln(n(D_p))}$")
#with plt.style.context(['science']):
fig, ax = plt.subplots(figsize=(3.2, 3.2),constrained_layout=True)
ax.scatter(filtered_X_Dp, filtered_nDp, s=5, color='red', alpha=0.8) #,label = 'shell')
ax.plot(x1,y1,color = 'black',linestyle = '--')
ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center') 
ax.set_xlim([140,600])
ax.set_ylim([-10,-2])
ax.set_yticks([-10, -8,-6, -4, -2])
ax.set_yticklabels([-10, -8,-6, -4, -2])
ax.set_xticks([150,300,450,600])
ax.set_xticklabels([150,300,450,600])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=5, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=5, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
#    ax.autoscale(tight=True)
ax.set(**pparam)
#plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
fig.savefig(FigurePath + FigureName+'.pdf')
fig.savefig(FigurePath+FigureName,dpi=500)


