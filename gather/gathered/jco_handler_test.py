import numpy as np
import jco_handler as jhand

jco = jhand.jco('pest_raw_struct.jco')
jco.from_binary()
for par in jco.parameters:
    pvec = jco[par]
    pass

u,s,vt = np.linalg.svd(jco.x)
