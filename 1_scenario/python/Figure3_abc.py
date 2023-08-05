import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # 添加这一行导入Line2D
import csv
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.font_manager as font_manager
font_manager.fontManager.addfont('/data/home/zzy/.fonts/ARIAL.TTF')
plt.rcParams['font.sans-serif']= 'ARIAL'

DataPath = '../Data/'
DataName = 'MAC_MACE_Rabs_MACEX_ABC_time.csv'
FigurePath = '../Fig/'
MAC_MACE_EABS=[]
Eabs_list = []
X = [i+1 for i in range(240)]
with open(DataPath+DataName, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        float_row = [float(x) for x in row]
        MAC_MACE_EABS.append(float_row)

MAC_shell = MAC_MACE_EABS[0]
MAC_core = MAC_MACE_EABS[1]
Eabs_list = MAC_MACE_EABS[2]
MAC_coreK = [5.8850 for i in range(240)]
MAC_shellK = [7.1988 for i in range(240)]
EabsK = [1.2233 for i in range(240)]

print(MAC_coreK[0])
print(max(MAC_core))
print(min(MAC_core))
print(sum(MAC_core[96:])/len(MAC_core[96:]))
print(MAC_shellK[0])
print(max(MAC_shell))
print(min(MAC_shell))
print(sum(MAC_shell[96:])/len(MAC_shell[96:]))
print(EabsK[0])
print(max(Eabs_list))
print(min(Eabs_list))
print(sum(Eabs_list[96:])/len(Eabs_list[96:]))
inpbox1 = [[],MAC_core[96:],[],MAC_shell[96:]]
inpbox2 = [[], Eabs_list[96:]]


#draw code
FigureName1 = 'Eabs_a'
fig, ax = plt.subplots(figsize=(7, 3),constrained_layout=False)
fig.subplots_adjust(bottom=0.2)
#ax.(X, Y_Mix_X, color='#1c1464',label = r'Per-particle'
ax.scatter(X, Eabs_list, s=1, color='black',label = 'per-particle method')
ax.plot(X,EabsK,color='red',label = 'k-value method')
ax.set_title(r'(a)', fontsize = 12 ,loc = 'left')
ax.set_xlabel('Time of simulation(h)', fontsize=12)
ax.set_ylabel(r'E$\mathrm{_{abs}}$', fontsize=12)
#ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
ax.set_xlim([-5,245])
ax.set_ylim([1,1.6])
ax.set_yticks([1,1.2,1.4,1.6])
#ax.set_yticklabels([1,1.5,2,2.5,3])
ax.set_xticks([24*i for i in range(11)])
#ax.set_xticklabels(['7/'+str(19+i) for i in range(11)])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(top=True, bottom=True, left=True, right=True)
plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
fig.savefig(FigurePath+FigureName1,dpi=1000)


colors = ['none','black','red','black']
FigureName2 = 'Eabs_b'
fig, ax = plt.subplots(figsize=(3.5, 3),constrained_layout=False)
fig.subplots_adjust(bottom=0.21)
bplot=ax.boxplot(inpbox1,widths=0.3,patch_artist=True,showmeans =False,meanline=False,showfliers=False,medianprops=dict(linestyle='solid',color='none'))
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
    patch.set(edgecolor = 'none')
# 添加线段
ax.hlines(y=MAC_coreK[0], xmin=0.85, xmax=1.15, color='red', linewidth=1)
ax.hlines(y=MAC_shellK[0], xmin=2.85, xmax=3.15, color='red', linewidth=1)
ax.set_title(r'(b)', fontsize = 12 ,loc = 'left')
ax.set_xticklabels(['k-$\mathrm{MAC_{core}}$','$\mathrm{MAC_{core}}$','k-$\mathrm{MAC_{shell}}$','$\mathrm{MAC_{shell}}$'], fontsize=10)
ax.set_ylabel(r'MAC($\mathrm{m^2/g}$)', fontsize=12)
#ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
#ax.set_xlim([0,240])
ax.set_ylim([0,10])
ax.set_yticks([0,2,4,6,8,10])
ax.set_yticklabels([0,2,4,6,8,10])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=45)
ax.tick_params(top=False, bottom=True, left=True, right=True)
#plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
fig.savefig(FigurePath+FigureName2,dpi=1000)


FigureName3 = 'Eabs_c'
fig, ax = plt.subplots(figsize=(2.5, 3),constrained_layout=False)
fig.subplots_adjust(bottom=0.21)
fig.subplots_adjust(left=0.2)
bplot=ax.boxplot(inpbox2,widths=0.3,patch_artist=True,showmeans =False,meanline=False,showfliers=False,medianprops=dict(linestyle='solid',color='none'))
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
    patch.set(edgecolor = 'none')
# 添加线段
ax.hlines(y=EabsK[0], xmin=0.85, xmax=1.15, color='red', linewidth=1)
ax.set_title(r'(c)', fontsize = 12 ,loc = 'left')
ax.set_xticklabels(['k-$\mathrm{E_{abs}}$','$\mathrm{E_{abs}}$'], fontsize=10)
ax.set_ylabel(r'$\mathrm{E_{abs}}$', fontsize=12)
#ax.text(520,-3,'k = '+str(abs(round(k,3))),fontsize=10,horizontalalignment='center', verticalalignment='center')
#ax.set_xlim([0,240])
ax.set_ylim([1,1.6])
ax.set_yticks([1,1.2,1.4,1.6])
#ax.set_yticklabels([1,1.5,2,2.5,3])
ax.tick_params(axis='y', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=0)
ax.tick_params(axis='x', which='major', direction='in', width=0.5, length=2, labelsize=10, pad=2, rotation=45)
ax.tick_params(top=False, bottom=True, left=True, right=True)
#plt.legend(loc='upper right',fontsize=10,frameon=False)#,bbox_to_anchor = (1,0.5))
fig.savefig(FigurePath+FigureName3,dpi=1000)


