#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================
import wx

import datetime

import nsqrPy
import nsqrPy.cmdr as cmdr
import nsqrPy.cmdrui as cmdrui


#=============================================================================
#===Configuration
#=============================================================================
#This command does not need any configuration parameters...

#=============================================================================
#===
#=============================================================================


class TaskStatus:
    NotStarted = 0
    InProgress = 1
    Complated = 2
    WaitingFor = 3
    Deferred = 4
    
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Commands to ease the GDT at work environment'''

    #---
    def __getOptions(self):
        return self.__options.keys()
    options = property(__getOptions)
    
    #--
    def __init__(self):
        self.names = ['gtd']
        self.__options = {}
        
    def activated(self, name):
        self.__options = {}
        
        app = cmdrui.application
        try:
            if not app.IsOutlook:
                return
        except:
            return
            
        options = []
        if app.getSelectedTask():
            options = {'move task to action list' : self.__moveToActionList,
                             'move task to master list' : self.__moveToMasterList,
                             'move task to incubation list' : self.__moveToIncubationList,
                             'move task to waiting for list' : self.__moveToWaitingList,
                             'create new action item from task' : self.__createActionItem}
                             
        elif app.getSelectedMail():
            options = {'create task to action list' : self.__createTaskToActionList,
                             'create task to master list' : self.__createTaskToMasterList,
                             'create task to incubation list' : self.__createTaskToIncubationList,
                             'create task to waiting for list' : self.__createTaskToWaitingList}
        else:
            options = {}
        self.__options = options
        
    #--
    def execute(self, name, option):
        print 'execute (%s, %s)' % (name, option)
        try:
            self.__options[option]()
            result = True
        except:
            nsqrPy.printException()
            result = False
        return result
        
    #---
    def __moveToActionList(self):
        task = cmdrui.application.getSelectedTask()
        
        task.Status = TaskStatus.NotStarted
        task.StartDate = datetime.datetime.now()
        task.DueDate = task.StartDate
        task.Save()
        
    #---
    def __moveToMasterList(self):
        task = cmdrui.application.getSelectedTask()
        
        task.Status = TaskStatus.NotStarted
        task.StartDate = '2/2/3000'
        task.DueDate = task.StartDate
        task.Save()
        
    #---
    def __moveToIncubationList(self):
        task = cmdrui.application.getSelectedTask()
        
        task.Status = TaskStatus.Deferred
        task.StartDate = '1/1/4501'
        task.DueDate = task.StartDate
        task.Save()
        
    #---
    def __moveToWaitingList(self):
        task = cmdrui.application.getSelectedTask()
        
        task.Status = TaskStatus.WaitingFor
        task.StartDate = '1/1/4501'
        task.DueDate = task.StartDate
        task.Save()
        
    #---
    def __createActionItem(self):
        oldTask = cmdrui.application.getSelectedTask()
        task = cmdrui.application.createTask()
        
        task.Subject = oldTask.Subject
        task.Body = '''
        === SOURCE TASK INFORMATION ===
        Subject: %s 
        url:outlook:%s
        ''' % (oldTask.Subject, oldTask.EntryID)
        
        task.Status = TaskStatus.NotStarted
        task.StartDate = datetime.datetime.now()
        task.DueDate = task.StartDate
        
    #---
    def __createTaskToActionList(self):
        task = self.__createTaskFromMail()
        
        task.Status = TaskStatus.NotStarted
        task.StartDate = datetime.datetime.now()
        task.DueDate = task.StartDate
    #---
    def __createTaskToMasterList(self):
        task = self.__createTaskFromMail()
        
        task.Status = TaskStatus.NotStarted
        task.StartDate = '2/2/3000'
        task.DueDate = task.StartDate
    #---
    def __createTaskToIncubationList(self):
        task = self.__createTaskFromMail()
        
        task.Status = TaskStatus.Deferred
        task.StartDate = '1/1/4501'
        task.DueDate = task.StartDate
    #---
    def __createTaskToWaitingList(self):
        task = self.__createTaskFromMail()
        
        task.Status = TaskStatus.WaitingFor
        task.StartDate = '1/1/4501'
        task.DueDate = task.StartDate
    
    def __createTaskFromMail(self):
        app = cmdrui.application
        mail = app.getSelectedMail()
        task = app.createTask()
        
        task.Subject = mail.Subject
        task.Body = '''
        === SOURCE E-MAIL INFORMATION ===
        Subject: %s 
        From: %s 
        To: %s 
        Sent On: %s 
        url:outlook:%s
        ''' % (mail.Subject, mail.Sender, mail.To, mail.SentOn, mail.EntryID)
        return task

#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass
    
    
    
