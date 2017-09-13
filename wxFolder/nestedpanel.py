import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)

        self.panel = wx.Panel(self)

        # create controls
        self.cntrlPanel = wx.Panel(self.panel)
        stc1 = wx.StaticText(self.cntrlPanel, label="wow it works")
        stc2 = wx.StaticText(self.cntrlPanel, label="yes it works")
        btn = wx.Button(self.cntrlPanel, label="help?")
        btn.Bind(wx.EVT_BUTTON, self._onShowHelp)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(stc1)
        sizer.Add(stc2)
        sizer.Add(btn)
        self.cntrlPanel.SetSizer(sizer)


        # create help panel
        self.helpPanel = wx.Panel(self.panel)
        self.stcHelp = wx.StaticText(self.helpPanel, label="help help help\n"*8)
        btn = wx.Button(self.helpPanel, label="close[x]")
        btn.Bind(wx.EVT_BUTTON, self._onShowCntrls)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.stcHelp)
        sizer.Add(btn)
        self.helpPanel.SetSizer(sizer)
        self.helpPanel.Hide()
        self.helpPanel.Raise()
        self.helpPanel.SetBackgroundColour((240,250,240))
        self.Bind(wx.EVT_SIZE, self._onSize)

        self._onShowCntrls(None)

    def _onShowHelp(self, event):
        self.helpPanel.SetPosition((0,0))
        self.helpPanel.Show()
        self.cntrlPanel.Hide()

    def _onShowCntrls(self, event):
        self.cntrlPanel.SetPosition((0,0))
        self.helpPanel.Hide()
        self.cntrlPanel.Show()

    def _onSize(self, event):
        event.Skip()
        self.helpPanel.SetSize(self.GetClientSizeTuple())
        self.cntrlPanel.SetSize(self.GetClientSizeTuple())

app = wx.PySimpleApp()
frame = MyFrame()
frame.Show()
app.SetTopWindow(frame)
app.MainLoop()