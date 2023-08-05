import numpy as np
import matplotlib.pyplot as plt
import os
import NC_X as NC
import matplotlib.colors as mcolors
DataPath = '../out/'
FigurePath = '../Fig/'
a = 'SO4,NO3,Cl,NH4,MSA,ARO1,ARO2,ALK1,OLE1,APl1,APl2,LIM1,LIM2,CO3,Na,Ca,OIN,OC,BC,H2O'
aero_list = a.split(',')
#print(gas_list)
#exit()

lists = []
X = []

for file in os.listdir(DataPath):
        #print(file)
   if os.path.splitext(file)[1].lower() in '.nc':
            lists.append(file)
lists = sorted(lists,key=lambda keys:[ord(i) for i in keys],reverse=False)
lists = lists[1:]

SO4 = []
NO3 = []
Cl = []
NH4 = []
MSA = []
ARO1 = []
ARO2 = []
ALK1 = []
OLE1 = []
API1 = []
API2 = []
LIM1 = []
LIM2 = []
CO3 = []
Na = []
Ca = []
OIN = []
OC = []
BC = []
H2O = []
Aero = []

X = [] #time label
for i in range(len(lists)):
    DataName = lists[i]
    SO4.append(NC.coculateC_SO4_masssum_func(DataPath,DataName))    #0
    NO3.append(NC.coculateC_NO3_masssum_func(DataPath,DataName))    #1
    Cl.append(NC.coculateC_Cl_masssum_func(DataPath,DataName))      #2
    NH4.append(NC.coculateC_NH4_masssum_func(DataPath,DataName))    #3
    MSA.append(NC.coculateC_MSA_masssum_func(DataPath,DataName))    #4
    ARO1.append(NC.coculateC_ARO1_masssum_func(DataPath,DataName))  #5
    ARO2.append(NC.coculateC_ARO2_masssum_func(DataPath,DataName))  #6
    ALK1.append(NC.coculateC_ALK1_masssum_func(DataPath,DataName))  #7
    OLE1.append(NC.coculateC_OLE1_masssum_func(DataPath,DataName))  #8
    API1.append(NC.coculateC_API1_masssum_func(DataPath,DataName))  #9
    API2.append(NC.coculateC_API2_masssum_func(DataPath,DataName))  #10
    LIM1.append(NC.coculateC_LIM1_masssum_func(DataPath,DataName))  #11
    LIM2.append(NC.coculateC_LIM2_masssum_func(DataPath,DataName))  #12
    CO3.append(NC.coculateC_CO3_masssum_func(DataPath,DataName))    #13
    Na.append(NC.coculateC_Na_masssum_func(DataPath,DataName))      #14
    Ca.append(NC.coculateC_Ca_masssum_func(DataPath,DataName))      #15
    OIN.append(NC.coculateC_OIN_masssum_func(DataPath,DataName))    #16
    OC.append(NC.coculateC_OC_masssum_func(DataPath,DataName))      #17
    BC.append(NC.coculateC_BC_masssum_func(DataPath,DataName))      #18
    H2O.append(NC.coculateC_H20_masssum_func(DataPath,DataName))    #19
    Aero.append(NC.coculate_particle_summass_func(DataPath,DataName)) #sum
    X.append(100*eval(DataName[-6])+10*eval(DataName[-5])+eval(DataName[-4])-1)
print(len(aero_list))
component=[[] for i in range(20)]
component[0]=SO4
component[1]=NO3
component[2]=Cl
component[3]=NH4
component[4]=MSA
component[5]=ARO1
component[6]=ARO2
component[7]=ALK1
component[8]=OLE1
component[9]=API1
component[10]=API2
component[11]=LIM1
component[12]=LIM2
component[13]=CO3
component[14]=Na
component[15]=Ca
component[16]=OIN
component[17]=OC
component[18]=BC
component[19]=H2O
#plot
FigureName = 'aero mass'
plt.figure(figsize=(16,9),dpi=100,constrained_layout=False)
for i in range(len(component)):
    plt.subplot(5,4,i+1)
    plt.plot(X,[k*1e9 for k in component[i]],color='black',linewidth=1.0,label=aero_list[i])
    plt.xlabel('time(h)')
    plt.ylabel('ug/m^3')
    plt.legend()
plt.savefig(FigurePath+FigureName)

