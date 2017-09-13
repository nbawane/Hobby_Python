import global_var
import wx.grid

import csv 

"""
All GUI related operations should be kept in this file   
"""
col1 = (224,224,224)

class GuiOpt:
    def __init__(self,gridobj,app):
        self.grid = gridobj
        self.app = app
        #self.grid.AutoSize()
        #self.cmdpos = 1
        #self.timestamppos = 0
        #self.addresspos = 2
        #self.datapos = 3
        self.GUI_COL = global_var.GUI_COL
        self.joiner = ' '*4   #space
        self.attr1 = wx.grid.GridCellAttr()
        self.attr1.SetBackgroundColour(col1)
        #with open('temp_file.csv','w') as csvfile:
        self.GUIrowrec = []
        self.addressmaprec = []
        
    def write_cmd_GUI(self,row,data):
        self.grid.SetCellValue(row,self.GUI_COL['CMD'],data)
    
    def autosizerow(self,currentrow):
        self.grid.AutoSizeRow(currentrow)
    
    def adjust_column_size(self):
        return
        self.grid.AutoSizeColumn(self.GUI_COL['Data'])
        self.grid.AutoSizeColumn(self.GUI_COL['Address'])	 
        self.grid.AutoSizeColumn(self.GUI_COL['Event'])
        self.grid.AutoSizeColumn(self.GUI_COL['DataSize(Bytes)'])
        self.grid.AutoSizeColumn(self.GUI_COL['AddrMap'])
        self.grid.AutoSizeColumn(self.GUI_COL['Timestamp(ns)'])        
    
    def write_data_GUI(self,row,data):
        offset = 0
        position=0
        increment = 32
        ##
        #to divide 
        
        if isinstance(data,list):
            while position < len(data):
                position += increment
                data.insert(position+offset,'\n')
            datafield = self.joiner.join(data)
            self.grid.SetCellValue(row,self.GUI_COL['Data'],str(datafield))
            offset += 1
            increment =33
        elif isinstance(data,str):
            self.grid.SetCellValue(row,self.GUI_COL['Data'],str(data))
        
    def Hidecolumns(self):
        return
        self.grid.HideCol(0)
        
    def write_chip_GUI(self,row,data):
        self.grid.SetCellValue(row,self.GUI_COL['Chip'],str(data))
    
    def write_datasize_GUI(self,row,data):
        self.grid.SetCellValue(row,self.GUI_COL['DataSize(Bytes)'],str(data))
        
    def write_addr_GUI(self,row,data):
        assert isinstance(data,list),"address field is not List"
        addr = self.joiner.join(data)   #separating with tab
        self.grid.SetCellValue(row,self.GUI_COL['Address'],addr)
        #self.addrcount += 1
    
    def write_subevent_GUI(self,row,data):
        assert isinstance(data,str),'Tag field is not string'
        self.grid.SetCellValue(row,self.GUI_COL['Event'],data)
    
    def write_timestamp_GUI(self,row,data):
        self.grid.SetCellValue(row,self.GUI_COL['Timestamp(ns)'],str(data))
        
    def set_grid_colour(self,row):
        #give alternate rows colour
        #return
        #cellattr = self.grid.GridCellAttr()

        for col in range(global_var.GUI_Column):
            self.grid.SetAttr(row,col, self.attr1)
        return
    def set_readybusy_time(self,row,data):
        self.grid.SetCellValue(row,self.GUI_COL['Ready/Busy(ns)'],str(data))
        
    def write_addrmap_GUI(self,row,addressmap):
        
        printstring = ''
        if isinstance(addressmap,dict):
            
            #row = 7
            for key in addressmap.keys():
                printstring = key+'='+str(addressmap[key])+'\n'+printstring
        elif isinstance(addressmap,str):
            printstring = addressmap
        self.grid.SetCellValue(row,self.GUI_COL['AddrMap'],printstring)
        self.GUIrowrec.append(row)
        self.addressmaprec.append(printstring)
        filterdata= dict(zip(self.GUIrowrec,self.addressmaprec))
        
        print filterdata
    def refresh_grid(self):
        '''
        THis is the API to refresh the the grid
        '''
        self.app.Yield()
        
        
      
    
    
        
    
    