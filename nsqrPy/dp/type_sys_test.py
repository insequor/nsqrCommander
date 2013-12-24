import unittest

import type_sys

#
#
#
class IDrawable (type_sys.Interface): pass
class IDrawableNoBase : pass

#
#
#    
class IEditable (IDrawable): pass

#
#
#
class EDrawable:
    def __init__(self):
        #print 'EDrawable.__init__'
        pass
        
    def __del__(self):
        #print 'EDrawable.__del__'
        pass
        

#
#
#        
class EEditable: pass

#------------------------------------------------------------------------------
class Test(unittest.TestCase):
    def setUp(self):
        '''
        Defines the extensions to be used for each test
        TODO: Implementation should be passed as scipt and class name this way 
              script can be loaded only when it is needed
        '''
        type_sys.extend('PointLT', 'IDrawable', EDrawable, True)
        type_sys.extend('PointLT', 'IEditable', EEditable, True)
        type_sys.extend('PointLT', 'IDrawableNoBase', EDrawable, True)
        pass
        
    def tearDown(self):
        '''
        Clears the extension tables
        '''
        type_sys.clear()
        pass
        
    def testSupportedOnLateType(self):
        '''
        Queries available interfaces on a given late types and implementations
        '''
        ltList, implList = type_sys.supportedOnLateType('PointLT')
        assert(ltList == ['IEditable', 'IDrawable', 'IDrawableNoBase'])
        
    def testSupportsInterface(self):
        '''
        Queries 
        '''
        ltList, implList = type_sys.supportsInterface('IDrawable')
        assert(ltList == ['PointLT'])
        
    def testSupportedByImplementation(self):
        '''
        '''
        ltList, itfList = type_sys.supportedByImplementation(EDrawable)
        assert(ltList == ['PointLT'])
        assert(itfList == ['IDrawable', 'IDrawableNoBase'])
        
        
        
    def testExtend(self):
        '''
        this sample uses text format. binary is considered slightly more efficient
        '''
        l = len(type_sys.ltDict)
        assert(l == 1)
        
    def testInstantiate(self):
        '''
        '''
        obj = type_sys.instantiate('PointLT')
        assert(obj)
        assert(obj.name == 'PointLT')
        
    def testInstantiateFromClass(self):
        '''
        '''
        class Point (type_sys.LateType):
            def __init__(self):
                type_sys.LateType.__init__(self, 'PointLT')
        obj = Point()
        assert(obj)
        assert(obj.name == 'PointLT')
        
    def testQueryOnLTObject(self):
        '''
        '''
        obj = type_sys.instantiate('PointLT')
        drawable = IDrawable(obj)
        assert(drawable)
        assert(drawable.__class__ == EDrawable)
        
    def testQueryFuncOnLTObject(self):
        '''
        '''
        obj = type_sys.instantiate('PointLT')
        drawable = type_sys.query(obj, IDrawableNoBase)
        assert(drawable)
        assert(drawable.__class__ == EDrawable)
        
    def testQueryOnLTObject2(self):
        '''
        '''
        class Point (type_sys.LateType):
            def __init__(self):
                type_sys.LateType.__init__(self, 'PointLT')
        obj = Point()
        drawable = IDrawable(obj)
        assert(drawable)
        assert(drawable.__class__ == EDrawable)
        
    def testQueryOnImplementation(self):
        '''
        '''
        obj = type_sys.instantiate('PointLT')
        drawable = IDrawable(obj)
        editable = IEditable(drawable)
        assert(editable.__class__ == EEditable)
        
    
        
    def testLifeCycle(self):
        class Point (type_sys.LateType):
            def __init__(self):
                #print 'Point.__init__'
                type_sys.LateType.__init__(self, 'PointLT')
            def __del__(self):
                #print 'Point.__del__'
                pass
        
        obj = Point()
        def foo():
            drawable1 = IDrawable(obj)
            drawable2 = IDrawable(obj)
            assert(drawable1 is drawable2)
            return id(drawable1)
        d1ID = foo()
        drawable3 = IDrawable(obj)
        drawable4 = IDrawable(obj)
        assert(drawable3 is drawable4)
        #
        #This test might fail, python might still use the 
        #existing address to create a new instance
        #
        #assert(d1ID != id(drawable3))
        
    def testNotShared(self):
        obj = type_sys.instantiate('PointLT')
        drawable1 = IDrawable(obj, False)
        drawable2 = IDrawable(obj)
        assert(drawable1 is not drawable2)
        
        
        

#------------------------------------------------------------------------------
def startTest():
    unittest.main()

#=============================================================================
if __name__ == '__main__':
    print 'type_sys_test.py'
    startTest()


