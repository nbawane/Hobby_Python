'''
GUI handeler
'''
import wx
import wx.grid as  gridlib
class MyForm(wx.Frame):
	def __init__(self):
		##
		# constructor to create the basic frame
		wx.Frame.__init__(self, None, wx.ID_ANY, "Hiding Rows and Columns")

		# Add a panel so it looks the correct on all platforms
		panel = wx.Panel(self, wx.ID_ANY)
		self.grid = gridlib.Grid(panel)
		rows = 4
		column = 600000
		self.grid.CreateGrid(column, rows)
		self.count = 0
		# change a couple column labels
		self.grid.SetColLabelValue(0, "Timestamp")
		self.grid.SetColLabelValue(1, "CMD")
		self.grid.SetColLabelValue(2, "Address")
		self.grid.SetColLabelValue(3, "Data")

		# change the row labels

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.grid, 1, wx.EXPAND, 5)
		panel.SetSizer(sizer)

	def writecommand(self, command):
		self.grid.AppendCols(1)
		self.count += 1
		self.grid.SetCellValue(1, self.count, command)


if __name__ == "__main__":
	app = wx.App()
	frame = MyForm()
	frame.Show()
	app.MainLoop()