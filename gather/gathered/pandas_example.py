from datetime import datetime
import numpy as np
import pandas
import matplotlib.pyplot as plt
import pestUtil



#--create some fake series
start_date = datetime(year=1996,month=1,day=1)
end_date = datetime(year=1996,month=3,day=30)
#--a date range with a 3-day interval
d_range = pandas.DateRange(start_date,end_date,offset=pandas.DateOffset(5))
#--give the series a values of 1
s1 = pandas.Series(1,index=d_range)

start_date = datetime(year=1996,month=1,day=4)
end_date = datetime(year=1996,month=3,day=30)
#--a date range with a 5-day interval
d_range = pandas.DateRange(start_date,end_date,offset=pandas.DateOffset(7))
#--give the series a values of 2
s2 = pandas.Series(2,index=d_range)



#--create a pandas date range using daily dates
start_date = datetime(year=1996,month=1,day=1)
end_date = datetime(year=1996,month=3,day=30)
d_range = pandas.DateRange(start_date,end_date,offset=pandas.DateOffset())
s_daily = pandas.Series(np.nan,d_range)


#--fill s_daily with the values from s1
s_daily_1 = s_daily.combine_first(s1)

#--fill s_daily_1 with values from s2
s_daily_2 = s_daily_1.combine_first(s2)

#--fill remaining nans with scalar
s_daily_scalar = s_daily_2.fillna(1.5)

#--fill remaining nans with forward filling
s_daily_ffill = s_daily_2.fillna(method='ffill')

#--fill remaining nans with back filling
s_daily_bfill = s_daily_2.fillna(method='bfill')

#--fill remaining nans with linear interpolations
s_daily_interp = s_daily_2.interpolate()



#--ugly plotting
fig = plt.figure()
ax = plt.subplot(411)
s_daily_1.plot(ax=ax,style='.')
s_daily_2.plot(ax=ax,style='.')
s_daily_scalar.plot(ax=ax,style='+')

ax2 = plt.subplot(412)
s_daily_1.plot(ax=ax2,style='.')
s_daily_2.plot(ax=ax2,style='.')
s_daily_ffill.plot(ax=ax2,style='+')

ax3 = plt.subplot(413)
s_daily_1.plot(ax=ax3,style='.')
s_daily_2.plot(ax=ax3,style='.')
s_daily_bfill.plot(ax=ax3,style='+')

ax4 = plt.subplot(414)
s_daily_1.plot(ax=ax4,style='.')
s_daily_2.plot(ax=ax4,style='.')
s_daily_interp.plot(ax=ax4,style='+')

ax.set_ylim(0,3)
ax2.set_ylim(0,3)
ax3.set_ylim(0,3)
ax4.set_ylim(0,3)

plt.show()

print s_daily


