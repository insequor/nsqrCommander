#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================
import nsqrPy
from nsqrPy.cmdr import Manager
import os
import win32gui
import win32api
import win32con
import wx

import SendKeys

#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = ''' '''
        
    #--
    def __init__(self):
        self.command = ''
        self.functions = {'close':self.__close,
                          'minimize':self.__minimize,
                          'maximize':self.__maximize}
        self.names = []
        
    #--
    def execute(self):
        try:
            print 'execute: ' + self.command
            print Manager.instance.lastWindowHandle
            function = self.functions[self.command]
            function(Manager.instance.lastWindowHandle )
            result = True
        except:
            result = False
            nsqrPy.printException()
        return result
    
    #---
    def getNames(self):
        return ['close', 'minimize', 'maximize']
    
    #
    def getOptions(self):
        return []
    
    #
    def activated(self, name):
        self.command = name
        
    #---
    def push(self, iName):
        self.command = iName
        return self
    
    #---
    def pop(self):
        self.command = ''
        return self
    
    #
    def __close(self, hwnd):
        print 'close window'
        win32gui.SendMessage(hwnd, 6374, 0, 0)
    
    #
    def __minimize(self, hwnd):
        print 'minimize window'
        win32gui.CloseWindow(hwnd)
    
    #
    def __maximize(self, hwnd):
        print 'maximize window'
        #p = self.GetWindowPlacement()
        #if p[1]==win32con.SW_MINIMIZE or p[1]==win32con.SW_SHOWMINIMIZED:
        #	self.SetWindowPlacement(p[0], win32con.SW_RESTORE, p[2], p[3], p[4])

#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdwindow.py'
    
    
    
