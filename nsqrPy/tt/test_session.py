import random
import unittest
import datetime

import session
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
        db.clean()
        
    def testStart(self): 
        event = session.start('sample task', user='oy')
        self.assertEqual(event.id, db.Events.start)
        
        self.assertEqual(session.isStarted('oy'), True)
        self.assertEqual(session.isPaused('oy'), False)
               
    def testPause(self):
        event = session.start('sample task', user='oy')
        event = session.pause(user='oy')
        
        self.assertEqual(event.id, db.Events.pause)
        self.assertEqual(session.isStarted('oy'), True)
        self.assertEqual(session.isPaused('oy'), True)
        
    def testPauseValueError(self):
        self.assertRaises(ValueError, session.pause)
        session.start('sample task')
        session.pause()
        self.assertRaises(ValueError, session.pause)
        session.stop()
        self.assertRaises(ValueError, session.pause)
        
    def testResume(self):
        event = session.start('sample task', user='oy')
        event = session.pause(user='oy')
        event = session.resume(user='oy')
        
        self.assertEqual(event.id, db.Events.resume)
        
        self.assertEqual(session.isStarted('oy'), True)
        self.assertEqual(session.isPaused('oy'), False)
        
    def testResumeValueError(self):
        self.assertRaises(ValueError, session.resume)
        session.start('sample task')
        self.assertRaises(ValueError, session.resume)
        session.stop()
        self.assertRaises(ValueError, session.resume)
        
        
    def testStop(self):
        event = session.start('sample task', user='oy')
        event = session.stop(user='oy')
        self.assertEqual(event.id, db.Events.stop)
        self.assertEqual(session.isStarted('oy'), False)
        self.assertEqual(session.isPaused('oy'), False)
        
    def testStopValueError(self):
        self.assertRaises(ValueError, session.stop)
        session.start('sample task')
        session.stop()
        self.assertRaises(ValueError, session.stop)
        
    
#------------------------------------------------------------------------------
def startTest():
    unittest.main()
    
if __name__ == '__main__':
    startTest()