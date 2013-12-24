#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================


#=============================================================================
#=== CONFIGURATION PARAMETERS
#=============================================================================

#only given number of elements will be stored in history
maxHistoryItem = 10

#=============================================================================
#===
#=============================================================================
import nsqrPy
import nsqrPy.cmdrui as cmdrui


#=============================================================================
#===
#=============================================================================
class Command :
    '''
    TODO:
    - Formatted text does not work for the moment
    - Shall we save the contents of the clipboard? An option?
    '''
    author = 'Ozgur Aydin Yuksel'
    info = """Add clipboard history for cut/copy/paste operations
    Main limitation is it will rely on common short cut keys (Ctrl+C/V/P)
    """
    
    #--
    def __init__(self):
        self.__history = []
        self.names = ['cut', 'cpy', 'paste']
        self.options = None
    
    #--- 
    def activated(self, name):
        if name == 'paste' and len(self.__history) > 0:
            self.options = self.__history
        else:
            self.options = None
    
    #--
    def execute(self, name, option):
        try:
            result = True
            copyItem = option
            
            if name == 'paste':
                cmdrui.application.selectedText = copyItem
                text = copyItem
            else:
                text = cmdrui.application.selectedText
                if name == 'cut':
                    cmdrui.application.selectedText = ''
                elif name == 'copy':
                    cmdrui.application.selectedText = copyItem
                
            if text != '':
                if text in self.__history:
                    self.__history.remove(text)
                self.__history.insert(0, text)
                cmdrui.putInClipboard(text)
                
            if maxHistoryItem <= 0:
                self.__history = []
            else:
                while len(self.__history) > maxHistoryItem:
                    self.__history.pop()
        except:
            nsqrPy.printException()
            result = False
        return result



#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdexit.py'
    
    
    
