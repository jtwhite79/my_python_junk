import re
import sys
import math
import calendar
import datetime
import numpy as np
import shapefile


def unique_list(lst):
    seen = {}
    result = []
    for item in lst:
        if marker in seen:
            seen[marker] = 1
            result.append(item)
    return result
    

def string_2_date(string):
    #--date format = mm/dd/yy
    raw = string.split('/')
    raw_month = int(raw[0])
    raw_day = int(raw[1])
    raw_year = int(raw[2])
    
    #--convert to 4 digit year
    if raw_year < 12: 
        raw_year += 2000
    else:
        raw_year += 1900
            
    
    return raw_year,raw_month
    
           

def load_pws_data(dfile):            
    permit_idx = 0
    name_idx = 2
    date_idx = 3
    data_idx = 4
    reqm_idx = 5    
    
    #--three lists are needed
    #--for individual well entries
    #--,accumulated permit entries
    #--and for partially accum entries
    #--use reqm and re matching to determine    
    permit_list_ind = []
    permit_list_acc = []
    permit_list_part = []
    #--year,month,data
    data_list_ind = []
    data_list_acc = []
    data_list_part = []
    
    fail_count = 0
    line_count = 0
    f = open(dfile,'r')
    header = f.readline()
    line_count += 1
    
    problems = []
    wre = re.compile('well',re.IGNORECASE)
    wfre = re.compile('wellfield',re.IGNORECASE)
    
    while True:
        line = f.readline()
        if line == '': break
        line_count += 1
        raw = line.strip().split(',')
        if len(raw) < 5:
            line2 = f.readline()
            line_count +=1
            line += line2 
            raw = line.strip().split(',')
            #print line_count,raw
                    
        if raw[data_idx] != '':                       
            #--this is a pain in the ass...some of the data records have ',' in the name attrib
            try:
                this_permit = raw[permit_idx]
                this_reqm = raw[reqm_idx]
                this_name = raw[name_idx].strip()
                this_date_str = raw[date_idx]
                this_data = float(raw[data_idx])        
                this_year,this_month = string_2_date(this_date_str)
            except:
                this_permit = raw[permit_idx]    
                this_name = raw[name_idx].strip()+' '+raw[name_idx+1].strip()       
                this_reqm = raw[reqm_idx+1]
                this_date_str = raw[date_idx+1]           
                this_data = float(raw[data_idx+1])        
                this_date = string_2_date(this_date_str)                                               
                                                                        
            #--try to find the index of this permit id in the list
            try:
                #--check if this_permit = this_reqm
                #--if so, this is the permit accumulated
                #--extraction                 
                if this_permit == this_reqm:
                    this_idx = permit_list_acc.index(this_permit)                                 
                    this_data_array = np.array([this_year,this_month,this_data])          
                    data_list_acc[this_idx] = np.vstack((data_list_acc[this_idx],this_data_array))                                       
                #--or use this pain in the ass re matching to find entire wellfield rates
                #--and add it to the partial accum list
                #--check for the word 'wellfield' in the name
                #--but not the word 'well' more than once
                elif len(wfre.findall(this_name)) == 1 and this_permit != this_reqm \
                and len(wre.findall(this_name)) < 2:
                    this_idx = permit_list_part.index(this_permit)                                 
                    this_data_array = np.array([this_year,this_month,this_data])          
                    data_list_part[this_idx] = np.vstack((data_list_acc[this_idx],this_data_array))
                    if this_name not in problems:
                        problems.append(this_name)
                #--else this is a simple individual well rate
                else:
                    this_idx = permit_list_ind.index(this_permit)                                 
                    this_data_array = np.array([this_year,this_month,this_data])          
                    data_list_ind[this_idx] = np.vstack((data_list_ind[this_idx],this_data_array))                               
                
            #--if not found, add this permit to the list
            #--and add new lists to data
            except:
                if this_permit == this_reqm:
                    permit_list_acc.append(this_permit)
                    this_data_array = np.array([this_year,this_month,this_data])
                    data_list_acc.append(this_data_array)
                elif len(wfre.findall(this_name)) == 1 and this_permit != this_reqm \
                and len(wre.findall(this_name)) < 2:
                    permit_list_part.append(this_permit)
                    this_data_array = np.array([this_year,this_month,this_data])
                    data_list_part.append(this_data_array)
                    if this_name not in problems:
                        problems.append(this_name)
                else:
                    permit_list_ind.append(this_permit)
                    this_data_array = np.array([this_year,this_month,this_data])
                    data_list_ind.append(this_data_array)
                                
        else:
            #print line_count,' missing data: ',line
            fail_count += 1   
            #break
                
    f.close()
    #for p in problems:
    #    print p    
    #print problems 
    print 'failures: ',fail_count
    return permit_list_acc,permit_list_ind,permit_list_part,data_list_acc,data_list_ind,data_list_part


def write_well_file(well_list,file_name):
    f = open(file_name,'w')
    f.write('# Average Annual pump rates from Broward PWS data\n')
    #--first find mxaxt    
    mxact = 0   
    for day in well_list:
        this_len = len(day)
        if this_len > mxact:
            mxact = this_len

    f.write('{0:10.0f} {1:10.0f}\n'.format(mxact,0))
    
    for day in well_list:
        write_well_sp(f,day)
    f.close()
    return   


def write_well_sp(f,wList):
    f.write('{0:10.0f} {1:10.0f} '.format(len(wList),0))
    f.write(' #  '+wList[0][5]+'\n')
    for item in wList:
        f.write('{0:10.0f} {1:10.0f} {2:10.0f} {3:10.3e}'\
                .format(item[0],item[1],item[2],item[3]))
        f.write(' #  '+item[4]+'\n')
    return

 
def get_names(this_row,this_col,name_list):
    this_names = ''
    for idx in range(len(name_list[0])):
        if name_list[0][idx] == this_row and name_list[1][idx] == this_col:
            this_names = this_names + ' ' + name_list[2][idx]
    return this_names

def sort_well_file_by_row_col(well_list):
    
    idx_row = 1
    idx_col = 2 
    sorted_list = [] 
    
    #--for each entry (day)
    for d_idx in range(len(well_list)):
        #--initialized a tracking list    
        visited = []
        for w in well_list[d_idx]:
            visited.append(False)
        
        this_sorted_list = []
        for w_idx in range(len(well_list[d_idx])):
            if visited[w_idx] == False:
                this_sorted_list.append(well_list[d_idx][w_idx])
                visited[w_idx] = True
                this_row = well_list[d_idx][w_idx][idx_row]
                this_col = well_list[d_idx][w_idx][idx_col]
                for ww_idx in range(len(well_list[d_idx])):
                    row = well_list[d_idx][ww_idx][idx_row]
                    col = well_list[d_idx][ww_idx][idx_col]
                    #print this_row,this_col,row,col
                    if w_idx != ww_idx and this_row == row and\
                      this_col == col:
                        #print well_list[d_idx][ww_idx]                        
                        this_sorted_list.append(well_list[d_idx][ww_idx])
                        visited[ww_idx] = True
        sorted_list.append(this_sorted_list)
    return sorted_list
                    
           


#--load the data...a real pain in the ass
data_file = 'BrowardPWSpumpage-mod.csv'
permits_acc,permits_ind,permits_part,data_acc,data_ind,data_part = load_pws_data(data_file)

#--load the current ibound.  used to make sure wells are located in active cells
ibound = np.loadtxt('..\\model_6layer_500\\ref\\ibound.ref')


#-------------------------------------------------------------------------------


#--calc average monthly rates
#--for the individual data
rates_ind = []
for p_idx in range(len(permits_ind)):
    #print permits_ind[p_idx]
    this_data = data_ind[p_idx]
    
    this_rates = np.zeros(12) - 999
    for month in range(1,13):
        this_month_data = this_data[np.where(this_data[:,1]==month)] 
        #print this_month_data
        
        #--accumulate for all entries in the same year on this day
        #--i.e. multiple wells reported for the same permit
        unique_years = np.unique(this_month_data[:,0])              
        #unique_rates = np.zeros((unique_years.shape[0],3))
        accum_years = []
        for year in unique_years:
            this_year = this_month_data[np.where(this_month_data[:,0]==year)]
            this_accum_year = np.cumsum(this_year[:,2])[-1]            
            accum_years.append(this_accum_year)
            #print permits_ind[p_idx],year,this_accum_year        
        
        accum = np.array(accum_years)
        
        #--not worrying about leap year
        num_days_month = calendar.monthrange(2011,month)[1]
        
        if this_month_data.shape[0] > 1:
            #this_mean = np.mean(this_month_data[:,2])
            this_mean = np.mean(accum)
        else:
            this_mean = 0                
        #print permits_ind[p_idx],this_accum_year,this_mean            
        
        #--convert to model units (from mg/month to cfd)
        if this_mean != 0:
            this_mean /= float(num_days_month)
            this_mean /= 7.481
            this_mean *= 1.0e6    
        #print permits[p_idx],month,this_mean,num_days_month
                
        this_rates[month-1] = this_mean    
    rates_ind.append(this_rates)    


#--calc average monthly rates
#--for the partial data
rates_part = []
for p_idx in range(len(permits_part)):
    #print permits_ind[p_idx]
    this_data = data_part[p_idx]
    
    this_rates = np.zeros(12) - 999
    for month in range(1,13):
        this_month_data = this_data[np.where(this_data[:,1]==month)] 
        #print this_month_data
        
        #--accumulate for all entries in the same year on this day
        #--i.e. multiple reports for the same permit
        unique_years = np.unique(this_month_data[:,0])                      
        accum_years = []
        for year in unique_years:
            this_year = this_month_data[np.where(this_month_data[:,0]==year)]
            this_accum_year = np.cumsum(this_year[:,2])[-1]            
            accum_years.append(this_accum_year)            
        
        accum = np.array(accum_years)
        
        #--not worrying about leap year
        num_days_month = calendar.monthrange(2011,month)[1]
        
        if this_month_data.shape[0] > 1:
            #this_mean = np.mean(this_month_data[:,2])
            this_mean = np.mean(accum)
        else:
            this_mean = 0                        
        
        #--convert to model units (from mg/month to cfd)
        if this_mean != 0:
            this_mean /= float(num_days_month)
            this_mean /= 7.481
            this_mean *= 1.0e6            
                
        this_rates[month-1] = this_mean    
    rates_part.append(this_rates)  



#--calc average monthly rates for the accumulated data
rates_acc = []
for p_idx in range(len(permits_acc)):
    #print permits_acc[p_idx]
    this_data = data_acc[p_idx]
    
    this_rates = np.zeros(12) - 999
    for month in range(1,13):
        this_month_data = this_data[np.where(this_data[:,1]==month)] 
        #print this_month_data
                             
        #--not worrying about leap year
        num_days_month = calendar.monthrange(2011,month)[1]                
        
        if this_month_data.shape[0] > 1:
            this_mean = np.mean(this_month_data[:,2])
        else:
            this_mean = 0
                    
        #--convert to model units (from mg/month to cfd)
        if this_mean != 0:
            this_mean /= float(num_days_month)
            this_mean /= 7.481
            this_mean *= 1.0e6    
        #print permits[p_idx],month,this_mean,num_days_month
        
        this_rates[month-1] = this_mean
    #break
    rates_acc.append(this_rates)    


#print len(rates_acc)
#for idx in range(len(rates_ind)):
#    print permits_ind[idx],rates_ind[idx]
#sys.exit()
          

#-------------------------------------------------------------------------------


#--load the shapes
file = 'PWS_modelDomain_layerPortion'
shp = shapefile.Reader(shapefile=file)
wells = shp.shapes()
header = shp.dbfHeader()
#--the dbf attribute indexes
permit_idx = 6 
row_idx = 31
col_idx = 32
#row_idx = 63
#col_idx = 64

util_idx = 22
name_idx = 7
portion_idxs = [55,56,57,58,59,60]
print header[row_idx]

##--load the grid shapefile for testing 
#file = 'broward_grid_ibound'
#grid_shp = shapefile.Reader(shapefile=file)
#cells = grid_shp.shapes()
##--set the writer instance for testing
#wr = shapefile.Writer()
#wr.field('row',fieldType='N',size=20)
#wr.field('col',fieldType='N',size=20)
#wr.field('rate',fieldType='N',size=20,decimal=4)


#nrow,ncol = 411,501 
nrow,ncol = 822,1002 
nlay = 6

#--loop over the well shapes once to determine how many wells are with each permit
#--and also to build the name string(s)
well_count_ind = np.zeros(len(permits_ind))
well_count_acc = np.zeros(len(permits_acc)) 
well_count_part = np.zeros(len(permits_part)) 
name_row = []
name_col = []
name = []
layer_portions = []
for w_idx in range(len(wells)):    
    
    this_rec = shp.record(w_idx)
    this_permit = this_rec[permit_idx]
    this_row = this_rec[row_idx]
    this_col = this_rec[col_idx]
    this_name = this_rec[name_idx]
    this_util = this_rec[util_idx]
    this_name_str = this_permit+'_'+this_util+'_'+this_name
    name_row.append(this_row)
    name_col.append(this_col)
    name.append(this_name_str)         
        
    if this_permit in permits_acc:    
        this_idx = permits_acc.index(this_permit)
        well_count_acc[this_idx] += 1
    if this_permit in permits_ind:    
        this_idx = permits_ind.index(this_permit)
        well_count_ind[this_idx] += 1    
    if this_permit in permits_part:    
        this_idx = permits_part.index(this_permit)
        well_count_part[this_idx] += 1     

name_list = [name_row,name_col,name]        



#--now build data list
well_file_list =[] 
well_file_name = 'avg_ann.wel'
day_count = 0
 
this_year = 2011
for month in range(1,13):
    num_days_month = calendar.monthrange(2011,month)[1]                    
    for day in range(1,num_days_month+1):        
        this_date = datetime.date(this_year,month,day).strftime('%B %d, %Y')        
        day_count +=1
        well_array = np.zeros((nlay,nrow,ncol))  
        this_well_file_list = []
        
        #--loop over the shp wells and fill the well_array
        for w_idx in range(len(wells)):    
            this_rec = shp.record(w_idx)
            this_permit = this_rec[permit_idx]            
            this_row = this_rec[row_idx]
            this_col = this_rec[col_idx]
            
            #--load layer portions            
            this_layer_portions = []
            for p in portion_idxs:
                this_layer_portions.append(this_rec[p])            
                       
            #--determine if accum and/or individual data exists
            #--try the accumulated first
            if this_permit in permits_acc:                
                this_idx = permits_acc.index(this_permit)
                this_rate = rates_acc[this_idx][month-1]                
                if this_rate != 0:
                    this_rate /= well_count_acc[this_idx]                                
                for lay in range(nlay):
                    if this_layer_portions[lay] != 0.0:
                        this_p_rate = this_rate * this_layer_portions[lay] 
                        well_array[lay,this_row-1,this_col-1] -= this_p_rate
            
            #--if no accumulated, then try ind                                                
            elif this_permit in permits_ind:
                this_idx = permits_ind.index(this_permit)
                this_rate = rates_ind[this_idx][month-1]                
                if this_rate != 0:
                    this_rate /= well_count_ind[this_idx]                                                
                for lay in range(nlay):
                    if this_layer_portions[lay] != 0.0:
                        this_p_rate = this_rate * this_layer_portions[lay] 
                        well_array[lay,this_row-1,this_col-1] -= this_p_rate
            
            #--finally try the partial rates
            elif this_permit in permits_part:
                print 'using partial record data'
                this_idx = permits_part.index(this_permit)
                this_rate = rates_part[this_idx][month-1]                
                if this_rate != 0:
                    this_rate /= well_count_part[this_idx]                                                
                for lay in range(nlay):
                    if this_layer_portions[lay] != 0.0:
                        this_p_rate = this_rate * this_layer_portions[lay] 
                        well_array[lay,this_row-1,this_col-1] -= this_p_rate
                                       
        #--get the indexes of wells that are active
        well_locs = np.argwhere(well_array!=0)
        #--get active well rates
        well_rates = well_array[np.where(well_array!=0)]
        #print well_locs.shape,well_rates.shape
        print 'month,day,total_days,total pumpage',\
               month,day,day_count,np.cumsum(well_rates)[-1]*7.481 / 1.0e6
        
        
        #--save the well file entries
        for w_idx in range(well_locs.shape[0]):
            this_lay = well_locs[w_idx,0] + 1
            this_row = well_locs[w_idx,1] + 1
            this_col = well_locs[w_idx,2] + 1
            #print this_row,this_col,well_locs[w_idx]
            this_ibound = ibound[this_row-1,this_col-1]
            if this_ibound > 0:
                this_rate = well_rates[w_idx]                        
                this_names = get_names(this_row,this_col,name_list)
                this_well_file_list.append([this_lay,this_row,this_col,this_rate,this_names,this_date])
            #break
        well_file_list.append(this_well_file_list) 
       
        #break
    #break
    #--write a grid with the rates for testing
    #for c_idx in range(len(cells)):
    #    this_rec = grid_shp.record(c_idx)
    #    this_row = this_rec[0]
    #    this_col = this_rec[1]  
    #    #print this_row,this_col
    #    this_rate = well_array[this_row-1,this_col-1]
    #    if this_rate != 0:
    #        wr.poly([cells[c_idx].points],shapeType=5)
    #        wr.record([this_row,this_col,this_rate])             
    #break   
print 'sorting by row col'
sorted_well_file_list = sort_well_file_by_row_col(well_file_list)            
print 'done'
write_well_file(sorted_well_file_list,well_file_name)
         
#wr.save(target='wells_cells_all')
    