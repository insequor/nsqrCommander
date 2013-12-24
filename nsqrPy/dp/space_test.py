import unittest

import space
import pickle


#------------------------------------------------------------------------------
class TestSpace(unittest.TestCase):
    def setUp(self):
        '''
        '''
        pass
        
    def tearDown(self):
        '''
        '''
        pass
        
    def testPickle(self):
        '''
        this sample uses text format. binary is considered slightly more efficient
        '''
        s = space.Space()
        print s.__class__, id(s)
        dump = pickle.dumps(s.__class__, True)
        print '----'
        print dump
        print '----'
        sCls = pickle.loads(dump)
        print sCls
        ss = sCls()
        print id(ss)
        print hash(ss)
        

#------------------------------------------------------------------------------
def startTest():
    unittest.main()

#=============================================================================
if __name__ == '__main__':
    print 'space_test.py'
    startTest()