import sgems
import math

seed = 14071789
num_realizations = 5000
nrow,ncol = 158,93
delr,delc = 1000,1000 

offset = (503800.0,2778800.0)
realization_path = 'D:/Users/jwhite/Projects/Broward/Geostats/SGEMS/l1_ds_reals/'
realization_prefix = 'layer1_thk_omni_ds'

prop_names = ['H_thk','Q1_thk','Q2_thk','Q3_thk','Q4_thk','Q5_thk','T1_thk','T2_thk','T3_thk',]

try:
    sgems.execute('DeleteObjects tbl29::halfmile')
except:
    pass
load_command = 'LoadObjectFromFile  D:/Users/jwhite/Projects/Broward/Geostats/12_layer/Table_29.sgems::s-gems' 
sgems.execute(load_command)

newGrid_command = 'NewCartesianGrid  halfmile::116::197::1::2650::2650::1.0::668350::288415::0'
sgems.execute(newGrid_command)
#--for OK 
#dssim_command_aniso = 'RunGeostatAlgorithm  dssim::/GeostatParamUtils/XML::<parameters>  '+\
#                '<algorithm name="dssim" />     <Grid_Name  value="1000_grid"  />     '+\
#                '<Property_Name  value="DsSim" />     <Nb_Realizations  value="'+str(num_realizations)+'" />     '+\
#                '<Seed  value="14071789" />     <Kriging_Type  value="Ordinary Kriging (OK)"  />     '+\
#                '<Hard_Data  grid="Layer_Thk"   property="Layer_1_thk"  />     <Assign_Hard_Data  value="1"  />     '+\
#                '<Max_Conditioning_Data  value="12" />     <Search_Ellipsoid  value="500000 55000 0  10 0 0" />    '+\
#                '<cdf_type  value="Uniform"  />     <LN_mean  value="1" />     <LN_variance  value="1" />     '+\
#                '<U_min  value="0" />     <U_max  value="30" />     <nonParamCdf  ref_on_file ="0"  ref_on_grid ="1"  '+\
#                'break_ties ="0" filename =""   grid =""  property ="">  <LTI_type  function ="Power"  extreme ="0"  '+\
#                'omega ="3" />  <UTI_type  function ="Power"  extreme ="0"  omega ="0.333" />  </nonParamCdf>    '+\
#                '<is_local_correction  value="1"  />     <Variogram  nugget="0" structures_count="1"  >    '+\
#                '<structure_1  contribution="22"  type="Exponential"   >      <ranges max="500000"  medium="55000"  min="0"   />      '+\
#                '<angles x="10"  y="0"  z="0"   />    </structure_1>  </Variogram>  </parameters>   
#
#sgems.execute(dssim_command)
#
#for r in range(0,num_realizations):
#
#    save_command = 'SaveGeostatGrid 1000_grid::'+realization_path+realization_prefix+str(r)+'.dat::gslib::0::DsSim__real'+str(r)
#    sgems.execute(save_command)
#sgems.execute('DeleteObjects Layer_Thk::1000_grid')