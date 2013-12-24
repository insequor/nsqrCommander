#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

#=============================================================================
#=== CONFIGURATION PARAMETERS
#=============================================================================
import nsqrPy
import nsqrPy.cmdrui as cmdrui

import os
import wx

#=============================================================================
#===
#=============================================================================
class Command:
    '''
    '''
    author = 'Ozgur Test'
    info = 'Open selected folder, application'
    
    #--
    def __init__(self):
        self.names = ['open']
        self.options = []
        
        self.__optionMap = None
        self.__params = []        
        self.__parse()
        
    #--
    def activated(self, name):
        #parsing is done only in constructor, user has to send refresh command
        #to recall the parse
        #self.__parse()
        pass
        
    #---
    def execute(self, name, option):
        result = False
        try:
            if self.__optionMap.has_key(option):
                exe = '"' + self.__optionMap[option] + '"'
                os.startfile(exe)
                result = True
            elif option.startswith('http://') or option.startswith('https://') or option.startswith('www.'):
                exe = '"' + option + '"'
                os.startfile(exe)
                result = True
                   
        except:
            nsqrPy.printException()
            result = False
        return result
        
    #--
    def __parse(self):
        sp = wx.StandardPaths.Get()
        #User Related folders
        configDir = cmdrui.getConfigDir()
        userDir = cmdrui.getUserDir()
        quickLaunchFolder = configDir + '\\Microsoft\\Internet Explorer\\Quick Launch'
        userStartFolder = userDir + '\\Start Menu'
        favoritesFolder = userDir + '\\Favorites'
        #All User Folders
        configDir = cmdrui.getConfigDir(True)
        userDir = cmdrui.getUserDir(True)
        allUserStartFolder = userDir + '\\Start Menu'
        allUserFavoritesFolder = userDir + '\\Favorites'

            
        searchFolders = [quickLaunchFolder, 
                         userStartFolder, 
                         allUserStartFolder, 
                         favoritesFolder, 
                         allUserFavoritesFolder]
                        
        
        extraApplications = []

        self.__optionMap = {}
        #-- Add the application from start menu settings
        def walkfunc(arg, dirname, fnames):
            for fname in fnames:
                name, ext = os.path.splitext(fname)
                shortname = os.path.basename(name)
                
                if ext.lower() == '.lnk' or ext.lower() == '.scf':
                    if arg.has_key(shortname):
                        names = dirname.split(os.sep)
                        num = len(names)
                        for i in range(1, num):
                            shortname = os.path.join(names[num - i], shortname)
                            if not arg.has_key(shortname):
                                break
                    assert(not arg.has_key(shortname))
                    arg[shortname] = dirname + os.path.sep + fname
                    
        #--
        for spath in searchFolders:
            os.path.walk(spath, walkfunc, self.__optionMap)

        for app in extraApplications:
            try:
                if not self.__optionMap.has_key(app[0]):
                    self.__optionMap[app[0]] = app[1]
            except:
                pass
                
        self.options = self.__optionMap.keys()
        self.options.sort()        


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdopen.py'
    
    
    
    
    
