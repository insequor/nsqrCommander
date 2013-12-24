import os
import sys

__doc__ = """Python module that contains several python scripts
            Written by Ozgur Aydin Yuksel, studio insequor, 2005"""
        
        

#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def printException():
    """
    Prints the exception information in case exection is thrown in a
    try/catch block
    """
    e = sys.exc_info ()
    sys.excepthook  ( e[0], e[1], e[2] )
           
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def addToSysPath(path):
    """
    Appends the given path to sys.path list if it is not already in
    """
    try:
        sys.path.index(path)
    except:
        sys.path.append(path)
   
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def getDirPath(name):
    """
    Returns the relative path to the given path name. Given path name 
    should be one of the sblings or one sblings of one of the parent nodes.
    if "bin" is given, possible return values might be "bin, "../bin",
    "../../bin" etc...
    """
    max = len(os.getcwd().split(os.sep))
    dir = name + os.sep 
    count = 0
    while not os.path.isdir(dir) and count < max:
        dir = os.pardir + os.sep + dir
        count += 1
        
    if count > max - 2:
        dir = None
    return dir

#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def getAbsDirPath(name):
    """
    Returns the dirPath but not relative to the current path but absolute
    It simply splits the current path, adds the given name to the path and
    check if the path exist. Each time it removes last dir from the current
    path
    """
    dir = getDirPath(name)
    if dir:
        dir = os.path.abspath(dir)
    return dir

#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def relativePath(spath1, spath2):
    """
    Returns the spath2 as relative to spath1
    """
    rpath = ''
    path1 = os.path.normpath(spath1)
    path2 = os.path.normpath(spath2)
    
    path1 = os.path.abspath(path1)
    path2 = os.path.abspath(path2)
    
    if os.path.splitext(path1)[1] != '':
        path1 = os.path.dirname(path1)

    p1list = path1.split(os.sep)
    p2list = path2.split(os.sep)
    
    if len(p1list) > len(p2list): maxLevel = len(p2list)
    else: maxLevel = len(p1list)
    found = False
    for levelIdx in range(0, maxLevel):
        if p1list[levelIdx] != p2list[levelIdx]:
            found = True
            break
    if not found:
        levelIdx += 1
    for idx in range(levelIdx, len(p1list)):
        rpath += '..' + os.sep
    addsep = False
    for idx in range(levelIdx, len(p2list)):
        if addsep :
            rpath += os.sep
        else:
            addsep = True
        rpath += p2list[idx]
    rpath = os.path.normpath(rpath)
    #if rpath == '.':
    #    print 'here'
    return rpath
    
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def isUnderPath(spath1, spath2):
    """
    checks if spath2 is under spath1
    """
    path1 = os.path.normpath(spath1)
    path2 = os.path.normpath(spath2)
    
    path1 = os.path.abspath(path1)
    path2 = os.path.abspath(path2)
   
    p1list = path1.split(os.sep)
    p2list = path2.split(os.sep)
    
    if len(p2list) <= len(p1list):
        return False
    
    for i in range(len(p1list)):
        if p1list[i] != p2list[i]: return False
    return True
    
    

    
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'test nsqrPy'
    import nsqrPy
    print dir(nsqrPy)
    print nsqrPy.traverser
    
