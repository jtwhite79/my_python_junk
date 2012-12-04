import sys
import numpy as np
import shapefile


nrow,ncol,nlay = 411,501,6
#nrow,ncol,nlay = 822,1002,6

#--index of row and col values in the grid shapefile
idx_row = 0
idx_col = 1
idx_num = 4
idx_ibnd = 8
idx_icbnd = 7

ghb_list = []
chd_list = []

chd_stage = -0.5

#--GHB codes: 30:northern,31:WCA1,32:WCA2A,33:WCA2B,34:WCA3B,35:southern

cond_dict = {5:50000.0,31:25000,32:25000,33:25000,34:25000}
stage_dict = {5:-0.5,31:11.0,32:11.0,33:11.0,34:4.5}
ghb_dict = {5:[],31:[],32:[],33:[],34:[]}
ghb_conc_dict  = {5:[],31:[],32:[],33:[],34:[]}

#--get the grid polygons
print 'loading grid polygons...'
file = 'broward_grid_ibound'
shp_poly = shapefile.Reader(shapefile=file)
cells = shp_poly.shapes()
records = shp_poly.records()
print 'grid loaded'

ghb = open('ghb.dat','w')
chd = open('chd.dat','w')
ghb_conc = open('ghb_conc.dat','w')
chd_conc = open('chd_conc.dat','w')
w_ghb,e_ghb = [],[]
w_ghb_c,e_ghb_c = [],[]
#--loop over each cell
coastal_list = []
for c,r in zip(cells,records):
    this_record = r  
    #print this_record
    #break
    #if c%100 == 0:
    #    print 'working on grid cell ',c+1,' of ',len(cells)
    this_row = this_record[idx_row]
    this_col = this_record[idx_col]
    this_ibnd = this_record[idx_ibnd]
    this_icbnd = this_record[idx_icbnd]
    if this_col % 100 == 0:
        print 'working on grid column ',this_col+1,' of ',ncol
    #--GHBs
    if this_ibnd in cond_dict.keys():
        stage = stage_dict[this_ibnd]
        cond = cond_dict[this_ibnd]
        
        
        if this_ibnd != 5:
            for l in range(nlay):
                this_line = '{0:9.0f} {1:9.0f} {2:9.0f} {3:9.3f} {4:9.3f}\n'\
                        .format(l+1,this_row,this_col,stage,cond) 
                ghb_dict[this_ibnd].append(this_line)
                this_line = '{0:9.0f} {1:9.0f} {2:9.0f} {3:9.3f}\n'\
                     .format(l+1,this_row,this_col,0.0) 
                ghb_conc_dict[this_ibnd].append(this_line) 
                
        #--coastal GHBs - layer 1 only
        else:
            this_line = '{0:9.0f} {1:9.0f} {2:9.0f} {3:9.3f} {4:9.3f}\n'\
                    .format(1,this_row,this_col,stage,cond) 
            ghb_dict[this_ibnd].append(this_line)
            this_line = '{0:9.0f} {1:9.0f} {2:9.0f} {3:9.3f}\n'\
                     .format(1,this_row,this_col,1.0) 
            ghb_conc_dict[this_ibnd].append(this_line)                     
            
    
     
    #CHDs
    elif this_ibnd == 2:
        for l in range(nlay):            
            this_line = '{0:9.0f} {1:9.0f} {2:9.0f} {3:9.3f} {4:9.3f}\n'\
                        .format(l+1,this_row,this_col,chd_stage,chd_stage) 
            chd.write(this_line)
            conc = 1.0
            if this_icbnd == 0:
                conc = 0.0                
      
            this_line = '{0:9.0f} {1:9.0f} {2:9.0f} {3:9.3f}\n'\
                     .format(l+1,this_row,this_col,conc) 
            chd_conc.write(this_line) 
        

ii = [5,31,32,33,34]        
for i in ii:        
    for l,ll in zip(ghb_dict[i],ghb_conc_dict[i]):
        ghb.write(l)
        ghb_conc.write(ll)

    
    
    
    
chd.close()
ghb.close()
ghb_conc.close()
chd_conc.close()
      
