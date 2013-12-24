#=============================================================================
#=== Ozgur Aydin Yuksel, 2008 (c)
#=============================================================================
import wx

import nsqrPy
import nsqrPy.cmdr as cmdr
import nsqrPy.cmdrui as cmdrui

try:
    import nsqrPy.tt as tt
except: 
    pass

__doc__ = '''
    Command interface for TT (Team/Task Tracker module)
'''

#=============================================================================
#===Configuration
#=============================================================================
#


#=============================================================================
#===
#=============================================================================
class Command_:
    author = 'Ozgur Aydin Yuksel'
    info = '''Client interface for nsqrPy.tt module: (Team/Task Tracker)'''
    
    #---
    def __getNames(self):
        names = ['ttstart', 'ttweek report'] 
        if tt.session.isPaused():
            names.append('ttresume')
            names.append('ttstop')
        elif tt.session.isStarted():
            names.append('ttpause')
            names.append('ttstop')
        return names
    names = property(__getNames)
    #--
    def __init__(self):
        self.__functions = {'ttstart' : self.__start,
         'ttpause' : self.__pause, 
         'ttresume' : self.__resume,
         'ttstop' : self.__stop,
         'ttweek report' : self.__weekReport}
        
        #self.names = self.__functions.keys()
        print 'cmdTT: %s' % cmdrui.getAppDataDir()
        dbName = 'sqlite:///%s/cmdTT.db' % cmdrui.getAppDataDir()
        dbName = dbName.replace('\\', '/')
        print dbName
        #s = tt.db.session('sqlite:///tt_test.db')
        s = tt.db.session(dbName)
        s.close()
        
    #---
    def __start(self, option):
        if not option:
            return
        task = option.strip()
        if task == '':
            return
        
        tt.session.start(task)
        
    #---
    def __pause(self, option):
        tt.session.pause()
        
    #---
    def __resume(self, option):
        tt.session.resume()
    
    #---
    def __stop(self, option):
        tt.session.stop()
        
    #---
    def __weekReport(self, option):
        '''
        Should generate a weekly report for the sessions
            It should contain daily reports of each tasks
        '''
        print 'Week report is not implemented yet'
    
    def activated(self, name):
        if name == 'ttstart':
            self.options = []
            for task in tt.db.tasks():
                self.options.append(task.name)
        else:
            self.options = None
            
    #--
    def execute(self, name, option):
        try:
            print 'cmdTT.execute (%s, %s)' % (name, option)
            self.__functions[name](option)
            result = True
        except:
            nsqrPy.printException()
            result = False
        return result


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdTT.py'
    
    
    
