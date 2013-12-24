import random
import unittest
import datetime
import db

#------------------------------------------------------------------------------
class TestUser(unittest.TestCase):
    def setUp(self):
        '''
        '''
        pass
        
    def tearDown(self):
        '''
        Empty the database for further tests
        '''
        db.User.clean()
        
    def testGetInvalidArgumentType(self):
        self.failUnlessRaises(TypeError, db.User.get, 5)
        
    def testGetNew(self):
        oy = db.User.get('oy')
        self.assertEqual(oy.name, 'oy')
        self.assertEqual(oy.id, 1)
        self.assertEqual(len(db.users()), 1)
    
    def testGetExisting(self):
        oy = db.User.get('oy')
        cn = db.User.get('cn')
        oy = db.User.get('oy')
        self.assertEqual(oy.name, 'oy')
        self.assertEqual(oy.id, 1)
        self.assertEqual(len(db.users()), 2)
            
    def testRemoveInvalidArgumentType(self):
        self.failUnlessRaises(TypeError, db.User.remove, 5)
        
    def testRemoveByName(self):
        oy = db.User.get('oy')
        db.User.remove('oy')
        self.assertEqual(len(db.users()), 0)
    
    def testRemoveByObject(self):
        oy = db.User.get('oy')
        db.User.remove(oy)
        self.assertEqual(len(db.users()), 0)
        
#------------------------------------------------------------------------------
class TestTask(unittest.TestCase):
    def setUp(self):
        '''
        '''
        pass
        
    def tearDown(self):
        '''
        Empty the database for further tests
        '''
        db.Task.clean()
        
       
    def testGetNew(self):
        task = db.Task.get('sample')
        self.assertEqual(task.name, 'sample')
        self.assertEqual(task.id, 1)
        self.assertEqual(len(db.tasks()), 1)
    
    def testGetExisting(self):
        task1 = db.Task.get('sample')
        task2 = db.Task.get('another')
        task = db.Task.get('sample')
        self.assertEqual(task.name, 'sample')
        self.assertEqual(task.id, 1)
        self.assertEqual(len(db.tasks()), 2)
            
    def testRemoveInvalidArgumentType(self):
        self.failUnlessRaises(TypeError, db.Task.remove, 5)
        
    def testRemoveByName(self):
        task = db.Task.get('sample')
        db.Task.remove('sample')
        self.assertEqual(len(db.tasks()), 0)
    
    def testRemoveByObject(self):
        task = db.Task.get('sample')
        db.Task.remove(task)
        self.assertEqual(len(db.tasks()), 0)



#------------------------------------------------------------------------------
class TestEvent(unittest.TestCase):
    def setUp(self):
        '''
        '''
        pass
        
    def tearDown(self):
        '''
        Empty the database for further tests
        '''
        db.Event.clean()
        
    def testAddInvalidName(self):
        self.failUnlessRaises(ValueError, db.Event.add,
          'oy', db.Events.start, datetime.datetime.today())
    
    def testAddInvalidDate(self):
        self.failUnlessRaises(TypeError, db.Event.add,
          'oy', db.Events.pause, 5)
    
    def testAdd(self):
        event = db.Event.add('oy', db.Events.start, datetime.datetime.today(), 'sample')
        self.assert_(event)
        self.assertEqual(len(db.events()), 1)
            
    def testRemoveInvalidArgumentType(self):
        self.failUnlessRaises(TypeError, db.Event.remove, 5)
    
    def testRemove(self):
        event = db.Event.add('oy', db.Events.start, datetime.datetime.today(), 'sample')
        db.Event.remove(event)
        self.assertEqual(len(db.events()), 0)
    


#------------------------------------------------------------------------------
class TestRelations(unittest.TestCase):
    '''
    Check the relations between User, Task and Events
    '''
    def setUp(self):
        pass
        
    def tearDown(self):
        db.Event.clean()
        db.User.clean()
        db.Task.clean()
            
        
    def testLastEvent(self):
        event = db.Event.add('oy', db.Events.start, datetime.datetime.now(), 'sample task')
        s = db.session()
        task = db.Task.get('sample task', s)
        oy = db.User.get('oy', s)
        le = oy.lastEvent()
        self.assert_(le)
        self.assertEqual(str(le), str(event))
        
    
    
#------------------------------------------------------------------------------
def startTest():
    unittest.main()


#------------------------------------------------------------------------------
# Sample Data Generation from StopWatch Log Files
#------------------------------------------------------------------------------
def fillFromLogFile(dbname, logfile):
    import time
    import datetime
    import session

    print 'creating sample data from logfile: ', logfile
    eventmap = {'Started':db.Events.start,
                'Paused' : db.Events.pause,
                'Resumed' : db.Events.resume,
                'Stopped' : db.Events.stop}
    log = file(logfile)
    s = db.session(dbname)
    for line in log.readlines():
        line = line.split(' ')
        #print line
        while True:
            try:
                line.remove('')
            except:
                break
        #date, time, event, task (if any)
        num = len(line)
        if num < 3:
            continue
        logtime = ' '.join(line[:2])
        event = line[2]
        event = event[:len(event)-1] #this is to remove endline or ":" character
        task = None
        if not eventmap.has_key(event):
            #print 'event not found [%s]' % event
            continue
            #if session.isStarted():
            #    event = db.Events.stop
            #else:
            #    continue
        else:
            event = eventmap[event]
        
        if event == db.Events.start:
            #clean up the task text from date-time information
            #endline characters
            #and event identifier
            task = ' '.join(line[3:])
            task = task[:len(task)-1]
            print task
        logtime = time.strptime(logtime, '%m/%d/%y %H:%M:%S')
        logtime = datetime.datetime(logtime.tm_year, logtime.tm_mon, logtime.tm_mday,
                                    logtime.tm_hour, logtime.tm_min, logtime.tm_sec)
        try:
            db.Event.add('oy', event, logtime, task, s)
        except:
            print 'error adding event: %s  %s' % (str(logtime), event)
        s.close()

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
if __name__ == '__main__':
    if 0:
        startTest()
    else:
        dbname = 'sqlite:///data/tt_test.sqlite'
        logfile = 'D:\\Home\\oy\\tools\\StopWatch\\data\\logfile.log'
        fillFromLogFile(dbname, logfile)