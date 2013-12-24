import wx
import nsqr
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
class TextValidator(wx.PyValidator):
    """
    TextCtrl Validator
    """
    def __init__(self):
        wx.PyValidator.__init__(self)
        
    def init(self, obj, attr, validateFunc, updateFunc,
            handleTextChanged = True, errColour = 'pink'):
        """
        validateFunc: Called to validate the value, it should return the value
        in desired format which will be set to the obj.attr It should receive
        the value as a string parameter str(), float(), int() functions are
        perfect candidates
        updateFunc: Called when value is updated if textChanged event is handled
        and value is valid. Receives the textCtrl and formatted value, value
        is what returned from validateFunc
        """
        self.__backColour = self.GetWindow().GetBackgroundColour()
        self.__errColour = errColour
        self.__obj = obj
        self.__attr = attr
        self.__handleTextChanged = handleTextChanged
        
            
        self.__validateFunc = validateFunc
        self.__updateFunc = updateFunc
        
        if handleTextChanged:
            self.Bind(wx.EVT_TEXT, self.__onTextChanged, self.GetWindow())
        
        self.TransferToWindow()
            
    def Clone(self):
        return TextValidator()
                
     
    def TransferToWindow(self):
        tc = self.GetWindow()
        try:
            tc.SetValue(str(getattr(self.__obj, self.__attr)))
        except:
            nsqr.printException()
            return False
        return True
    
    def TransferFromWindow(self):
        #HACK: Nothing to be done, it's all handled in Validate
        return True
    
    def Validate(self, win):
        return self.__validate(win, win.GetValue())
        
    def __onTextChanged(self, evt):
        self.__validate(self.GetWindow(), evt.GetString())
            
    def __validate(self, wnd, value):
        res = True
        try: val = self.__validateFunc(value)
        except: res = False
        if res:
            wnd.SetBackgroundColour(self.__backColour)
            setattr(self.__obj, self.__attr, val)
            if self.__updateFunc:
                self.__updateFunc(wnd, val)
        else:
            wnd.SetBackgroundColour(self.__errColour)
            if not wx.Validator_IsSilent():
                wx.Bell()
        wnd.Refresh()
        
        return res
    
class NumericValidator:
    """
    Validate function for numeric values. It supports min, max check
    """
    def __init__(self, numericFunc, min=None, max=None):
        """
        numericFunc: Convertion function (int, float etc)
        min: minimum value if available
        max: maximum value if available
        """
        self.__numericFunc = numericFunc
        self.__min = min
        self.__max = max
        
    
    def __call__(self, value):
        """Validator function"""
        val = self.__numericFunc(value)
        if self.__min != None and val < self.__min:
            raise Exception, \
                  'value is less then minimum: ' + str((val, self.__min))
        elif self.__max != None and value > self.__max:
            raise Exception, \
                  'value is greater then maximum: ' + str((val, self.__max))
        return val
        
class IntValidator(NumericValidator):
    def __init__(self, min=None, max=None):
        NumericValidator.__init__(self, int, min, max)
        
class FloatValidator(NumericValidator):
    def __init__(self, min=None, max=None):
        NumericValidator.__init__(self, float, min, max)