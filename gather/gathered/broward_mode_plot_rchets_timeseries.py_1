import pylab
import pandas


df = pandas.read_csv('rchets.csv',index_col=0,parse_dates=True)
df = df.resample('12M',how='sum')
(df['rmean']-df['emean']).plot(kind='bar')
pylab.show()


