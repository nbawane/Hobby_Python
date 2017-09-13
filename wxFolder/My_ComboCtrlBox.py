import wx
import wx.combo
import os
class FileSelectorCombo(wx.combo.ComboCtrl):
	def __init__(self, *args, **kw):
		wx.combo.ComboCtrl.__init__(self, *args, **kw)
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.aniTimer = wx.Timer(self)

	def AnimateShow(self, rect, flags):
		self.aniStart = wx.GetLocalTimeMillis()
		self.aniRect = wx.Rect(*rect)
		self.aniFlags = flags

		dc = wx.ScreenDC()
		bmp = wx.EmptyBitmap(rect.width, rect.height)
		mdc = wx.MemoryDC(bmp)
		if "wxMac" in wx.PlatformInfo:
			pass
		else:
			mdc.Blit(0, 0, rect.width, rect.height, dc, rect.x, rect.y)
		del mdc
		self.aniBackBitmap = bmp

		self.aniTimer.Start(10, wx.TIMER_CONTINUOUS)
		self.OnTimer(None)
		return False

	def OnTimer(self, evt):
		stopTimer = False
		popup = self.GetPopupControl().GetControl()
		rect = self.aniRect
		dc = wx.ScreenDC()

		if self.IsPopupWindowState(self.Hidden):
			stopTimer = True
		else:
			pos = wx.GetLocalTimeMillis() - self.aniStart
			if pos < CUSTOM_COMBOBOX_ANIMATION_DURATION:
				# Actual animation happens here
				width = rect.width
				height = rect.height

				center_x = rect.x + (width / 2)
				center_y = rect.y + (height / 2)

				dc.SetPen(wx.BLACK_PEN)
				dc.SetBrush(wx.TRANSPARENT_BRUSH)

				w = (((pos * 256) / CUSTOM_COMBOBOX_ANIMATION_DURATION) * width) / 256
				ratio = float(w) / float(width)
				h = int(height * ratio)

				dc.DrawBitmap(self.aniBackBitmap, rect.x, rect.y)
				dc.DrawRectangle(center_x - w / 2, center_y - h / 2, w, h)
			else:
				stopTimer = True

		if stopTimer:
			dc.DrawBitmap(self.aniBackBitmap, rect.x, rect.y)
			popup.Move((0, 0))
			self.aniTimer.Stop()
			self.DoShowPopup(rect, self.aniFlags)

class test(wx.Frame):
	def __init__(self,app):

		wx.Frame.__init__(self,None,-1,'Tool')
		cc = FileSelectorCombo(self, size=(250, -1))
		fgs = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)
		fgs.Add(cc)
		fgs.Add((10, 10))
		fgs.Add(wx.StaticText(self, -1, "Custom popup action, and custom button bitmap"))

		box = wx.BoxSizer()
		box.Add(fgs, 1, wx.EXPAND | wx.ALL, 20)
		self.SetSizer(box)

app = wx.App()
frame = test(app)
frame.Show()
app.MainLoop()
