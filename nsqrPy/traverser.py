#==============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#==============================================================================

import os
import sys

__doc__ = """Traverser script for qrSearch
You can register your own functions for folder and file processing. For file 
processing you have options to register for all extensions or per extension. If 
there is an handler for all extensions, that will be called before any other.
"""


class IgnoreMode:
    """
    Ignore codes for traversing which handler functions should return
    """
    none = 0
    folder = 1
    folders = 2
    files = 3
    file = 4

__folderHandler = None

__fileHandler = {}

#==============================================================================
#===
#==============================================================================
def setFolderHandler(iHandler):
    """
    iHandler: Handler function
    
    Set a handler function for the traversed folders. It returns the old handler
    function if any. A handler function should return True or False value. If it 
    returns False folder and its contents are not traversed. Function should have
    the following signature:
    
    def myHandler(iPath, iName, iFullPath):
        ...
        return True/False
    Where:
        iPath = Path containing the folder, including the driver info
        iName = Name of the folder (without the path)
        iFullPath = iPath + os.sep + iName
    """
    global __folderHandler
    oldHandler = __folderHandler
    __folderHandler = iHandler
    return oldHandler


#==============================================================================
#===
#==============================================================================
def setFileHandler(iExtension, iHandler):
    """
    iExtension: Extension of the file to set an handler. Valid values are:
        None: For all extensions
        ''  : For no extensions
        '.<ext>: For specific (<ext>) extension
    iHandler: Hander Function
    
    Sets a handler function for traversed files. It returns the old handler function
    if any. Handler functions are set per extension or for all files. If there 
    is a function set for all files, it will be called first. If it returns 
    True and if there is any function set for the current extension then the 
    second function will be called.
    
    Handler function should have the following signature:
    
    def myHandler(iPath, iName, iExtension, iFullPath):
        ...
        return True/False
    Where:
        iPath = Path containing the folder, including the driver info
        iName = Name of the folder (without the path)
        iExtension = Extension of the file being traversed (including the dot)
        iFullPath = iPath + os.sep + iName
    """
    global __fileHandler
    if __fileHandler.has_key(iExtension):
        oldHandler = __fileHandler[iExtension]
    else:
        oldHandler = None
    __fileHandler[iExtension] = iHandler
    return oldHandler



#==============================================================================
#===
#==============================================================================
def __handleFolder(iPath, iName, iFullPath):
    """
    
    """
    global __folderHandler

    ignore = None
    if __folderHandler is not None:
        ignore = __folderHandler(iPath, iName, iFullPath)
    
    if (ignore == IgnoreMode.folder):
        return
    
    names = os.listdir(iFullPath)
    for name in names:
        targetPath = iFullPath + os.sep + name
        if os.path.isdir(targetPath) and ignore != IgnoreMode.folders:
            __handleFolder(iFullPath, name, targetPath)
        elif os.path.isfile(targetPath) and ignore != IgnoreMode.files:
            __handleFile(iFullPath, name, targetPath)
    
    pass
    
#==============================================================================
#===
#==============================================================================
def __handleFile(iPath, iName, iFullPath):
    """
    """
    global __fileHandler
    ext = os.path.os.path.splitext(iName)[1].lower()
    if __fileHandler.has_key(ext):
        handler = __fileHandler[ext]
        if handler != None:
            handler(iPath, iName, ext, iFullPath)
            
    
#==============================================================================
#===
#==============================================================================
def traverse(iFullPath):
    """
    """
    if not os.path.isdir(iFullPath):
        print 'Given path ' + iFullPath + 'is not a folder to traverse!'
        return
    
    splitted = os.path.split(iFullPath)
    parentPath = splitted[0]
    name = splitted[1]
    
    print parentPath
    print name
    
    __handleFolder(parentPath, name, iFullPath)    
    
   

#==============================================================================
#===
#==============================================================================
if __name__ == '__main__':
    import config
    print 'this is main from traverser.py'
    
    class myClass:
        def __init__(self, iName):
            self.name = iName
        def myFolderHandler(self, iPath, iName, iFullPath):
            try:
                idx = config.ignoreFolderList.index(iName)
                return IgnoreMode.folder
            except:
                idx = -1

            if idx != -1:
                ignore = IgnoreMode.folder 
            elif iName != 'src':
                ignore = IgnoreMode.files 
            else:
                print self.name + ' myFolderHandler: '  + iFullPath
                ignore = IgnoreMode.folders 
            return ignore
            
            
        def myFileHandler(self, iPath, iName, iExtension, iFullPath):
            if iExtension != '.cpp':
                return IgnoreMode.file
            
            print self.name + ' myFileHandler: ' + iFullPath
            return IgnoreMode.none
    
    my = myClass('test')
    setFolderHandler(my.myFolderHandler)
    setFileHandler(None, my.myFileHandler)
    setFileHandler('.xml', my.myFileHandler)
    
    print sys.argv
    numDirs = len(sys.argv)
    if numDirs == 1:
        traverse('E:\Ozgur\WS\R7A_Verification')
    else:
        for i in range(1, numDirs):
            print i
            traverse(sys.argv[i])
        
