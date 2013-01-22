import xml.etree.ElementTree as xml


fname = 'testcase.xml'
tree = xml.parse(fname)
root = tree.getroot()
#--first level elements
for child in root:
    if child.text:
        print child.text    
    for key,val in child.attrib.iteritems():
        print child.tag,key,val        
    
    for gchild in child:
        if gchild.text:
            print gchild.text
        for key,val in gchild.attrib.iteritems():
            print gchild.tag,key,val



