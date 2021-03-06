#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================
import sys
import os
import wx

import config

for path in config.paths:
    if not path in sys.path: 
        sys.path.append(path)
        
appFolder = os.path.dirname(sys.argv[0])
appFolder = os.path.dirname(appFolder)
    
if config.dataPath != '':
    appDataFolder = config.dataPath + os.sep
else:    
    appDataFolder = os.path.join(appFolder, 'data' + os.sep)


if config.commandsPath != '':
    appCommandsFolder = config.commandsPath
else:    
    appCommandsFolder = os.path.join(appFolder, 'commands')


import nsqrPy
import nsqrPy.wx 
import nsqrPy.cmdr as cmdr
import nsqrPy.cmdrui as cmdrui

cmdr.Manager.configFolder = appCommandsFolder

#from nsqrPy.cmdrui.simplepanel import SimplePanel as GUIPanel
from nsqrPy.cmdrui.htmlpanel import SimplePanel as GUIPanel

#=============================================================================
#===
#=============================================================================

class SimplePanelFrame ( wx.Frame ):
    def __init__ (self):
        wx.Frame.__init__ (self, None, -1, 'nsqrCommander-Desktop',
        #style= wx.RESIZE_BORDER|wx.FRAME_TOOL_WINDOW|wx.CAPTION|wx.STAY_ON_TOP)
        style = wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.SetTransparent(188)
        manager = None         
        try:
            manager = cmdr.Manager()
            manager.refresh()
        except:
            manager = None
            nsqrPy.printException()
            
        self.panel = GUIPanel(self, manager)
        self.SetSize((800, 450))
        self.Centre()
               
        self.controller = cmdrui.Controller(manager, self.panel)    
    
    #---
    def afterCreated(self):
        self.Hide()

   
#=============================================================================
#===
#=============================================================================
class TestApp ( wx.App ):
    def __init__(self):
        wx.App.__init__(self)
        self.ProcessMessage = None
        
        
    def OnInit (self):
        try:
            self.SetAppName('nsqrCommander')
            
            global appDataFolder
            
            sys.stdout = nsqrPy.wx.MsgRedirector ()
            sys.stderr = nsqrPy.wx.ErrorRedirector ()
        
            cmdrui.logWindow = wx.Frame(None, -1, 'nsqrCommander - Log Window')
            cmdrui.logWindow.Bind(wx.EVT_CLOSE, self.__onClosingLogWindow)
            logWnd = wx.TextCtrl(cmdrui.logWindow, size=(0,150), style=wx.TE_MULTILINE)
            wx.Log_SetActiveTarget(wx.LogTextCtrl(logWnd))
            cmdrui.logWindow.SetSize((600, 400))
            cmdrui.logWindow.Show()
            
            print 'log window is activated'
            
            self.__tbIcon = wx.TaskBarIcon ()
            iconFile = appDataFolder + 'app_icon.ico'
            icon = wx.Icon (iconFile, wx.BITMAP_TYPE_ICO)
            if not self.__tbIcon.SetIcon (icon, 'nsqrCommander'):
                print 'Could not set icon.'
                
            self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.__onEvtTaskbarLeftUp)
            
            self.__frame = SimplePanelFrame()
            self.__frame.Hide()
        except:
            self.__frame = wx.Frame(None, -1, 'FAILED!')
            logWnd = wx.TextCtrl(self.__frame, size=(0,150), style=wx.TE_MULTILINE)
            wx.Log_SetActiveTarget(wx.LogTextCtrl(logWnd))
            nsqrPy.printException()
            self.__frame.Show ()
        
        if self.__frame:
            self.SetTopWindow (self.__frame )
        
        return True
        
    #---
    def OnExit(self):
        if self.__tbIcon:
            self.__tbIcon.RemoveIcon ()
    
    #---
    def __onEvtTaskbarLeftUp(self, evt):
        self.ExitMainLoop ()
        self.ProcessIdle ()
    
    #---
    def __onClosingLogWindow(self, evt):
        '''We override the close event for the log window so it will be hidden only'''
        cmdrui.logWindow.Hide()
        

#=============================================================================
#===
#=============================================================================
def main():
    app = TestApp()
    app.MainLoop()
    f = file('ozgur.txt', 'w')
    f.write('some text')
    f.close()
    
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    main()
    
        
