from mpl_toolkits.mplot3d import axes3d                             
import matplotlib.pyplot as plt                                     
from matplotlib import cm                                           
                                                                    
fig = plt.figure()                                                  
ax = fig.gca(projection='3d')                                       
X, Y, Z = axes3d.get_test_data(0.05)                                
ax.plot_surface(X, Y, Z,color='#888888',facecolor='none')           
cset = ax.contourf(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
cset = ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm) 
cset = ax.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)  
                                                                    
ax.set_xlabel('Hydraulic Conductivity')                                                  
ax.set_xlim(-40, 40) 
ax.set_xticklabels([])                                               
ax.set_ylabel('Reach Conductance')                                                  
ax.set_ylim(-40, 40)                                                
ax.set_yticklabels([])
ax.set_zlabel('Sum of squared residual')                                                  
ax.set_zlim(-100, 100)                                              
ax.set_zticklabels([])

plt.savefig('obj.png',format='png',dpi=600,bbox_inches='tight')                                                                    
plt.show()                                                          