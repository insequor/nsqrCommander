import sys
import nsqrPy
from xml.dom.minidom import parse, parseString, getDOMImplementation

__doc__ = """
Document for XMLedObject.py
"""

class Node:
    """
    """
    def __init__(self):
        """
        """
        self.tagName = ''
        self.text = ''
        self.cdata = ''
        self.__valid = False
        self.__elements = []
        self.__attributes = []
        pass
    
    def init(self, xmlnode, dict=None, data=None):
        """
        """
        try:
            self.tagName = xmlnode.tagName
            self.__valid = False
            for child in xmlnode.childNodes:
                if child.nodeType == child.ELEMENT_NODE:
                    if not hasattr(self, child.tagName):
                        setattr(self, child.tagName, [])
                    if dict and dict.has_key(child.tagName):
                        newNode = dict[child.tagName]()
                    else:newNode = Node()
                    newNode.init(child, dict, data)
                    getattr(self, child.tagName).append(newNode)
                    self.__elements.append(newNode)
                elif child.nodeType == child.TEXT_NODE:
                    if len(child.data)>0:
                        self.text += child.data.strip()
                elif child.nodeType == child.CDATA_SECTION_NODE:
                    if len(child.data)>0:
                        self.cdata += child.data.strip()
            if xmlnode.attributes:
                for attr in xmlnode.attributes.items():
                    setattr(self, attr[0], attr[1])
                    self.__attributes.append((attr[0], attr[1]))
            self.__valid = True
        except:
            self.__valid = False
            nsqrPy.printException()
                
    def testPrint(self, indent=''):
        print indent + 'Tag Name: ', self.tagName
        print indent + 'Text: ', self.text
        print indent + 'CData: ', self.cdata
        for attr in self.__attributes:
            print indent, attr
        for e in self.__elements:
            e.testPrint(indent+'   ')
    def load(self, fileName):
        """
        """
        try:
            loaded = False
            doc = parse(fileName)
            assert doc.documentElement
            dict = None
            data = None
            self.init(doc.documentElement, dict, data)
            loaded = self.__valid
        except:
            loaded = False
            nsqrPy.printException()
        return loaded
    
    def save(self, fileName):
        """
        """
        try:
            saved = False
            saved = True
        except:
            saved = False
            nsqrPy.printException()
        return saved
    

if __name__ == '__main__':
    print 'Testing XMLedObject.py'
    print __doc__
    node = Node()
    infile = 'D:\\temp\\wikishore\\_main.xml'
    outfile = infile + '.xml'
    if node.load(infile):
        print 'Load is OK'
        node.testPrint()
        if node.save(outfile):
            print 'Save is OK'
    
    del node
    
    
if 0:
    docText = """Doc:
    """
    
    todoText = """TODO:
    """
    
    bugsText = """Bugs:
    """
    
    #-----------------------------------------------------------------------------
    #--- As default node has following members:
    #---    .text:
    #---    .cdata:
    #-----------------------------------------------------------------------------
    class Node:
        def __init__ (self, node=None, dict=None, data=None):
            self.name = ''
            self.text = ''
            self.cdata = ''
            self.__valid = False
            self.__elements = []
            
            if node:
                self.init(node, dict, data)
            
        def init (self, node, dict=None, data=None):
            if not node:
                return
            try:
                for child in node.childNodes:
                    if child.nodeType == child.ELEMENT_NODE:
                        if not self.isExist(child.tagName):
                            self.addAttr(child.tagName, [])
                        if dict and dict.has_key(child.tagName):
                            newNode = dict[child.tagName](child, dict, data)
                        else:
                            newNode = Node(child, dict, data)
                        getattr(self, child.tagName).append(newNode)
                        newNode.name = child.tagName
                        self.__elements.append(newNode)
                    elif child.nodeType == child.TEXT_NODE:
                        if len(child.data)>0:
                            self.text += child.data.strip()
                    elif child.nodeType == child.CDATA_SECTION_NODE:
                        if len(child.data)>0:
                            self.cdata += child.data.strip()
                if node.attributes:
                    for attr in node.attributes.items():
                        setattr(self, attr[0], attr[1])
                self.__valid = True
            except:
                e = sys.exc_info ()
                sys.excepthook  ( e[0], e[1], e[2] )
                pass
         
        def __isValid(self): return self.__valid
        valid = property(__isValid)
        
        def getElements(self): return self.__elements
        
        def isExist(self, attr):
            return hasattr(self, attr)
        def addAttr(self, attr, val):
            setattr(self, attr, val)
    pass
    #-----------------------------------------------------------------------------
    #---
    #-----------------------------------------------------------------------------
    class Document (Node):
        """Document Class:
        """
        def __init__ (self, doc=None, dict=None, data=None):
            Node.__init__(self)
            self.__valid = False
            if doc:
                self.init(doc, dict, data)
        
        def init(self, doc, dict=None, data=None):
            if not doc:
                return
            if doc.documentElement:
                Node.init(self, doc.documentElement, dict, data)
            else:
                print 'XML Document should contain root node!'
                
       
    pass
    #-----------------------------------------------------------------------------
    #---
    #-----------------------------------------------------------------------------
    def getXMLDocument(fileName):
        """uses xml.minidom.parse() to parse given file.
           Returns the xml document
        """
        try:
            return parse(fileName)
        except:
            e = sys.exc_info ()
            sys.excepthook  ( e[0], e[1], e[2] )
            return None
            
        
    def getXMLDocumentFromBuffer(buffer):
        try:
            return parseString(buffer)
        except:
            e = sys.exc_info ()
            sys.excepthook  ( e[0], e[1], e[2] )
            return None
        
    pass
    
    #-----------------------------------------------------------------------------
    #--- TEST AREA
    #-----------------------------------------------------------------------------
    class TopicClass (Node):
        def __init__ (self, node, dict=None, data=None):
            print '===>Topic Class is called'
            Node.__init__(self, node, dict)
            
    def main ():
        try:
            print docText
            print todoText
            print bugsText
            
            topic = TopicClass (None, None)
            
            fileName = '../data/sample.xml'
            xmldoc = getXMLDocument(fileName)
            dict = {}
            dict['topic'] = TopicClass
            doc = Document(xmldoc, dict)
            docNode = doc.document[0]
            print docNode.name
            print docNode.author
            print docNode.date
            for topic in doc.topic:
                print 'Topic Name: ' + topic.name
                print 'Topic Text: ' + topic.text
                print 'Topic CData: ' + topic.cdata
                
                
        except:
            e = sys.exc_info ()
            sys.excepthook  ( e[0], e[1], e[2] )
    
    if __name__ == '__main__':
        main()