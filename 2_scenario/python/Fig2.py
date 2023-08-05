#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import csv
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
nDp40_60nm = [[] for i in range(File_number)] #save dp 60-80
nDp60_80nm = [[] for i in range(File_number)] #save dp 80-100
nDp80_100nm = [[] for i in range(File_number)] #save dp 100-120
nDp100_120nm = [[] for i in range(File_number)] #save dp 120-140

nDp = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=0,Dc_max=10000)
nDp40_60nm = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=40,Dc_max=60)
nDp60_80nm = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=60,Dc_max=80)
nDp80_100nm = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=80,Dc_max=100)
nDp100_120nm = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=100,Dc_max=120)


list_nDp = []
list_nDp40_60nm = []
list_nDp60_80nm = []
list_nDpnDp80_100nm = []
list_nDpnDp100_120nm = []
# time add
def nDp_to_filtered_nD(nDp,timeafter=96):
    timeafter=96
    nDp = list(map(list, zip(*nDp)))#do T process keep Dp-Bin as hang
    list_nDp = []
    for i in range(len(nDp)):
        list_nDp.append(sum(nDp[i][timeafter:])) # do Sum(n(dp[time]))
    BC_conc_SUM2 = sum(list_nDp) # do Sum n[dp]
    norm_nDp = [list_nDp[i]/BC_conc_SUM2 for i in range(len(list_nDp))] #do normalized process
    return norm_nDp
mean_CT_bin = 0
norm_nDp = nDp_to_filtered_nD(nDp,timeafter=96)
#for i in range(len(norm_nDp)):
#    mean_CT_bin+=norm_nDp[i]*x[i]
#print(mean_CT_bin)
norm_nDp40_60nm = nDp_to_filtered_nD(nDp40_60nm,timeafter=96)
norm_nDp60_80nm = nDp_to_filtered_nD(nDp60_80nm,timeafter=96)
norm_nDp80_100nm = nDp_to_filtered_nD(nDp80_100nm,timeafter=96)
norm_nDp100_120nm = nDp_to_filtered_nD(nDp100_120nm,timeafter=96)

print('validation of norm_sum=1?')
print(sum(norm_nDp)) #validation
print()

n_DP_ln = list(map(logF, norm_nDp)) #log process
n_DP_ln40_60nm = list(map(logF, norm_nDp40_60nm))
n_DP_ln60_80nm = list(map(logF, norm_nDp60_80nm))
n_DP_ln80_100nm = list(map(logF, norm_nDp80_100nm))
n_DP_ln100_120nm = list(map(logF, norm_nDp100_120nm))


filtered_X_Dp40_60nm = [i for i, j in zip(x,n_DP_ln40_60nm) if j < 0 and i>=10] # do filter n>0 and Dp>=140nm
filtered_nDp40_60nm = [j for i, j in zip(x,n_DP_ln40_60nm) if j < 0 and i>=10]

filtered_X_Dp60_80nm = [i for i, j in zip(x,n_DP_ln60_80nm) if j < 0 and i>=40] # do filter n>0 and Dp>=140nm
filtered_nDp60_80nm = [j for i, j in zip(x,n_DP_ln60_80nm) if j < 0 and i>=40]

filtered_X_Dp80_100nm = [i for i, j in zip(x,n_DP_ln80_100nm) if j < 0 and i>=70] # do filter n>0 and Dp>=140nm
filtered_nDp80_100nm = [j for i, j in zip(x,n_DP_ln80_100nm) if j < 0 and i>=70]

filtered_X_Dp100_120nm = [i for i, j in zip(x,n_DP_ln100_120nm) if j < 0 and i>=100] # do filter n>0 and Dp>=140nm
filtered_nDp100_120nm = [j for i, j in zip(x,n_DP_ln100_120nm) if j < 0 and i>=100]

linefitmin = 140
filtered_X_Dp = [i for i, j in zip(x,n_DP_ln) if j < 0 and i>=linefitmin ] # do filter n>0 and Dp>=140nm
filtered_nDp = [j for i, j in zip(x,n_DP_ln) if j < 0 and i>=linefitmin]

filtered_X_Dp=[i+5 for i in filtered_X_Dp]



#filtered_X_Dp = [i for i, j in zip(x,n_DP_ln) if j < 0 and i>=140] # do filter n>0 and Dp>=140nm
#filtered_nDp = [j for i, j in zip(x,n_DP_ln) if j < 0 and i>=140]

#coculate B and K
k,b=optimize.curve_fit(f_1,filtered_X_Dp,filtered_nDp)[0]
k40_60nm,b40_60nm=optimize.curve_fit(f_1,filtered_X_Dp40_60nm,filtered_nDp40_60nm)[0]
k60_80nm,b60_80nm=optimize.curve_fit(f_1,filtered_X_Dp60_80nm,filtered_nDp60_80nm)[0]
k80_100nm,b80_100nm=optimize.curve_fit(f_1,filtered_X_Dp80_100nm,filtered_nDp80_100nm)[0]
k100_120nm,b100_120nm=optimize.curve_fit(f_1,filtered_X_Dp100_120nm,filtered_nDp100_120nm)[0]
#data: y=kx+b
K_list = [k40_60nm,k60_80nm,k80_100nm,k100_120nm]

print('sep_bin k')
print(K_list)
print(max(K_list))
print(min(K_list))
print()
x1 = np.arange(140,600,0.01)

y1 = x1*k+b
print('1/k:',end='')
print(1/k)
print()
x40_60nm = np.arange(min(filtered_X_Dp40_60nm),max(filtered_X_Dp40_60nm),0.01)
x60_80nm = np.arange(min(filtered_X_Dp60_80nm),max(filtered_X_Dp60_80nm),0.01)
x80_100nm = np.arange(min(filtered_X_Dp80_100nm),max(filtered_X_Dp80_100nm),0.01)
x100_120nm = np.arange(min(filtered_X_Dp100_120nm),max(filtered_X_Dp100_120nm),0.01)

y40_60nm = x40_60nm*k40_60nm+b40_60nm
y60_80nm = x60_80nm*k60_80nm+b60_80nm
y80_100nm = x80_100nm*k80_100nm+b80_100nm
y100_120nm = x100_120nm*k100_120nm+b100_120nm

mean_filtered_nDp = sum(filtered_nDp)/len(filtered_nDp)
sum_upper = 0
sum_lower = 0
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
print()
#plot1
FigureName = 'size_distribution_a'
fig, ax = plt.subplots(figsize=(3.5, 3.5),constrained_layout=False)
ax.scatter(filtered_X_Dp, filtered_nDp, s=5, color='red', alpha=0.8) #,label = 'shell')
ax.plot(x1,y1,color = 'black',linestyle = '-.')
ax.axvline(x=linefitmin, color='grey', linestyle='--', linewidth=1)
ax.set_title('(a)', fontsize = 12 ,loc = 'left')
ax.set_ylabel( r'$\mathrm{ln(n(D_p))}$', fontsize=12,labelpad = 0)
ax.set_xlabel(r'$\mathrm{D_p}$ (nm)', fontsize=12,labelpad = 0)
ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.text(500,-4,'$\mathrm{R^2}$ = '+str(abs(round(R_2,4))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.set_xlim([140,600])
ax.set_ylim([-10,-2])
ax.set_yticks([-10, -8,-6, -4, -2])
ax.set_yticklabels([-10, -8,-6, -4, -2])
ax.set_xticks([150,300,450,600])
ax.set_xticklabels([150,300,450,600])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
#ax.autoscale(tight=True)
#plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
#fig.savefig(FigurePath + FigureName+'.pdf')
fig.savefig(FigurePath+FigureName,dpi=1000)

#plot
FigureName1 = 'size_distribution_b'
pparam = dict(xlabel = '$\mathrm{D_p}$ (nm)',ylabel = r"$\mathrm{ln(n(D_p))}$")
fig, ax = plt.subplots(figsize=(3.5, 3.5),constrained_layout=False)
ax.scatter(filtered_X_Dp40_60nm, filtered_nDp40_60nm, s=5, color='#12cbc5', alpha=0.8 ,label = '$\mathrm{D_c}$ = 10-40 nm')
ax.scatter(filtered_X_Dp60_80nm, filtered_nDp60_80nm, s=5, color='#1593c3', alpha=0.8 ,label = '$\mathrm{D_c}$ = 40-70 nm')
ax.scatter(filtered_X_Dp80_100nm, filtered_nDp80_100nm, s=5, color='#0452d7', alpha=0.8 ,label = '$\mathrm{D_c}$ = 70-100 nm')
ax.scatter(filtered_X_Dp100_120nm, filtered_nDp100_120nm, s=5, color='#1c1464', alpha=0.8 ,label = '$\mathrm{D_c}$ = 100-130 nm')

ax.plot(x40_60nm,y40_60nm,color = '#12cbc5',linestyle = '--')
ax.plot(x60_80nm,y60_80nm,color = '#1593c3',linestyle = '--')
ax.plot(x80_100nm,y80_100nm,color = '#0452d7',linestyle = '--')
ax.plot(x100_120nm,y100_120nm,color = '#1c1464',linestyle = '--')
#ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.set_title('(b)', fontsize = 12 ,loc = 'left')
ax.set_ylabel( r"$\mathrm{ln(n(D_p))}$", fontsize=12,labelpad = 0)
ax.set_xlabel(r'$\mathrm{D_p}$ (nm)', fontsize=12,labelpad = 0)
ax.set_xlim([0,600])
ax.set_ylim([-12,0])
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

