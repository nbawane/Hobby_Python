import wx
import wx.lib.scrolledpanel as scrolled

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "CheckBox Dialog",size=(400,250))
        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, size=(350,150),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.VSCROLL)
        self.button = wx.Button(self.panel, label="Choose Colours")
        sizer.Add(self.log, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.button, 0, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.panel.options = ['Red','Green','Black','White','Orange','Blue','Yellow']
        self.panel.selected = [0,0,0,0,0,0,0]

    def OnButton(self,event):
        dlg = ShowOptions(parent = self.panel)
        dlg.ShowModal()
        if dlg.result:
            result_text = 'Selected: '
            for item in range(len(dlg.result)):
                if dlg.result[item]:
                    result_text += self.panel.options[item]+' '
            self.log.AppendText(result_text+'\n\n')
            self.panel.selected = dlg.result
        else:
            self.log.AppendText("No selection made\n\n")
        dlg.Destroy()

class ShowOptions(wx.Dialog):
    def __init__(self, parent):
        self.options = parent.options
        self.selected = parent.selected
        o_str = ''
        for item in self.options:
            o_str = o_str+item+','
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "CheckBoxes", size= (400,250))
        self.top_panel = wx.Panel(self,wx.ID_ANY)
        self.avail_options = wx.TextCtrl(self.top_panel, wx.ID_ANY, o_str,style = wx.TE_READONLY)
        self.bot_panel = wx.Panel(self,wx.ID_ANY)
        self.scr_panel = scrolled.ScrolledPanel(self,wx.ID_ANY)
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        scr_sizer = wx.BoxSizer(wx.VERTICAL)
        bot_sizer = wx.BoxSizer(wx.VERTICAL)
        self.items = []
        for item in range(len(self.options)):
            self.item = wx.CheckBox(self.scr_panel,-1,self.options[item])
            self.item.SetValue(self.selected[item])
            self.items.append(self.item)
            self.item.Bind(wx.EVT_CHECKBOX, self.Select)
        self.saveButton =wx.Button(self.bot_panel, label="Save")
        self.closeButton =wx.Button(self.bot_panel, label="Cancel")
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveOpt)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        top_sizer.Add(self.avail_options,0,flag=wx.EXPAND)
        for item in self.items:
            scr_sizer.Add(item,0)
        bot_sizer.Add(self.saveButton,0,flag=wx.CENTER)
        bot_sizer.Add(self.closeButton,0,flag=wx.CENTER)
        self.scr_panel.SetupScrolling()

        self.top_panel.SetSizer(top_sizer)
        self.scr_panel.SetSizer(scr_sizer)
        self.bot_panel.SetSizer(bot_sizer)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.top_panel,0,flag=wx.EXPAND)
        mainsizer.Add(self.scr_panel,1,flag=wx.EXPAND)
        mainsizer.Add(self.bot_panel,0,flag=wx.EXPAND)
        self.SetSizer(mainsizer)
        self.Select(None)
        self.Show()

    def Select(self, event):
        selection = []
        for item in self.items:
            x = item.GetValue()
            selection.append(x)
        selected_text = ''
        for item in range(len(selection)):
            if selection[item]:
                    selected_text += self.options[item]+' '
            self.avail_options.SetValue(selected_text)

    def OnQuit(self, event):
        self.result = None
        self.Destroy()

    def SaveOpt(self, event):
        self.result = []
        for item in self.items:
            x = item.GetValue()
            self.result.append(x)
        self.Destroy()

app = wx.App()
frame = MyFrame(None)
frame.Show()
app.MainLoop()