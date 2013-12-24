#-----------------------------------------------------------------------------
import getpass
import time
import datetime

import db #nsqrPy.tt.db 

__doc__ = '''
Session management for tt module. Developer's activity is managed by sessions 
within each session developer does a specific activity. Following events are 
related with sessions:
    * start
    * pause
    * resume
    * stop
    
'''

verbose = True

#------------------------------------------------------------------------------
def start(task, user=None, logtime=None, sess=None):
    '''
    Logs a start event 
        task: name of the task to be started, it will be added to the tasks table
        user: if not given login user name will be used
        logtime: datetime.datetime object, if not given current time will be used
    '''      
    if user is None:
        user = getpass.getuser()
    if logtime is None:
        logtime = datetime.datetime.now()
    if isStarted(user, sess):
        if verbose:
            print 'There is already an active task, sending stop for it'
        stop(user, logtime)
    event = db.Event.add(user, db.Events.start, logtime, task, sess)
    if verbose:
        print '> logging start event for: %s' % task
        print '>  user     = %s' % user
        print '>  log time = %s' % str(logtime)
    return event

#------------------------------------------------------------------------------    
def pause(user=None, logtime=None, sess=None):
    '''
    '''
    if user is None:
        user = getpass.getuser()
    if logtime is None:
        logtime = datetime.datetime.now()
    event = db.Event.add(user, db.Events.pause, logtime, sess=sess)
    if verbose:
        print '> logging pause event'
        print '>  user     = %s' % user
        print '>  log time = %s' % str(logtime)
    return event

#------------------------------------------------------------------------------
def resume(user=None, logtime=None, sess=None):
    '''
    '''
    if user is None:
        user = getpass.getuser()
    if logtime is None:
        logtime = datetime.datetime.now()
    event = db.Event.add(user, db.Events.resume, logtime, sess=sess)
    if verbose:
        print '> logging resume event'
        print '>  user     = %s' % user
        print '>  log time = %s' % str(logtime)
    return event

#------------------------------------------------------------------------------    
def stop(user=None, logtime=None, sess=None):
    '''
    '''
    if user is None:
        user = getpass.getuser()
    if logtime is None:
        logtime = datetime.datetime.now()
    event = db.Event.add(user, db.Events.stop, logtime, sess=sess)
    if verbose:
        print '> logging stop event'
        print '>  user     = %s' % user
        print '>  log time = %s' % str(logtime)
    return event

#------------------------------------------------------------------------------
def isStarted(user=None, sess=None):
    '''
    Returns True if the last event from user is Events.start, pause or resume
    otherwise False
    '''
    if user is None:
        user = getpass.getuser()
    if sess is None:
        s = db.session()
    else:
        s = sess
    user = db.User.get(user, s)
    event = user.lastEvent()
    if not event:
        return False
    if event.id != db.Events.stop:
        return True
    return False
    
    
#------------------------------------------------------------------------------
def isPaused(user=None, sess=None):
    '''
    Returns True if the last event from user is Events.pause, otherwise False 
    '''
    if user is None:
        user = getpass.getuser()
    if sess is None:
        s = db.session()
    else:
        s = sess
    user = db.User.get(user, s)
    event = user.lastEvent()
    if not event:
        return False
    if event.id == db.Events.pause:
        return True
    return False
    
#------------------------------------------------------------------------------
def weekReport(year=None, month=None, day=None, week=None):
    '''
    Should return the report object for given day
    TODO: This should take the user name and day for the event
    week=week number
    year, month, day: date to be used to find the week number for the report
    '''
    startDate = None
    endDate = None
    if week is not None:
        assert(False, 'week number is not implemented yet')
    else:
        assert(year is not None and month is not None and day is not None)
        startDate = datetime.datetime(year, month, day)
        startDate = startDate - datetime.timedelta(startDate.weekday())
        endDate = startDate + datetime.timedelta(4)
    assert(startDate is not None and endDate is not None)
    startNum = startDate.year * 10000 + startDate.month * 100 + startDate.day
    endNum = endDate.year * 10000 + endDate.month * 100 + endDate.day
    
    s = db.session()
    events = s.query(db.Event).filter(db.Event.date>=startNum and db.Event.date <= endNum).all()
    for event in events:
        print event
    
    if 0:
        #reports is a dictionary which will keep the generated report for each user
        reports = {}
        content = ''
        for event in db.events():
            if reports.has_key(event.userId):
                report = reports[event.userId]
            else:
                report = []
                reports[event.userId] = report
            
            content += '>>> ' + str(event) + '\n'
        return None

#------------------------------------------------------------------------------
class SessionInfo:
    def __init__(self, id):
        self.id = id
        self.events = []
        
    def addEvent(self, event):
        if len(self.events) == 0:
            assert(event.id == db.Events.start)            
        else:
            assert(event.id != db.Events.start)
            assert(event.sessionId == self.id)
            assert(event.taskId == self.events[0].taskId)
        self.events.append(event)
        
    def totalTime(self):
        '''
        Returns the total spent time as datetime.timedelta object
        '''
        num = len(self.events)
        assert(num > 1)
        startDate = self.events[0].datetime()
        endDate = self.events[num-1].datetime()
        print 'Total: ', endDate - startDate
        return endDate - startDate
        pass
        
    def pausedTime(self):
        '''
        Returns the total paused time as datetime.timedelta object
        '''
        num = len(self.events)
        assert(num > 1)
        pauseStart = None
        pauseEnd = None
        pausedTime = datetime.timedelta()
        for event in self.events:
            if pauseStart is None:
                assert(event.id != db.Events.resume)
                if event.id == db.Events.pause:
                    pauseStart = event.datetime()
            elif pauseEnd is None:
                assert(event.id != db.Events.pause and event.id != db.Events.start)
                pauseEnd = event.datetime()
                pausedTime += pauseEnd - pauseStart
                pauseStart = None
                pauseEnd = None
            else:
                assert(False)
        print 'Paused: ', pausedTime
        return pausedTime
            
    def startTime(self):
        assert(len(self.events) > 1)
        return self.events[0].date
    
    def endTime(self):
        assert(len(self.events) > 1)
        return self.events[len(self.events)-1].date
        
#------------------------------------------------------------------------------
def dayReport(year=None, month=None, day=None):
    '''
    '''
    assert(year is not None and month is not None and day is not None)
    startNum = year * 10000 + month * 100 + day
    
    s = db.session()
    events = s.query(db.Event).filter(db.Event.date==startNum).all()
    idx = 0
    #ignore all events before the first start
    for event in events:
        print event.id
        print event
        if event.id == db.Events.start:
            break
        idx += 1
    print 'first start found in ', idx
    events = events[idx:]
        
    #create SessionInfo objects for....
    sessionInfo = None
    sessions = []
    for event in events:
        print event
        if sessionInfo is None or sessionInfo.id != event.sessionId:
            sessionInfo = SessionInfo(event.sessionId)
            sessions.append(sessionInfo)
        sessionInfo.addEvent(event)
    
    print 'Sessions..... ', len(sessions)
    
    for sessionInfo in sessions:
        sessionInfo.totalTime()
        sessionInfo.pausedTime()
    if 0:
        #reports is a dictionary which will keep the generated report for each user
        reports = {}
        content = ''
        for event in db.events():
            if reports.has_key(event.userId):
                report = reports[event.userId]
            else:
                report = []
                reports[event.userId] = report
            
            content += '>>> ' + str(event) + '\n'
        return None

#------------------------------------------------------------------------------
if __name__ == '__main__':
    if 0:
        import test_session
        test_session.startTest()
    elif 1:
        s = db.session('sqlite:///tt_test.db')
        s.close()
        #fillFromLogFile('D:\\Home\\oy\\tools\\nsqrpy.google.code\\nsqrPy\\tt\\logfile.log')
        dayReport(2008, 5, 23)
    else:
        fillSampleData()
        
        print '>>>>'
        dayReport(2008, 5, 31)
        