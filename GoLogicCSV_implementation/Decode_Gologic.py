'''
file to decode command, data, Data in and Data out
This file has methods to return above fields
'''
import global_var
import GetFlags
import GUIopt
print_flag = 0	#this flag is to print data on console

class Decoder:
    def __init__(self,togglefrequency):
	self.togglefrequency = int(togglefrequency)*10**6 #this frequency is used to calculate the data
        self.getFlags = GetFlags.GetFlags()
        self.datasize = 0
	self.datasize_write = 0
	self.data_list_write = []
	self.data_time_write = []
        self.addrsize = 0
        self.addr_list = []
        self.addr_time = []
        self.data_time=[]
        self.data_list = []
        self.timestamp_data = []
        self.datainflaf = 0
        self.dataoutflag = 0
        self.startstoprdybsy = 0
        self.rdybystime = 0
        self.relativetime = 0

    def check_cmd(self,row,prevrow):
	'''
	row : curent row(list form)
	prevrow : previous row(list form)
	return :
	    deccoded command and relative timestamp starting from 0ns
	'''
        ##
        #extract command    
        curr_data = self.getFlags.get_data_field(row)
        prev_data = self.getFlags.get_data_field(prevrow)
        time = self.ConvertTime(self.getFlags.get_time_stamp(row),self.getFlags.get_time_unit(row))
        self.relativetime +=time
        command = None

        if self.getFlags.get_ale_flag(row)==0 and self.getFlags.get_cle_flag(row)==1\
           and self.getFlags.get_write_enable_flag(row)==1 and self.getFlags.get_read_enable_flag(row) == 1:
                ##
                #To sense edge trigger      
            if self.getFlags.get_write_enable_flag(prevrow)==0 and (curr_data==prev_data):
                command = self.getFlags.get_data_field(row)
        else:
            command = None
        ##print command
        return command,self.relativetime

    def check_addr(self,row,prevrow):
        ##
        #extract address
        if self.getFlags.get_ale_flag(row)==1 and self.getFlags.get_cle_flag(row)==0:

            if self.getFlags.get_write_enable_flag(prevrow)==0 and \
               (self.getFlags.get_data_field(row)==self.getFlags.get_data_field(prevrow))\
               and self.getFlags.get_write_enable_flag(row)==1 and self.getFlags.get_read_enable_flag(row)==1:    
                ##
                #To sense edge trigger        
                #self.latch_data_and_time()
                addr = self.getFlags.get_data_field(row)
                time = self.ConvertTime(self.getFlags.get_time_stamp(row),self.getFlags.get_time_unit(row))
                self.addrsize +=1 
                self.addr_list.append(addr)
                self.addr_time.append(time)
                return 1
            else:
                return 1
        else:
            return None


            #print 'ADDR %s'%self.getFlags.get_data_field(row)      

    def check_data_read(self,row,prevrow):
	'''
	extract the data on falling edge and rising edge
	'''
        ##
        #extract data
        data = self.getFlags.get_data_field(row)
        if self.getFlags.get_ale_flag(row)==0 and self.getFlags.get_cle_flag(row)==0:

            if (self.getFlags.get_read_enable_flag(prevrow)==0 and self.getFlags.get_read_enable_flag(row)==1)\
	       or (self.getFlags.get_read_enable_flag(prevrow)==1 and self.getFlags.get_read_enable_flag(row)==0)\
               and self.getFlags.get_write_enable_flag(row)==1:     
		
                data = self.getFlags.get_data_field(row)
                time = self.ConvertTime(self.getFlags.get_time_stamp(row),self.getFlags.get_time_unit(row))
                self.datasize += 1
                self.data_list.append(data)
                self.data_time.append(time)
                return 1
            else:
                return 1
        else:
            return None
	
    def check_spcases_read(self,row,prevrow):
	'''
	method to extract 
	'''
        data = self.getFlags.get_data_field(row)
        if self.getFlags.get_ale_flag(row)==0 and self.getFlags.get_cle_flag(row)==0:

            if (self.getFlags.get_read_enable_flag(prevrow)==0 and self.getFlags.get_read_enable_flag(row)==1)\
	       and self.getFlags.get_write_enable_flag(row)==1:     
		
                data = self.getFlags.get_data_field(row)
                #time = self.ConvertTime(self.getFlags.get_time_stamp(row),self.getFlags.get_time_unit(row))
                #self.datasize += 1
                return data
        else:
            return None	
    
    def check_data_write(self,row,prevrow):
	return
        ##
        #extract data
        if self.getFlags.get_ale_flag(row)==0 and self.getFlags.get_cle_flag(row)==0:
            if self.getFlags.get_write_enable_flag(row)==1:

                #print 'DATA : %s'%self.getFlags.get_data_field(row)
                #self.latch_addr_and_time()
                data_write = self.getFlags.get_data_field(row)
                time_write = self.ConvertTime(self.getFlags.get_time_stamp(row),self.getFlags.get_time_unit(row))
                self.datasize_write += 1
                self.data_list_write.append(data_write)
                self.data_time_write.append(time_write)  
                return 1
            else:
                return 1
        else:
            return None      
	
    def get_enabled_chip(self,row):
	current_chip = None
	ce0 = int(self.getFlags.get_ce_0_flag(row))
	ce1 = int(self.getFlags.get_ce_1_flag(row))
	ce2 = int(self.getFlags.get_ce_2_flag(row))
	ce3 = int(self.getFlags.get_ce_3_flag(row))
	chips= [ce0,ce1,ce2,ce3]
	
	enabled_chip = filter(lambda x: x<1, chips)
	
	if len(enabled_chip)>1:
	    return 'Multiple Chips Selected'
	elif len(enabled_chip)==1:
	    return enabled_chip[0]
	elif (ce0==ce1==ce2==ce3==1) or (ce0==ce1==ce2==ce3==0):
	    return 'Chip Not Selected'	    
	
	

    def check_rdy_bsy(self,row,prevrow,current_command):
        """
        calculate the busy period based on the falling edge and rising edge 
        of ready/busy signal
        doesn't return as of now only prints the busy time
        """
	
        if (self.getFlags.get_ready_busy_state(row)==0 and self.getFlags.get_ready_busy_state(prevrow)==1 )\
           and (self.getFlags.get_data_field(row)==self.getFlags.get_data_field(prevrow)):
            ##
            #falling edge detection
            self.startstoprdybsy = 1  #start accumulating time
	    self.current_command = current_command
            if print_flag:
                print 'rdy bsy start'
	    #return 'rdy bsy start'
        if (self.getFlags.get_ready_busy_state(row)==1 and self.getFlags.get_ready_busy_state(prevrow)==0 )\
           and (self.getFlags.get_data_field(row)==self.getFlags.get_data_field(prevrow)):
            ##
            #Rising edge detection
            if print_flag:
                print 'rdy sy stop'
	    #return 'rdy sy stop'
            self.startstoprdybsy = 0
        if self.startstoprdybsy == 1:
            time = self.ConvertTime(self.getFlags.get_time_stamp(row),self.getFlags.get_time_unit(row))
            self.rdybystime += time
        elif self.rdybystime >0 and self.startstoprdybsy == 0:
            if print_flag:
                print 'Ready/Busy time : %s'%self.rdybystime
	    temp_busy_time=self.rdybystime
	    self.rdybystime = 0 
	    return temp_busy_time,self.current_command
        return None,None   

    def latch_dataread_and_time(self):
        """
        upon calling and certain conditions are satisfied 
        latches the data in form of list and time in terms of nano second
        retruns the same
        """
        tempdata = None
        temp_datasize = 0
        if self.datasize>0:  #minimum datasize 2k
            #temp_datasize = self.datasize
            if print_flag:
                print 'datasize : ',self.datasize
            self.datasize = 0 
            tempdata = self.data_list[:]
	    tempdata,temp_datasize=self.remove_duplicate(tempdata)
            if print_flag:
                print "Time : %s | Data %s"%(sum(self.data_time),self.data_list)
            del self.data_list[:]
            del self.data_time[:]
            return tempdata,temp_datasize
        else:
            return None,None
	
    def latch_datawrite_and_time(self):
	tempdata_write = None
	temp_datasize_write = 0
	if self.datasize_write>0:  #minimum datasize 2k
	    #temp_datasize = self.datasize
	    if print_flag:
		print 'datasize : ',self.datasize_write
	    self.datasize_write = 0 
	    tempdata_write = self.data_list_write[:]
	    tempdata_write,temp_datasize_write=self.remove_duplicate(tempdata_write)
	    if print_flag:
		print "Time : %s | Data %s"%(sum(self.data_time_write),self.data_list_write)
	    del self.data_list_write[:]
	    del self.data_time_write[:]
	    return tempdata_write,temp_datasize_write
	else:
	    return None,None	

    def latch_addr_and_time(self):
        """
        upon calling and certain conditions are satisfied 
        latches the data in form of list and time in terms of nano second
        retruns the same
        """    
        temp_addr = None
        if self.addrsize>0:
            #assert (self.addrsize in [1,3,5]),"Address field is not standard "
            #self.guiopt.write_addr_GUI(self.addr_list)
            if print_flag:
                print 'address size : ',self.addrsize
                print 'Time : %s | ADDR%d %s'%(sum(self.addr_time),self.addrsize,self.addr_list)
            self.addrsize = 0 
            temp_addr = self.addr_list[:] #deep copy
            del self.addr_list[:]
            del self.addr_time[:]
            return temp_addr


    def ConvertTime(self,time,unit = 'ns'):
        """
        :param time: time to convert
        :param unit: s/ms/us/ns
        :return: converted time to ns format
        """
        s  = 10**9
        ms = 10**6
        us = 10**3
        ns = 1
        if unit == 'ms':
            return float(time)*ms

        if unit == 'us':
            return float(time)*us

        if unit == 'ns':
            return float(time)*ns  

        if unit == 's':
            return float(time)*s  

    def remove_duplicate(self,addrlist):
	b=[]
	x=None
	for i in addrlist:
	    if i==x:
		continue
	    else:
		b.append(i)
		x=i
	return b,len(b)
        
        