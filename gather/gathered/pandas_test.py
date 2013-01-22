import numpy as np
import pandas

df1 = pandas.DataFrame({'A':[1.,np.nan,3.,5.,np.nan],
                        'B':[np.nan,2.,3.,np.nan,6.]})

df2 = pandas.DataFrame({'A':[5.,2.,4.,np.nan,3.,7.],
                        'B':[np.nan,np.nan,3.,4.,6.,8.]})
                            
print df1
print df2                            
                            
df1 = df1.combine_first(df2)
print df1                            

combiner = lambda x, y:np.where(pandas.isnull(x),y,x)

df1.combine(df2,combiner)
print df1
