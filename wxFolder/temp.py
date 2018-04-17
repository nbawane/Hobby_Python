import sys
import wx
def my_excepthook(type, value, traceback):
    print 'Unhandled error:', type, value

sys.excepthook = my_excepthook
wx.GetApp().GetTopWindow()
print 'Before exception'

raise RuntimeError('This is the error message')

print 'After exception'