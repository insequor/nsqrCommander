#------------------------------------------------------------------------------
import cherrypy

import db #nsqrPy.tt.db
import session #nsqrPy.tt.session

#------------------------------------------------------------------------------
__doc__ = '''HTTP Server to handle the DB part It can be started as a standalone
application or within the sampe application as a new thread
'''

#------------------------------------------------------------------------------
class Reports:
    @cherrypy.expose
    def index(self):
        return ">> main page for reports"
    
    @cherrypy.expose
    def events(self):
        content = '>> All events:\n'
        for event in db.events():
            content += '>>> ' + str(event) + '\n'
        return content
    
    @cherrypy.expose
    def sessions(self):
        #return session.dayReport()
        pass
    
    
#------------------------------------------------------------------------------
class Server:
    reports = Reports()
    
    @cherrypy.expose 
    def index(self):
        return ">> main page"
    
    @cherrypy.expose 
    def list(self, a=None):
        return 'Server.list: %s' % str(a)
    
    
#------------------------------------------------------------------------------
def startCherry():
    cherrypy.quickstart(Server())
    f = file('ozgur.txt', 'w')
    f.write('some text')
    f.close()
    
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'nsqrPy.tt.server'
    startCherry()
