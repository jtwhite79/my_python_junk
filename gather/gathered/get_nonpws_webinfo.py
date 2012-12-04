import re
import urllib2 
import httplib
import xml.etree.ElementTree as xml
import multiprocessing as mp
from Queue import Queue
import shapefile




def get_record(args):
    '''args = [job_no,link']
    '''
    job_no = args[0]
    link = args[1]
    #print 'getting permit info from link',link
    re_exp = re.compile('expiration',re.IGNORECASE)    
    url = urllib2.urlopen(link)
    lines = url.readlines()
    #--find the line with the info
    for line in lines:
        if re_exp.search(line) is not None:
            approv_date,exp_date,source = parse_content(line)
    
    return [job_no,[approv_date,exp_date,source]]

def parse_content(line):    
    re_src = re.compile('source',re.IGNORECASE)
    re_date = re.compile('[0-9]{2}-...-[0-9]{4}')
    dates = re_date.findall(line)
    approv_date = dates[0]
    exp_date = dates[1]    
    raw = re_src.split(line)
    source = raw[1].split('>')[3].split('<')[0]
    return approv_date,exp_date,source

def worker(jobq,resultq):
    
    while True:
        args = jobq.get()
        #--check for sentinel
        if args is None:
            break
        #try:
        print 'getting record',args[0]
        results = get_record(args)
        resultq.put_nowait(results)
        #except:
        #    failq.put_nowait(args)

        jobq.task_done()
    #--sentinel task is done
    jobq.task_done()         

def main():

    #-----------------------------------------------------------
    #--load the shapefile
    print 'loading shapefile...'
    shp = shapefile.Reader('shapes\\nonpws_poly')
    records = shp.records()
    header = shp.dbfHeader()
    print len(records),' records loaded from shapefile'
    #--find the indexs of important attributes
    idxs = {}
    idxs['link'] = None
    idxs['permit_no'] = None
    idxs['county'] = None
    idxs['final_acti'] = None
    idxs['project_na'] = None
    idxs['app_status'] = None
    for i,h in enumerate(header):
        for k,v in idxs.iteritems():
            if k.upper() == h[0].upper():           
                idxs[k] = i
                break
    for k,v in idxs.iteritems():
        if v == None:
            raise IndexError,'couldnt find index for '+k

    #--build a list of only the records that are needed
    valid_record,valid_shape = [],[]
    counties = ['BROWARD','MIAMI-DADE','PALM BEACH']
    for i,r in enumerate(records):    
        p,c = r[idxs['permit_no']],r[idxs['county']]
        n = r[idxs['project_na']]       
        a_stat = r[idxs['app_status']]        
        if p != '' and c in counties and a_stat.upper() == 'COMPLETE':
            valid_record.append(r)
            valid_shape.append(shp.shape(i))
    print len(valid_record),' records needed'

    #--a new shapefile with less junk in it
    wr = shapefile.Writer()
    for i,item in enumerate(header):
        if item[0].lower() in idxs.keys():
            wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
    #--add three new fields for the web content
    wr.field('web_adate',fieldType='C',size='20')
    wr.field('web_edate',fieldType='C',size='20')
    wr.field('web_src',fieldType='C',size='50')

    #--get the web info
    print 'retrieving records...'
    #--build the job queue args
    job_no = 0
    queue_args = []
    for r,s in zip(valid_record,valid_shape):
        queue_args.append([job_no,r[idxs['link']]])
        job_no += 1
        #break
        if job_no >= 20:
            break
    
    #--create queues
    jobq = mp.JoinableQueue()
    resultsq = mp.Queue()   

    #--start the processes
    num_procs = 2
    procs = []
    for i in range(num_procs):
        p = mp.Process(target=worker,args=(jobq,resultsq))
        p.daemon = True
        p.start()
        procs.append(p)

    #--add the args to jobq
    for qa in queue_args:
        jobq.put(qa)

    #--add sentinels...
    for p in procs:
        jobq.put(None)

    #--block until all finish
        for p in procs:
            p.join() 
            print p.name,'Finished' 
    #--transfer the results queue to a list
    results = []
    while True:
        try:
            rr = resultsq.get_nowait()
            results.append(rr)
        except:
            break
    
    idx = 0
    failed = []
    for r,s in zip(valid_record,valid_shape):
        #--find the web result
        result = None
        for rr in results:
            if rr[0] == idx:
                result = rr
                break
        if result is None:
            failed.append(idx)
        else:
            a_date,e_date,source = result[1]        
            r.append(a_date)
            r.append(e_date)
            r.append(source)
            wr.poly([s.points],shapeType=shapefile.POLYGON)
            wr.record(r)
        idx += 1
    wr.save('nonpws_web')
    
    f = open('failed.dat','w')
    for fa in failed:
        f.write(valid_record[fa][idxs['permit_no']]+'\n')
    f.close()
            
if __name__ == '__main__':                                                       
    mp.freeze_support() # optional if the program is not frozen                  
    main()   