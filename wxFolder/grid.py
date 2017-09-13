import wx
import wx.grid as gridlib
import time

class MyForm(wx.Frame):
    def __init__(self,app):
        ##
        # constructor to create the basic frame
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tool")

        # Add a panel so it looks the correct on all platforms
        self.app = app
        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(panel)
        rows = 4
        column = 1000
        self.grid.CreateGrid(column, rows)
        self.count = 0
        self.button = wx.Button(panel, label="Test")

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.button)
        # change a couple column labels
        self.grid.SetColLabelValue(0, "Timestamp")
        self.grid.SetColLabelValue(1, "CMD")
        self.grid.SetColLabelValue(2, "Address")
        self.grid.SetColLabelValue(3, "Data")

        # Few More operations to calculate CMD,Timestamp field
        # self.display = wx.ComboBox(self, -1)
        # self.Show()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        # sizer.Add(self.display,0,wx.EXPAND)
        panel.SetSizer(sizer)
        self.Show()
        for i in range(10):
            self.count += 1
            self.grid.SetCellValue(self.count,1,'CMD4')
            self.grid.SetCellValue(self.count,0,str(self.count))
            self.grid.SetCellValue(self.count, 2, "Extracted Address")
            self.grid.SetCellValue(self.count, 3, "Extracted Data")
            time.sleep(0.5)
            if self.count%2==0:
                self.grid.HideCol(1)
            else:
                self.grid.ShowCol(1)

            self.grid.SetColSize(2,200)
            quo,rem = divmod(self.count,1)
            wx.CheckListBox()
if __name__ == "__main__":
    wx.ComboBox()
    app = wx.App()
    frame = MyForm(app)
    app.MainLoop()