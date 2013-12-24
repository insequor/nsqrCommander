#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================
import nsqrPy
import nsqrPy.cmdr as cmdr
import nsqrPy.cmdrui as cmdrui

import os

#=============================================================================
#===Configuration
#=============================================================================

#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''
    Switching between pages of a single application if application provides
    any
    '''
    
    #---
    def __getNames(self):
        if cmdrui.application and len(cmdrui.application.windows):
            return ['pages']
        return []
    names = property(__getNames)
    
    #---
    def __getOptions(self):
        return self.__options.keys()
    options = property(__getOptions)
    
    #--
    def __init__(self):
        self.__options = {}
        
    #--
    def activated(self, name):
        try:
            options = {}
            assert(cmdrui.application)
            for wnd in cmdrui.application.windows:
                wndname = cmdrui.application.getWindowTitle(wnd)
                if options.has_key(wndname):
                    fullPath = cmdrui.application.getWindowPath(wnd)
                    paths = fullPath.split(os.sep)
                    num = len(paths)
                    for i in range(num):
                        wndname = os.path.join(paths[num - i - 2], wndname)
                        if not options.has_key(wndname):
                            break
                assert(not options.has_key(wndname))
                options[wndname] = wnd
        except:
            options = {}
            nsqrPy.printException()
        self.__options = options
         
    #--
    def execute(self, name, option):
        try:
            result = True
            if self.__options.has_key(option):
                assert(cmdrui.application)
                wnd = self.__options[option]
                cmdrui.application.showWindow(wnd)
        except:
            nsqrPy.printException()
            result = False
        return result
    


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'cmdPages'
    