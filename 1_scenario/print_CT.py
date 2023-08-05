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


DataPath = './Dp_Dc_Conc/'
DataName = 'Dp_Dc_ConcA.csv'
FigurePath = './Dp_Dc_Conc/'

Dp_Dc_Conc = []
#Read
with open(DataPath+DataName, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        float_row = [float(x) for x in row]
        Dp_Dc_Conc.append(float_row)
print(len(Dp_Dc_Conc))
Dp = Dp_Dc_Conc[:240]
Dc = Dp_Dc_Conc[240:480]
conc = Dp_Dc_Conc[480:]
print(len(Dp))
print(len(Dc))
print(len(conc))
File_number = len(Dp)


CT = []
CONC_CT=[]
conc_nDp_sum = 0
conc_nDp_sum40_120 = 0

conc = conc[96:]
Dc = Dc[96:]
Dp = Dp[96:]
sum_Dp=0
conc_Dp=0
for i in range(len(conc)):
    for j in range(len(conc[i])):
        if Dc[i][j]>0:
            sum_Dp+=conc[i][j]*Dp[i][j]
            conc_Dp+=conc[i][j]
            conc_nDp_sum += conc[i][j]
            CT.append(Dp[i][j] - Dc[i][j])
            CONC_CT.append(conc[i][j])
        if 110>= Dc[i][j] >= 70:
            conc_nDp_sum40_120+= conc[i][j]
print(sum_Dp/conc_Dp)
sum_CT=0
sum_Dp = 0
sum_Dc = 0
for i in range(len(CONC_CT)):
    sum_CT+=CONC_CT[i]*CT[i]
mean_CT = sum_CT/sum(CONC_CT)

print(mean_CT)
print(round(conc_nDp_sum40_120/conc_nDp_sum*100,2),end = '%')
conc_BC = sum(CONC_CT)
conc_sum = 0
for i in range(len(conc)):
    conc_sum+=sum(conc[i])
print(round(conc_BC/conc_sum*100,2),end = '%')
print()

#CT bin 
bin_gap = 10
n_bin = 60
nCT = [0 for i in range(n_bin)]
x = [i * bin_gap for i in range(n_bin)] 
for i in range(n_bin):
    for j in range(len(CT)):
        if i*bin_gap < CT[j] <= (i+1)*bin_gap:
            nCT[i]+=CONC_CT[j]
nCT_sum = sum(nCT)
nCT = [i/nCT_sum for i in nCT]
ln_CONC_CT = list(map(logF,nCT))
print(ln_CONC_CT)

#k and b
filtered_X_CT = [i for i, j in zip(x,ln_CONC_CT) if j < 0 and i>=20 ] # do filter n>0 and Dp>=140nm
filtered_nCT = [j for i, j in zip(x,ln_CONC_CT) if j < 0 and i>=20]

k,b=optimize.curve_fit(f_1,filtered_X_CT,filtered_nCT)[0]
x1 = np.arange(20,600,0.01)
y1 = x1*k+b

#R2
mean_filtered_nCT = sum(filtered_nCT)/len(filtered_nCT)
sum_upper = 0
sum_lower = 0
for i in range(len(filtered_X_CT)):
    yi = filtered_nCT[i]
    yi_pred = filtered_X_CT[i]*k+b
    y_mean = mean_filtered_nCT
    upper = (yi_pred-yi)**2
    lower = (yi-y_mean)**2
    sum_upper+= upper
    sum_lower+= lower
R_2 = 1-sum_upper/sum_lower
print(R_2)

#plot


FigureName1 = 'Distribution of CT'
fig, ax = plt.subplots(figsize=(3.5, 3.5),constrained_layout=False)
ax.scatter(x, ln_CONC_CT, s=5, color='#1c1464', alpha=0.8 ,label = 'CT')
ax.plot(x1,y1,color = 'red',linestyle = '--')
ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.text(520,-4,'$\mathrm{R^2}$ = '+str(abs(round(R_2,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.set_title('(b)', fontsize = 12 ,loc = 'left')
ax.set_ylabel( r"$\mathrm{ln(n(CT))}$", fontsize=12,labelpad = 0)
ax.set_xlabel(r'$\mathrm{CT}$ (nm)', fontsize=12,labelpad = 0)
ax.set_xlim([0,600])
#ax.set_ylim([-15,0])
ax.set_yticks([-12,-10, -8,-6, -4, -2,0])
ax.set_yticklabels([-12,-10, -8,-6, -4, -2,0])
ax.set_xticks([0,150,300,450,600])
ax.set_xticklabels([0,150,300,450,600])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
#ax.autoscale(tight=True)
plt.legend(loc='lower left',fontsize=8,frameon=False)#,bbox_to_anchor = (1,0.5))
#fig.savefig(FigurePath + FigureName1+'.pdf')
fig.savefig(FigurePath+FigureName1,dpi=1000)

