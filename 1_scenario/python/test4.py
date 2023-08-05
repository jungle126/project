#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k 
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import csv
import os
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

DataPath = '../Data/'
FigurePath = '../Fig/'
DataName = 'Dp_Dc_Conc.csv'

Dp_Dc_Conc = []
#Read
with open(DataPath+DataName, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        float_row = [float(x) for x in row]
        Dp_Dc_Conc.append(float_row)
print('validate the len of list')
print(len(Dp_Dc_Conc))
Dp = Dp_Dc_Conc[:240]
Dc = Dp_Dc_Conc[240:480]
conc = Dp_Dc_Conc[480:]
print(len(Dp))
print(len(Dc))
print(len(conc))
print()
File_number = len(Dp)

y = [[] for i in range(240)] #save dp
nDc = [[] for i in range(240)]


#data cut
x = [i * 10 for i in range(60)] # x,Dp from 0 to (Dp_max//50+1)*50 sep = 50    [0, 10, 20, ..., 300 ]   len = index +
for k in range(240):
    y[k] = [0 for i in range(60)]
    nDc[k] = [0 for i in range(60)]
    for i in range(len(Dp[k])):
        for j in range(60):
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
    list_nDP.append(sum(y[i][96:]))
n_DP_ln = list(map(logF, list_nDP))
nDc = list(map(list, zip(*nDc)))
for i in range(len(y)):
    list_nDc.append(sum(nDc[i][96:]))
n_Dc_ln = list(map(logF, list_nDc))
#coculate B and K

linefitmin = 140
filtered_X_Dp = [i for i, j in zip(x,n_DP_ln) if j > 0 and i>=linefitmin ] # do filter n>0 and Dp>=140nm
filtered_nDp = [j for i, j in zip(x,n_DP_ln) if j > 0 and i>=linefitmin]
filtered_X_Dp = [i+5 for i in filtered_X_Dp]
plot_X = [i for i, j in zip(x,n_DP_ln) if j > 0]
plot_X = [i+5 for i in plot_X]
plot_Y = [j for i, j in zip(x,n_DP_ln) if j > 0]

k,b=optimize.curve_fit(f_1,filtered_X_Dp,filtered_nDp)[0]

#data: y=kx+b
x1 = np.arange(linefitmin,600,0.01)
y1 = x1*k+b 


#point

filtered_X_Dc = [i for i, j in zip(x,n_Dc_ln) if j > 0]
filtered_nDc = [j for j in n_Dc_ln if j > 0]
filtered_X_Dc = [i+5 for i in filtered_X_Dc]
#plot
FigureName = 'aft_96hmoveln'
pparam = dict(xlabel = '$\mathrm{D_p}$ (nm)',ylabel = r"$\mathrm{ln(n(D_p))}$")
with plt.style.context(['science']):
    fig, ax = plt.subplots(figsize=(3.2, 3))
    ax.scatter(filtered_X_Dc, filtered_nDc, s=5, color = 'grey',alpha =0.8,label = 'BC-core')
    ax.scatter(plot_X, plot_Y, s=5, color='red',label = 'shell')
    ax.plot(x1,y1,color = 'black',linestyle = '-.')
    ax.text(400,18,'k='+str(round(k,3)),fontsize=9,horizontalalignment='center', verticalalignment='center') 
    ax.set_xlim([0,600])
    ax.set_ylim([0,30])
    ax.set_yticks([0, 5, 10, 15, 20, 25,30])
    ax.set_yticklabels([0,5,10,15,20,25,30])
    ax.set_xticks([0,150,300,450,600])
#    ax.set_xticklabels([0,100,200,300,400,500])
#    ax.autoscale(tight=True)
    ax.set(**pparam)
    plt.legend(loc='lower left',fontsize=6.5,frameon=False)#,bbox_to_anchor = (1,0.5))
    fig.savefig(FigurePath+FigureName,dpi=500)


