

__doc__ = '''
    This module will provide/manage database access for data processing code. 
    
    Each scenario is considered in a single database file (sqlite) which will keep
    all instances of scenario components. 
    
    There are few requirements:
        * Load on request: Data will be loaded only when it is requested, only 
          required parts will be kept in the memory
        * Save continuously: Data save will not wait for user request. All operations
          will be saved at the moment they happen. They will be committed with user request
          though, so user can discard the changes at any time
        * Support Undo: All actions untill the commit can be undone
        * Support User Provided content: User can provide custom data containers, database
          will need to support them
        * Avoid read/write duplications: Shared objects will be stored once and retrieved once
        
    
    Serialization (Pickling):
        Python provides pickle module for serializing objects. We will not use it for 
        all data IO. But it will be used to (de)serialize object types. Each object 
        should provide its own interface for data IO. Here how it should be
            obj #provided by user
            dump = pickle.dumps(obj.__class__) #serialize user provided class
            obj.store() #inform user to store its own contents
            
            ...
            dump #loaded data for class information
            objCls = pickle.loads(dump) #de-serialize the class from db
            obj = objCls() #create an instance of the object
            obj.retrieve() #inform user to load its own contents
            
            Class information will be kept in a single table so class of each object
            will not be pickled/unpickled
            
    Scenario Format:
        A scenario is a "graph" of scenario components. There is no tree-like 
        hierarchy since scenario is input/output relations of scenario components 
        which can be better visualize as a graph. However, there is still a "level
        hierarchy" which works more like containers/packages/groups of components.
        "root" contains all other scenario compoenent. 
        
    Duplications:
        Builtin "id" function returns a unique identifier for each object. We will
        use this identifier to find if an object is already stored or not. 
        
        When retrieving the objects we will create new instances, therefore identifier
        values will be changed. We will use a mapping between stored and retrieved object
        identifiers to see if it is already created...
        
        PROBLEM: Documentation says, this is the address of the object and two objects 
        with non-overlapping life times might have same ids. Might not be likely but 
        plausable... 
        
        QUESTION: Can we get a hash value from an object which will contain the id and
        the creation time? How can we get back the object if we know this id?
        ANSWER: hash builtin function calls __hash__ on the object. By default it returns 
        id for the custom classes. We can override it there to get the creation time value 
        as well. And NO, WE CAN NOT get object from ID or Hash value unless we keep a reference
        causing object to stay alive. They say there is a "weak reference" concept, which do not
        force the object to stay alive. If we keep the object in a dictionary with week reference
        and handle the __del__ method to remove itself from dictionary, than it might work?
        
        PROBLEM: Once we pickle the class information of an object, that object might
        still be modified with extra properties or functions (extensions?), how we will
        manage non-class attributes?
        
        NOTE: __setstate__ and __getstate__ methods are called during pickling which then
        can be used to customize the data
        
        
        Extension Management:
        We want to mimic the usage in DS framework such that:
            MyLateType.extend(Drawable)
            MyLateType.extend(Editable)
            
            lt = MyLateTypeLT()
            e = Editable(lt)
            e.update()
            
            d = Drawable(lt)
            d.update()
            
            dd = Drawable(e)
            dd.update()
            
        In above example "d" and "dd" might be different instances, but their 
        dictionaries should be identical.
        
        
        
        
            
        
'''

import pickle

#------------------------------------------------------------------------------
class Drawable:
    def __init__(self):
        self.e = None
        print 'Drawable.__init__'
    def __del__(self):
        print 'Drawable.__del__'
        
class Editable:
    def __init__(self):
        self.d = None
        print 'Editable.__init__'
    def __del__(self):
        print 'Editable.__del__'
        
def foo():
    d = Drawable()
    e = Editable()
    d.e = e
    #Circular dependency introduced!
    e.d = d
    

import weakref
     
def foo2(td):
    d = Drawable()
    td[id(d)] = d
    print len(td)
    
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'db.py'
    
    #foo()
        


    td = weakref.WeakValueDictionary()
    foo2(td)
    print len(td)
    def remember(obj):
        oid = id(obj)
        _id2obj_dict[oid] = obj
        return oid

    

    print 'end'
    

    
    
    
    