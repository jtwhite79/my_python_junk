import re
import copy
import sys
import xml.etree.ElementTree as xml

'''not supported:
                 tied parameters
   need to:
                 cast floats and ints
                 input checking (mandatory args)
                 error handling       
'''                 


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


def loadpst(fname):
    '''load the text pest control file
    to provide tags and attributes for the 
    xml tree.  Also builds the required list by looking
    for '[' and ']' and builds the repeatable entry list
    by keying on the '(' and ')'


    special treatment of the tied parameter mess

    '''
    f = open(fname,'r') 
    #--nested list of parameter names
    pst_list = []
    #--nested list of bools for required pars
    req_list = []
    #--list of bools for repeatable entries (pars,obs,etc)
    #--one entry for each section    
    rep_list = []
    for line in f:        
        if not line.startswith('('):            
            pst_list.append([])
            req_list.append([])
            rep_list.append(False)
            raw = line.strip().split()
            rq = True
            for i,r in enumerate(raw):
                if r.startswith('['):
                    rq = False                                    
                req_list[-1].append(rq)
                if r.endswith(']'):
                    rq = True                    
                r = r.replace('[','')
                r = r.replace(']','')
                                            
                pst_list[-1].append(r)
        else:
            rep_list[-1] = True                                                                        
    f.close()
    
    #--now fix the tied parameter mess
    for i,p_list in enumerate(pst_list):
        if 'PARTIED' in p_list:
            break
    #--remove the entries at index i from all three lists
    temp = pst_list.pop(i)
    req_list.pop(i)
    rep_list.pop(i)

    #--add the partied attribute to the end of the parameter data line
    pst_list[i-1].append('PARTIED')
    
    #--add a dummy bool to the required list
    req_list[i-1].append(False)

    return pst_list,req_list,rep_list
    

def build_pstxml(pst_list,req_list):
    '''build an empty xml tree from the pst text list         
    '''
    root = xml.Element(pst_list[0][0])
    for r_list,p_list in zip(req_list[1:],pst_list[1:]):
        if p_list[0].startswith('*'):            
            #--try since the first one doesn't have any nodes
            try:
                root.append(el)
            except:
                pass                 
            #--strip off the '* and replace spaces with underscore
            #--also replace the '/' with an underscore                            
            #tag = '_'.join(p_list[1:])
            #tag = tag.replace('/','_')
            tag = 'section'
            el = xml.Element(tag)
                        
            #--set the text as the original name
            el.text = (' '.join(p_list)).strip()
        else:
            for r,p in zip(r_list,p_list):
                #print p,el.keys()                
                el2 = xml.Element(p)
                el2.set('mandatory',str(r))
                el.append(el2)
               
                
    return root                              

                                                            
def pst2xml(fname,pstxml,pst_list,req_list,rep_list):
    '''load a pst into xml format
    fname = pst file name
    pstxml = the (empty) xml tree for the pst
    pst_list = the pst varible list
    req_list = the boolean required var list (not used yet)
    rep_list = boolean repeatable list
    
    special treatment is given to prior information
    equations are not parsed, they are grouped into text strings
        
    special treatment of the tied parameter mess
    '''
    f = open(fname,'r')
    #--read the pcf line
    f.readline()    
    #--create a new xml tree to populate
    root = xml.Element('pcf')      
    #--counters for position in the file and in the pst_list,rep_list
    l_count,p_count = 1,1
    while True:
        line = f.readline()
        if line == '':
            break
        #--if this is the start of a section      
        elif line.strip().startswith('*'):            
            #--find the node
            for node in pstxml:                                
                if node.text.strip() == line.strip():                   
                    node.text = node.text.strip()
                    root.append(copy.deepcopy(node))
                    break
            #--find the index in pst_list
            for i,p_list in enumerate(pst_list):
                if p_list[0] == '*':
                    s = ' '.join(p_list)                    
                    if s == line.strip():                        
                        p_count = i+1
                        break                                                                
        
        #--if this is a non-repeatable section                                          
        elif rep_list[p_count] is False:           
            p_list = pst_list[p_count]
            r_list = req_list[p_count]
            raw = line.strip().split()            
            for pval,pitem,ritem in zip(raw,p_list,r_list):                                                                
                elem = root[-1].find(pitem)
                if elem is not None:
                    elem.set('value',pval)                    
                else:                     
                     raise KeyError,'attribute '+pitem+\
                           ' not found in element '+\
                           ' '.join(root[-1].keys())                                   
            p_count += 1   
        
        #--this is a repeatable section
        else:                                    
            #--if subelements do not have value attributes
            #--then remove its attributes and subelements
            hasval = False
            for n in root[-1][-1]:               
                if 'value' in n.keys():
                    hasval = True
                    break            
            
            if not hasval:    
                #--remove attributes from this element (if any)                       
                for key in root[-1].keys():
                    root[-1].attrib.popitem()  
                #--remove  subelements
                for n in root[-1][::-1]:
                    root[-1].remove(n)
                         
            #--add a new subelement
            root[-1].append(copy.deepcopy(node))            
            #--set the tag of this element equal to the first line entry
            #--and remove the text tag
            raw = line.strip().split()
            root[-1][-1].tag = raw[0]
            root[-1][-1].text='' 
            root[-1].text = node.text           
                        

            #--if this is the PI section, modify raw to conform
            if 'PRIOR' in root[-1].text.upper():
                temp = []
                temp.append(raw[0])
                temp.append(' '.join(raw[1:-2]))
                temp.extend(raw[-2:])
                raw = temp                                         
            p_list = pst_list[p_count]
            r_list = req_list[p_count]                     
                                   
            for pval,pitem,ritem in zip(raw,p_list,r_list):                                                              
                elem = root[-1][-1].find(pitem)
                if elem is not None:
                    elem.set('value',pval)
                else:                     
                     print line,p_list,node.tag
                     raise KeyError,'subelement '+pitem+\
                           ' not found under element '+\
                           root[-1].text                      
        l_count += 1                                                                                              
    f.close()
    #--to reconsile tied parameters
    root = check_tied(root)

    return root                                                           


def check_tied(root):
    '''deals tied parameters and cleans up the XML tree accordingly     
    '''

    #--first find any of the parameters that may have a
    #--a 'tied' partrans    
    p_idx = None    
    tied = []
    for i,section in enumerate(root):
        if 'PARAMETER DATA' in section.text.upper():
            p_idx = i
            for entry in section:                
                ptrans = entry.find('PARTRANS')
                parnme = entry.find('PARNME')                                
                if ptrans.attrib['value'].upper() == 'TIED':
                    tied.append(parnme.attrib['value'])
                    
    #--deal parmeter entries with 'tied' partrans                
    for t in tied:        
        #--t_junk stores the junk entry
        #--partied_value stores the true value of partied
        true_idx,junk_entry,partied_value = None,None,None
        for i,entry in enumerate(root[p_idx]):
            if entry.tag == t:
                partrans = entry.find('PARTRANS')
                if partrans.attrib['value'].upper() != 'TIED':
                    junk_entry = entry
                    partied_value = partrans.attrib['value']
                else:
                    true_idx = i 
        #--set partied for the correct entry
        root[p_idx][true_idx].find('PARTIED').attrib['value'] = partied_value
        #--set the mandatory flag
        root[p_idx][true_idx].find('PARTIED').attrib['mandatory'] = 'True'
        #--remove the junk entry
        root[p_idx].remove(junk_entry)                                                                                                                  
    return root


def xml2pst(fname,pst_list,rep_list):
    '''writes a PEST control file from an XML file
    special handling of the tied parameter mess

    '''
    #--load the XML tree
    tree = xml.parse(fname)
    pst = tree.getroot()    
    #--copy the pst_list and blank it out
    pstxml = copy.deepcopy(pst_list)
    for s in pstxml:
        for i,ss in enumerate(s):
            s[i] = '' 
    #--set the first entry
    pstxml[0][0] = 'pcf'        
    
    #--work through each section in the pst XML tree
    for section in pst:
        #--find this section marker in the pst_list           
        for i,p_list in enumerate(pst_list):                                    
            if p_list[0] == '*' and ' '.join(p_list) == section.text.strip():
                #print section.text.strip()
                pstxml[i] = p_list                
                break                                           
        #--check for tied parameters
        if 'PARAMETER DATA' in section.text.upper():
            partied_section = []            
            for entry in section:
                ptied = entry.find('PARTIED')         
                if 'value' in ptied.keys():
                    pname = entry.find('PARNME')         
                    partied_section.append([pname.attrib['value'],ptied.attrib['value']])
                    #--remove the partied value
                    entry.find('PARTIED').attrib['value'] = ''
        
        for elem in section:                        
            #--if this element has subelements
            #--then this is a repeatable section
            if len(elem) > 0:                                
                #--find the last occurence of a 
                #--match to all sub elements
                #--so we know where to insert it
                #--this maintains the ordering
                idx,sub_list = None,None
                c = 0 
                for ii,p_list in enumerate(pst_list):
                    match = True
                    for subelem in elem:                                                            
                        if subelem.tag not in p_list:                            
                            match = False
                            break
                    if match:                         
                        idx = ii
                        c += 1                        
                
                #--initialize a sub list
                #-- should use None, but empty strings make it easier to print later                                
                sub_list = [''] * len(pst_list[idx])
                #--populate the sublist
                for subelem in elem:                                                            
                    iidx = pst_list[idx].index(subelem.tag)                 
                    if 'value' in subelem.keys():
                        sub_list[iidx] = subelem.attrib['value']                            
                #--expensive inserts - no alternative - staying with unstructured
                pst_list.insert(idx,copy.deepcopy(pst_list[idx]))
                pstxml.insert(idx,copy.deepcopy(sub_list))                
            
            #--only use non-repeatable entries that have a value attribute
            elif 'value' in elem.attrib.keys():                                
                idx,iidx = None,None
                for ii,p_list in enumerate(pst_list):                    
                    if elem.tag in p_list:                                                                                              
                        idx = ii
                        iidx = p_list.index(elem.tag)
                        break                               
                if 'value' in elem.keys():
                    pstxml[idx][iidx] = elem.attrib['value']   
    #--insert tied parameter info (in any)
    #--find the index to insert tied parameters
    idx = None
    for i,p_list in enumerate(pst_list):
        if '*' in p_list and ' '.join(p_list).upper() == '* OBSERVATION GROUPS':
            idx = i
            break
    #--insert tied parameters data and text                   
    for pt_entry in partied_section:
         pst_list.insert(idx,['PARNME','PARTIED'])
         pstxml.insert(idx,pt_entry)   
         idx += 1                                                                  
    
    return pstxml

if __name__ == '__main__':

    #--load the text pest control file for par names
    pst,req,rep = loadpst('pst_base.dat')

    #--build an XML element tree
    pstxml = build_pstxml(pst,req)

    #--write out the empty tree
    indent(pstxml)
    xml.ElementTree(pstxml).write('test.xml')

    #--load a PST file into an element tree
    pstxml_var = pst2xml('this_tied.pst',pstxml,pst,req,rep)

    #--write out the populated tree
    indent(pstxml_var)
    xml.ElementTree(pstxml_var).write('test_var.xml')

    #--load the XML file into a nested list
    pst2 = xml2pst('test_var.xml',pst,rep)

    f = open('test.pst','w')
    for p2 in pst2:  
        #print p2
        #for pp2 in p2:
        #    if pp2.strip() != '':
        #        f.write(pp2+'  ')
        #f.write('\n')              
        if p2[0].strip() != '':
            f.write(' '.join(p2)+'\n')
    f.close()    