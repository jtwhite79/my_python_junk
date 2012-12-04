from datetime import datetime
import shapefile
#-----------------------------------------------------------
#--load the shapefile with the wfield names added
print 'loading shapefile...'
shp = shapefile.Reader('shapes\\nonpws_web_points')

header = shp.dbfHeader()

#--find the indexs of important attributes
idxs = {}
idxs['lu_desc'] = None
idxs['permit_no'] = None
idxs['county'] = None
idxs['final_acti'] = None
idxs['project_na'] = None
idxs['permit_dur'] = None
idxs['app_status'] = None
idxs['web_adate'] = None
idxs['web_edate'] = None
idxs['web_src'] = None
idxs['app_rcvd_d'] = None

for i,h in enumerate(header):
    for k,v in idxs.iteritems():
        if k.upper() == h[0].upper():           
            idxs[k] = i
            break

for k,v in idxs.iteritems():
    if v == None:
        raise IndexError,'couldnt find index for '+k
#--this takes awhile...
records = shp.records()
shapes = shp.shapes()
print len(records),' records loaded from shapefile'


#--build a list of unique permit nos
print 'building unique permit number list'
permit_no = []
for rec in records:
    p_no = rec[idxs['permit_no']]
    if p_no not in permit_no and a_stat.upper() == 'COMPLETE':
        permit_no.append(p_no)
print str(len(permit_no)),'unique permit numbers found'
 

#--setup the new shapefile writer instance
wr = shapefile.Writer()
wr.field('permit_no',fieldType='C',size='20')
wr.field('project_na',fieldType='C',size='50')
wr.field('web_src',fieldType='C',size='50')
wr.field('start_date',fieldType='C',size='20')
wr.field('end_date',fieldType='C',size='20')
   
print 'reducing entries by permit number'
for p_no in permit_no:
    #--find all the records with this permit no
    p_records = []
    p_shapes = []
    for rec,shape in zip(records,shapes):
        if rec[idxs['permit_no']] == p_no:
            p_records.append(rec)
            p_shapes.append(shape)
    #--find the extreme dates
    dmin,dmax = datetime(2100,1,1),datetime(1900,1,1)    
    print 'permit',p_no,'entries',len(p_records)
    for i,p in enumerate(p_records):        
        d = datetime.strptime(p[idxs['app_rcvd_d']],'%Y-%m-%d')
        if d < dmin:
            dmin = d            
        d = datetime.strptime(p[idxs['web_adate']],'%d-%b-%Y')
        if d < dmin:
            dmin = d           
        d = datetime.strptime(p[idxs['web_edate']],'%d-%b-%Y')
        if d > dmax:
            dmax = d            
    #--write a new record - just use the first shape in the list - doesn't matter where it is located
    nr = [p[idxs['permit_no']],p[idxs['project_na']],p[idxs['web_src']],dmin.strftime('%d-%d-%Y'),dmax.strftime('%d-%d-%Y')]
    wr.poly([p_shapes[0].points],shapeType=shapefile.POINT)
    wr.record(nr)


        #break
    #break
wr.save('shapes\\nonpws_web_points_reduce')
    
    
    



