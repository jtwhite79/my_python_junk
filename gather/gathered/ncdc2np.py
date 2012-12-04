import os,re
import numpy as np
import datetime


def load_ncdc_daily(file):
    assert os.path.exists(file)
    reg = re.compile('COOPID')
    data = np.zeros((8))
    coopid = []
    f = open(file,'r')
    header = f.readline().strip().split(',')
    lcount = 2;
    for line in f:
        raw = line.strip().split(',')
        #print lcount,len(raw)
        if len(raw) > 1 and reg.search(line) == None:
            if raw[12] == 'T': raw[12] = 0.002 
            elif raw[12] == ' ':raw[12] = 99999
            if raw[13] == 'null':raw[13] = -1
            elif raw[13] == ' ':raw[13] = 0 
            elif raw[13] == 'S':raw[13] = -2 
            elif raw[13] == 'A':raw[13] = -3 
            elif raw[13] == ')':raw[13] = -4 
            elif raw[13] == 'E':raw[13] = -5         
            this_date = datetime.date(int(raw[3]),int(raw[4]),int(raw[5]))
            this_ord_date = datetime.date.toordinal(this_date)
            #print lcount,len(raw),this_date,raw
            temp = np.array([float(raw[0]),float(raw[1]),this_ord_date,float(raw[12]),float(raw[13]),float(raw[3]),float(raw[4]),float(raw[5])])
            data = np.vstack((data,temp))
        elif reg.search(line) != None: coopid.append(raw[0])   
        lcount += 1;
    f.close()
    data = np.delete(data,[0],axis=0)
    return coopid,data


file = 'broward_data.dat'
ids,data = load_ncdc_daily(file)
data.tofile('broward_data_np.dat',sep=',')

