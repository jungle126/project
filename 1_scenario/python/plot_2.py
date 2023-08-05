import numpy as np
import matplotlib.pyplot as plt
import os
import NC_X
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
DataPath = '/data/home/zzy/CHI_PartMC/baselineF/out/'
FigurePath = DataPath

lists = []
conc_BC = []
conc = []
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
    conc.append(conc_sum)
    conc_BC.append(BC_conc_sum)
    X.append(100*eval(DataName[-6])+10*eval(DataName[-5])+eval(DataName[-4])-1)
#绘图
FigureName = 'conc_1'
fig=plt.figure(figsize=(16,9),dpi=300)#添加画布
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

twin1 = ax.twinx()

p1, = ax.plot(X,conc,"g-", label="conc")
p2, = twin1.plot(X, conc_BC, "b-", label="conc_BC")
ax.set_ylim(0, 1.2e9)
plt.xlim(0,250)
twin1.set_ylim(0, 1.2e9)

ax.set_xlabel("time(h)")
ax.set_ylabel("conc(m^-3)")
twin1.set_ylabel("conc(m^-3)")



ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())

ax.legend(handles=[p1, p2],bbox_to_anchor=(0.6,1))
plt.savefig(FigurePath + FigureName) 
