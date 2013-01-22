import xml.etree.ElementTree as xml
import copy

def indent(elem, level=0):
    '''for prettyprinting XML
    '''
    i = "\n" + level*"  "
    if len(elem):        
        
        if not elem.text or not elem.text.strip():
        #try:
        #    elem.text += i + "  "
        #except TypeError:
            elem.text = i + "  "
        else:
            elem.text += i + "  "                            
        if (not elem.tail or not elem.tail.strip()) :
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i




xml_file = 'UMD.02\\xml\\SWNetFlow.xml'
tree = xml.parse(xml_file)
root = tree.getroot()

prefix = 'bf_'
ctag = 'swbudget'
unique_sites = []
unique_count = []
for swbudget in root.findall(ctag):    
    site = swbudget.attrib['name'].split()[0].strip()[:6]
    if site not in unique_sites:
        unique_sites.append(site)
        unique_count.append(1)
        name = site+'_1'
        if len(name) > 10:
            raise Exception('too long')
        swbudget.attrib['name'] = name
    else:
        count = unique_count[unique_sites.index(site)] 
        name = site+'_'+str(count + 1)
        if len(name) > 10:
            raise Exception('too long')
        swbudget.attrib['name'] = name
        unique_count[unique_sites.index(site)] += 1

indent(root)
xml.ElementTree(root).write('UMD.02\\xml\\SWNetFlow_rename.xml')
