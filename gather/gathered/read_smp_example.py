import numpy
from datetime import datetime
import pandas
import pestUtil
reload(pestUtil)


#--load a single site
smp = pestUtil.smp('heads_gap.out')
#smp = pestUtil.smp('s20_h_dbkey13037.smp',date_fmt='%m/%d/%Y')
site_names,offset_idx = smp.get_unique_from_file(smp.site_index,needindices=True)
#--load only one site
site_0 = smp.load(site=site_names[0])


#--load a single site with pandas
smpp = pestUtil.smp('heads_gap.out',pandas=True)
#smp = pestUtil.smp('s20_h_dbkey13037.smp',date_fmt='%m/%d/%Y')
site_names,offset_idx = smpp.get_unique_from_file(smp.site_index,needindices=True)
#--load only one site
site_0p = smpp.load(site=site_names[0])


#--load all sites
smp2 = pestUtil.smp('heads_gap.out',load=True)
#smp2 = pestUtil.smp('s20_h_dbkey13037.smp',date_fmt='%m/%d/%Y',load=True)
site_0,dates,vals = smp2.get_site(site_names[0])


#--load all sites with pandas
smp2p = pestUtil.smp('heads_gap.out',load=True,pandas=True)
#smp2 = pestUtil.smp('s20_h_dbkey13037.smp',date_fmt='%m/%d/%Y',load=True)
site_0,datesp,valsp = smp2p.get_site(site_names[0])


start_date = datetime(year=1996,month=1,day=1)
end_date = datetime(year=1998,month=11,day=30)
for oday in range(start_date.toordinal(),end_date.toordinal()):
     dt = datetime.fromordinal(oday)
     [names,values] = smp2.active(dt)
     [namesp,valuesp] = smp2p.active(dt)
     if values:
        print names
        print values      


