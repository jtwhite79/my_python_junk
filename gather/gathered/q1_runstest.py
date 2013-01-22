import numpy as np
import runs

data = np.loadtxt('q1.dat')
z = runs.runstest(data)
print z