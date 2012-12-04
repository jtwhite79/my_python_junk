import sgems
import math

seed = 14071789
num_realizations = 10000
nrow,ncol = 158,93
delr,delc = 1000,1000 

offset = (503800.0,2778800.0)
realization_path = 'D:/Users/jwhite/Projects/Broward/Geostats/SGEMS/realizations/'
realization_prefix = 'layer1_thk_omni_'

try:
    sgems.execute('DeleteObjects Layer_Thk::1000_grid')
except:
    pass
load_command = 'LoadObjectFromFile  D:/Users/jwhite/Projects/Broward/Geostats/SGEMS/Layer1_cdf.sgems::s-gems' 
sgems.execute(load_command)

newGrid_command = 'NewCartesianGrid  1000_grid::'+str(ncol)+'::'+str(nrow)+'::1::'+str(delc)+'::'+str(delr)+'::1.0::'+str(offset[0])+'::'+str(offset[1])+'::0'
sgems.execute(newGrid_command)

sgsim_command = 'RunGeostatAlgorithm  sgsim::/GeostatParamUtils/XML::<parameters>  '+\
                '<algorithm name="sgsim" />     <Grid_Name  value="1000_grid"  />     '+\
                '<Property_Name  value="SgSim1" />     <Nb_Realizations  value="'+str(num_realizations)+'" />     '+\
                '<Seed  value="'+str(seed)+'" />     <Kriging_Type  value="Ordinary Kriging (OK)"  />     '+\
                '<Trend  value="0 0 0 0 0 0 0 0 0 " />    <Local_Mean_Property  value=""  />     '+\
                '<Assign_Hard_Data  value="1"  />     '+\
                '<Hard_Data  grid="LayerThk"   property="Layer_1_thkcdf"  />     '+\
                '<Max_Conditioning_Data  value="12" />     '+\
                '<Search_Ellipsoid  value="100000 100000 100000  0 0 0" />    '+\
                '<Use_Target_Histogram  value=""  />     '+\
                '<nonParamCdf  ref_on_file ="0"  ref_on_grid ="1"  break_ties ="0" filename =""   '+\
                'grid ="Layer_Thk"  property ="Layer_1_thk">  <LTI_type  function ="Power"  '+\
                'extreme ="0"  omega ="3" />  <UTI_type  function ="Power"  extreme ="0"  '+\
                'omega ="0.333" />  </nonParamCdf>    <Variogram  nugget="0" structures_count="1"  >    '+\
                '<structure_1  contribution="20"  type="Exponential"   >      '+\
                '<ranges max="100000"  medium="100000"  min="0"   />      '+\
                '<angles x="0"  y="0"  z="0"   />    </structure_1>  </Variogram>  </parameters>   '
sgems.execute(sgsim_command)

for r in range(0,num_realizations):

    save_command = 'SaveGeostatGrid 1000_grid::'+realization_path+realization_prefix+str(r)+'.dat::gslib::0::SgSim1__real'+str(r)
    sgems.execute(save_command)
#sgems.execute('DisplayObject 1000_grid::SgSim1__real9')