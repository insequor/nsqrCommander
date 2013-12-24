#=============================================================================
#=== Ozgur Aydin Yuksel, 2008 (c)
#=============================================================================

#=============================================================================
# Additional paths to include the sys.path so required python code can be found
# - first to the location for nsqrPy if that is not already in the python path
#
#=============================================================================
#paths = ['D:\\Home\\oy\\docs\\projects\\nsqrpy.google.code',
#         'D:\\Home\\oy\\projects\\nsqrpy.google.code']
paths = []

#=============================================================================
# Folder where the data items are stored. Leave empty to use the default
# - default path is "<root dir>\data"
#=============================================================================
#dataPath = 'D:\\Home\\oy\\docs\\projects\\nsqrpy.google.code\\nsqrCommander\\data'
#dataPath = 'D:\\Home\\oy\\projects\\nsqrpy.google.code\\nsqrCommander\\data'
dataPath = ''

#=============================================================================
# Folder where the commands are stored. Leave empty to use the default
# - default path is "<root dir>\commands"
#=============================================================================
#commandsPath = ''
#commandsPath = 'D:\\Home\\oy\\docs\\projects\\nsqrpy.google.code\\nsqrPy\\cmdr\\commands'
#commandsPath = 'D:\\Home\\oy\\projects\\nsqrpy.google.code\\nsqrPy\\cmdr\\commands'
commandsPath = ''

#=============================================================================
import os
import sys
def getRootPath():
    import os
    import sys
    
    #First try to parse the root path from given argument
    folder = sys.argv[0]
    num = len(folder.split(os.sep))
    for i in range(num):
        folder = os.path.dirname(folder)
        if os.path.isdir(os.path.join(folder, 'nsqrPy')):
            return folder
            break
    
    #First try to parse the root path from given argument
    folder = os.path.abspath(os.curdir)
    num = len(folder.split(os.sep))
    for i in range(num):
        folder = os.path.dirname(folder)
        if os.path.isdir(os.path.join(folder, 'nsqrPy')):
            return folder
            break
    
    return None

rootPath = getRootPath()
if rootPath:
    paths.append(rootPath)
    dataPath = os.path.join(rootPath, 'nsqrCommander', 'data')
    commandsPath = os.path.join(rootPath, 'nsqrPy', 'cmdr', 'commands')
    #print paths
    #print dataPath
    #print commandsPath

#=============================================================================
if __name__ == '__main__':
    print '''
    This is not a standalone script, it should be used as config file by 
    the actual application
    '''
    

    
