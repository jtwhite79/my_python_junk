import multiprocessing as mp
import numpy as np
import pandas
import shapefile


def worker(pid,nrow,ncol,pixel_map,jobq):
    while True:
        args = jobq.get()
        if args == None:
            break
        aname = args[0]
        pixel_values = args[1]
        arr = np.zeros((nrow,ncol),dtype=np.float32)
        for i in range(nrow):
            for j in range(ncol):
                pf_list = pixel_map[(i,j)]
                for (p,f) in pf_list:               
                    arr[i,j] += pixel_values[p] * f                         
        arr.tofile(aname)
        jobq.task_done()
        print pid,aname
    jobq.task_done()
    return            


def main():

    aprefix = 'rch\\rch_'
    #aprefix = 'et\\et_'
    print 'loading forcing dataframe'
    df = pandas.read_csv('NEXRAD.csv',index_col=0,parse_dates=True)
    #df = pandas.read_csv('PET.csv',index_col=0,parse_dates=True)
    df[df <0.0] = 0.0
    df_keys = list(df.keys())

    print 'loading grid shapefile info'
    grid_shapename = '..\\shapes\\tsala_grid_nexrad'
    grid_shape = shapefile.Reader(grid_shapename)
    fieldnames = shapefile.get_fieldnames(grid_shapename,ignorecase=True)
    row_idx,col_idx = fieldnames.index('ROW'),fieldnames.index('COLUMN_')
    pix_idx,frac_idx = fieldnames.index('NEX_PIX'),fieldnames.index('NEX_FRAC')
    pixel_map = {}
    pixel_numbers = []
    nrow,ncol = -1.0E+10,-1.0E+10
    for i in range(grid_shape.numRecords):
        if i % 500 == 0:
            print i,'of',grid_shape.numRecords,'\r',
        rec = grid_shape.record(i)
        pix,frac = rec[pix_idx],rec[frac_idx]
        r,c = rec[row_idx],rec[col_idx]
        if r > nrow: nrow = r
        if c > ncol: ncol = c
        idx_tup = (r-1,c-1)    
        pf_list = []
        if len(pix) > 0:
            pf_list = []
        
            for p,f in zip(pix.split(','),frac.split(',')):
                p = str(p)
                f = float(f)
                pf_list.append((p,f))            
        pixel_map[idx_tup] = pf_list
        



    #--check for missing pixels
    missing = []
    for idx_tup,pf_list in pixel_map.iteritems():
        for p,f in pf_list:            
            if p not in df_keys and  p not in missing:
                missing.append(p)
    if len(missing) > 0:
        print 'missing data for',len(missing),' pixels'
        print len(df_keys)
        for m in missing:
            print m
        raise Exception()


    print 'processing dataframe rows'
    q_args = []
    for dt,pixel_values in df.iterrows():
        print dt
        aname = aprefix+dt.strftime('%Y%m%d')+'.ref'    
        q_args.append([aname,pixel_values])
    
    
    jobq = mp.JoinableQueue()  

    procs = []
    num_procs = 3
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=worker,args=(i,nrow,ncol,pixel_map,jobq))
        p.daemon = True
        print 'starting process',p.name
        p.start()
        procs.append(p)
    
    for q in q_args:
        jobq.put(q)

    for p in procs:
        jobq.put(None)      
    
    for p in procs:
        p.join() 
        print p.name,'Finished' 


if __name__ == '__main__':                                                                       
    main()         