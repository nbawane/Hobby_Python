import wx

class ColumnSelect(wx.Frame):
	def __init__(self):
		parent = None
		self.columns = {'Timestamp(ns)': 0,
		 'Chip': 1,
		 'Event': 2,
		 'AddrMap': 3,
		 'Ready/Busy(ns)': 4,
		 'CMD': 5,
		 'Address': 6,
		 'Data': 7,
		 'DataSize(Bytes)': 8}

		wx.Frame.__init__(self,parent, -1, 'Column Select', size=(300, 200))
		self.panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)

		controlsizer = wx.BoxSizer(wx.VERTICAL)
		checkboxsizer = wx.BoxSizer(wx.VERTICAL)

		textone = wx.StaticText(self,label='Select Columns to hide')
		checkboxsizer.Add(textone)
		checkboxsizer.AddSpacer(10)
		for column_name in self.columns.keys():
			checkboxobj = wx.CheckBox(self,label=column_name)
			checkboxsizer.Add(checkboxobj)
			checkboxobj.Bind(wx.EVT_CHECKBOX,self.onSelect)

		applybutton = wx.Button(self,label='apply')

		controlsizer.Add(applybutton)

		sizer.Add(self.panel)

		sizer.Add(checkboxsizer)
		sizer.AddSpacer(10)
		sizer.Add(controlsizer)

		self.SetSizer(sizer)

	def onSelect(self,event):
		obj = event.GetEventObject()
		print obj.GetLabel()
		wx.PyCommandEvent()

app = wx.App()
frame = ColumnSelect()
frame.Show()
app.MainLoop()

