"""
This is the main file 
all operation starts from here,one should start reading the from here
"""

#import csv
import pandas
import wx
import wx.grid as  gridlib
from threading import Thread
from wx.lib.pubsub import Publisher

import global_var
import GetFlags
import Decode_Gologic
import GUIopt
import Operation_Decode
import AddressMap
import CustomWidget


class Main:
    def __init__(self,csvsheet,gridobj,memory_name,app,togglefrequency):
        self.grid = gridobj
	self.app=app
	self.memory_name = memory_name
        self.csvsheet = csvsheet #can be any sequence
        self.globalvarobj = global_var.GetColNums()
        self.getcolumns()   #initialize global var
        self.COL_POSITION = global_var.COL_POSITION
        self.getflags= GetFlags.GetFlags()
        #self.guiopt = GUIopt.GuiOpt(self.grid,self.app)
        self.addressmap = AddressMap.AdressMapOperation(self.memory_name) #this needs to be updated with the combobox input
        self.optdecode = Operation_Decode.OptDecode(self.grid,self.csvsheet,self.addressmap,self.app,togglefrequency)
        self.prevrow = None
        self.command = None
        self.GUICurrentrow = 0

    def parser(self):
        ##
        #to get columns info
        print self.COL_POSITION
        self.optdecode.decodeoperation()
        #quo,rem = divmod(index,100000)
        #if rem == 0:
            #self.grid.MoveCursorDownBlock(expandSelection=False)
            #wx.Yield()
        #self.prevrow = row

    def getcolumns(self):
        """
        returns the dictionary with column name and column number
        """
        self.globalvarobj.col_position_dict(list(self.csvsheet.columns.values))
	#self.globalvarobj.col_position_dict(self.csvsheet[0])

'''
Class for GUI Initialization
'''

class GridPanel(wx.Panel):
    grid = None

    def __init__(self,parent,app):
        """
        Basic User Interface design
        """
        ##
        #constructor to create the basic frame
        wx.Panel.__init__(self, parent=parent)
        #filename = r'C:\GoLogicInterpreter\BICSTRACE_Sample.csv'
        #filename = r'C:\GoLogicInterpreter\Book1.csv'
        #self.fd = csv.reader(open(filename))

        self.globalvarobj = global_var.GetColNums()
	self.app =app
        self.GUI_COl = global_var.GUI_COL
        self.GUI_Row = global_var.GUI_Row
        self.GUI_Column = global_var.GUI_Column
        # Add a panel so it looks the correct on all platforms

        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(panel)
        self.grid = gridlib.Grid(self)

        self.grid.CreateGrid(self.GUI_Row,self.GUI_Column)
        self.GUI_COl = global_var.GUI_COL
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 0, wx.EXPAND)
        self.SetSizer(sizer)
	self.hide_flag = 0
	
	self.grid.SetColSize(self.GUI_COl['Timestamp(ns)'],100)
	self.grid.SetColSize(self.GUI_COl['Event'],150)
	self.grid.SetColSize(self.GUI_COl['AddrMap'],150)
	self.grid.SetColSize(self.GUI_COl['CMD'],100)
	self.grid.SetColSize(self.GUI_COl['Ready/Busy(ns)'],100)
	self.grid.SetColSize(self.GUI_COl['Address'],120)
	self.grid.SetColSize(self.GUI_COl['Data'],600)
	self.grid.SetColSize(self.GUI_COl['DataSize(Bytes)'],100)
	
	   
    def grid_operation(self,fd,memory_name,togglefrequency):
	self.fd = fd
	self.memory_name = memory_name
	parserobj = Main(self.fd,self.grid,self.memory_name,self.app,togglefrequency)
        for key in self.GUI_COl:
            #loop to give titles of fields
            self.grid.SetColLabelValue(self.GUI_COl[key],key)
        parserobj.parser()
        # change the row labels
        #self.grid.AutoSizeColumn(self.GUI_COl['MainEvent'])   #Autoresize according to content on  colmns

        #self.grid.AutoSize()

    def hidecolumn(self):
	'''
	To toggle the column view mode
	hide/show Address and Datasize column
	'''
	self.hide_flag = not self.hide_flag
	if self.hide_flag:
	    self.grid.HideCol(global_var.GUI_COL['Address'])
	    self.grid.HideCol(global_var.GUI_COL['DataSize(Bytes)'])
	else:
	    self.grid.ShowCol(global_var.GUI_COL['Address'])
	    self.grid.ShowCol(global_var.GUI_COL['DataSize(Bytes)'])	    
	    self.grid.SetColSize(self.GUI_COl['Address'],200)	#after show it goes to label size so needed to resizeit
	    self.grid.SetColSize(self.GUI_COl['DataSize(Bytes)'],100)

class ControlPanel(wx.Panel):


    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent = parent)
        #self.gridpanel = gridpanel
	#---------------------------------------Static texts----------------------------------------------#
        self.txtOne = wx.StaticText(self, -1, label = "Enter CSV path", pos = (20,10))#widget to print the title
	self.txtTwo=wx.StaticText(self, -1, label = "Select Memory Type", pos =	(150,10))#widget to print the title
        self.txtPlace = wx.TextCtrl(self, pos =	(20,30))    #widget to to get the file csv filename from
	self.enterfrequencystatictext = wx.StaticText(self,-1,label='Enter Toggle frequency(MHz)',pos=(350,10))
	self.frequencyinput = wx.TextCtrl(self,pos=(350,30))
	
	#-------------------------------------------Buttons------------------------------------------------#
        button = wx.Button(self, label = "Start", pos =	(20,70))    #Button to start the parsing operation
        button.Bind(wx.EVT_BUTTON, self.onButton)
	
	filterbutton = button = wx.Button(self, label = "Filter", pos =(350,70))    #Opens a window to select the values to be displayed 
        filterbutton.Bind(wx.EVT_BUTTON, self.onFilterButton)	
	
	button = wx.Button(self, label = "Toggle Mode", pos =	(150,70))    #Button to start the parsing operation
        button.Bind(wx.EVT_BUTTON, self.onButton_toggle)
	
	#------------------------------------------Combobox-------------------------------------------------#
	'''
	to give options for memory type select,this memory type is used to select the proper address mapping
	'''
	self.MemoryTypes = ['Bics3_128Gb','Bics3_256Gb']
	wx.ComboBox(self, -1, pos=(150,30), size=(150, -1), choices=self.MemoryTypes, style=wx.CB_READONLY) 	
	self.Bind(wx.EVT_COMBOBOX, self.OnSelect)
	

    def onButton_toggle(self,event):
	self.GetParent().GetParent().toggle_operation()
	
    def onButton(self, event):
        #return
        """
        Gets the CSV file path to parse
        and Runs the main parser
        """
        #gridinst = GridPanel.get_gridinst()
        filename = self.txtPlace.GetValue()
	togglefrequency = self.frequencyinput.GetValue()
        #self.fd = csv.reader(open(filename))
	#chunksize = 10**6
	
	self.fd = pandas.read_csv(filename, sep=',')
	#self.fd=df.values
        #parserobj = Main(self.fd,self.gridpanel.grid)
        #parserobj.parser()
        self.GetParent().GetParent().start_operation(self.fd,self.memory_name,togglefrequency)
	
    def OnSelect(self,event):
	item=event.GetSelection()    #gets the selected options from combobox
	self.memory_name = self.MemoryTypes[item] #gets the memory_name 

    def onFilterButton(self,event):
	#wx.StaticText(self, -1,label='start filter',pos=(550,10))
	filteroperation = CustomWidget.FilterWidget()
	
	

class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,app):
        """Creates two panel ,One for control widgets and other for grid"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "GoLogic Interpretor",size=(800,600))  #Gives size and Title to Frame

        self.splitter = wx.SplitterWindow(self)
        self.panelOne = ControlPanel(self.splitter)
        self.panelTwo = GridPanel(self.splitter,app)
        
        
        self.splitter.SplitHorizontally(self.panelOne, self.panelTwo)
        self.splitter.SetMinimumPaneSize(100)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.splitter, 2, wx.EXPAND)

        self.SetSizer(self.sizer)	  
        
	# create a pubsub receiver, this will refresh the grid
	#Publisher().subscribe(self.updateDisplay, "update")        
        
    def start_operation(self,fd,memory_name,togglefrequency):
        self.panelTwo.grid_operation(fd,memory_name,togglefrequency)
	
    def toggle_operation(self):
	self.panelTwo.hidecolumn()
	
if __name__ == '__main__':
    """
     starting point of programm
     """
    app = wx.App()
    frame = MainFrame(app)
    frame.Show()
    app.MainLoop()     
