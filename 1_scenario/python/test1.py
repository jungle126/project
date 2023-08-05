from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import os
import NC_X
import matplotlib
import numpy as np
import move as mv
import matplotlib.font_manager as font_manager
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
sigma_mean_chi = []
np_Y_Mix_X = np.array(Y_Mix_X)
for i in range(len(Y_Mix_X)):
     sigma_mean_chi.append(np.std(np_Y_Mix_X)/np_Y_Mix_X.mean(axis=0))
X2 = X1[:-1]
print(sigma_mean_chi)
print(X2)
exit()

#draw code
FigureName = 'steady_state_a'
fig, ax = plt.subplots(figsize=(7, 3),constrained_layout=False)
fig.subplots_adjust(bottom=0.2)
ax.plot(X, Y_Mix_X, color='#1c1464',label = r'$\mathrm{\chi}$')
ax.plot(X1, Y_Mix_Xmove, color='#1c1464',linestyle = '--',alpha=0.6,label = r'$\mathrm{\chi_{move}}$')

ax.set_title(r'(a)', fontsize = 12 ,loc = 'left')
ax.set_xlabel('Day', fontsize=12)
ax.set_ylabel(r'Mixing state metric $\mathrm{\chi}$', fontsize=12)
#ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.set_xlim([0,240])
ax.set_ylim([0,1])
ax.set_yticks([0, 0.25,0.5,0.75,1])
ax.set_yticklabels([0,25,50,75,100])
#ax.set_yticklabels([-10, -8,-6, -4, -2])
ax.set_xticks([24*i for i in range(11)])
ax.set_xticklabels(['7/'+str(19+i) for i in range(11)])
ax2 = ax.twinx()
ax2.set_ylabel('$\mathrm{\frac{\sigma_{\chi}}{\overline{\chi}}}$', fontsize=12)
ax2.set_ylim(0, 1)
ax2.set_yticks([0, 0.25,0.5,0.75,1])
ax2.set_yticklabels([0,25,50,75,100])
ax2.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=45)
ax.tick_params(top=True, bottom=True, left=True, right=True)
plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
fig.savefig(FigurePath+FigureName,dpi=1000)
