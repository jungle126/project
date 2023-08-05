#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os
import NC_X

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


DataPath = '/data/home/zzy/CHI_PartMC/baselineR6/out/'
FigurePath = DataPath

#Read data
lists = [] #save dataname
for file in os.listdir(DataPath):
        #print(file)
   if os.path.splitext(file)[1].lower() in '.nc':
            lists.append(file)
lists = sorted(lists,key=lambda keys:[ord(i) for i in keys],reverse=False)
listtime = [i+1 for i in range(240)]
DataName = lists[1:]
File_number = len(DataName)
#
Dc = [[] for i in range(File_number)]
Dp = [[] for i in range(File_number)]
Dc_Dp = [[] for i in range(File_number)]
conc = [[] for i in range(File_number)]
BC_conc = []
#abstract data
for i in range(File_number):
    Dc_Dp_mean,Dc[i],Dp[i],Dc_Dp[i] = NC_X.coculateC_DcDp_func(DataPath, DataName[i])
    conc[i],conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName[i])
    BC_conc.append(BC_conc_sum)
bin_gap=1000
n_bin= 10
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
nDp40_120nm = [[] for i in range(File_number)] #save dp 60-80

nDp = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=0,Dc_max=10000)
nDp40_120nm = filter_fun(Dp,Dc,conc,bin_gap,n_bin,File_number,Dc_min=10,Dc_max=130)


list_nDp = []
list_nDp40_120nm = []
# time add
BC_conc_SUM2_list = []
def nDp_to_filtered_nD(nDp,timeafter=96):
    timeafter=96
    nDp = list(map(list, zip(*nDp)))#do T process keep Dp-Bin as hang
    list_nDp = []
    for i in range(len(nDp)):
        list_nDp.append(sum(nDp[i][timeafter:])) # do Sum(n(dp[time]))
    BC_conc_SUM2 = sum(list_nDp) # do Sum n[dp]
    return BC_conc_SUM2

BC_conc_SUM = nDp_to_filtered_nD(nDp,timeafter=96)
BC_conc_SUM40_120nm = nDp_to_filtered_nD(nDp40_120nm,timeafter=96)

frac = BC_conc_SUM40_120nm/BC_conc_SUM
print(round(frac*100,3),end='%')
exit()
