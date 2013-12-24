#=============================================================================
#=== Ozgur Aydin Yuksel, 2008 (c)
#=============================================================================

import sys
import os

   
#=============================================================================
if __name__ == '__main__':
    '''
    launcher application written so it can emulate the python development environment
    without the need to install python and all required modules. It can take two 
    arguments:
        1: Script to execute (just the name, no extension): It should have a "main"
           function which will be called after importing the script
        2: Script path: Where the script is located
        
    Both arguments are optional. If script name is not given then "application" will be
    imported. If second argument is not given than path will be parsed from application 
    and current path. In both cases "nsqrCommander" folder will be searched to locate the
    "nsqrCommander\src" folder. Same search is also done to locate the "nsqrPy" folder
    '''
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'application'
        
    if len(sys.argv) > 2:
        scriptPath = sys.argv[2]
        if not scriptPath in sys.path:
            sys.path.append(scriptPath)
    else:
        commanderPath = None
        folder = sys.argv[0]
        num = len(folder.split(os.sep))
        for i in range(num):
            folder = os.path.dirname(folder)
            if os.path.isdir(os.path.join(folder, 'nsqrCommander')):
                commanderPath = folder
                break
        if not commanderPath:
            folder = os.path.abspath(os.curdir)
            num = len(folder.split(os.sep))
            for i in range(num):
                folder = os.path.dirname(folder)
                if os.path.isdir(os.path.join(folder, 'nsqrCommander')):
                    commanderPath = folder
                    break
        
        if commanderPath:
            commanderPath = os.path.join(commanderPath, 'nsqrCommander', 'src')
            if not commanderPath in sys.path:
                sys.path.append(commanderPath)
    
    try:
        exec 'import ' + name
        exec name + '.main()'
    except:
        print 'An error occurred while executing given script!'
        e = sys.exc_info ()
        sys.excepthook  ( e[0], e[1], e[2] )