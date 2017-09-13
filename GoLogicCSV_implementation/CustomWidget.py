import wx

class FilterWidget(wx.Frame):
	def __init__(self,parent = None):
		wx.Frame.__init__(self,parent,-1,"Filter",size=(300,200))

		self.top_panel = wx.Panel(self)
		self.bot_panel = wx.Panel(self, wx.ID_ANY)
		sizer = wx.BoxSizer(wx.VERTICAL)
		bottom_sizer = wx.BoxSizer(wx.VERTICAL)
		choices = ['block','die','plane','chip','block','die','plane','chip','block','die','plane','chip','block','die','plane','chip','block','die','plane','chip']
		self.checklistbox = wx.CheckListBox(self.top_panel,-1,choices=choices,size=(200,100))
		sizer.Add(self.checklistbox,0, wx.EXPAND | wx.ALL, 10)
		self.Bind(wx.EVT_CHECKLISTBOX,self.EvtCheckListBox,self.checklistbox)

		self.applyfilter = wx.Button(self.bot_panel,-1,label = 'Apply')
		self.Bind(wx.EVT_BUTTON,self.onApplyFilter,self.applyfilter)
		bottom_sizer.Add(self.applyfilter	,1,wx.EXPAND | wx.ALL, 10)

		self.top_panel.SetSizer(sizer)
		self.bot_panel.SetSizer(bottom_sizer)

		mainsizer = wx.BoxSizer(wx.VERTICAL)
		mainsizer.Add(self.top_panel,0,wx.EXPAND)
		mainsizer.Add(self.bot_panel,0,wx.EXPAND)

		self.SetSizer(mainsizer)
		
		self.Show()

	def EvtCheckListBox(self, event):
		index = event.GetSelection()
		label = self.checklistbox.GetString(index)
		self.checklistbox.SetSelection(index)  # so that (un)checking also selects (moves the highlight)

	def onApplyFilter(self,event):
		pass

if __name__ == '__main__':
	appob = wx.App()
	widgetobj = FilterWidget(None)
	widgetobj.Show()
	appob.MainLoop()
