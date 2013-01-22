import numpy as np

rand = np.random.randn(1000000)

np.savetxt('rand.dat',rand)