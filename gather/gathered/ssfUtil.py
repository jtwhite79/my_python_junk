import datetime,re
import numpy as np
import pylab
from matplotlib.dates import *
import matplotlib.ticker as tk

def listdate2ordarray(dlist,tlist,dlim='/'):
    assert len(dlist)==len(tlist)
    ordArray = np.zeros((len(dlist)))
    for l in range(0,len(dlist)):
        draw = dlist[l].split(dlim)
        thisDay = int(draw[0])
        thisMonth = int(draw[1])
        thisYear = int(draw[2])
        traw = tlist[l].split(':')
        thisHour = int(traw[0])
        thisMin = int(traw[1])
        thisSec = float(traw[2])
        thisDate = datetime.datetime(thisYear,thisMonth,thisDay)
        
        ordArray[l] =  thisDate.toordinal()
    return ordArray

def load_ssf(file):
    data = []
    names = []
    f = open(file,'r')
    
    raw = f.readline().strip().split()
    d,t = [raw[1]],[raw[2]]
    dataList = [raw[3]]
    thisSite = raw[0]
    for line in f:
        raw = line.strip().split()
        
        if raw[0] != thisSite:
            print thisSite,raw[0]
            dataArray = np.array(dataList)
            ordArray = listdate2ordarray(d,t)
            names.append(thisSite)
            ordArray = np.vstack((ordArray,dataArray))
            data.append(ordArray.transpose().astype(float))
            d,t = [raw[1]],[raw[2]]
            dataList = [raw[3]]
            thisSite = raw[0]
        else:
            
            d.append(raw[1])
            t.append(raw[2])
            dataList.append(raw[3])
    dataArray = np.array(dataList)
    
    ordArray = listdate2ordarray(d,t)
    #print dataArray.shape,ordArray.shape
    names.append(thisSite) 
    ordArray = np.vstack((ordArray,dataArray))
    #print ordArray.shape
    data.append(ordArray.transpose().astype(float))            
    f.close()
    return names,data

def write_ssf(site,array,file):
    f = open(file,'w')
    for rec in array:
        this_dt = datetime.datetime.fromordinal(rec[0]) 
        date_string = str(this_dt.day).zfill(2)+'/'+str(this_dt.month).zfill(2)+'/'+str(this_dt.year)
        time_string = str(this_dt.hour).zfill(2)+':'+str(this_dt.minute).zfill(2)+':'+str(this_dt.second).zfill(2)
        #print site,date_string,time_string,rec[1] 
        f.write(site.ljust(15)+' '+date_string+' '+time_string+' '+str(rec[1])+'\n')
    f.close()



def load_tsproc_list(file):
    reg = re.compile('V_TABLE')
    data = []
    names = []
    f = open(file,'r')
    blank = f.readline()
    tsname = f.readline()
    raw = f.readline().strip().split()
    d,t = [raw[1]],[raw[2]]
    dataList = [raw[3]]
    thisSite = raw[0]
    #for line in f:
    while True:
        line = f.readline()
        
        
        if line == '': break
        raw = line.strip().split()
        #if raw[0] != thisSite:
        if len(raw) == 0:
            #print thisSite,raw[0]
            dataArray = np.array(dataList)
            ordArray = listdate2ordarray(d,t)
            names.append(thisSite)
            ordArray = np.vstack((ordArray,dataArray))
            data.append(ordArray.transpose().astype(float))
            
            tsname = f.readline()
            #print tsname
            if reg.search(tsname) != None: break
            line = f.readline()
            raw = line.strip().split()
            d,t = [raw[1]],[raw[2]]
            dataList = [raw[3]]
            thisSite = raw[0]
        else:
            
            d.append(raw[1])
            t.append(raw[2])
            dataList.append(raw[3])
    dataArray = np.array(dataList)
    
    ordArray = listdate2ordarray(d,t)
    #print dataArray.shape,ordArray.shape
    names.append(thisSite) 
    ordArray = np.vstack((ordArray,dataArray))
    #print ordArray.shape
    data.append(ordArray.transpose().astype(float))            
    f.close()
    return names,data


def plot_ts(t,data,names=None,output='show',ax=None,color=None,lw=1.0):
    #print 'total date range: ',t[-1]-t[0]
    #--set up date formatters
    if t[-1]-t[0] < 90:
       majortick   = MonthLocator() 
       minortick   = DayLocator(15)                                               
       minFmt = DateFormatter('%d')                                     
       majFmt = DateFormatter('%b')       
    elif t[-1]-t[0] < 365:
        majortick   = MonthLocator() 
        minortick   = DayLocator()                                               
        minFmt = DateFormatter('')                                     
        majFmt = DateFormatter('%b')   
    elif t[-1]-t[0] < 5280:
        majortick   = YearLocator() 
        minortick   = MonthLocator((5,9))                                               
        minFmt = DateFormatter('%b')                                     
        majFmt = DateFormatter('%Y')           
    elif t[-1]-t[0] < 3650:
        majortick   = YearLocator(2) 
        minortick   = MonthLocator()                                               
        minFmt = DateFormatter('')                                     
        majFmt = DateFormatter('%Y')       
    else:
        majortick   = YearLocator(5) 
        minortick   = YearLocator()                                               
        minFmt = DateFormatter('')                                    
        majFmt = DateFormatter('%Y')       
   

    if ax == None:
        fig = pylab.figure()
        ax = pylab.subplot(111)
    #print data.shape
    try:
        for s in range(0,np.shape(data)[1]):
            if color != None:
             
                ax.plot(t,data[:,s],label=names[s],color=color[s],lw=lw)
            else:
                ax.plot(t,data[:,s],label=names[s],lw=lw)
    except:
        if color != None:
            ax.plot(t,data,label=names,color=color,lw=lw)
        else:
            ax.plot(t,data,label=names,lw=lw)
    
    if names != None:
        ax.legend()
    
    ax.xaxis.set_major_locator(majortick)
    ax.xaxis.set_minor_locator(minortick)
    ax.xaxis.set_major_formatter(majFmt)
    ax.xaxis.set_minor_formatter(minFmt)
    
    if output =='show' : 
        pylab.show()
        return
    elif output == None: return ax
    else:
         fmt = output.split('.')[-1]
         pylab.savefig(output,orientation='portrait',format=fmt,dpi=150)
         return 



#names,data = load_ssf('flows.out')
#print names,len(data),data[0].shape
#print data[0][0,0],data[0][0,1]
#plot_ts(data[0][:,0],data[0][:,1],names[0])