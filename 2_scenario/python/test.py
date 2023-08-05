from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import os
import NC_X
import matplotlib
import numpy as np
DataPath = '../out/'
FigurePath = '../Fig'

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
    none,conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName)
    BC_containing_conc.append(BC_conc_sum)
    BC_containing_mass.append(NC_X.coculate_particle_containBC_summass_func(DataPath,DataName))
    Dc_Dp_mean,Dc,Dp,Dc_Dp = NC_X.coculateC_DcDp_func(DataPath, DataName)
    Y_Mix_X.append(NC_X.coculateC_X_func(DataPath,DataName))
    Y_mean_DcDp.append(Dc_Dp_mean)
    X.append(int(DataName[-6:-3]))
xlimmin = 0
xlimmax = 240
ylimmin = 0
ylimmax1 = 1
ylimmax2 = max(BC_containing_conc)*1.5e10//1e10
ylimmax3 = max(BC_containing_mass)*1.5e19//1e10
BC_containing_mass = [i*1e9 for i in BC_containing_mass]
#draw code
FigureName = 'fig_1-3'
fig, axs = plt.subplots(2,2,figsize=(6.4,5.2),dpi=1000,sharex=True,constrained_layout=True)
# upper left
axs[0,0].set_title('(a)',loc='left',fontsize=12)
axs[0,0].plot(X, Y_Mix_X, 'g-', label='BC_containing_conc')
#axs[0].boxplot([Y_Mix_X[72:]],positions=[max(X)+6],sym='k+',vert=True,showmeans=True,meanline=False,widths=10,
#              meanprops=dict(linestyle='solid',marker = 'o', markersize = 0.5,markerfacecolor = 'w',markeredgecolor = 'r',markeredgewidth = 0.5),
#              showfliers = True,flierprops = {'color':'gray','marker':'.', 'markersize':0.2, 'markeredgecolor':'gray'},
#              boxprops = dict(color = 'k',linewidth = 0.5),
#              medianprops = dict(linestyle = 'solid',color = 'r',linewidth=0.25),
#              capprops = dict(linewidth=0.5),
#              whiskerprops = dict(linewidth =0.5),
#              whis = (10,90))
axs[0,0].set_xlabel('Time',fontsize=10)
axs[0,0].set_ylabel('$\mathrm{\chi}$(%)',fontsize=10)
axs[0,0].set_xlim(xlimmin,xlimmax)
axs[0,0].set_ylim(ylimmin,ylimmax1)
axs[0,0].set_xticks([i*24 for i in range(11)])
axs[0,0].set_xticklabels([0,1,2,3,4,5,6,7,8,9,10])
axs[0,0].set_yticks([0,0.5,1])
axs[0,0].set_yticklabels([0,50,100])
axs[0,0].tick_params('y')
axs[0,0].legend(loc='lower left',fontsize=10,frameon=False)

# upper right
axs[0,1].set_title('(b)',loc='left',fontsize=12)
axs[0,1].plot(X,Y_mean_DcDp, 'g-', label='Dc_Dp_mean')
axs[0,1].set_xlabel('Time',fontsize=10)
axs[0,1].set_ylabel('$\mathrm{D_c/D_p}$(%)',fontsize=10)
axs[0,1].set_xlim(xlimmin,xlimmax)
axs[0,1].set_ylim(ylimmin,ylimmax1)
axs[0,1].set_xticks([i*24 for i in range(11)])
axs[0,1].set_xticklabels([0,1,2,3,4,5,6,7,8,9,10])
axs[0,1].set_yticks([0,0.5,1])
axs[0,1].set_yticklabels([0,50,100])
axs[0,1].tick_params('y')
axs[0,1].legend(loc='lower left',fontsize=10,frameon=False)

# lower left
axs[1,0].set_title('(c)',loc='left',fontsize=12)
axs[1,0].plot(X, BC_containing_conc, 'g-', label='BC_containing_conc')
axs[1,0].set_xlabel('Time',fontsize=10)
axs[1,0].set_ylabel('Number concentration($\mathrm{m^{-3}}$)',fontsize=10)
axs[1,0].set_xlim(xlimmin,xlimmax)
axs[1,0].set_ylim(ylimmin,ylimmax2)
axs[1,0].set_xticks([i*24 for i in range(11)])
axs[1,0].set_xticklabels([0,1,2,3,4,5,6,7,8,9,10])
axs[1,0].tick_params('y')
axs[1,0].legend(loc='lower right',fontsize=10,frameon=False)

# lower right
axs[1,1].set_title('(d)',loc='left',fontsize=12)
axs[1,1].plot(X, BC_containing_mass, 'y-', label='BC_containing_mass')
axs[1,1].set_xlabel('Time',fontsize=10)
axs[1,1].set_ylabel('Mass concentration($\mathrm{\mu g m^{-3}}$)',fontsize=10)
axs[1,1].set_xlim(xlimmin,xlimmax)
axs[1,1].set_ylim(ylimmin,ylimmax3)
axs[1,1].set_xticks([i*24 for i in range(11)])
axs[1,1].set_xticklabels([0,1,2,3,4,5,6,7,8,9,10])
axs[1,1].tick_params('y')
axs[1,1].legend(loc='lower right',fontsize=10,frameon=False)

fig.savefig(FigurePath+FigureName)
exit()




#ax.text(400,18,'k='+str(round(k,3)),fontsize=9,horizontalalignment='center', verticalalignment='center')
#    ax.set_xlim([0,500])
#    ax.set_ylim([0,30])
#    ax.set_yticks([0, 5, 10, 15, 20, 25,30])
#    ax.set_yticklabels([0,5,10,15,20,25,30])
#    ax.set_xticks([0,100,200,300,400,500])
#    ax.set_xticklabels([0,100,200,300,400,500])
#    ax.set(**pparam)
#    plt.legend(loc='lower left',fontsize=6.5,frameon=False)#,bbox_to_anchor = (1,0.5))
#    fig.savefig(FigurePath + FigureName+'.pdf')
#    fig.savefig(FigurePath+'fig7-20h.jpg',dpi=500)
#
#FigureName = 'fig1 X_optX_DcDP.jpg'
#fig=plt.figure(figsize=(6,4),dpi=300)#添加画布
#plt.xlabel("time(h)")
#plt.ylabel("rate")
#plt.ylim(0, 1)
#plt.xlim(0,250)
#plt.plot(X, Y_Mix_X,'b-',label='Mix_X')
#plt.plot(X, Y_Opt_X,'g-',label='Opt_X')
#plt.plot(X, Y_mean_DcDp,'r-.',label='Mean_Dc/Dp')
#plt.legend()
#plt.savefig(FigurePath + FigureName ) 

