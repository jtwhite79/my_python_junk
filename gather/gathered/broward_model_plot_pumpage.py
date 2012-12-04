import pandas
import pylab


df = pandas.read_csv('..\\..\\_pumpage\\dataframes\\pws_filled_zeros.csv',parse_dates=True,index_col=0)

#--group by permit numbers
permits = {}
for depname in df.keys():
    p = depname.split('_')[0]
    if p not in permits.keys():
        permits[p] = [depname]
    else:
        permits[p].append(depname)
cfd_2_gpm = 7.481 / 25.0 / 60.0
df *= cfd_2_gpm
plt_dir = 'png\\input\\'
for permit,depnames in permits.iteritems():
    fig = pylab.figure(figsize=(16,8))
    ax = pylab.subplot(111)
    ax.plot(list(df.index),df[depnames[0]].values,label=depnames[0],ls='--',lw=0.5)
    sum = df[depnames[0]].values
    for depname in depnames[1:]:
        ax.plot(list(df.index),df[depname].values,label=depname,ls='--',lw=0.5)
        sum += df[depname].values
    
    ax.plot(list(df.index),sum,'k-',lw=1.5)
    ax.grid()
    ax.legend(loc=2)
    ax.set_ylabel('gpm')
    #pylab.show()
    pylab.savefig(plt_dir+permit+'.png',dpi=300,fmt='png',bbox_inches='tight')
    pylab.close('all')
    #break






