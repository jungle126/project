import numpy as np 
import matplotlib.pyplot as plt
import os
import NC_X
import scienceplots
DataPath = '/data/home/zzy/CHI_PartMC/baselineF3/out/'
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
lists = lists[1:5]

for i in range(len(lists)):
    DataName = lists[i]
    none,conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName)
    BC_containing_conc.append(BC_conc_sum)
    BC_containing_mass.append(NC_X.coculate_particle_containBC_summass_func(DataPath,DataName))
    Dc_Dp_mean,Dc,Dp,Dc_Dp = NC_X.coculateC_DcDp_func(DataPath, DataName)
    Y_Mix_X.append(NC_X.coculateC_X_func(DataPath,DataName))
    Y_mean_DcDp.append(Dc_Dp_mean)
    X.append(int(DataName[-6:-3]))
#draw code
FigureName = 'fig_1.2'
#pparam = dict(xlabel = '$\mathrm{D_p}$ (nm)',ylabel = r"$\mathrm{ln(n(D_p))}$")
with plt.style.context(['science']):
    fig, axs = plt.subplots(1,2,figsize=(6.4, 2),dpi=1000,constrained_layout=True)
    axs[0].plot(X, Y_Mix_X, 'r-', label='Y_Mix_X')
    axs[0].plot(X, Y_mean_DcDp, 'b-', label='Y_mean_DcDp')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Y_Mix_X / Y_mean_DcDp')
    axs[0].tick_params('y')
    axs[0].legend(loc='upper left')

# 右边子图
#fig, ax2 = plt.subplots(1,2,2,figsize=(6.4, 2),dpi=1000)
    axs[1].plot(X, BC_containing_conc, 'g-', label='BC_containing_conc')
    axs[1].set_ylabel('BC_containing_conc')
    axs[1].tick_params('y', colors='g')
    axs[1].set_ylim(0,1e8)
    axs[1].legend(loc='upper right')

    ax3 = axs[1].twinx()
    ax3.spines["right"].set_position(("axes", 1.2))
    ax3.plot(X, BC_containing_mass, 'y-', label='BC_containing_mass')
    ax3.set_ylabel('BC_containing_mass')
    #ax3.set_ylim(0,1)
    ax3.tick_params('y', colors='y')
    ax3.legend(loc='lower right')
fig.savefig(FigurePath + FigureName+'.pdf')
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
