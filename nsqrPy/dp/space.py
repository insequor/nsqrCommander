

__doc__ = '''
    A space is a list of values (numerical or string form) which defines the 
    values on a certain axis. Multiple spaces can be put together to construct
    a function. A simple y = f(x) function contains two spaces; one for X axis
    and one for y axis. 
    
    Each space has N dimensions. Number of dimensions defines how many index values
    are required to access a certain value. In above example, both X and Y spaces has
    1 Dimension (N=1). For z = f(x, y) function z will have 2 Dimensions since for each
    value there are two indices required.
    
    "z" as space uses index values to access the content, however "f" as function needs
    "x" and "y" values (not the indices but actual values). A "space" can be seen as a 
    simple container, while "f" contains the "function knowladge". It should be possible 
    to define "f" as a "computation" which will return the values which are computed on the 
    fly, while "z" could only contain the actual values. Accessing values through "f" might
    be space efficient (function can be defined as algorithm), while accessing space should 
    be speed efficient (both the indirection is gone, also values are already computed). To do
    that, a space should always be requested from function, which might actually computed the
    values before returning the space
    
    This module defines the interface for user implemented spaces and some default ones which 
    should be ready to use. It is also a base for numpy code pieces.
'''

import numpy

#------------------------------------------------------------------------------
class Space:
    def __init__(self):
        print 'Space is here'
        
    def __hash__(self):
        print 'ozgur'
        return object.__hash__(self)        
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'space.py'
    print __doc__
    
    s = Space()
    print hash(s)
    print id(s)
    
    
    
    