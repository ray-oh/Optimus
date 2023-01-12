#!/usr/bin/env python
# coding: utf-8

"""
Module:         auto_utility_browser.py
Description:    Utilities for browser automation
Created:        30 Jul 2022

Versions:
20210216    Reorganize utility file
"""

# Email Individual Reports to Respective Recipients
import datetime
import os
import shutil
from pathlib import Path
import pandas as pd
import win32com.client as win32

from prefect import task, flow, get_run_logger, context
from prefect.task_runners import SequentialTaskRunner

## Set Date Formats
today_string = datetime.datetime.today().strftime('%m%d%Y_%I%p')
today_string2 = datetime.datetime.today().strftime('%b %d, %Y')

## Set Folder Targets for Attachments and Archiving
attachment_path = Path.cwd() / 'data' / 'attachments'
archive_dir = Path.cwd() / 'archive'
#src_file = Path.cwd() / 'data' / 'Example4.xlsx'
src_file = Path.cwd() / 'mail.xlsx'

#df = pd.read_excel(src_file)
#df.head()

today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) #.strftime('%Y-%m-%d')
#print(today.strftime('%d/%m/%Y %H:%M %p'))

#global sentEmailSubjectList
sentEmailSubjectList = []

class EmailsSender:
    def __init__(self):
        logger = get_run_logger()
        #self.outlook = win32.Dispatch('outlook.application')
        # https://stackoverflow.com/questions/50127959/win32-dispatch-vs-win32-gencache-in-python-what-are-the-pros-and-cons
        from pathlib import Path
        import tempfile
        #tempfolder = Path(str(tempfile.gettempdir()) + '/gen_py').absolute.__str__() # prints the current temporary directory
        tempfolder = Path(tempfile.gettempdir(), 'gen_py') #.absolute.__str__()
        #print(tempfolder)
        try:
            #logger.info("Initialize EmailsSender class")
            #raise AttributeError
            self.outlook = win32.gencache.EnsureDispatch('outlook.application')
            #logger.info("Launch COM object")
            #self.outlook = win32.Dispatch('outlook.application')      
        except AttributeError:
            # using gencache may have AttributeError - if so, delete gen_py in temp folder and relauch com object
            logger.info("AttributeError - relaunch COM object")
            f_loc = tempfolder #r'C:\Users\svc_supplychain\AppData\Local\Temp\gen_py'
            #for f in Path(f_loc):
            #    Path.unlink(f)
            #Path.rmdir(f_loc)
            import shutil
            shutil.rmtree(f_loc)
            self.outlook = win32.gencache.EnsureDispatch('outlook.application')
        
        self.olOutbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(4) #outlook.olFolderOutbox)

        # get list of previous sent items
        #import datetime
        global today
        #print(today.strftime('%d/%m/%Y %H:%M %p'))
        global sentEmailSubjectList
        #print('>>>> sentEmailSubList',len(sentEmailSubjectList))
        if len(sentEmailSubjectList) == 0: sentEmailSubjectList = self.folderItemsList(ofolder=5,dateRange_StartOn=today)          #.sentFolderList()                
        #print('>>>> sentEmailSubList',len(sentEmailSubjectList))

        #from auto_core_lib_helper import _ifObjectExist
        #print(_ifObjectExist('sentEmailSubjectList'))
        #if _ifObjectExist('sentEmailSubjectList'):

    def refreshMail(self):
        logger = get_run_logger()

        #olNS = self.outlook.GetNamespace("MAPI")  #.GetDefaultFolder(4) #outlook.olFolderOutbox)
        #olNS.SendAndReceive(False)
        #OutlookApp = self.outlook
        #_syncObject = OutlookApp._SyncObject  #= null
        #_syncObject = olNS.SyncObjects[1]
        #_syncObject.Start()
            
        #System.Threading.Thread.Sleep(30000)

        #_syncObject.Stop()
        #_syncObject = null


        nsp = self.outlook.GetNamespace("MAPI")
        objSyncs = nsp.SyncObjects
        objSyc = objSyncs.AppFolders

        from win32com.client import constants
        mpfInbox = nsp.GetDefaultFolder(constants.olFolderInbox)  #olFolderSentMail  #olFolderOutbox
        logger.info("-----------------------------------refreshMail")

        #mpfInbox.InAppFoldersSyncObject = True
        objSyc.Start

        objSyc.Stop

        #folder = nsp.Folders.Item("Your Mailbox")
        #inbox = folder.Folders.Item("Inbox")
        #msg = inbox.Items
        msg = mpfInbox.Items
        msgs = msg.GetLast().ReceivedTime #.Subject
        print(msgs)



    def temp2():
        import pythoncom
        pythoncom.CoInitialize()    # to avoid com_error: (-2147221008, 'CoInitialize has not been called.', None, None)

        from pathlib import Path
        try:
            logger.info("Try 1 ,,,23")
            #office = win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
            import win32com.client as win32
            #xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())

            self.outlook = win32.Dispatch('outlook.application',pythoncom.CoInitialize())
            #self.outlook = win32.gencache.EnsureDispatch('outlook.application')
            self.olOutbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(4) #outlook.olFolderOutbox)

        except AttributeError:
            logger.info("Try 2")

            f_loc = r'C:\Users\svc_supplychain\AppData\Local\Temp\gen_py'
            for f in Path(f_loc):
                Path.unlink(f)
            Path.rmdir(f_loc)
            self.outlook = win32.gencache.EnsureDispatch('outlook.application')
            self.olOutbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(4) #outlook.olFolderOutbox)

    def temp():
        logger = get_run_logger()
        try:
            logger.info("Try 1")

            from win32com import client as win32
            #self.outlook = win32.gencache.EnsureDispatch('outlook.application')
            self.outlook = win32.Dispatch('outlook.application')
            self.olOutbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(4) #outlook.olFolderOutbox)
            #xl = client.gencache.EnsureDispatch('Excel.Application')
        except AttributeError:
            logger.info("Try 2")

            # Corner case dependencies.
            import os
            import re
            import sys
            import shutil
            # Remove cache and try again.
            MODULE_LIST = [m.__name__ for m in sys.modules.values()]
            for module in MODULE_LIST:
                if re.match(r'win32com\.gen_py\..+', module):
                    del sys.modules[module]
            shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
            from win32com import client as win32
            #import win32com.client as win32
            #xl = client.gencache.EnsureDispatch('Excel.Application')
            self.outlook = win32.gencache.EnsureDispatch('outlook.application')      
            self.olOutbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(4) #outlook.olFolderOutbox)

    def send_email(self, boolDisplay=False, boolRun=True, **members):
        # parameters/members: EmailObj or To, CC, Subject, HTMLBody, Attachment etc. Attachment comma delimited list
        logger = get_run_logger()
        #logger.info(', '.join(['{}={!r}'.format(k, v) for k, v in members.items()]))
        mail = self.outlook.CreateItem(0)

        if not boolRun: 
            logger.info(f"Skip run:{not boolRun}")
            return  # skip send_email if boolRun is False

        for key,value in members.items():
            #logger.info("{}: {}".format(key,value))
            if key == "EmailObj":
                for item in value:
                    if item=="To" and value[item] is not None:
                        mail.To = value[item]
                    elif item=="CC" and value[item] is not None:
                        mail.CC = value[item]
                    elif item=="Subject" and value[item] is not None:
                        mail.Subject = value[item]
                    elif item=="Body" and value[item] is not None:
                        mail.Body = value[item]
                    elif item=="HTMLBody" and value[item] is not None:
                        mail.HTMLBody = value[item]
                    elif item=="Attachment" and value[item] is not None:
                        attachments = value[item].split(',')
                        for item in attachments:
                            from pathlib import Path
                            file = Path(item.strip())
                            if file.is_file():
                                # file exists
                                mail.Attachments.Add(file.resolve().absolute().__str__())
            else:
                if key=="To" and value is not None: mail.To = value #'To address'
                if key=="CC" and value is not None: mail.CC = value #'To address'
                if key=="Subject" and value is not None: mail.Subject = value
                if key=="Body" and value is not None: mail.Body = value
                if key=="HTMLBody" and value is not None: mail.HTMLBody = value #this field is optional
                if key=="Attachment" and value is not None: # and type(value)==list:
                    attachments = value.split(',')
                    for item in attachments:
                        from pathlib import Path
                        file = Path(item.strip())
                        if file.is_file():
                            # file exists
                            mail.Attachments.Add(file.resolve().absolute().__str__())        

        from auto_initialize import checkFileValid
        from pathlib import Path, PureWindowsPath
        # if mail.HTMLBody is a valid file, replace mail.HTMLBody with the content of the file
        # current directory is the folder of the script file
        if checkFileValid(Path(mail.HTMLBody)):
            html_file = Path(mail.HTMLBody).resolve().absolute().__str__()
            with open(html_file, 'r') as f:
                mail.HTMLBody = f.read()
                f.close()
        #print(f"current dir {Path('.').resolve().absolute().__str__()}")
        #print(f"mail.HTML {mail.HTMLBody}")

        if boolDisplay:
            mail.Display(True)
            #pass
        else:
            mail.Send()
            #print('email sent')
            pass
        #logger.info(boolDisplay)
        #logger.info('Count after:' + str(self.olOutbox.Items.Count))
                    
    def wait_send_complete(self, timeOut=900):
        logger = get_run_logger()
        #olOutbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(4) #outlook.olFolderOutbox)
        #print('Count:', self.olOutbox.Items.Count)
        #logger.info('   ###################################################')
        logger.info(f"   Outbox sending in progress - outbox item count: {self.outlook.GetNamespace('MAPI').GetDefaultFolder(4).Items.Count}" )
        #logger.info(f"Outbox Items: {self.outlook.GetNamespace('MAPI').GetDefaultFolder(4).Items[1].Subject}" )
        import time
        for i in range(timeOut):
            # https://learn.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders
            itemsInOutbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(4).Items.Count
            if itemsInOutbox == 0: return True #break
            time.sleep(1) # Sleep for 1 seconds           
            logger.info(f"   Timeout countdown {i} to {timeOut}.  Outbox item count: {itemsInOutbox}")

        logger.info('   Timeout:' + str(itemsInOutbox))
        return False
    
    def sentFolderList(self):
        logger = get_run_logger()
        logger.info(f"Sentbox item count: {self.outlook.GetNamespace('MAPI').GetDefaultFolder(5).Items.Count}" )

        import win32com.client as win32
        import datetime

        dateRange_StartOn = datetime.datetime(2022, 11, 27, 0, 1)
        dateRange_UpTo =  datetime.datetime(2022, 11, 27, 8, 0)
        #outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        sentfolder = self.outlook.GetNamespace('MAPI').GetDefaultFolder(5)
        #acc = outlook.Folders("myemail@myprovide.com")
        #inbox = acc.folders("Inbox") #Language-specific to the users GUI. "Inbox" is not a universal, internally fixed name

        def tzInfo2Naive(in_dtObj): #Convert the tzInfo of the datetime object to naive (none)
            return datetime.datetime(in_dtObj.year,in_dtObj.month,in_dtObj.day,in_dtObj.hour,in_dtObj.minute)
        print(type(sentfolder.Items))
        format = '%d/%m/%Y %H:%M %p'
        strDate = datetime.datetime.strftime(dateRange_StartOn, format)
        #Format("1/15/99 3:30pm", "ddddd h:nn AMPM")
        _sFilter_ = "[LastModificationTime] > '" + strDate  + "'"
        print(_sFilter_)
        #https://learn.microsoft.com/en-us/office/vba/api/outlook.items.restrict
        folderItems = sentfolder.Items.Restrict(_sFilter_)
        logger.info(f"Folder item count: {folderItems.Count}" )
        #for message in sentfolder.Items.Restrict(_sFilter_):
        subjectList = []
        for message in folderItems:
            sub = message
            timeReceived = message.ReceivedTime #datetime-object
            timeReceived = tzInfo2Naive(timeReceived)
            #if timeReceived > dateRange_StartOn and timeReceived < dateRange_UpTo:
            #    print("%s :: %s" % (str(timeReceived), sub.Subject))
            if not str(sub.Subject) in subjectList:
                print("%s :: %s" % (str(timeReceived), sub.Subject))
                subjectList = subjectList + [str(sub.Subject)]

        return subjectList

    def folderItemsList(self, ofolder=5, dateRange_StartOn = datetime.datetime(2022, 11, 27, 0, 1)):
        logger = get_run_logger()
        #logger.info(f"Folder {ofolder}, item count: {self.outlook.GetNamespace('MAPI').GetDefaultFolder(ofolder).Items.Count}" )

        #import win32com.client as win32
        import datetime

        #dateRange_StartOn = datetime.datetime(2022, 11, 27, 0, 1)
        #dateRange_UpTo =  datetime.datetime(2022, 11, 27, 8, 0)
        
        #outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        folder = self.outlook.GetNamespace('MAPI').GetDefaultFolder(ofolder)
        #acc = outlook.Folders("myemail@myprovide.com")
        #inbox = acc.folders("Inbox") #Language-specific to the users GUI. "Inbox" is not a universal, internally fixed name

        def tzInfo2Naive(in_dtObj): #Convert the tzInfo of the datetime object to naive (none)
            return datetime.datetime(in_dtObj.year,in_dtObj.month,in_dtObj.day,in_dtObj.hour,in_dtObj.minute)
        #logger.info(type(folder.Items))
        format = '%d/%m/%Y %H:%M %p'
        strDate = datetime.datetime.strftime(dateRange_StartOn, format)
        #Format("1/15/99 3:30pm", "ddddd h:nn AMPM")
        _sFilter_ = "[LastModificationTime] > '" + strDate  + "'"
        #logger.info(_sFilter_)
        #https://learn.microsoft.com/en-us/office/vba/api/outlook.items.restrict
        folderItems = folder.Items.Restrict(_sFilter_)
        #for message in sentfolder.Items.Restrict(_sFilter_):
        subjectList = []
        logMaillist = ""
        if folderItems.Count > 0:
            for message in folderItems:
                sub = message
                timeReceived = message.ReceivedTime #datetime-object
                timeReceived = tzInfo2Naive(timeReceived)
                #if timeReceived > dateRange_StartOn and timeReceived < dateRange_UpTo:
                #    print("%s :: %s" % (str(timeReceived), sub.Subject))
                if not str(sub.Subject) in subjectList:
                    #print("%s :: %s" % (str(timeReceived), sub.Subject))
                    logMaillist = logMaillist + f"{tzInfo2Naive(sub.ReceivedTime)}::{sub.Subject}\n"
                    subjectList = subjectList + [str(sub.Subject)]
            #logger.info(f"{tzInfo2Naive(sub.ReceivedTime)}::{sub.Subject}\n")
            logger.info(f"Folder item count: {folderItems.Count}, {logMaillist}" )
            #logger.info(logMaillist)

        return subjectList

