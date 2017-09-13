'''
Decodes the operation sequence
'''

import GetFlags
import Decode_Gologic
import GUIopt
from copy import deepcopy
import csv


class OptDecode:
    
    def __init__(self,grid,csvsheet,addressmap,app,togglefrequency):
        self.grid = grid
        self.app=app
        self.csvsheet = csvsheet
        self.addressmap = addressmap
        self.getflags = GetFlags.GetFlags()
        self.guiopt = GUIopt.GuiOpt(self.grid,self.app)
        self.decodegologic = Decode_Gologic.Decoder(togglefrequency)
        command = None
        self.GUIrow = 0
        self.tagrow = 0
        self.commandlist=[]
        self.tempdict = {}
        self.read_erase = 0
        self.dcodflag=0
        self.current_command = None
        #with open('temp.csv',w,newline ='') as csvfile:
            #csvdata = csv.writer(csvfile,delimiter = ',',)
    
    def decodeoperation(self):
        prevrow=None
        datalist = []
        datalistwrite=[]
        datasize = 0
        datasizewrite=0
        command_flag = 0
        increment_row_flag=1
        self.csvsheet = self.csvsheet.values    #pandas values 
        for index,row in enumerate(self.csvsheet):
            if index%100==0:
                self.guiopt.refresh_grid()
                
            if self.GUIrow==10:
                self.guiopt.adjust_column_size()
                self.guiopt.Hidecolumns()
            if prevrow is None:
                prevrow = row            
            
            #####################################################
            
            #Command Decoding
            command,relativetime = self.decodegologic.check_cmd(row, prevrow)
            if command:
                self.current_command = command
                #command_flag=1
              
                self.GUIrow += 1   
                self.guiopt.write_cmd_GUI(self.GUIrow,command)
                self.guiopt.write_timestamp_GUI(self.GUIrow,relativetime)
                
                #self.tempdict[command]=self.GUIrow
                #self.commandlist.append(self.tempdict.copy())#to avoid reference issues
                #self.tempdict.clear()   #clear the temp dict
                
                if self.GUIrow%2 == 0:
                    self.guiopt.set_grid_colour(self.GUIrow)    #highlight the background
                method = 'cmd'+command
                try:
                    method_to_call = getattr(self,method)
                except AttributeError,TypeError:
                    method_to_call=getattr(self,'notyetdefined')
                method_to_call(self.GUIrow)    
                
            ###################################################
            
            #Ready/Busy decoding
            readybusy,busycommand=self.decodegologic.check_rdy_bsy(row, prevrow,self.current_command)
            if readybusy is not None:
                readybusy = 'CMD'+busycommand+' busy for '+str(readybusy)
                self.guiopt.set_readybusy_time(self.GUIrow, readybusy)
                
            ###################################################
            #Address decoding
            
            addrdata = self.decodegologic.check_addr(row, prevrow)
            
            if addrdata == 1:
                pass
            elif addrdata is None:
                addresslist = self.decodegologic.latch_addr_and_time()
               
                if type(addresslist)==list and len(addresslist ) > 0:
                    #self.decode_address_map(self.GUIrow,addresslist)
                    self.guiopt.write_addr_GUI(self.GUIrow,addresslist)
                    if self.current_command == '65':
                        self.addrdict = self.addressmap.decode_die(addresslist)
                    else:
                        self.addrdict = self.addressmap.decode_address(addresslist)
                    self.guiopt.write_addrmap_GUI(self.GUIrow, self.addrdict)
                    self.guiopt.autosizerow(self.GUIrow)
            ###################################################
            
            #Data read Decoding

            if self.current_command == '70':
                status = self.decodegologic.check_spcases_read(row,prevrow)
                self.guiopt.write_data_GUI(self.GUIrow,status)  
                self.guiopt.write_datasize_GUI(self.GUIrow,'1')                

            else:
                data = self.decodegologic.check_data_read(row, prevrow)
                
                if data == 1:
                    pass
                elif data is None:
                    
                    datalist,datasize = self.decodegologic.latch_dataread_and_time()
                   
                    if type(datalist)==list and len(datalist ) > 0:
                        self.guiopt.write_data_GUI(self.GUIrow,datalist)  
                        self.guiopt.write_datasize_GUI(self.GUIrow,datasize)
            ###################################################
            #Data write Decoding
            if self.current_command in ['80','85']:
                datawrite = self.decodegologic.check_data_write(row, prevrow)
                
                if datawrite == 1:
                    pass
                elif datawrite is None:
                    
                    datalistwrite,datasizewrite = self.decodegologic.latch_datawrite_and_time()
                   
                    if type(datalistwrite)==list and len(datalistwrite) > 0:
                        self.guiopt.write_data_GUI(self.GUIrow,datalistwrite)  
                        self.guiopt.write_datasize_GUI(self.GUIrow,datasizewrite)                    
            ###################################################
            chip = self.decodegologic.get_enabled_chip(row)
            self.guiopt.write_chip_GUI(self.GUIrow, chip)
            prevrow = row
        #print self.commandlist
        
        #self.get_tag_names()
        
        
    def get_tag_names(self):
        #temp_list = []
        self.dcodflag = 0
        for commandrow in self.commandlist:
            (command,row), =commandrow.items()
            method = 'cmd'+command
            try:
                method_to_call = getattr(self,method)
            except AttributeError,TypeError:
                #command is not defined then notyetdefined is called
                method_to_call=getattr(self,'notyetdefined')
            method_to_call(row)
    def cmd11(self,row):
        self.guiopt.write_subevent_GUI(row, 'Plane Switch')
    def cmd65(self,row):
        self.guiopt.write_subevent_GUI(row, 'DieSelection')
    
    def cmd80(self,row):
        self.guiopt.write_subevent_GUI(row, 'Write Operation')
        
    def cmd10(self,row):
        self.guiopt.write_subevent_GUI(row, 'programm data')
        
    def cmd60(self,row):
        #self.read_erase = row
        if self.dcodflag == 0:
            self.dcodflag = 1
            self.read_erase = row
        #self.guiopt.write_subevent_GUI(row, 'Read Operation')
        
    def cmd30(self,row):
        if self.dcodflag == 1:
            self.guiopt.write_subevent_GUI(self.read_erase, 'Read Operation')
            self.dcodflag = 0
        self.guiopt.write_subevent_GUI(row, 'Toggle Out Data')
   
    def cmdD0(self,row):
            if self.dcodflag == 1:
                self.guiopt.write_subevent_GUI(self.read_erase, 'Erase Operation')
                self.dcodflag = 0
            self.guiopt.write_subevent_GUI(row, 'Start erase')        
            3
    def cmdA2(self,row):
        self.guiopt.write_subevent_GUI(row, 'SLC Operation')
    
    def cmd70(self,row):
        self.guiopt.write_subevent_GUI(row, 'Status')
            
    def notyetdefined(self,row):
        self.guiopt.write_subevent_GUI(row, 'Not yet defined')
        
    def cmd5(self,row):
        self.guiopt.write_subevent_GUI(row, 'Reg Read Single Plane')
        
    def cmdE0(self,row):
        self.guiopt.write_subevent_GUI(row, 'toggleout reg data')
        
    
        