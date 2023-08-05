import numpy as np
import os
import NC_X
DataPath = '../out/'
FigurePath = DataPath
name_string = 'SO2,NO2,CO,O3,PM2.5,PM10'
name_list = name_string.split(',')
def avg_maxfunc(DataPath):
#gas+PM
    SO2_time = []
    NO2_time = []
    CO_time = []
    O3_time = []
    PM2_5_time = []
    PM10_time = []

    gas_back = []
    lists = []
    X = []

    for file in os.listdir(DataPath):
        #print(file)
        if os.path.splitext(file)[1].lower() in '.nc':
            lists.append(file)
    lists = sorted(lists,key=lambda keys:[ord(i) for i in keys],reverse=False)
    lists = lists[1:]
    Dc=[[] for i in range(len(lists))]
    Dp=[[] for i in range(len(lists))]
    Dc_Dp = [[] for i in range(len(lists))]
    conc = [[] for i in range(len(lists))]
    P_mass = [[] for i in range(len(lists))]
    for i in range(len(lists)):
        DataName = lists[i]
        P_mass[i] = NC_X.coculate_particle_listmass_func(DataPath,DataName)
        gas_back = NC_X.coculate_backgass_func(DataPath,DataName)
        Dc_Dp_mean,Dc[i],Dp[i],Dc_Dp[i] = NC_X.coculateC_DcDp_func(DataPath, DataName)
        conc[i],conc_sum,BC_conc_sum = NC_X.coculateC_conc_func(DataPath, DataName)
        SO2_time.append(gas_back[17])
        NO2_time.append(gas_back[5])
        CO_time.append(gas_back[16])
        O3_time.append(gas_back[10])
        pm2_5,pm10=0,0
        for j in range(len(Dp[i])):
            if Dp[i][j]<=2500:pm2_5+=P_mass[i][j]*conc[i][j]
            if Dp[i][j]<=10000:pm10+=P_mass[i][j]*conc[i][j]
        PM10_time.append(pm10)
        PM2_5_time.append(pm2_5)
        X.append(100*eval(DataName[-6])+10*eval(DataName[-5])+eval(DataName[-4])-1)

#gas_Unit:ppb-ug/m3
    SO2_time = [i*2.86 for i in SO2_time]
    NO2_time = [i*2.05 for i in NO2_time]
    CO_time = [i*1.25 for i in CO_time]
    O3_time = [i*2.14 for i in O3_time]
    PM2_5_time = [i*1e9 for i in PM2_5_time]
    PM10_time = [i*1e9 for i in PM10_time]
#get the max
    SO2_max = round(max(SO2_time),2)
    NO2_max = round(max(NO2_time),2)
    CO_max = round(max(CO_time),2)
    O3_max = round(max(O3_time),2)
#get the average
    SO2_avg = round(sum(SO2_time)/len(SO2_time),2)
    NO2_avg = round(sum(NO2_time)/len(NO2_time),2)
    CO_avg = round(sum(CO_time)/len(CO_time),2)
    O3_avg = round(sum(O3_time)/len(O3_time),2)
    PM2_5_avg = round(sum(PM2_5_time)/len(PM2_5_time),2)
    PM10_avg = round(sum(PM10_time)/len(PM10_time),2)
#list process
    gas_max = []
    gas_avg = []
    
    gas_max.append(SO2_max)
    gas_max.append(NO2_max)
    gas_max.append(CO_max)
    gas_max.append(O3_max)

    gas_avg.append(SO2_avg)
    gas_avg.append(NO2_avg)
    gas_avg.append(CO_avg)
    gas_avg.append(O3_avg)
    gas_avg.append(PM2_5_avg)
    gas_avg.append(PM10_avg)
    return gas_avg,gas_max

gas_avg,gas_mix = avg_maxfunc(DataPath)
for i in range(len(gas_avg)):
    print(name_list[i],end=':')
    print(gas_avg[i])

    




