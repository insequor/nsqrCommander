

#------------------------------------------------------------------------------

__doc__ = '''Team(Task) Tracker
'''

import session

#------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'nsqrPy.tt'
    import nsqrPy
    import nsqrPy.tt as tt
    print '>>> Contents of tt:'
    for d in dir(tt):
        print d
        
    print '>>> Contents of tt.session:'
    for d in dir(tt.session):
        print d
        
    print '>>> Contents of tt.db:'
    for d in dir(tt.db):
        print d
    