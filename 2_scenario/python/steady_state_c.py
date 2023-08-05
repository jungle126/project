from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import os
import NC_X
import matplotlib
import numpy as np
import move as mv
import matplotlib.font_manager as font_manager
from scipy.optimize import curve_fit 

font_manager.fontManager.addfont('/data/home/zzy/.fonts/ARIAL.TTF')
plt.rcParams['font.sans-serif']= 'ARIAL'

DataPath = '/data/home/zzy/CHI_PartMC/baselineR6/out/'
FigurePath = DataPath

lists = [] #savd filenames
BC_containing_conc = []
BC_containing_mass = []
Y_Mix_X = []
Y_mean_DcDp = []
X = []
for file in os.listdir(DataPath):
        #print(file)
   if os.path.splitext(file)[1].lower() in '.nc':
            lists.append(file)
lists = sorted(lists,key=lambda keys:[ord(i) for i in keys],reverse=False)
lists = lists[1:]

for i in range(len(lists)):
    DataName = lists[i]
    Y_Mix_X.append(NC_X.coculateC_X_func(DataPath,DataName))
    X.append(int(DataName[-6:-3]))
X = [i-1 for i in X]
#do move average
Y_Mix_Xmove = mv.smoothmoveavg(Y_Mix_X,24,'valid')
X1 = mv.smoothmoveavg(X,24,'valid')
X1 = [i-0.5 for i in X1]

#caculate the sigma/mean to show the stable
X2 = []
sigma_mean_chi = []
np_Y_Mix_X = np.array(Y_Mix_X)
for i in range(217):
    X2.append(i+1)
    sigma_mean_chi.append(np.std(np_Y_Mix_X[i:i+24])/np_Y_Mix_X[120:].mean(axis=0))
print(len(sigma_mean_chi))
print(len(X2))
for i in range(len(sigma_mean_chi)):
    if sigma_mean_chi[i] < sum(sigma_mean_chi[120:])/len(sigma_mean_chi[120:]):
#    if sigma_mean_chi[i] < 0.03:
        X_mark = X2[i]
        break
print(X_mark)

#fitting
def function(t,Y0,YP,K):
    y = Y0*np.exp(-K*t)+YP*(1-np.exp(-K*t))
    return y
x_fit = np.linspace(0,240,2400)

Y_init_mean = sum(Y_Mix_X[120:])/len(Y_Mix_X[120:])
#Y_init =np.array([abs(i - Y_init_mean) for i in Y_Mix_Xmove])
Y_init =np.array([abs(i - Y_init_mean) for i in Y_Mix_X])
#Y_init = np.array(Y_Mix_Xmove)
#X_init =np.array(X1)
X_init = np.array(X)
#Y_init = np.array(Y_Mix_X)
print(Y_init)
print(X_init)
p_est_l,err_est_l = curve_fit(function,X_init,Y_init,method='lm')
print(p_est_l[-1])
y_fit = function(x_fit,*p_est_l)
#y_fit = [i*100 for i in y_fit]
tau = 1/p_est_l[-1]
taulist = [tau*(1+i) for i in range(5)]
taulist = np.array(taulist)
tauYlist = function(taulist,*p_est_l)
#draw code
FigureName = 'steady_state_a'
fig, ax = plt.subplots(figsize=(7, 3),constrained_layout=False)
fig.subplots_adjust(bottom=0.2)
ax.plot(X, Y_Mix_X, color='#1c1464',label = 'Before SMA')
#ax.plot(X1, Y_Mix_Xmove, color='#1c1464',linestyle = '--',alpha=0.6,label = 'After SMA')
#ax.scatter([X_mark],[Y_Mix_X[X_mark-1]],marker='*',color = 'red',s=10)
ax.scatter(taulist,tauYlist,marker='*',color = 'red',s=10)
for i in range(len(tauYlist)):
    ax.axvline(x=taulist[i], ymin=0, ymax=tauYlist[i], color='red', linestyle='--', linewidth=0.5)
    #ax.text(taulist[i],0,str(i+1)+'$\mathrm{\tau}$',fontsize=10,horizontalalignment='center', verticalalignment='center')

#ax.text(X_mark,Y_Mix_X[X_mark-1]+0.12,r'Moment of steady state',fontsize=10,horizontalalignment='center', verticalalignment='center')
#ax.text(X_mark-12,Y_Mix_X[X_mark-1]-0.08,r'$\mathrm{\frac{\sigma_{\chi}}{\overline{\chi}}}$ < 3%',fontsize=10,horizontalalignment='center', verticalalignment='center')
#ax.axvline(x=X_mark, ymin=0, ymax=Y_Mix_X[X_mark-1], color='red', linestyle='--', linewidth=0.5)
#ax.text(X_mark+10,0.05,r'8:00',fontsize=10, color='red',horizontalalignment='center', verticalalignment='center')
ax.plot(x_fit,y_fit,linestyle = '--',label = 'fitting')
ax.legend(loc='upper right',fontsize=8,frameon=False)#,bbox_to_anchor = (1,0.5))
ax.set_title(r'(a)', fontsize = 12 ,loc = 'left')
#ax.set_xlabel('Day', fontsize=12)
ax.set_xlabel('Time of simulation(h)', fontsize=12)
ax.set_ylabel(r'Mixing state metric $\mathrm{\chi}$(%)', fontsize=12)
ax.set_xlim([-5,245])
ax.set_ylim([0,1])
ax.set_yticks([0, 0.25,0.5,0.75,1])
ax.set_yticklabels([0,25,50,75,100])
ax.set_xticks([24*i for i in range(11)])
ax.set_xticklabels([24*i for i in range(11)])
#ax.set_xticklabels(['7/'+str(19+i) for i in range(11)])
#ax2 = ax.twinx()
#ax2.set_ylabel(r'$\mathrm{\frac{\sigma_{\chi}}{\overline{\chi}}}$(%)', labelpad=15,fontsize=12,rotation=0)
#ax2.set_ylim(0, 1)
#ax2.set_yticks([0, 0.25,0.5,0.75,1])
#ax2.set_yticklabels([0,25,50,75,100])
#ax2.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
fig.savefig(FigurePath+FigureName,dpi=1000)
