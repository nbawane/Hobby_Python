import wx
import wx.grid as gridlib


class MyForm(wx.Frame):
    def __init__(self):
        ##
        # constructor to create the basic frame
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tool")

        self.gridevent = gridlib.GridEvent()
        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(panel)
        column = 4
        row = 1000
        self.grid.CreateGrid(row, column)
        self.count = 0
        self.button = wx.Button(panel, label="Test")

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.button)
        # change a couple column labels
        self.grid.SetColLabelValue(0, "Timestamp")
        self.grid.SetColLabelValue(1, "CMD")
        self.grid.SetColLabelValue(2, "Address")
        self.grid.SetColLabelValue(3, "Data")
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK,self.onrightclick)
        # self.grid.ShowRow()

        # Few More operations to calculate CMD,Timestamp field

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        # sizer.Add(self.display,0,wx.EXPAND)
        panel.SetSizer(sizer)
        for i in range(100):
            self.count += 1
            self.grid.SetCellValue(self.count,1,'CMD4')
            self.grid.SetCellValue(self.count,0,str(self.count))
            self.grid.SetCellValue(self.count, 2, "Extracted Address")
            self.grid.SetCellValue(self.count, 3, "Extracted Data")
            if self.count%2==0:
                self.grid.HideRow(self.count)

            self.grid.DeleteRows()
    def onrightclick(self,evt):
        print "OnLabelRightDClick: (%d,%d) %s\n" % (evt.GetRow(),
                                                    evt.GetCol(),
                                                    evt.GetPosition())
        col,row = evt.GetRow(),evt.GetCol()
        print 'printing event',evt
        print "%d,%d"%(col,row)
        print self.grid.GetCellValue(col,row)
        self.grid.SetCellBackgroundColour()

if __name__ == "__main__":

    app = wx.App()
    frame = MyForm()
    frame.Show()
    app.MainLoop()