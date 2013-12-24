import unittest

import function

#------------------------------------------------------------------------------
class TestFunction(unittest.TestCase):
    def setUp(self):
        '''
        '''
        pass
        
    def tearDown(self):
        '''
        '''
        pass
        
    def testIndex(self):
        f = function.Function(None)
        print f

    def testIndex2(self):
        print '...TestFunction.testIndex()'

#------------------------------------------------------------------------------
def startTest():
    unittest.main()

#=============================================================================
if __name__ == '__main__':
    print 'function_test.py'
    startTest()