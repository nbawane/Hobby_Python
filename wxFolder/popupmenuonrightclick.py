import wx

app = wx.PySimpleApp()


class MyPopupMenu(wx.Menu):
	def __init__(self, WinName):
		wx.Menu.__init__(self)

		self.WinName = WinName

		item = wx.MenuItem(self, wx.NewId(), "Item One")
		self.Append(item)
		self.Bind(wx.EVT_MENU, self.OnItem1, item)

		item = wx.MenuItem(self, wx.NewId(), "Item Two")
		self.Append(item)
		self.Bind(wx.EVT_MENU, self.OnItem2, item)

		item = wx.MenuItem(self, wx.NewId(), "Item Three")
		self.Append(item)
		self.Bind(wx.EVT_MENU, self.OnItem3, item)

	def OnItem1(self, event):
		id_selected = event.GetId()
			obj = event.GetEventObject()
			print "Option =", id_selected
			print obj.GetLabel(id_selected)
		print "From the range:"
		for i in range(obj.MenuItemCount):
			print "\t\t", obj.MenuItems[i].GetLabel()


		print "Item One selected in the %s window" % self.WinName

	def OnItem2(self, event):
		print "Item Two selected in the %s window" % self.WinName

	def OnItem3(self, event):
		print "Item Three selected in the %s window" % self.WinName


class MyWindow(wx.Window):
	def __init__(self, parent, color):
		wx.Window.__init__(self, parent, -1)

		self.color = color

		self.SetBackgroundColour(color)
		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

	def OnRightDown(self, event):
		menu = MyPopupMenu(self.color)
		self.PopupMenu(menu, event.GetPosition())
		menu.Destroy()


class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, "Test", size=(300, 200))

		sizer = wx.GridSizer(2, 2, 5, 5)

		sizer.Add(MyWindow(self, "blue"), 1, wx.GROW)
		sizer.Add(MyWindow(self, "yellow"), 1, wx.GROW)
		sizer.Add(MyWindow(self, "red"), 1, wx.GROW)
		sizer.Add(MyWindow(self, "green"), 1, wx.GROW)

		self.SetSizer(sizer)

		self.Show()


frame = MyFrame()
app.SetTopWindow(frame)
app.MainLoop()