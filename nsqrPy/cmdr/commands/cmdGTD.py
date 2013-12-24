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

print 'LOADING GTD'
#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Commands to ease the GDT at work environment'''
    
    
    #--
    def __init__(self):
        self.__functions = {'gtd' : self.__foo}
        
        self.names = self.__functions.keys()
    #--
    def execute(self, name, option):
        try:
            self.__functions[name]()
            result = True
        except:
            nsqrPy.printException()
            result = False
        return result    
    
    #---
    def __foo(self):
        print 'sandox method'
    

#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass
    
    
    
