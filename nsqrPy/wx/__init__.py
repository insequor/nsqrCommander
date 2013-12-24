import os
import sys
import wx
import nsqrPy

__doc__ = """Custom scripts for wxPython
            Written by Ozgur Aydin Yuksel, studio insequor, 2005"""
        
#------------------------------------------------------------------------------
#--- Message redicting for wxLogger
#------------------------------------------------------------------------------
class Redirector :
    def __init__ ( self ):
        try: __t = wx
        except: import wx
        pass
    def write(self, text):
        if text == '\n': #--looks like print sends end of line seperately
            return
        self.printText (text)
    def write(self, text, tags=(), mark='insert'):
        l = len(text)
        if l > 0 and text[l-1] == '\n':
            text = text[:l-1]
        if len(text) > 0:
            self.printText (text)
        
    def writelines(self, l):
        map(self.write, l)
        
    def printText ( self, text ): pass
    
    def flush(self): pass
        
class MsgRedirector ( Redirector ):
    def __init__ ( self ):
        Redirector.__init__ ( self )
        
    def printText ( self, text ):
        wx.LogMessage ( text )
        
class ErrorRedirector ( Redirector ):
    def __init__ ( self ):
        Redirector.__init__ ( self )
        
    def printText ( self, text ):
        wx.LogError ( text )
        


#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
class TestApp ( wx.App ):
    frameCreator = None
    def OnInit (self):
        try:
            sys.stdout = MsgRedirector ()
            sys.stderr = ErrorRedirector ()
            self.frame = TestApp.frameCreator(self)
            try:
                self.frame.afterCreated()
            except:
                pass
        except:
            self.frame = wx.Frame(None, -1, 'FAILED!')
            logWnd = wx.TextCtrl(self.frame, style=wx.TE_MULTILINE)
            wx.Log_SetActiveTarget(wx.LogTextCtrl(logWnd))
            nsqrPy.printException()
            self.frame.Show ()
        self.SetTopWindow (self.frame )
        
        return True
    
def createTestApp(frameCreator):
    """
    Utility function to test frames. It uses TestApp class and given function
    (should be defined as static) to create the main frame. Function should
    not receive any parameters and return a wx.Frame derived object
    
    It also redirects print messages to wx
    """
    try:
        TestApp.frameCreator = frameCreator
        app = TestApp ()
        app.MainLoop()
    except:
        nsqrPy.printException()
        
        
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'test nsqrPy.wx'
    
    #
    def myFrameCreator(app):
        frm = wx.Frame(None, title='Test frame for nsqrPy.wx')
        logWnd = wx.TextCtrl(frm, style=wx.TE_MULTILINE)
        wx.Log_SetActiveTarget(wx.LogTextCtrl(logWnd))
        frm.Show()
        
        print 'This is some sample text', 'with thwo lines'
        print 'And with [%s] ' % ('params')
        return frm
    
    #
    #
    createTestApp(myFrameCreator)
    