import numpy as np
import matplotlib.pyplot as plt
import os
import NC_X
DataPath = '/data/home/zzy/CHI_PartMC/baselineF/out/'
FigurePath = DataPath

lists = []
Y_Opt_X = []
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
    Dc_Dp_mean,Dc,Dp,Dc_Dp = NC_X.coculateC_DcDp_func(DataPath, DataName)
    Y_Mix_X.append(NC_X.coculateC_X_func(DataPath,DataName))
    Y_Opt_X.append(NC_X.coculateC_Opt_X_func(DataPath,DataName))
    Y_mean_DcDp.append(Dc_Dp_mean)
    X.append(int(DataName[-6:-3]))
#绘图
#print(X)
#exit()
FigureName = 'fig1 X_optX_DcDP.jpg'
fig=plt.figure(figsize=(6,4),dpi=300)#添加画布
plt.xlabel("time(h)")
plt.ylabel("rate")
plt.ylim(0, 1)
plt.xlim(0,250)
plt.plot(X, Y_Mix_X,'b-',label='Mix_X')
plt.plot(X, Y_Opt_X,'g-',label='Opt_X')
plt.plot(X, Y_mean_DcDp,'r-.',label='Mean_Dc/Dp')
plt.legend()
plt.savefig(FigurePath + FigureName ) 
