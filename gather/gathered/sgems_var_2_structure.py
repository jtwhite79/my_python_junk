import os
from xml.etree import ElementTree as xml
import pestUtil

def load_sgems_var(fname):
    tree = xml.parse(fname)
    root = tree.getroot()
    prefix = fname.split('\\')[-1]
    par_dict = {'structure_name':prefix}
    for k,val in root.attrib.iteritems():
        par_dict[k] = val
    for istr,structure in enumerate(root):
        str_name = prefix+'_'+structure.tag.split('_')[-1]
        str_dict = {}
        for k,val in structure.attrib.iteritems():
            str_dict[k] = val
        for element in structure:
            for k,val in element.attrib.iteritems():
                str_dict[k] = val
        str_dict['structure_number'] = str(istr+1)
        par_dict[str_name] = str_dict
   
    return par_dict


def sgems_2_struct(sgems_dict):
    str_list = pestUtil.structure_list
    str_dict = {'STRUCTNAME':sgems_dict['structure_name']}
    str_dict['NUMVARIOGRAM'] = sgems_dict['structures_count']
    str_dict['NUGGET'] = sgems_dict['nugget']
    sgems_dict.pop('structures_count')
    sgems_dict.pop('nugget')
    sgems_dict.pop('structure_name')
    istr = 1
    for s_name,s_dict in sgems_dict.iteritems():        
        var_dict = {'VARNAME':s_name}        
        var_dict['CONTRIBUTION'] = s_dict['contribution']
        max,med = float(s_dict['max']),float(s_dict['medium'] )
        var_dict['A'] = '{0:10.4e}'.format(max)
        if med == 0:
            var_dict['ANISOTROPY'] = '1.0'
        else:
            var_dict['ANISOTROPY'] = '{0:10.4e}'.format(max / med)
        var_dict['VARTYPE'] = pestUtil.vario_type_dict[s_dict['type'].lower()]
        var_dict['BEARING'] = s_dict['x']
        str_dict[s_name] = var_dict
    return str_dict
        



vdir = 'variograms_new\\'
files = os.listdir(vdir)
f_out = open('fieldgen\\pest_structures.dat','w')
for f in files:
    tree = xml.parse(vdir+f)
    root = tree.getroot()
    if root.tag.upper() == 'VARIOGRAM_MODEL':
        pars = load_sgems_var(vdir+f)
        struct = sgems_2_struct(pars)
        s_name = f.split('.')[0]
        #pestUtil.write_structure_from_dict('fieldgen\\pest_structures\\'+s_name+'.str',s_name,struct)
        pestUtil.write_structure_from_dict(f_out,s_name,struct)
        print f

#--also covert the gslib tbl29 file to seperate smp files
pestUtil.gslib_2_smp('data\\Table_29_ls.dat')        
