import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
#import Image

fname = 'Figures\\newton.png'
img_org = mpimg.imread(fname)
nrow,ncol,nlay = img_org.shape
std = np.linspace(1,20,20)
for i,s in enumerate(std):
    #rand = np.random.normal(0.0,s,(nrow,ncol))
    #img = img_org.copy()
    #for k in range(nlay):
    #    img[:,:,k] += rand
    fig = plt.figure(figsize=(3,3))
    img = img_org[::s,::s,:]
    print img.shape
    ax = plt.subplot(111)
    #print rand.shape                       
    imgplt = ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])        
    plt.savefig('Figures\\std_'+str(i)+'.png.',dpi=300,format='png',bbox_inches='tight')
    plt.close('all')

