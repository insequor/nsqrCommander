import wx

#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
class LabeledCtrl(wx.Panel):
    """A label control which holds given children in a horizontal sizer"""
    def __init__(self, parent, label, labelSize=(100,20)):
        wx.Panel.__init__(self, parent, -1, size=labelSize,
                          style=wx.WS_EX_VALIDATE_RECURSIVELY )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lblCtrl = wx.StaticText(self, -1, label, size=labelSize)
        sizer.Add(lblCtrl, 0, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.SetSizeHints(self)
        
    def addCtrl(self, ctrl):
        self.GetSizer().Add(ctrl, 1, wx.EXPAND)
        self.GetSizer().Layout()