import wx
import wx.grid as gridlib


########################################################################
class MyForm(wx.Frame):
	""""""

	# ----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, parent=None, title="Grid Tutorial Two", size=(650, 320))
		panel = wx.Panel(self)

		myGrid = gridlib.Grid(panel)
		myGrid.CreateGrid(15, 6)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(myGrid)
		panel.SetSizer(sizer)


if __name__ == "__main__":
	app = wx.PySimpleApp()
	frame = MyForm()
	frame.Show()
	app.MainLoop()