import os
import imageio
DataPath = '../Fig/CT_dis/'
GIFPath = '../Fig/CT_dis/'
GIFName = 'CT_distribution_evolution.gif'
lists = []
for file in os.listdir(DataPath):
        #print(file)
   if os.path.splitext(file)[1].lower() in '.png':
            lists.append(file)
lists = sorted(lists,key=lambda x: int(x[16:-5]),reverse=False)
print(lists)
gif_images = []
for i in range(len(lists)):
    gif_images.append(imageio.imread(DataPath+lists[i]))   
imageio.mimsave(GIFPath+GIFName, gif_images, duration=30)   
