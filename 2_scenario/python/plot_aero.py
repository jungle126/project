import matplotlib.pyplot as plt
import os
import NC_X as NC
DataPath = '../out/'
FigurePath = '../Fig'
FigureName = 'species_mass.jpg'
lists = []

# process data
for file in os.listdir(DataPath):
        #print(file)
   if os.path.splitext(file)[1].lower() in '.nc':
            lists.append(file)
lists = sorted(lists,key=lambda keys:[ord(i) for i in keys],reverse=False)
lists = lists[1:]
print('0:3,5:8,18,19')
print('SO4 NO3 Cl NH4 ARO1 ARO2 ALK1 OLE1 BC H2O')
SO4 = []
NO3 = []
Cl = []
NH4 = []
ARO1 =[]
ARO2 = []
ALK1 = []
OLE1 = []
BC = []
H2O = []
X = [] #time label
for i in range(len(lists)):
    DataName = lists[i]
    SO4.append(NC.coculateC_SO4_masssum_func(DataPath,DataName))    #0
    NO3.append(NC.coculateC_NO3_masssum_func(DataPath,DataName))    #1
    Cl.append(NC.coculateC_Cl_masssum_func(DataPath,DataName))      #2
    NH4.append(NC.coculateC_NH4_masssum_func(DataPath,DataName))    #3
    ARO1.append(NC.coculateC_ARO1_masssum_func(DataPath,DataName))  #5
    ARO2.append(NC.coculateC_ARO2_masssum_func(DataPath,DataName))  #6
    ALK1.append(NC.coculateC_ALK1_masssum_func(DataPath,DataName))  #7
    OLE1.append(NC.coculateC_OLE1_masssum_func(DataPath,DataName))  #8
    BC.append(NC.coculateC_BC_masssum_func(DataPath,DataName))      #18
    H2O.append(NC.coculateC_H20_masssum_func(DataPath,DataName))    #19
    X.append(100*eval(DataName[-6])+10*eval(DataName[-5])+eval(DataName[-4])-1)

#print(SO4, NO3, Cl, NH4, ARO1, ARO2, ALK1, OLE1, BC, H2O,sep = '\n')
    
#plot part
plt.figure(figsize=(16,9),dpi=300)
#1
plt.subplot(5,2,1)
x = X
y1 = SO4
plt.plot(x,y1,color='red',linewidth=2.0,label='SO4')
plt.xlabel('time(h)')
plt.ylabel('SO4_mass(kg)') 

#2
plt.subplot(5,2,2)
x = X
y2 = NO3
plt.plot(x,y2,color='orange',linewidth=2.0,label='NO3')
plt.xlabel('time(h)')
plt.ylabel('NO3_mass(kg)')

#3
plt.subplot(5,2,3)
x = X
y3 = Cl
plt.plot(x,y3,color='yellow',linewidth=2.0,label='Cl')
plt.xlabel('time(h)')
plt.ylabel('Cl_mass(kg)')

#4
plt.subplot(5,2,4)
x = X
y4 = NH4
plt.plot(x,y4,color='greenyellow',linewidth=2.0,label='NH4')
plt.xlabel('time(h)')
plt.ylabel('NH4_mass(kg)')

#5
plt.subplot(5,2,5)
x = X
y5 = ARO1
plt.plot(x,y5,color='green',linewidth=2.0,label='ARO1')
plt.xlabel('time(h)')
plt.ylabel('ARO1_mass(kg)')

#6
plt.subplot(5,2,6)
x = X
y6 = ARO2
plt.plot(x,y6,color='aqua',linewidth=2.0,label='ARO2')
plt.xlabel('time(h)')
plt.ylabel('ARO2_mass(kg)')


#7
plt.subplot(5,2,7)
x = X
y7 = ALK1
plt.plot(x,y7,color='blue',linewidth=2.0,label='ALK1')
plt.xlabel('time(h)')
plt.ylabel('ALK1_mass(kg)')


#8
plt.subplot(5,2,8)
x = X
y8 = OLE1 
plt.plot(x,y8,color='blueviolet',linewidth=2.0,label='OLE1')
plt.xlabel('time(h)')
plt.ylabel('OLE1_mass(kg)')

#9
plt.subplot(5,2,9)
x = X
y9 = BC
plt.plot(x,y9,color='black',linewidth=2.0,label='BC')
plt.xlabel('time(h)')
plt.ylabel('BC_mass(kg)')

#10
plt.subplot(5,2,10)
x = X
y10 = H2O
plt.plot(x,y10,color='pink',linewidth=2.0,label='H2O')
plt.xlabel('time(h)')
plt.ylabel('H2O_mass(kg)')


#save

plt.savefig(FigurePath+FigureName)
