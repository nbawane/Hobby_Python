import time
import wx

from threading import Thread
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import

########################################################################
class TestThread(Thread):
	"""Test Worker Thread Class."""

	# ----------------------------------------------------------------------
	def __init__(self):
		"""Init Worker Thread Class."""
		Thread.__init__(self)
		self.start()  # start the thread

	# ----------------------------------------------------------------------
	def run(self):
		"""Run Worker Thread."""
		# This is the code executing in the new thread.
		for i in range(6):
			time.sleep(10)
			wx.CallAfter(self.postTime, i)
		time.sleep(5)
		wx.CallAfter(pub.sendMessage, "update", "Thread finished!")

	# ----------------------------------------------------------------------
	def postTime(self, amt):
		"""
		Send time to GUI
		"""
		amtOfTime = (amt + 1) * 10
		pub.sendMessage("update", amtOfTime)


########################################################################
class MyForm(wx.Frame):
	# ----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")

		# Add a panel so it looks the correct on all platforms
		panel = wx.Panel(self, wx.ID_ANY)
		self.displayLbl = wx.StaticText(panel, label="Amount of time since thread started goes here")
		self.btn = btn = wx.Button(panel, label="Start Thread")

		btn.Bind(wx.EVT_BUTTON, self.onButton)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.displayLbl, 0, wx.ALL | wx.CENTER, 5)
		sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
		panel.SetSizer(sizer)

		# create a pubsub receiver
		pub.subscribe(self.updateDisplay, "update")

	# ----------------------------------------------------------------------
	def onButton(self, event):
		"""
		Runs the thread
		"""
		TestThread()
		self.displayLbl.SetLabel("Thread started!")
		btn = event.GetEventObject()
		btn.Disable()

	# ----------------------------------------------------------------------
	def updateDisplay(self, msg):
		"""
		Receives data from thread and updates the display
		"""
		t = msg.data
		if isinstance(t, int):
			self.displayLbl.SetLabel("Time since thread started: %s seconds" % t)
		else:
			self.displayLbl.SetLabel("%s" % t)
			self.btn.Enable()


# ----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
	app = wx.PySimpleApp()
	wx.ComboCtrl()
	frame = MyForm().Show()
	app.MainLoop()