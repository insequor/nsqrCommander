#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================
import nsqrPy

from win32gui import * 
from win32con import * 


gwl_style = GWL_STYLE 

#--
def enumerationHandler(hwnd, resultList): 
    if IsWindowVisible(hwnd): 
        val = GetWindowLong(hwnd, gwl_style) 
        if val & WS_VISIBLE: 
            if not val & WS_CHILD: 
                if not val & WS_EX_TOOLWINDOW: 
                    if val & WS_EX_CONTROLPARENT: 
                        txt = GetWindowText(hwnd) 
                        txt = txt.strip()
                        if not resultList.has_key(txt):
                            resultList[txt] = hwnd
                                    
#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = 'Replacement for Alt+Tab, switches between running applications'
    
    #---
    def __getOptions(self):
        options = []
        for item in self.__options:
            options.append(item)
        return options        
    options = property(__getOptions)
    
    #---
    def __init__(self):
        self.names = ['go', 'switch']
        #self.options is provided through the property
        
    #--
    def activated(self, name):
        '''
        '''
        self.__options = {}
        EnumChildWindows(GetDesktopWindow(), enumerationHandler, self.__options)
      
    #--
    def execute(self, name, option):
        result = False
        try:
            text = option.strip()
            hwnd = self.__options[text]
            ShowWindow(hwnd, 1)
            BringWindowToTop(hwnd)
            SetActiveWindow(hwnd)
            SetForegroundWindow(hwnd)
            result = True
        except:
            result = False
            nsqrPy.printException()
        return result


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdswitch.py'
    cmd = CmdSwitch()
    cmd.activated()
    print cmd.getOptions()
    