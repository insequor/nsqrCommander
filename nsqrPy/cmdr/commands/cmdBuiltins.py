#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================
import wx

import nsqrPy
import nsqrPy.cmdr as cmdr
import nsqrPy.cmdrui as cmdrui

#=============================================================================
#===Configuration
#=============================================================================
#This command does not need any configuration parameters...


#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Currently only exits the Cmdr application. It should receive the 
    application name as input later.'''
    
    
    #--
    def __init__(self):
        self.__functions = {'capslock' : self.__capslock,
         'exit' : self.__exit, 
         #'help' : self.__help,
         'hide log window' : self.__hideLogWindow,
         #'preferences' : self.__preferences,
         'refresh' : self.__refresh,
         'show log window' : self.__showLogWindow}
        
        self.names = self.__functions.keys()
        
    
    #---
    def __capslock(self):
        cmdrui.sendKeys('{CAPSLOCK}')
        
    #---
    def __exit(self):
        wx.GetApp().Exit()
        
    #---
    def __help(self):
        print 'help'
        assert(0)
    
    #---
    def __hideLogWindow(self):
        cmdrui.logWindow.Hide()
        
    #---
    def __preferences(self):
        print 'preferences'
        print cmdr.manager
    
    #---
    def __refresh(self):
        cmdr.Manager.instance.refresh()
        
    #---
    def __showLogWindow(self):
        cmdrui.logWindow.Show()
        print 'show window'
    #--
    def execute(self, name, option):
        try:
            self.__functions[name]()
            result = True
        except:
            nsqrPy.printException()
            result = False
        return result


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdexit.py'
    
    
    
