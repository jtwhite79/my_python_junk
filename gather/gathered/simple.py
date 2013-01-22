import numpy as np

dim = 100
initial = np.zeros((100))
initial[0] = 1.0
current = initial.copy()
for ts in range(0,100):
    for cell in range(1,initial.shape[0]-1):
        current[cell] = current[cell-1] + 2.0 * current[cell] + current[cell+1]/2.0 * dim
        
