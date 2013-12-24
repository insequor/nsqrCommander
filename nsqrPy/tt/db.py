#------------------------------------------------------------------------------
import os

import time
import datetime

import sqlalchemy as sqla
import sqlalchemy.orm as orm

#------------------------------------------------------------------------------
__doc__ = '''
    --- Tables ----------------------------------------------------------------
    tbl_users
        Simple user name-id table
        
    tbl_tasks
        Tasks are user indenpendent. This lets us keeping track of all effort 
        done on a certain task even the effort is from different users.
        
    tbl_events
        start, stop, pause, resume events are stored with the event data and 
        time. Duration information is not stored with the events. It has to be
        derived at runtime
        
        Each event between a start and stop on a certain task is considered a 
        session (continious working period on a certain task). 
'''

verbose = True
__session = None

#------------------------------------------------------------------------------
# Module functions
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def session(dbName=None):
    '''
    Returns a session instance to interact with database
        dbName: Name of the database file, if none given memory db will be used
    '''
    global __session
    if not __session:
        #engine = sqla.create_engine('sqlite:///tt_test.db', echo=False)
        if not dbName:
            engine = sqla.create_engine('sqlite:///:memory:', echo=False)
        else:
            engine = sqla.create_engine(dbName, echo=False)
            
        metadata = sqla.MetaData()
        tbl_users = sqla.Table('tbl_users', metadata,
            sqla.Column('id', sqla.Integer, primary_key=True),
            sqla.Column('name', sqla.String(20)))
            
        tbl_tasks = sqla.Table('tbl_tasks', metadata,
            sqla.Column('id', sqla.Integer, primary_key=True),
            sqla.Column('name', sqla.Text))
        
        tbl_events = sqla.Table('tbl_events', metadata,
            sqla.Column('userId', sqla.Integer, sqla.ForeignKey('tbl_users.id'), primary_key=True),
            sqla.Column('taskId', sqla.Integer, sqla.ForeignKey('tbl_tasks.id'), primary_key=True),
            sqla.Column('sessionId', sqla.Integer, primary_key=True),
            sqla.Column('id', sqla.Integer, primary_key=True),
            sqla.Column('date', sqla.Integer, primary_key=True),
            sqla.Column('time', sqla.Integer, primary_key=True))
        
        metadata.create_all(engine)
        
        #
        #backref field in relation indicates that relation is bi-directional. we can get back to 
        #the file information from a given tag object simple by calling tag.file. This will return
        #a single record from files table
        #
        orm.mapper(User, tbl_users, properties={'events':orm.relation(Event, backref='user', cascade="all")})
        orm.mapper(Task, tbl_tasks, properties={'events':orm.relation(Event, backref='task', cascade="all")})
        orm.mapper(Event, tbl_events)
          
        
        __session = orm.sessionmaker(bind=engine, autoflush=True, transactional=True)
    
    return __session()

#------------------------------------------------------------------------------
def destroySession():
    global __session
    __session = None

#------------------------------------------------------------------------------
def clean():
    '''
    cleans all the tables in the database without destroying the tables themselves
    '''
    Event.clean()
    User.clean()
    Task.clean()
        
#------------------------------------------------------------------------------
def tasks(name=None, sess=None):
    '''
    Returns all tasks. If name is given results will be limited to those have
    given name in their name field (contains, not identical)
    '''
    if sess is None:
        s = session()
    else:
        s = sess
    if name is None:
        results = s.query(Task).all()
    else:
        results = s.query(Task).filter(Task.name.like('%'+name+'%')).all()
    if sess is None:
        s.close()
    return results
    
    
#------------------------------------------------------------------------------
def users(sess=None):
    if sess is None:
        s = session()
    else:
        s = sess
    results = s.query(User).all()
    if sess is None:
        s.close()
    return results

#------------------------------------------------------------------------------
def events(sess=None):
    if sess is None:
        s = session()
    else:
        s = sess
    results = s.query(Event).all()
    if sess is None:
        s.close()
    return results

#------------------------------------------------------------------------------
# Record related classes
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class User(object):
    '''
    '''
    @staticmethod
    def get(name, sess=None):
        '''
        Automatically create a user or return the one from DB
        '''
        if type(name) is not str and type(name) is not unicode:
            raise TypeError('Expecting string object')
        
        if sess is None:
            s = session()
        else:
            s = sess
            
        user = s.query(User).filter(User.name==name).first()
        if user is None:
            user = User(name)
            s.save(user)
            s.commit()
            user = s.query(User).filter(User.name==name).first()
        if sess is None:
            s.close()
        return user
    
    @staticmethod
    def remove(user, sess=None):        
        if sess is None:
            s = session()
        else:
            s = sess
        if type(user) == User:
            s.delete(user)
        elif type(user) is str or type(user) is unicode:
            s.delete(User.get(user))
        else:
            raise TypeError('Expecting User or string object')
        s.commit()
        if sess is None:
            s.close()
        
    @staticmethod
    def clean(sess=None):
        '''
        Clean all entries from this table
        '''
        if sess is None:
            s = session()
        else:
            s = sess
        for entry in s.query(User).all():
            s.delete(entry)
        s.commit()
        if sess is None:
            s.close()
    
       
    def __init__(self, name):
        self.name = name
        #self.id = auto
        
    def currentTask(self):
        '''
        Checks the events table to find the last entry from this user. Returns the
        task from there. 
        TODO: We might need to find a faster way to do this...
        TODO: We might need to check the order as well. Normally all events are entered
              in date time order, but you newer now
        '''
        event = self.lastEvent()
        if event:
            return event.task
        return None
    
    def lastEvent(self):
        '''
        Returns the last event record from user
        '''
        events = self.events
        num = len(events)
        if num > 0:
            return events[num-1]
        return None
        
    def __repr__(self):
        return '<User name=%s, id=%s>' % (self.name, self.id)
   
#------------------------------------------------------------------------------
class Task(object):
    '''
    '''
    @staticmethod
    def get(name=None, id=None, sess=None):
        '''
        Automatically create a task or return the one from DB
        '''
        task = None
        if sess is None:
            s = session()
        else:
            s = sess
            
        if name is not None:
            namestr = str(name)
            
            task = s.query(Task).filter(Task.name==namestr).first()
            if task is None:
                task = Task(namestr)
                s.save(task)
                s.commit()
                #
                #We don't do this call in User.get and it works. But in case of Tasks
                #if I try to access task.events it creates problem without below line
                #
                task = s.query(Task).filter(Task.name==namestr).first()
        elif id is not None:
            task = s.query(Task).filter(Task.id==id).first()
        
        if sess is None:
            s.close()
        return task
    
    @staticmethod
    def remove(task, sess=None):
        if sess is None:
            s = session()
        else:
            s = sess
        if type(task) == Task:
            s.delete(task)
        elif type(task) is str or type(task) is unicode:
            s.delete(Task.get(task))
        else:
            raise TypeError('Expecting to receive a Task or string object')
        s.commit()
        if sess is None:
            s.close()
        
    @staticmethod
    def clean(sess=None):
        '''
        Clean all entries from this table
        '''
        if sess is None:
            s = session()
        else:
            s = sess
        for entry in s.query(Task).all():
            s.delete(entry)
        s.commit()
        if sess is None:
            s.close()
        
    def __init__(self, name):
        self.name = name
        #self.id = auto
        
    def __repr__(self):
        return '<Task name=%s, id=%i>' % (self.name, self.id)
 
#------------------------------------------------------------------------------
class Event(object):
    '''
    '''
    @staticmethod
    def add(userName, eventId, logtime, taskName=None, sess=None):
        '''
            datetime: time.struct_time object
        '''
        if eventId == Events.start and taskName is None:
            raise ValueError('for start event task name can not be empty')
        
        if type(logtime) is not datetime.datetime:
            raise TypeError('logtime is expected to be a datetime object')
        
        if eventId == Events.start and taskName is None:
            raise ValueError('task name has to be given for start event')
        
        if sess is None:
            s = session()
        else:
            s = sess
            
        user = User.get(userName, s)
        lastEvent = user.lastEvent()
        sessionId = -1
        if lastEvent:
            sessionId = lastEvent.sessionId
        if eventId == Events.start:
            sessionId += 1
        elif lastEvent is None:
            raise ValueError('This event require an already started session, please use start event first')
        
        if eventId == Events.pause and lastEvent.id != Events.start and lastEvent.id != Events.resume:
            raise ValueError('To pause, you should start first')
        if eventId == Events.resume and lastEvent.id != Events.pause:
            raise ValueError('To resume, you should pause first')
        if eventId == Events.stop and lastEvent.id == Events.stop:
            raise ValueError('To stop, you should start first')
        
        if taskName is None:
            task = lastEvent.task
        else:
            task = Task.get(taskName, s)
        assert(task)
        event = Event(user.id, sessionId, task.id, eventId, logtime)
        
        s.save(event)
        s.commit()
        if sess is None:
            s.close()
        return event
    
    @staticmethod
    def remove(event, sess=None):
        if type(event) is not Event:
            raise TypeError('Expected to receive an Event object')
        if sess is None:
            s = session()
        else:
            s = sess
        s.delete(event)
        s.commit()  
        if sess is None:
            s.close()
        
    @staticmethod
    def clean(sess=None):
        '''
        Clean all entries from this table
        '''
        if sess is None:
            s = session()
        else:
            s = sess
        for entry in s.query(Event).all():
            s.delete(entry)
        s.commit()
        if sess is None:
            s.close()
        
    def __init__(self, userId, sessionId, taskId, id, logtime):
        '''
            logtime: datetime.datetime object
        '''
        self.userId = userId
        self.sessionId = sessionId
        self.taskId = taskId
        self.id = id
        self.date = logtime.year * 10000 + logtime.month * 100 + logtime.day
        self.time = logtime.hour * 10000 + logtime.minute * 100 + logtime.second
        
    def datetime(self):
        year = int(self.date / 10000)
        month = int((self.date - year * 10000) / 100)
        day = self.date - year * 10000 - month * 100
        
        hour = int(self.time / 10000)
        minute = int ((self.time - hour * 10000) / 100)
        second = self.time - hour * 10000 - minute * 100
        
        return datetime.datetime(year, month, day, hour, minute, second)
    
    def __repr__(self):
        return '<Event userId=%i, sessionId=%i, taskId=%i, id=%i, logtime=%i - %i>' % \
            (self.userId, self.sessionId, self.taskId, self.id, self.date, self.time)

#------------------------------------------------------------------------------
class Events:
    '''
    '''
    start = 0
    pause = 1
    resume = 2
    stop = 3
    @staticmethod
    def dumb():
        print 'Following events are supported:'
        print '... start  %i' % Events.start
        print '... pause  %i' % Events.pause
        print '... resume %i' % Events.resume
        print '... stop   %i' % Events.stop
        
#------------------------------------------------------------------------------
if __name__ == '__main__':
    import test_db
    test_db.startTest()
    
    
    