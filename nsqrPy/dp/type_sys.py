
import weakref


__doc__ = '''
    This script defines the type system of data processing module. It is an attempt
    to realize what DS frameworks does with LateType & Interface mechanism

    Therms of interest:
      LateType: Some sort of class identifier which can be extended
      
      LateTypeObject: An object instantiated from a given late type
      
      Interface: A definition which can extend a given late type
      
      Implementation: A class which gives implementation of an interface to extend
      a certain late type     
    
'''
ltDict = {}     # {lateTypeName : {interface : (implementation, shareable) } }
itfDict = {}    # {interface : {lateType : implementation} }
implDict = {}   # {implementation : {lateType : interface} }

#------------------------------------------------------------------------------
class LateType:
    def __init__(self, ltName):
        self.name = ltName
        self.extensions = weakref.WeakValueDictionary()
        #self.extensions = {}

#------------------------------------------------------------------------------
class Interface (object): 
    def __new__(cls, obj, shared=True):
        '''
        obj should either be the late type object and should have a reference
        to it (i.e. being an extension on late type object)
        '''
        return query(obj, cls, shared)     
        
    def __init__(self):
        '''
        Interface itself should never be instantiated
        '''
        assert(0)
                
#------------------------------------------------------------------------------
def extend(lateType, interface, implementation, shareable):
    '''
    Parameters:
    lateType: Late type name to be extended
    interface: Interface name to be extended
    implementation: Implementation name to be extended
    shareable: If true same instance (if available) can be shared, if false
        each time a new instance is created
    '''
    if not ltDict.has_key(lateType):
        ltDict[lateType] = {}
    valueDict = ltDict[lateType]
    
    #TODO: We need to check what to do if same interface is implemented again and again
    valueDict[interface] = (implementation, shareable)    
    
    if not itfDict.has_key(interface):
        itfDict[interface] = {}
    valueDict = itfDict[interface]
    valueDict[lateType] = implementation
    
    if not implDict.has_key(implementation):
        implDict[implementation] = {}
    valueDict = implDict[implementation]
    valueDict[lateType] = interface
    
    
    

#------------------------------------------------------------------------------
def query(obj, interface, shared=True):
    '''
    '''
    cls = interface
    ltObject = obj
    if hasattr(obj, 'ltObject'):
        ltObject = obj.ltObject
        
    assert(hasattr(ltObject, 'name'))
    name = ltObject.name
    
    if shared:
        assert(hasattr(ltObject, 'extensions'))
        if ltObject.extensions.has_key(cls):
            return ltObject.extensions[cls]
                
    assert(ltDict.has_key(name))
    ltiDict = ltDict[name]
    
    itfName = str(cls)
    #When query is called from new string name is like "<'xxx'>" format
    #If query is called directly it doesn't have this characters
    #also name contains the module name as well
    if itfName[len(itfName) - 2:] == "'>":
        itfName = itfName[: len(itfName) - 2]
    idx = itfName.rfind('.')
    if idx >= 0:
        itfName = itfName[idx+1:]
    assert(ltiDict.has_key(itfName))
    implCls, shareble = ltiDict[itfName]
    
    assert(implCls)
    
    impl = implCls()
    impl.ltObject = ltObject
    
    if shared:
        ltObject.extensions[cls] = impl
    
    return impl
    
#------------------------------------------------------------------------------
def instantiate(lateType):
    '''
    '''
    return LateType(lateType)
    

#------------------------------------------------------------------------------
def supportedOnLateType(lateType):
    '''
    '''
    if ltDict.has_key(lateType):
        valueDict = ltDict[lateType]
        return (valueDict.keys(), valueDict.values())
    return (None, None)
    
#------------------------------------------------------------------------------
def supportsInterface(interface):
    '''
    '''
    if itfDict.has_key(interface):
        valueDict = itfDict[interface]
        return (valueDict.keys(), valueDict.values())
    return (None, None)

#------------------------------------------------------------------------------
def supportedByImplementation(implementation):
    '''
    '''
    if implDict.has_key(implementation):
        valueDict = implDict[implementation]
        return (valueDict.keys(), valueDict.values())
    return (None, None)

#------------------------------------------------------------------------------
def clear():
    ltDict = {}
    itfDict = {}
    implDict = {}
        
#===============================================================================
if __name__ == '__main__':
  print 'test_sys.py'
  print __doc__
