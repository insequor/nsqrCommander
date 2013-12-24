import copy

#===============================================================================
class Function(object):
  def __init__(self, data):
    self.resultPTList = []
    self.resultUnitList = []
    
    self.argumentPTList = []
    self.argumentUnitList = []

    if data:
      self.resultPTList = copy.deepcopy(data.resultPTList)
      self.resultUnitList = copy.deepcopy(data.resultUnitList)
      
      self.argumentPTList = copy.deepcopy(data.argumentPTList)
      self.argumentUnitList = copy.deepcopy(data.argumentUnitList)
    
    
  def __repr__(self):
    repr = '''
    Printing information for instance of %s
      
      result physical type list: %s
      result unit list: %s
      
      argument physical type list: %s
      argument unit list: %s
    ''' % (self.__class__,
    self.functionClass, 
    self.loadCondition, 
    self.id,
    self.resultPTList,
    self.resultUnitList,
    self.argumentPTList,
    self.argumentUnitList)
    return repr
    
  def __str__(self):
    return self.__repr__()

#===============================================================================
class LoadFunction (Function):
  def __init__(self, data=None):
    print 'LoadFunction.__init__'
    Function.__init__(self, data)
    
#===============================================================================
class TransferFunction (Function):
  def __new__(cls, data=None):
    print cls
    try:
      if data and not isinstance(data, TransferFunction):
        print '   Given data is not convertable'
        return None
        
      return Function.__new__(cls, data)
      
    except:
      print 'exception during instantiation'
      return None
      
    return None
    
  def __init__(self, data=None):
    print 'TransferFunction.__init__'
    Function.__init__(self, data)
    self.functionType = 'TransferFunction'
    
  
    
#===============================================================================
if __name__ == '__main__':
  print 'testing functions.py'
  lf = LoadFunction()
  print lf
  
  print isinstance(lf, Function)
  print isinstance(lf, LoadFunction)
  print isinstance(lf, TransferFunction)
  
  tf = TransferFunction()
  tf.id.append('ozgur')
  print tf
  
  ttf = TransferFunction(lf)
  print ttf
  
  print isinstance(tf, TransferFunction)
  ttf = TransferFunction(tf)
  ttf.id[0] = 'diana'
  print ttf
  
  print tf.id
