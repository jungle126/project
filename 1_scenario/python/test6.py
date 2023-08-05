#Dp_Dc_distribution
#show Dc distribution and Dp distribution and k 
import math
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os
import NC_X
from scipy import optimize
import scienceplots
#log10 func
def log10F(va):
    if va == 0:
        return 0
    else:
        return math.log10(va)

#set DataPath
DataPath = '/data/home/zzy/CHI_PartMC/baselineR5/out/'
#set FigsavePath
FigurePath = DataPath
DataName = 'urban_plume_0001_00000013.nc'
#set nf name
nf = nc.Dataset(DataPath + DataName,'r')
aero_conc = np.array(nf.variables['aero_num_conc'])
mass = np.array(nf.variables['aero_particle_mass'])
#mass=20*5000
conc = aero_conc.tolist()
BC_mass = mass[18] # BC mass
BC_mass = BC_mass.tolist() #np to list
POA_mass = mass[17]  #POA(OC) mass
POA_mass = POA_mass.tolist()
SOA_mass = mass[5]+mass[6]+mass[7]+mass[8]+mass[9]+mass[10]+mass[11]+mass[12] 
SOA_mass = SOA_mass.tolist()
SO4_mass = mass[0]
SO4_mass = SO4_mass.tolist()
NH4_mass = mass[3]
NH4_mass = NH4_mass.tolist()
NO3_mass = mass[1]
NO3_mass = NO3_mass.tolist()

massT = mass.T #mass = 5000*20
P_mass = [] #mass of particle
for i in range(len(massT)):
    P_mass.append(sum(massT[i]))

##filter the BC-containing particle
#new list to save BC-containing paticle
conc_BC = []
BC_BC = []
POA_BC = []
SOA_BC = []
SO4_BC = []
NH4_BC = []
NO3_BC = []
pg_BC = []
for i in range(len(BC_mass)):
    if BC_mass[i]!= 0:
        conc_BC.append(conc[i])
        BC_BC.append(BC_mass[i])
        POA_BC.append(POA_mass[i])
        SOA_BC.append(SOA_mass[i])
        SO4_BC.append(SO4_mass[i])
        NH4_BC.append(NH4_mass[i])
        NO3_BC.append(NO3_mass[i])
        pg_BC.append(BC_mass[i]*1e15)
#test sum_mass ug/m3
BC_SUM = sum([conc_BC[i]*BC_BC[i]*1e9 for i in range(len(conc_BC))])
POA_SUM = sum([conc_BC[i]*POA_BC[i]*1e9 for i in range(len(conc_BC))])
SOA_SUM = sum([conc_BC[i]*SOA_BC[i]*1e9 for i in range(len(conc_BC))])
SO4_SUM = sum([conc_BC[i]*SO4_BC[i]*1e9 for i in range(len(conc_BC))])
print(BC_SUM)
print(POA_SUM)
print(SOA_SUM)
print(SO4_SUM)



#for i in range(len(BC_mass)):
pg_log = list(map(log10F, pg_BC)) # x-pg to x-logpg
#log -5to-1 0.2bin  data cut
binlen = 12
BC = [0 for i in range(binlen)]
POA = [0 for i in range(binlen)]
SOA = [0 for i in range(binlen)]
SO4 = [0 for i in range(binlen)]
NH4 = [0 for i in range(binlen)]
NO3 = [0 for i in range(binlen)]
X_pg = [-5+4/binlen*i for i in range(binlen)]
for i in range(len(pg_log)):
    for j in range(binlen):
        pg_log_min = -5+4/binlen*j 
        pg_log_max = -5+4/binlen*(j+1)
        if pg_log_min <= pg_log[i] < pg_log_max:
            BC[j] += conc_BC[i]*BC_BC[i]*1e9   #1e9 is kg/m3 to ug/m3
            POA[j] += conc_BC[i]*POA_BC[i]*1e9
            SOA[j] += conc_BC[i]*SOA_BC[i]*1e9
            SO4[j] += conc_BC[i]*SO4_BC[i]*1e9
            NH4[j] += conc_BC[i]*NH4_BC[i]*1e9
            NO3[j] += conc_BC[i]*NO3_BC[i]*1e9

FigureName = 'plot3-1800.png'
fig = plt.figure(figsize=(6.4,4), dpi=500)
color_list = ['#281A90','#0B53DB','#1788C4','#32AA88','#95B457','#FBB232']
label_list = ['BC','POA','SOA','$SO_4$','$NH_4$','$NO_3$']
plt.stackplot(X_pg, BC, POA, SOA,SO4,NH4,NO3, colors=color_list, labels=label_list)
plt.plot(X_pg, BC, linestyle = '--',color = 'white')
#plt.plot(X_pg, [BC[i]+POA[i] for i in range(len(X_pg))], label='POA')
#plt.plot(X_pg, [BC[i]+POA[i]+SOA[i] for i in range(len(X_pg))], label='SOA')
#plt.plot(X_pg, [BC[i]+POA[i]+SOA[i]+SO4[i] for i in range(len(X_pg))], label='SO4')
#plt.plot(X_pg, [BC[i]+POA[i]+SOA[i]+SO4[i]+NH4[i] for i in range(len(X_pg))], label='NH4')
plt.plot(X_pg, [BC[i]+POA[i]+SOA[i]+SO4[i]+NH4[i]+NO3[i] for i in range(len(X_pg))], linestyle = '-',color = 'black')
# 设置图例和坐标轴标签
plt.legend()
#plt.ylim(0,1.5)
plt.xlim(-5,-1-4/binlen)
plt.xticks([-4,-3,-2],['$10^{-4}$','$10^{-3}$','$10^{-2}$'])
plt.xlabel('X_pg(log pg)')
plt.ylabel('Concentration($\mathrm{\mu g/m^3}$)')
plt.savefig(FigurePath+FigureName,dpi=500)
exit()




