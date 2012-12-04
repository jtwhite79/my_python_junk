import sgems
sgems.execute('LoadObjectFromFile  D:/Users/jwhite/Projects/Broward/Geostats/SGEMS/Layer1_thk.sgems::s-gems')
data = sgems.get_property('Layer_Thk','Layer_1_thk NGVD_meters')
print data