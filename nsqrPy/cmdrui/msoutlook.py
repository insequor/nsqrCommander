import wx
import win32gui as gui
import win32con as con
import win32com as com
import win32com.client
import win32process as process
import pythoncom

import win32clipboard as clipboard

import SendKeys

from defaultapplication import DefaultApplication

#=============================================================================
#===
#=============================================================================

class MSOutlook(DefaultApplication):
    #---
    
    #---
    def __init__(self, hwnd = None):
        '''
        If hwnd is None, current window will be retrieved
        '''
        print 'MSOutlook Application Detected'
        DefaultApplication.__init__(self, hwnd)
        
        self.outlook = com.client.Dispatch('Outlook.Application')
        return 
        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'msoutlook.py'
    
    