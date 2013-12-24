#=============================================================================
#=== Ozgur Aydin Yuksel, 2008 (c)
#=== 
#=== Setup script to generate executable with py2exe
#=============================================================================


from distutils.core import setup
import py2exe
 
import sys
import os

try:
    if len(sys.argv) == 1:
        sys.argv.append('py2exe')

    opts = {
        "py2exe": {
            "dist_dir": "bin",
        }
    }

    packages = ['pickle', 
                'pyHook', 
                'wx', 
                'wx.html',
                'SendKeys', 
                'win32con', 
                'win32com',
                'win32com.client',
                'win32api', 
                'win32gui',
                'win32process', 
                'win32clipboard',
                'getpass']
    setup(
        options = {'py2exe': 
                        {'bundle_files':3, 
                         'includes':packages,
                         'dist_dir':'../../nsqrCommanderLauncher',
                         'compressed':1,
                         'optimize':2
                        }
                  },
        windows = [ 
                    {'script': 'launcher.py',
                     "icon_resources": [(1, "../data/app_icon.ico")]}
                  ],
                
        #console = [ 
        #            {'script': 'launcher.py'}
        #          ],
                
        zipfile = "lib/python25.zip",
    )

except:
    e = sys.exc_info ()
    sys.excepthook  ( e[0], e[1], e[2] )
