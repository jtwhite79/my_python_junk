#-------------------------------------------------------------------------------
#--some simple TSPROC input file generation helpers
#--stay with the dd/mm/yyyy format!

import os
import sys
import copy
#import datetime
from datetime import timedelta,datetime
import re


#--globals
SERIES = 'SERIES_NAME'
VTABLE = 'V_TABLE_NAME'
STABLE = 'S_TABLE_NAME'
CTABLE = 'C_TABLE_NAME'
ETABLE = 'E_TABLE_NAME'
PEST_CONTEXT = 'pest_prep'

DATE_FMT = '%d/%m/%Y'


#--some generic func
def write_date_file(file,start,end,interval):
    '''start and end are datetimes, interval is a timedelta
    '''
    stime = '00:01:00'
    etime = '00:00:00'
    sec = timedelta(minutes=1)
    fout = open(file,'w')  
    if interval == None:        
        start_string = (start+sec).strftime(DATE_FMT+' %H:%M:%S')
        end_string = end.strftime(DATE_FMT+' %H:%M:%S')        
        fout.write(start_string+' '+end_string+'\n')
        fout.close()
        return        
    else:    
        date = start
        while date <= end:        
            sdate = date
            edate = date + interval
            if edate >= end:
                break
            start_string = (sdate+sec).strftime(DATE_FMT+' %H:%M:%S')
            end_string = edate.strftime(DATE_FMT+' %H:%M:%S')                
            fout.write(start_string+' '+end_string+'\n')            
            date += interval
        fout.close()
        return



#def load_datefile(datefile):
#    dates,times = [],[]
#    try:
#        f = open(datefile,'r')
#        for line in f:
#            raw = line.strip().split()
#            dates.append([raw[0],raw[2]])
#            times.append([raw[1],raw[3]])
#        f.close()
#    except: pass
#    return dates,times

#def get_unique_ssf_obs(file):
#    unique = []
#    f = open(file,'r')
#    for line in f:
#        this_name = line.strip().split()[0]
#        if this_name not in unique:
#            unique.append(this_name)
#    f.close()
#    return unique



class base_block():
    def __init__(self,block_type,context,name,data_type,item_keys,\
                 item_vals,role,wght=None,max_min=None):
        #--check that the new series name is the accepted length
        assert len(name) <= 10,'new series name greater than 10 charaters: '+name
        if wght != None:
            assert role=='final', 'role must be final if wght != None:'+str(name)
            #assert context == pest_context
        if role == 'final' and context == PEST_CONTEXT and wght == None:
            print 'Warning -- assigning generic weight 1.0 for final pest '\
                  +data_type+' :'+str(name)
            wght = 1.0
        self.block_type = block_type.lower()
        self.context = context
        self.name = name.lower()
        self.data_type = data_type
        self.role = role
        self.wght = wght
        self.max_min = max_min
        
       
        #--check the num keys == num vals
        assert len(item_keys) == len(item_vals)
        self.item_keys = item_keys
        self.item_values = item_vals
    
    def __repr__(self):
        string = 'block_type:'+self.block_type
        string += ',context:'+self.context
        string += ',name:'+self.name
        string += ',data_type:'+self.data_type
        string += ',role:'+self.role
        string += ',wght:'+str(self.wght)
        string += ',max_min:'+str(self.max_min)
        
        return string

    
    def write_entry(self,f_obj):
        if not self.block_type.startswith('*'):
            f_obj.write('\nSTART '+self.block_type+'\n')
            f_obj.write(' CONTEXT '+self.context+'\n')
            for idx in range(len(self.item_keys)):
                f_obj.write(' '+self.item_keys[idx].lower()+' '+\
                            str(self.item_values[idx])+'\n')
            f_obj.write('END '+self.block_type+'\n')
        return  
    
    def copy(self):
        return copy.deepcopy(self)


class tsproc(base_block):    
    #-----------------------------------
    #--general class methods
    def __init__(self,tsproc_file,out_file='tsproc.out',out_fmt='short',\
                 instances=[],context=PEST_CONTEXT):       
        self.tsproc_file = tsproc_file
        self.out_file = out_file 
        self.out_fmt = out_fmt
        self.context = context
               
        #--a list of block objects
        self.blocks = []
        #--a list of block ids
        self.block_operations = []
        
        #--a list of the last blocks operated on
        #self.last_blocks = []
        
        #--for adding in multiple instances of tsproc objects
        i_count = 1
        for i in instances:
            self.add(i,prefix=str(i_count))
                           
        #--a flag for writing pest input files
        self.pest = False                                   
    
        #--a counter for generic file name needs
        self.fcount = 1

    def copy_blocks(self,existing_blocks,prefix,block_operation='copy',\
                    context='all'):
        new_blocks = []
        for block in existing_blocks:
            new_name = prefix+block.name
            self.check_name(new_name)
            new_block = block.copy()
            setattr(new_block,'name',new_name)
            setattr(new_block,'context',context)
            #--check for any values that contain the block name and change them                        
            item_values = getattr(new_block,'item_values')            
            for idx in range(len(item_values)):
                try:
                    if re.search(block.name,item_values[idx],re.IGNORECASE) != None:
                        item_values[idx] = prefix + item_values[idx]
                except:
                    pass
            setattr(new_block,'item_values',item_values)                                
            self.blocks.append(new_block)
            new_blocks.append(new_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)            
            self.block_operations.append(this_op) 
        return new_blocks
            
    
    
    def add_blocks(self,object_instance,prefix='',block_operations=''):        
        #--method to add object instances
        #--checks names for duplication
        #print len(object_instance.blocks),len(object_instance.block_operations)
        new_blocks = []
        for b_idx in range(len(object_instance.blocks)):
            new_name = prefix + object_instance.blocks[b_idx].name + block_operation
            #print new_name
            self.check_name(new_name)
            object_instance.blocks[b_idx].name = new_name
            self.blocks.append(object_instance.blocks[b_idx])
            new_blocks.append(object_instance.blocks[b_idx])
            self.block_operations.extend(object_instance.block_operations[b_idx])                                 
        return new_blocks
        
    def add_existing_blocks(self,blocks,block_operations=[]):
        new_blocks = []
        for i,b in enumerate(blocks):
            #if b.name != '':
            #    self.check_name(b.name)
            self.blocks.append(b)
            new_blocks.append(b)
            if len(block_operations) == len(blocks):
                self.block_operations.append(block_operations[i])
        return new_blocks
    
    def num_blocks(self):
        return len(self.blocks)        
    
    def get_contexts(self):
        contexts = []
        for block in self.blocks:
            if block.context not in contexts:
                contexts.append(block.context)
        return contexts
    
    def set_context(self,context):
        self.context = context

    def get_block_index(self,name):
        for b_idx in range(self.num_blocks()):
            if self.blocks[b_idx].name == name:
                return b_idx
        return None            
    
            
    def get_block_operations(self):        
        return self.block_operations
       
    def get_blocks(self,existing_blocks=None,operations=None,name=None,dtype=None,role=None):
        #--method used to 1.)get all blocks, 2.)get a list of blocks with the same ID
        #-- 3.) get a specific block by name, or 4.)get a list of blocks with the same dtype
        if existing_blocks == None:
            existing_blocks = self.blocks
        
        if operations != None:
            if not isinstance(operations,list):
                operations = [operations]
            blocks = []
            for b_idx in range(self.num_blocks()):
                this_block_op = self.block_operations[b_idx]
                match = True
                for op in operations:
                    #print this_block_op,op
                    
                    if op not in this_block_op:
                        match = False                        
                if match == True:
                    blocks.append(self.blocks[b_idx])
            return blocks
        elif name != None:
            for block in existing_blocks:                
                if block.name.lower() == name.lower():
                    return block
            return None
        elif dtype != None:
            blocks = []
            for block in existing_blocks:
                if block.data_type.lower() == dtype.lower():
                    blocks.append(block)
            return blocks 
        elif role != None:
            blocks = []
            for block in existing_blocks:
                if block.role.lower() == role.lower():
                    blocks.append(block)
            return blocks            
        else:
            return copy.deepcopy(existing_blocks)                    
    
    
    def name_exists(self,name):
        if self.get_blocks(name=name) != None:
            return True
        else:
            return False            
            
    def check_name(self,name):
        if self.name_exists(name):            
            raise TypeError('Error - existing series with name '+str(name))         

    def get_name(self,name,suffix):
        #if len(name) == 10:
        #    new_name = name[:-2] + suffix
        #elif len(name) == 9:
        #    new_name = name[:-1] + suffix
        #else:
        #    new_name = name + suffix
        new_name = name[:-2] + suffix
        try:
            self.check_name(new_name)
        except:
            new_name = name[:-3]+str(self.fcount)+suffix
            self.check_name(new_name)
            self.fcount += 1
        return new_name                                              
    
    #-----------------------------------
    #--load series blocks 
    #--add an 'or' block_operation   
    def get_series_ssf(self,site_list,ssf_file,context='all',prefix='',\
                       block_operation='get_series_ssf',role='intermediate',\
                       wght=None,max_min=None,series_list=None):        
        
        suffix = 'or'
        if series_list == None:
            series_list = []
            for site in site_list:
                series_list.append(prefix+site+suffix)
        else:
            assert len(site_list) == len(series_list)
        

        this_item_keys = ['FILE','SITE','NEW_SERIES_NAME']
        new_blocks = []
        for site,series_name in zip(site_list,series_list):                       
            self.check_name(series_name)                            
            this_item_values = [ssf_file,site,series_name]           
            this_block = base_block('GET_SERIES_SSF',context,\
                                         series_name,SERIES,this_item_keys,\
                                         this_item_values,role,wght=wght,
                                         max_min=max_min)

            self.blocks.append(this_block)
            new_blocks.append(this_block)
            self.block_operations.append([block_operation])
        return new_blocks            
                  

    def get_mul_series_ssf(self,site_list,ssf_file,context='all',prefix='',\
                       block_operation='get_series_ssf',role='intermediate',\
                       wght=None,max_min=None,series_list = None,suffix='or'):        
                
        if series_list == None:
            series_list = []
            for site in site_list:
                series_list.append(prefix+site+suffix)
        else:
            assert len(site_list) == len(series_list)
        this_item_keys = ['FILE']        
        this_item_values = [ssf_file] 
        dummy_blocks = []                  
        for site,series_name in zip(site_list,series_list):           
            self.check_name(series_name)                          
            this_item_keys.extend(['SITE','NEW_SERIES_NAME'])
            this_item_values.extend([site,series_name])           
            this_block = base_block('**DUMMY**',context,\
                                         series_name,SERIES,['dummy'],\
                                         ['dummy'],'intermediate',wght=wght,
                                         max_min=max_min)                    
            dummy_blocks.append(this_block)
            self.blocks.append(this_block)            
            self.block_operations.append([block_operation])
        this_block = base_block('GET_MUL_SERIES_SSF',context,\
                                         'get_mul',SERIES,this_item_keys,\
                                         this_item_values,role,wght=wght,
                                         max_min=max_min)
        self.blocks.append(this_block)        
        self.block_operations.append([block_operation])
        return dummy_blocks        

       
    #--need to convert to datetime usage   
    #def get_series_swr(self,rchgrp_list,swr_data_type,bin_file_name,\
    #                        start_date,series_name_list=None,\
    #                        start_time='00:00:00',context='all',\
    #                        block_operation='get_series_swr',\
    #                        role='intermediate',prefix='',wght=None,
    #                        max_min=None):
    #    #--check that atleast the start_date contains '/'
    #    assert len(start_date.split('/')) == 3
    #    
    #    if series_name_list != None:
    #        assert len(rchgrp_list) == len(series_name_list), \
    #               'reachgroup list != series_name_list'
    #                               
    #    suffix = 'or'
    #    
    #    this_item_keys = ['FILE','REACH_GROUP_NUMBER','DATA_TYPE',\
    #                      'DATE_1','TIME_1','NEW_SERIES_NAME']
    #    
    #    
    #    new_blocks = []
    #    for idx in range(len(rchgrp_list)):
    #        if series_name_list == None:
    #            if int(rchgrp_list[idx]) != -999:
    #                this_series_name = prefix+swr_data_type[:2]+\
    #                                   str(rchgrp_list[idx])+suffix
    #            else:
    #                 this_series_name = prefix+swr_data_type[:2]+\
    #                                   'all'+suffix
    #        else:
    #            this_series_name = series_name_list[idx]
    #        
    #        self.check_name(this_series_name)               
    #        
    #        this_item_values = [bin_file_name,str(rchgrp_list[idx]),\
    #                            swr_data_type,start_date,start_time,\
    #                            this_series_name]
    #        this_block = base_block('GET_SERIES_SWR',context,this_series_name,\
    #                                SERIES,this_item_keys,this_item_values,role,
    #                                wght=wght,max_min=max_min)
    #        self.blocks.append(this_block)
    #        new_blocks.append(this_block)
    #        self.block_operations.append([block_operation])
    #    return new_blocks
    
    
    
    def get_mul_series_swr(self,rchgrp_list,swr_data_type,bin_file_name,\
                            start_dt,series_name_list=None,swr_file_type='flow',\
                            context='all',\
                            block_operation='get_mul_series_swr',\
                            role='intermediate',prefix='',wght=None,
                            max_min=None):
        
        start_date = start_dt.strftime(DATE_FMT)
        start_time = start_dt.strftime('%H:%M:%S')

        if series_name_list != None:
            assert len(rchgrp_list) == len(series_name_list), \
                   'reachgroup list != series_name_list'
                                   
        suffix = 'or'
        if swr_file_type == 'flow':
            this_item_keys = ['FILE','DATA_TYPE','FILE_TYPE',\
                          'DATE_1','TIME_1']
            this_item_values = [bin_file_name,swr_data_type,swr_file_type,start_date,\
                            start_time]                            
        elif swr_file_type == 'stage':
            this_item_keys = ['FILE','FILE_TYPE',\
                          'DATE_1','TIME_1']
            this_item_values = [bin_file_name,swr_file_type,start_date,\
                            start_time]                       
        block_name = 'mul_swr'
        
        new_blocks = []
        for idx in range(len(rchgrp_list)):
            if series_name_list == None:
                if int(rchgrp_list[idx]) != -999:
                    this_series_name = prefix+swr_data_type[:2]+\
                                       str(rchgrp_list[idx])+suffix
                else:
                     raise TypeError,'accumulated reach group flows not'+\
                                    ' supported in GET_MUL_SWR_SERIES'
            else:
                this_series_name = series_name_list[idx]
            
            self.check_name(this_series_name)               
            this_item_keys.extend(['ITEM_NUMBER','NEW_SERIES_NAME'])                          
            
            this_item_values.extend([str(rchgrp_list[idx]),this_series_name])
            
            #--create dummy blocks for each series                     
            this_block = base_block('**DUMMY**',context,this_series_name,\
                                    SERIES,this_item_keys,this_item_values,role,
                                    wght=None,max_min=None)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            self.block_operations.append([block_operation])
        
        #--create the actual block that will be written
        this_block = base_block('GET_MUL_SERIES_SWR',context,block_name,\
                                SERIES,this_item_keys,this_item_values,'intermediate',
                                wght=wght,max_min=max_min)             
        
        self.blocks.append(this_block)    
        self.block_operations.append([block_operation])                           
        #--don't return the actual written block, only the dummy blocks
        return new_blocks
                    
    
    def new_series_uniform(self,series_names,start_dt,end_dt,interval=1,suffix='un',\
                            units='days',value=-999,role='intermediate',\
                            wght=None,max_min=None,block_operation='new_series_uniform',context='all'):
        item_keys = ['NEW_SERIES_NAME','DATE_1','TIME_1','DATE_2','TIME_2','TIME_INTERVAL','TIME_UNIT','NEW_SERIES_VALUE']
        item_vals = ['junk',start_dt.strftime(DATE_FMT),start_dt.strftime('%H:%M:%S'),end_dt.strftime(DATE_FMT),end_dt.strftime('%H:%M:%S'),interval,units,value]
        new_blocks = []        
        for name in series_names:
            name = name[:-2] + suffix   
            item_vals[0] = name
            this_block = base_block('NEW_SERIES_UNIFORM',context,name,SERIES,item_keys,item_vals,role,wght=wght,max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            self.block_operations.append([block_operation])    
        return new_blocks


    def new_series_uniform_like(self,like_series_blocks,constant_list,\
                           context='all',block_operation='new_series_uniform',\
                           suffix='ul',role='intermediate',wght=None,\
                           max_min=None):       
        this_item_keys = ['LIKE_SERIES','NEW_SERIES_NAME','CONSTANT']
        new_blocks = []
        for b_idx in range(len(like_series_blocks)):
            this_like_block = like_series_blocks[b_idx]         
            #--check that this like block exists
            if self.name_exists(this_like_block.name) == False:
                print 'like series block does not exist:'+\
                                  this_like_block.name 
                raise IndexError
            #print this_like_block.name,constant_list[b_idx]
            this_series_name = constant_list[b_idx]+suffix    
            this_item_values = [this_like_block.name,this_series_name,\
                                constant_list[b_idx]]                        
            self.check_name(this_series_name)
            this_block = base_block('NEW_SERIES_UNIFORM',context,\
                                    this_series_name,SERIES,this_item_keys,\
                                    this_item_values,role,wght=wght,\
                                    max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            self.block_operations.append([block_operation])
        return new_blocks                                                            
    
    def get_constants(self,file_name,block_name='constant',context='all',\
                      block_operation='get_constants',):
       #--role cannot be final
       role='intermediate'
       self.check_name(block_name)
       this_item_keys = ['FILE']
       this_item_values = [file_name]
       this_block = base_block('GET_CONSTANTS',context,block_name,\
                               None,this_item_keys,this_item_values,\
                               role,wght=None)
       self.blocks.append(this_block)
       self.block_operations.append([block_operation])
       return this_block
                    
    
    #-----------------------------------
    #--manipulate series blocks
    #--manipulate blocks add a block_operation to the series name
   


    def lowpass_filter(self,existing_blocks,cutoff,block_operation='lowpass',\
                           context='all',wght=None,max_min=None,suffix='lp',\
                           role='intermediate'):
        this_item_keys = ['FILTER_TYPE','SERIES_NAME','NEW_SERIES_NAME',\
                          'CUTOFF_FREQUENCY','FILTER_PASS','STAGES','REVERSE_SECOND_STAGE']
        new_blocks = []
        for block in existing_blocks:
            this_series_name = self.get_name(block.name,suffix)            
            assert block.data_type == SERIES
            self.check_name(this_series_name)            
            this_item_vals = ['butterworth',block.name,this_series_name,\
                                cutoff,'low','2','yes']
            this_block = base_block('DIGITAL_FILTER',context,this_series_name,SERIES,\
                                    this_item_keys,this_item_vals,role,wght=wght,max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)             
            self.block_operations.append(this_op)
        return new_blocks                                                     
 


    def baseflow_filter(self,existing_blocks,block_operation='digital_filter',\
                        alpha=0.9,passes=1,clip_input='no',clip_zero='no',\
                        context='all',wght=None,max_min=None,suffix='df',
                        role='intermediate'):
        
        this_item_keys = ['FILTER_TYPE','SERIES_NAME','NEW_SERIES_NAME',\
                          'ALPHA','PASSES','CLIP_INPUT','CLIP_ZERO']
        new_blocks = []
        for block in existing_blocks:
            this_series_name = self.get_name(block.name,suffix)            
            assert block.data_type == SERIES
            self.check_name(this_series_name)            
            this_item_vals = ['baseflow_separation',block.name,this_series_name,\
                                alpha,passes,clip_input,clip_zero]
            this_block = base_block('DIGITAL_FILTER',context,this_series_name,SERIES,\
                                    this_item_keys,this_item_vals,role,wght=wght,max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)             
            self.block_operations.append(this_op)
        return new_blocks                                                     
 
   

    def reduce_time_like(self,existing_blocks,like_blocks,\
                         block_operation='reduce_time_like',\
                         context='all',role='intermediate',\
                         wght=None,max_min=None,suffix='rl'):
        
        this_item_keys = ['SERIES_NAME','NEW_SERIES_NAME','LIKE_SERIES_NAME']
        assert len(existing_blocks) == len(like_blocks)
        new_blocks = []
        for block,like_block in zip(existing_blocks,like_blocks):            
            assert block.data_type == SERIES
            assert like_block.data_type == SERIES
            this_series_name = self.get_name(block.name,suffix)
            self.check_name(this_series_name)
            this_item_values = [block.name,this_series_name,\
                                like_block.name]                                                                           
            this_block = base_block('REDUCE_TIME_SPAN',context,\
                                    this_series_name,SERIES,this_item_keys,\
                                    this_item_values,role,wght=wght,\
                                    max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)            
            self.block_operations.append(this_op) 
        return new_blocks            
                                    
    
    def reduce_time(self,existing_blocks,start_dt,\
                    block_operation='reduce_time'\
                    ,context='all',role='intermediate',wght=None,\
                    max_min=None,end_dt=None,\
                    suffix = 'rd'):                
        
        start_date = start_dt.strftime(DATE_FMT)
        start_time = start_dt.strftime('%H:%M:%S')
        
        

        this_item_keys = ['SERIES_NAME','NEW_SERIES_NAME',\
                          'DATE_1','TIME_1']
        if end_dt != None:            
            end_date = end_dt.strftime(DATE_FMT)
            end_time = end_dt.strftime('%H:%M:%S')
            this_item_keys.append('DATE_2')                         
            this_item_keys.append('TIME_2')
        new_blocks = []
        for block in existing_blocks:
            
            this_series_name = self.get_name(block.name,suffix)            
            assert block.data_type == SERIES
            self.check_name(this_series_name)            
            this_item_values = [block.name,this_series_name,\
                                start_date,start_time]
            if end_dt != None:
                end_date = end_dt.strftime(DATE_FMT)
                end_time = end_dt.strftime('%H:%M:%S')
                this_item_values.append(end_date)                                
                this_item_values.append(end_time)
            this_block = base_block('REDUCE_TIME_SPAN',context,this_series_name,\
                                    SERIES,this_item_keys,this_item_values,role,\
                                    wght=wght,max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)             
            self.block_operations.append(this_op)
        return new_blocks            
                
     
    def volume_calc(self,existing_blocks,datefile,units='days',\
                    block_operation='volume_calc',context='all',\
                    role='intermediate',wght=None,suffix='vl',\
                    max_min=None):
        #--check that atleast a file exists
        assert os.path.exists(datefile) == True            
        this_item_keys = ['SERIES_NAME','NEW_V_TABLE_NAME','FLOW_TIME_UNITS'\
                          ,'DATE_FILE']
        new_blocks = []                          
        for block in existing_blocks:
            this_vtable_name = self.get_name(block.name,suffix)
            assert block.data_type == SERIES
            self.check_name(this_vtable_name)
            this_item_values = [block.name,this_vtable_name,units,datefile]
            this_block = base_block('VOLUME_CALCULATION',context,this_vtable_name,\
                                    VTABLE,this_item_keys,this_item_values,role,\
                                    wght=wght,max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)            
            self.block_operations.append(this_op)      
        return new_blocks                                                       


    def drawdown(self,existing_blocks,datefile,reference=True,first=False,\
                 block_operation='drawdown',context='all',role='intermediate',
                 wght=None,max_min=None,suffix='dd'):
        #--check that atleast a file exists
        assert os.path.exists(datefile) == True         
        this_item_keys = ['SERIES_NAME','DATE_FILE','NEW_SERIES_NAME',\
                          'INCLUDE_FIRST','REFERENCE_TO_FIRST']   
        ref_value = 'no'
        if reference:
            ref_value = 'yes'
        
        first_value = 'no'
        if first:
            first_value = 'yes'
        new_blocks = []
        for block in existing_blocks:
            this_series_name = self.get_name(block.name,suffix)
            assert block.data_type == SERIES
            self.check_name(this_series_name)
            this_item_values = [block.name,datefile,this_series_name,\
                                first_value,ref_value]
            this_block = base_block('SERIES_BLOCK_DRAWDOWN',context,this_series_name,\
                                    SERIES,this_item_keys,this_item_values,role,\
                                    wght=wght,max_min=max_min)
            
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)            
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)            
            self.block_operations.append(this_op)     
        return new_blocks             
         
        
    def statistics(self,existing_blocks,operation_list,\
                   date_time_list=None,block_operation='statistics',\
                   context='all',role='intermediate',wght=None,\
                   max_min=None):
        this_item_keys = ['SERIES_NAME','NEW_S_TABLE_NAME']
        this_item_keys.extend(operation_list)
        suffix = 'st'
        new_blocks = []
        for block in existing_blocks:
            assert block.data_type == SERIES
            
            if date_time_list == None:
                this_stable_name = block.name[:-2]+suffix
                
                self.check_name(this_stable_name)
                this_item_values = [block.name,this_stable_name]
                for op in operation_list:
                    this_item_values.append('yes')
                this_block = base_block('SERIES_STATITICS',context,\
                                        this_stable_name,STABLE,\
                                        this_item_keys,this_item_values,role,\
                                        wght=wght,max_min=max_min)
                                
                self.blocks.append(this_block)
                new_blocks.append(this_block)
                this_block_index = self.get_block_index(block.name)
                this_op = copy.deepcopy(self.block_operations[this_block_index])
                this_op.append(block_operation)            
                self.block_operations.append(this_op) 
                
               
                
            #--if date_time_list 
            if date_time_list != None:
                dt_count = 1
                              
                this_item_keys_cpy = copy.deepcopy(this_item_keys)
                this_item_keys_cpy.extend(['DATE_1','TIME_1','DATE_2','TIME_2'])
                for dt_idx in range(len(date_time_list[0])):
                    this_stable_name = self.get_name(block.name,suffix)+str(dt_count)
                    self.check_name(this_stable_name)
                    this_item_values = [block.name,this_stable_name]
                    for op in operation_list:
                        this_item_values.append('yes')  
                    this_item_values.extend([date_time_list[0][dt_idx][0],\
                                             date_time_list[1][dt_idx][0],\
                                             date_time_list[0][dt_idx][1],\
                                             date_time_list[1][dt_idx][1]])                     
                    this_block = base_block('SERIES_STATITICS',context,\
                                            this_stable_name,STABLE,\
                                            this_item_keys_cpy,\
                                            this_item_values,role,wght=wght,\
                                            max_min=max_min)
                                    
                    self.blocks.append(this_block)
                    new_blocks.append(this_block)
                    this_block_index = self.get_block_index(block.name)
                    this_op = copy.deepcopy(self.block_operations[this_block_index])
                    this_op.append(block_operation)            
                    self.block_operations.append(this_op)      
                    
                    dt_count += 1   
            return new_blocks
   
    def sum_2_series(self,existing_blocks_1,existing_blocks_2,\
                        block_operation='add_2_series'\
                        ,context='all',role='intermediate',wght=None,\
                        max_min=None):
        #--a wrapper for series equation                                            
        assert len(existing_blocks_1) == len(existing_blocks_2)                     
        suffix = 'qs'                                                               
        new_blocks = []
        for b_idx in range(len(existing_blocks_1)):                                 
            this_equation = existing_blocks_1[b_idx].name +' + ' + \
                            existing_blocks_2[b_idx].name                           
            this_series_name = existing_blocks_1[b_idx].name[:-2]+suffix            
            self.check_name(this_series_name)                                       
            assert existing_blocks_1[b_idx].data_type == SERIES                     
            assert existing_blocks_2[b_idx].data_type == SERIES                     
            this_block =self.__series_equation(this_equation,existing_blocks_1[b_idx].name,\
                                 this_series_name,context,block_operation,\
                                 role,wght,max_min)
            new_blocks.append(this_block)
        return new_blocks          
    
    def mult_2_series(self,existing_blocks_1,existing_blocks_2,\
                        block_operation='mult_2_series'\
                        ,context='all',role='intermediate',wght=None,\
                        max_min=None):
        #--a wrapper for series equation                                            
        assert len(existing_blocks_1) == len(existing_blocks_2)                     
        suffix = 'qm' 
        new_blocks = []                                                              
        for b_idx in range(len(existing_blocks_1)):                                 
            this_equation = existing_blocks_1[b_idx].name +' * ' + \
                            existing_blocks_2[b_idx].name                           
            this_series_name = existing_blocks_1[b_idx].name[:-2]+suffix            
            self.check_name(this_series_name)                                       
            assert existing_blocks_1[b_idx].data_type == SERIES                     
            assert existing_blocks_2[b_idx].data_type == SERIES                     
            this_block = self.__series_equation(this_equation,existing_blocks_1[b_idx].name,\
                                 this_series_name,context,block_operation,\
                                 role,wght,max_min)
            new_blocks.append(this_block)
        return new_blocks            
    
   
    def difference_2_series(self,existing_blocks_1,existing_blocks_2,\
                            block_operation='difference_2_series'\
                            ,context='all',role='intermediate',wght=None,\
                            max_min=None,suffix='qf'):   
        #--a wrapper for series equation
        assert len(existing_blocks_1) == len(existing_blocks_2)        
        new_blocks = []
        for b_idx in range(len(existing_blocks_1)):
            this_equation = existing_blocks_1[b_idx].name +' - ' + \
                            existing_blocks_2[b_idx].name
            this_series_name = existing_blocks_1[b_idx].name[:-2]+suffix
            self.check_name(this_series_name)
            assert existing_blocks_1[b_idx].data_type == SERIES
            assert existing_blocks_2[b_idx].data_type == SERIES
            this_block = self.__series_equation(this_equation,existing_blocks_1[b_idx].name,\
                                 this_series_name,context,block_operation,role,wght,\
                                 max_min)
            new_blocks.append(this_block)
        return new_blocks                                             
    
    def accumulate_2_first(self,existing_blocks,\
                                  block_operation='accumulate_2_first',\
                                  context='all',role='intermediate',wght=None,\
                                  final_series_name=None,max_min=None):
        #--a wrapper for series equation
        suffix = 'ac'
        accum_block = existing_blocks[0]  
        if final_series_name == None:                                     
            final_series_name = accum_block.name[:-2] + suffix                 
        #print final_series_name
        self.check_name(final_series_name)
        
        #--accumulate all but the last block with an fixed intermediate role
        new_blocks = []
        for b_idx in range(1,len(existing_blocks)-1):
            this_equation = accum_block.name + ' + ' +\
                            existing_blocks[b_idx].name
            this_block = self.__series_equation(this_equation,accum_block.name,'',context,\
                                 block_operation,'intermediate',wght,max_min)
            new_blocks.append(this_block)                                 
        #--now accumulate the last block with a (potentially) final role               
        this_equation = accum_block.name + ' + ' +\
                        existing_blocks[-1].name                       
        this_block = self.__series_equation(this_equation,accum_block.name,final_series_name,context,\
                             block_operation,role,wght,max_min)
        new_blocks.append(this_block)
        return new_blocks                             
                             
    
    def copy_2_series(self,existing_blocks,new_names,block_operation='copy',\
                      context='all',role='intermediate',wght=None,maxmin=None,suffix=''):
        new_blocks = []
        assert len(new_names) == len(existing_blocks),'the list of new names is not the same length as the existing blocks list'
        for block,new_name in zip(existing_blocks,new_names):
            #print block
            assert block.data_type == SERIES,block.name+' is not a series'
            this_series_name = new_name + suffix
            #if wght != None:
            #    if wght == 'other':
            #        this_wght = block.wght
            #    else:
            #        this_wght = wght
            #if maxmin != None:
            #    if wght == 'other':
            #        this_maxmin = block.max_min
            #    else:
            #        this_maxmin = maxmin
            #print this_wght
            self.check_name(this_series_name)
            this_block = self.__series_equation(block.name,block.name,this_series_name,\
                                  context,block_operation,role,wght,maxmin)
            new_blocks.append(this_block)
        return new_blocks    
                             
                                                
    def __series_equation(self,equation,existing_series_name,\
                            new_series_name,context,block_operation,role,wght,\
                            max_min):
        #--a private method that is only access by member methods
        if new_series_name != '':
            this_item_keys = ['NEW_SERIES_NAME','EQUATION']
            this_item_values = [new_series_name,equation]
        else:
            this_item_keys = ['IN_PLACE','EQUATION']
            this_item_values = ['yes',equation]
        #print equation
        this_block = base_block('SERIES_EQUATION',context,\
                                new_series_name,SERIES,this_item_keys,\
                                this_item_values,role,wght=wght,max_min=max_min)
        
        self.blocks.append(this_block)
        this_block_index = self.get_block_index(existing_series_name)
        this_op = copy.deepcopy(self.block_operations[this_block_index])
        this_op.append(block_operation)            
        self.block_operations.append(this_op) 
        return this_block     

       
        
    def series_avg(self,existing_blocks,datefile,sample_time='middle',\
                   block_operation='series_average',context='all',\
                   role='intermediate',suffix='av',wght=None,\
                   max_min=None):
        assert os.path.exists(datefile),'file does not exist:'+datefile
        this_item_keys = ['SERIES_NAME','NEW_SERIES_NAME','DATE_FILE',\
                          'SAMPLE_TIME']
        new_blocks = []
        for block in existing_blocks:
            this_series_name = self.get_name(block.name,suffix)
            assert block.data_type == SERIES
            self.check_name(this_series_name)
            this_item_values = [block.name,this_series_name,\
                                datefile,sample_time]                                                                           
            this_block = base_block('SERIES_TIME_AVERAGE',context,\
                                    this_series_name,SERIES,this_item_keys,\
                                    this_item_values,role,wght=wght,\
                                    max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)            
            self.block_operations.append(this_op)      
        return new_blocks
    
    def new_time_base(self,existing_blocks,time_base_blocks,context='all',\
                      block_operation='new_time_base',suffix='tb',\
                      role='intermediate',wght=None,max_min=None):
    
        this_item_keys = ['SERIES_NAME','NEW_SERIES_NAME','TB_SERIES_NAME']
        new_blocks = []
        if len(existing_blocks) == len(time_base_blocks):
            for block,tb_block in zip(existing_blocks,time_base_blocks):                            
                assert block.data_type == SERIES
                assert tb_block.data_type == SERIES
                this_series_name = self.get_name(block.name,suffix)                   
                self.check_name(this_series_name)        
                this_item_values = [block.name,this_series_name,\
                                tb_block.name]                                                                           
                this_block = base_block('NEW_TIME_BASE',context,\
                                        this_series_name,SERIES,this_item_keys,\
                                        this_item_values,role,wght=wght,\
                                        max_min=max_min)
                self.blocks.append(this_block)
                new_blocks.append(this_block)
                this_block_index = self.get_block_index(block.name)
                this_op = copy.deepcopy(self.block_operations[this_block_index])
                this_op.append(block_operation)            
                self.block_operations.append(this_op)   
        else:
           for idx in range(len(existing_blocks)):
                block = existing_blocks[idx]
                tb_block = time_base_blocks[0]
                assert block.data_type == SERIES
                assert tb_block.data_type == SERIES
                this_series_name = self.get_name(block.name,suffix)                   
                self.check_name(this_series_name)        
                this_item_values = [block.name,this_series_name,\
                                tb_block.name]                                                                           
                this_block = base_block('NEW_TIME_BASE',context,\
                                        this_series_name,SERIES,this_item_keys,\
                                        this_item_values,role,wght=wght,\
                                        max_min=max_min)
                self.blocks.append(this_block)
                new_blocks.append(this_block)
                this_block_index = self.get_block_index(block.name)
                this_op = copy.deepcopy(self.block_operations[this_block_index])
                this_op.append(block_operation)            
                self.block_operations.append(this_op)    
        return new_blocks                                               
                                   
    def displace_constant(self,existing_blocks,constants,fill_value=0.0,\
                          block_operation='displace_constant',context='all',\
                          suffix='dp',role='intermediate',wght=None,max_min=None):
        
        this_item_keys = ['SERIES_NAME','NEW_SERIES_NAME','CONSTANT_NAME','FILL_VALUE']
        assert len(existing_blocks) == len(constants)
        new_blocks = []
        for idx in range(len(existing_blocks)):
            block = existing_blocks[idx]
            this_series_name = self.get_name(block.name,suffix)
            assert block.data_type == SERIES
            self.check_name(this_series_name)
            this_item_values = [block.name,this_series_name,\
                                constants[idx],fill_value]                                                                           
            this_block = base_block('SERIES_DISPLACE_CONSTANT',context,\
                                    this_series_name,SERIES,this_item_keys,\
                                    this_item_values,role,wght=wght,\
                                    max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)            
            self.block_operations.append(this_op)      
        return new_blocks    
    
        
    def vol_2_series(self,existing_blocks,time_absc='start',\
                     block_operation='vol_2_series',context='all'\
                     ,suffix='vs',role='intermediate',wght=None,\
                     max_min=None):
        this_item_keys = ['NEW_SERIES_NAME','V_TABLE_NAME','TIME_ABSCISSA']
        new_blocks = []
        for block in existing_blocks:
            assert block.data_type == VTABLE
            this_series_name = self.get_name(block.name,suffix)
            self.check_name(this_series_name)
            this_item_values = [this_series_name,block.name,time_absc]
            this_block = base_block('V_TABLE_TO_SERIES',context,\
                                    this_series_name,SERIES,this_item_keys,\
                                    this_item_values,role,wght,\
                                    max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            #print this_block_index,self.block_operations[this_block_index]
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)            
            self.block_operations.append(this_op) 
        return new_blocks                
            
           
    def exceedence_time(self,existing_blocks,time_units,flows,\
                        block_operation='exceedence_time',under_over='over',\
                        context='all',suffix='ex',role='intermediate',wght=None,\
                        max_min=None,delays=None):
        
        if delays != None:
            assert len(delays) == len(flows)
               
        this_item_keys = ['SERIES_NAME','NEW_E_TABLE_NAME','EXCEEDENCE_TIME_UNITS','UNDER_OVER'] 
        flow_delay = []
        for f in flows:
            this_item_keys.append('FLOW')
            flow_delay.append(f)
            if delays != None:
                this_item_keys.append('DELAY')
                flow_delay.append(delay[flows.index(f)])
        
        new_blocks = []
        for block in existing_blocks:
            assert block.data_type == SERIES
            this_series_name = self.get_name(block.name,suffix)
            self.check_name(this_series_name)
            this_item_values = [block.name,this_series_name,time_units,under_over]
            this_item_values.extend(flow_delay)
            this_block = base_block('EXCEEDENCE_TIME',context,this_series_name,\
                                    ETABLE,this_item_keys,this_item_values,\
                                    role,wght,max_min=max_min)
            self.blocks.append(this_block)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            this_op = copy.deepcopy(self.block_operations[this_block_index])
            this_op.append(block_operation)
            self.block_operations.append(this_op)                                    
        return new_blocks                
        
                
                
                                                   
                                    
    
    
    #-----------------------------------
    #--release blocks
    def erase_entity(self,existing_blocks,context='all',role='None'):        
        new_blocks = []
        for block in existing_blocks:
            assert block.role.lower() != 'final',\
                'Cannot erase_entity for a \'final\' role block'
            this_item_keys = [block.data_type]
            this_item_values = [block.name]
            this_block = base_block('ERASE_ENTITY',context,'','',\
                                    this_item_keys,this_item_values,role)
            new_blocks.append(this_block)
            this_block_index = self.get_block_index(block.name)
            self.blocks.pop(this_block_index)
            self.block_operations.pop(this_block_index)                                    
        return new_blocks            
           
                  
    #-----------------------------------
    #--writing methods
    def write_blocks(self):
        for block in self.blocks:
            block.write_entry(self.f_obj)
        return
                
    def write_settings(self):
        self.f_obj.write('\nSTART SETTINGS\n')
        #contexts = self.get_contexts()
        #if len(contexts) > 1:
        #    for context in contexts:
        #        if context == PEST_CONTEXT:
        #            self.f_obj.write(' CONTEXT '+context+'\n')
        #        else:
        #            self.f_obj.write('#CONTEXT '+context+'\n')    
        #else:
        #     self.f_obj.write(' CONTEXT '+contexts[0]+'\n')    
        self.f_obj.write(' CONTEXT '+self.context+'\n')    
        if DATE_FMT == '%d/%m/%Y':
            dfmt = 'dd/mm/yyyy'
        elif DATE_FMT == '%m/%d/%Y':            
            dfmt = 'mm/dd/yyyy'
        else:
            raise TypeError('Date format specifer must be either %d/%m%/Y or %m/%d/%Y')
        self.f_obj.write('DATE_FORMAT '+dfmt+'\n')
        self.f_obj.write('END SETTINGS\n')
        return 
    
    def write_tsproc(self):
        self.f_obj = open(self.tsproc_file,'w')
        self.write_settings()
        self.write_blocks()
        self.list_output()
        if self.pest != False:
            self.pest.write_entry(self.f_obj)
        self.f_obj.close()
    
    def list_output(self):
        self.f_obj.write('\nSTART LIST_OUTPUT\n')
        self.f_obj.write('CONTEXT all\n')
        self.f_obj.write(' FILE '+self.out_file+'\n')       
        out_blocks = []
                
        for block in self.blocks:           
            if block.data_type == SERIES:   
                if block.role == 'final' and block.context != PEST_CONTEXT:
                    self.f_obj.write(' '+block.data_type+' '+block.name+'\n')
                    out_blocks.append(block)
        
        for block in self.blocks:
            if block.data_type == VTABLE:
                if block.role == 'final' and block.context != PEST_CONTEXT:
                    self.f_obj.write(' '+block.data_type+' '+block.name+'\n')
                    out_blocks.append(block)
                    
        for block in self.blocks:
            if block.data_type == STABLE:
                if block.role == 'final' and block.context != PEST_CONTEXT:
                    self.f_obj.write(' '+block.data_type+' '+block.name+'\n')
                    out_blocks.append(block)
        
        for block in self.blocks:
            if block.data_type == CTABLE:
                if block.role == 'final' and block.context != PEST_CONTEXT:
                    self.f_obj.write(' '+block.data_type+' '+block.name+'\n')
                    out_blocks.append(block) 
        
        for block in self.blocks:
            if block.data_type == ETABLE:
                if block.role == 'final' and block.context != PEST_CONTEXT:
                    self.f_obj.write(' '+block.data_type+' '+block.name+'\n')
                    out_blocks.append(block)                                                  
        
        self.f_obj.write(' SERIES_FORMAT '+self.out_fmt+'\n')
        self.f_obj.write('END LIST_OUTPUT\n')
        
        
    
    #-----------------------------------
    #--write pest
    def write_pest(self,tpl_file_list,mod_file_list,obs_blocks,mod_blocks,\
                   svd=False,parms=None,parm_grp=None,context=PEST_CONTEXT,\
                   role='None',global_maxmin=None,model_cmd='model.bat'):
        
        #--some defense
        final_blocks = self.get_blocks(role='final')        
        #for m in mod_blocks:
        #    assert m in final_blocks, 'block not in final blocks: '+str(m)                    
        assert len(tpl_file_list) == len(mod_file_list)
        assert len(obs_blocks) == len(mod_blocks)          
        for tpl in tpl_file_list:
            assert os.path.exists(tpl), 'template file not found:'+tpl
        
        this_item_keys = []
        this_item_values = []
        for idx in range(len(tpl_file_list)):
            this_item_keys.append('TEMPLATE_FILE')
            this_item_keys.append('MODEL_INPUT_FILE')
            this_item_values.append(tpl_file_list[idx])
            this_item_values.append(mod_file_list[idx])
        this_item_keys.append('NEW_INSTRUCTION_FILE')
        this_item_values.append('tsproc.ins')
        this_item_keys.append('MODEL_COMMAND_LINE')
        this_item_values.append(model_cmd)
        if svd:
            this_item_keys.append('TRUNCATED_SVD')
            this_item_values.append('1.0e-3')
        if parms:
            this_item_keys.append('PARAMETER_DATA_FILE')
            this_item_values.append(parms)
        if parm_grp:
            this_item_keys.append('PARAMETER_DATA_FILE')
            this_item_values.append(parms)
        this_item_keys.append('NEW_PEST_CONTROL_FILE')
        this_item_values.append('pest.pst')
        
        #--loop over each block in mod_bocks                        
        for m_block,o_block in zip(mod_blocks,obs_blocks):
                                                                       
            assert o_block.data_type == m_block.data_type,\
                   o_block.name+' not the same dtype as '+m_block.name
                   
            this_data_type = o_block.data_type            
            this_item_keys.append('OBSERVATION_'+this_data_type)
            this_item_values.append(o_block.name)
            this_item_keys.append('MODEL_'+this_data_type)
            this_item_values.append(m_block.name)  
                                                                           
            this_item_keys.append(this_data_type[:-5]+'_WEIGHTS_EQUATION')
            this_item_values.append(str(o_block.wght))
            if o_block.max_min != None:
                this_item_keys.append(this_data_type[:-5]+'_WEIGHTS_MIN_MAX')
                this_item_values.append(o_block.max_min)
            elif global_maxmin != None:
                this_item_keys.append(this_data_type[:-5]+'_WEIGHTS_MIN_MAX')
                this_item_values.append(global_maxmin)
        

        this_block = base_block('WRITE_PEST_FILES',context,'','',\
                                this_item_keys,this_item_values,context)
        #self.blocks.append(this_block)       
        #self.block_operations.append('write_pest')
        self.pest = this_block





#-------------------------------------------------------------------------------         
#--for testing
if __name__ == '__main__':
    #--'obs' series work
    obsfile = 'test_obs.ssf'
    obslist = ['ser1_o','ser2_o','ser3_o']

    tsproc_obj = tsproc('tsproc_test.dat')
    tsproc_obj.get_series_ssf(obslist,obsfile)
    tsproc_obj.get_series_swr_flow([1,2,3],'qeflow','swr_binfile.fls','01/01/2001',prefix='o')

    current_blocks = tsproc_obj.get_blocks(operations = 'get_series_swr_flow') 
    tsproc_obj.reduce_time(current_blocks,'02/01/2000')
    current_blocks = tsproc_obj.get_blocks(operations = 'reduce_time') 

    tsproc_obj.volume_calc(current_blocks,'tsproc_test.dat')

    tsproc_obj.drawdown(current_blocks,'tsproc_test.dat')
    dt_list = [[['01/01/2001','02/01/2001'],['01/01/2001','02/01/2001']],\
              [['00:00:00','01:01:01'],['00:00:00','01:01:01']]]
    current_blocks = tsproc_obj.get_blocks(operations = 'drawdown')           
    tsproc_obj.statistics(current_blocks,['sum','junk'],date_time_list=dt_list)

    tsproc_obj.difference_2_series(current_blocks,current_blocks)
    tsproc_obj.series_avg(current_blocks,'tsproc_test.dat')
    vtables_obs = tsproc_obj.get_blocks(dtype=VTABLE)
    tsproc_obj.vol_2_series(vtables_obs,role='final')
    #tsproc_obj.erase_entity(swr_blocks)
    obs_final_blocks = tsproc_obj.get_blocks(role='final')

    #--'mod' series work
    obsfile = 'test_mod.ssf'
    obslist = ['ser1_m','ser2_m','ser3_m']
    tsproc_obj2 = tsproc('temp.dat')
    tsproc_obj2.get_series_ssf(obslist,obsfile,context='pest_prep')
    tsproc_obj2.get_series_swr_flow([1,2,3],'qeflow','swr_binfile.fls','01/01/2001',\
                prefix='m',context='pest_prep')

    current_blocks = tsproc_obj2.get_blocks(operations = 'get_series_swr_flow') 
    tsproc_obj2.reduce_time(current_blocks,'02/01/2000')
    current_blocks = tsproc_obj2.get_blocks(operations = 'reduce_time') 

    tsproc_obj2.volume_calc(current_blocks,'tsproc_test.dat')

    tsproc_obj2.drawdown(current_blocks,'tsproc_test.dat')
    dt_list = [[['01/01/2001','02/01/2001'],['01/01/2001','02/01/2001']],\
              [['00:00:00','01:01:01'],['00:00:00','01:01:01']]]
    current_blocks = tsproc_obj2.get_blocks(operations = 'drawdown')           
    tsproc_obj2.statistics(current_blocks,['sum','junk'],date_time_list=dt_list)

    tsproc_obj2.difference_2_series(current_blocks,current_blocks)
    tsproc_obj2.series_avg(current_blocks,'tsproc_test.dat')
    vtables_obs = tsproc_obj2.get_blocks(dtype=VTABLE)
    tsproc_obj2.vol_2_series(vtables_obs,role='final')

    mod_final_blocks = tsproc_obj2.get_blocks(role='final')

    wght_list = []
    for b in mod_final_blocks:
        wght_list.append(1.0)

    tsproc_obj.write_pest(['tpl1.tpl','tpl2.tpl'],['mod1.dat','mod2.dat'],\
                          obs_final_blocks,mod_final_blocks,wght_list)


    tsproc_obj.write_tsproc()
