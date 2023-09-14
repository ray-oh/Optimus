#!/usr/bin/env python
# coding: utf-8

"""
Module:         generalAutomationScript.py
Description:    RPA automation with Excel front end
Created:        30 Jul 2022

Versions:
20210216    Refactor KB Quest code - reusable sub routines - sub_TXT_*
            helper functions - hoverClick, hoverRclick, waitImage, waitImageDisappear, try_catch
            Logging
            Reorganize assets - image, log, output folders

"""
from logging import raiseExceptions
from prefect import task, flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner

import config
from auto_utility_PDF_Image import *
#from auto_utility_logging import *
from auto_utility_file import *
from auto_utility_browser import *
from auto_utility_parsers import *

import rpa as r
import traceback
import os.path
from os import path
from ctypes import windll

from datetime import date, datetime, timedelta
import time

# manage windows
# https://pypi.org/project/PyGetWindow/
import pygetwindow as gw
class Window:
    def __init__(self):
        '''instantiate a new windows object'''
        self.title = []
        self.new = []
        self.win = []
        self.snap()

    def get(self, name=''):
        '''returns list of all windows'''        
        return gw.getWindowsWithTitle(name)

    def getTitles(self, name=''):
        '''returns titles of all windows'''        
        return gw.getWindowsWithTitle(name)
    
    
    def snap(self, name=''):
        '''returns list of all windows'''        
        logger = get_run_logger()    
        selectedWindows = gw.getWindowsWithTitle(name)
        win_list = []
        title_list = []
        titles_str = f"{log_space}List of open windows:"
        for win in selectedWindows:
            #if win.title != '':
            #logger.debug(f'{log_space}Open Windows:{win.title}')
            #print(f'{log_space}Open Windows:{win.title}')
            win_list = win_list + [win]
            title_list = title_list + [win.title]
            if not win.title == '':
                titles_str = titles_str + '\n' + f'     {log_space}' + win.title
        #return result
        #print(win_list, title_list)
        logger.debug(f'{titles_str}')
        self.win = win_list
        self.title = title_list

    def getNew(self):
        new_set = self.get()
        prev_set = self.win
        #print(new_set,prev_set)
        new = Diff(new_set, prev_set)
        #self.win = new_set
        self.new = new
        #self.title = self._title()
        return new

    def getTitles(self, selection):
        titles = []
        for item in selection:
            titles = titles + [item.title]
        return titles
    
    def closeNew(self):
        logger = get_run_logger()    
        try:            
            #print(f'closed {self.new}')
            logger.debug(f'{log_space}Closed:{self.getTitles(self.new)}')
            for win in self.new:
                win.close()
            self.new = []
        except Exception as e:
            logger.debug('none closed')
            logger.debug(str(e))
            pass

    def focus(self, name=''):
        '''bring selected window to front'''
        logger = get_run_logger()    
        try:
            print('Focus *******', name.lower())
            self.snap()
            for win in self.win:  #self.new
                #print('list',str(win.title).lower())
                if name.lower() in str(win.title).lower():
                    print('selected ****',str(win.title).lower())                    
                    logger.debug(f'{log_space}Focus:{win.title}')
                    win.minimize()
                    win.restore()
        except Exception as e:
            logger.debug('error')
            logger.debug(str(e))
        
        
# Python code to get difference of two lists
# Not using set()
def Diff(li1, li2):
    #li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    li_dif = [i for i in li1 if i not in li2]
    return li_dif    
    
# manage processes - kill processes that match the list of specified process names
def process_kill(process=[]):
    import psutil
    import time
    #print(psutil.process_iter())
    #print(process)
    for proc in psutil.process_iter(): #process:
        #print(f"kill {proc.name()}")
        if proc.name() in process:
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                processUser = psutil.Process(processID).username()
                etime = (time.time() - proc.create_time())/60/60 # in hours
                print(processName , ' ::: ', processID, etime, processUser)
                if not 'SYSTEM' in processUser:
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print('error')
                pass

# this version can be removed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''
def process_list2(name='', minutes=30):
    #List processes less than time in min
    logger = get_run_logger()
    import psutil
    import time
    # Iterate over all running process
    result = []
    targetedList = ['chrome.exe','python.exe']
    exclusionList_system = ['svchost.exe', 'LogonUI.exe','winlogon.exe','ctfmon.exe',
    'smartscreen.exe','SearchFilterHost.exe','SearchProtocolHost.exe','dwm.exe',
    'msiexec.exe','TabTip.exe','rdpclip.exe','fontdrvhost.exe','csrss.exe',
    'WUDFHost.exe']
    exclusionList_security = ['TaniumCX.exe','vm3dservice.exe','rdpinput.exe']
    exclusionList_others = ['Code.exe']
    exclusionList = exclusionList_system + exclusionList_security + exclusionList_others

    def getListOfProcessSortedByCreateTime():

        #Get list of running process sorted by Created Time

        listOfProcObjects = []
        # Iterate over the list
        for proc in psutil.process_iter():
            try:
                # Fetch process details as dict
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
                pinfo['etime'] = round((time.time() - proc.create_time())/60,1) # in minutes
                # Append dict to list
                listOfProcObjects.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Sort list of dict by key vms i.e. memory usage
        #listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
        listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['etime'], reverse=True)        

        return listOfProcObjects

    log_str = f"{log_space}Running Process of last {minutes} min:\n"
    for proc in getListOfProcessSortedByCreateTime():
        log_str = log_str + f"     {log_space}{processName} ::: ID {processID} ::: {etime} min\n"


    log_str = f"{log_space}Running Process of last {minutes} min:\n"
    for proc in getListOfProcessSortedByCreateTime(): #psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            etime = round((time.time() - proc.create_time())/60,1) # in minutes
            if name in processName and etime < minutes:#etime < 60*30: #and not processName in 'svchost.exe python.exe msedge.exe conhost.exe TaniumCX.exe':
                result = result + [proc]
                if not processName in exclusionList:
                    log_str = log_str + f"     {log_space}{processName} ::: ID {processID} ::: {etime} min\n"
                #print(f"{log_space}{processName} ::: {processID} {etime}")
            #logger.debug(f"{log_space}{processName} ::: {processID} {etime}")           
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    logger.debug(log_str) 
    return result
'''

def process_list(name='', minutes=30):
    '''List processes less than time in min'''
    logger = get_run_logger()
    import psutil
    import time
    # Iterate over all running process
    result = []
    targetedList = ['chrome.exe','python.exe']
    exclusionList_system = ['svchost.exe', 'LogonUI.exe','winlogon.exe','ctfmon.exe',
    'smartscreen.exe','SearchFilterHost.exe','SearchProtocolHost.exe','dwm.exe',
    'msiexec.exe','TabTip.exe','rdpclip.exe','fontdrvhost.exe','csrss.exe',
    'WUDFHost.exe','WmiPrvSE.exe','conhost.exe']
    exclusionList_security = ['TaniumCX.exe','TaniumClient.exe','vm3dservice.exe','rdpinput.exe']
    exclusionList_others = ['Code.exe','msedge.exe']
    exclusionList = exclusionList_system + exclusionList_security + exclusionList_others

    def getListOfProcessSortedByCreateTime():
        '''
        Get list of running process sorted by Created Time
        '''
        result = []
        listOfProcObjects = []
        # Iterate over the list
        for proc in psutil.process_iter():
            try:
                processName = proc.name()
                etime = round((time.time() - proc.create_time())/60,1) # in minutes                
                if name in processName and etime < minutes:#etime < 60*30: #and not processName in 'svchost.exe python.exe msedge.exe conhost.exe TaniumCX.exe':                
                    if not processName in exclusionList:
                        result = result + [proc]                       
                        # Fetch process details as dict
                        pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                        pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
                        pinfo['etime'] = etime
                        # Append dict to list
                        listOfProcObjects.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Sort list of dict by key vms i.e. memory usage
        #listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
        listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['etime'], reverse=True)        

        return listOfProcObjects, result

    listOfProcObjects, result = getListOfProcessSortedByCreateTime()
    #print(listOfProcObjects)
    #print(result)
    #log_space = '     '
    log_str = f"{log_space}Running Process of last {minutes} min:\n"
    for proc in listOfProcObjects:
        log_str = log_str + f"     {log_space}{proc['name']} ::: ID {proc['pid']} ::: {proc['etime']} min\n"
        pass

    logger.debug(log_str)
    #print(log_str)
    return result


# import configuration Excel
#def readExcelConfig(sheet, excel = '.\main.xlsx'):
#mainExcelConfigFile = '.\main.xlsm'
# define above in the main file with config.json
import pandas as pd
#print('autohelper lib', startfile)
def readExcelConfig(sheet, excel = config.STARTFILE, refresh=True):
    logger = get_run_logger()
    from config import PROGRAM_DIR, STARTFILE

    #logger.info(f"readExcelConfig {sheet} {excel}")

    #print('readexcelconfig', config.STARTFILE)
    excel = getFullPath(excel)
    #logger.info(f"readExcelConfig fullpath {sheet} {excel}")

    #print('excel value', excel)
    logger.debug(f"refreshExcel {sheet} {excel} {PROGRAM_DIR} {STARTFILE}")
    if refresh:#refreshExcel(excel):
        from pathlib import Path, PureWindowsPath
        
        import pythoncom
        pythoncom.CoInitialize()    # to avoid com_error: (-2147221008, 'CoInitialize has not been called.', None, None)
        '''
        #import win32com.client
        #xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
        
        # https://stackoverflow.com/questions/61071022/pywintypes-com-error-2147221008-coinitialize-has-not-been-called-none-n
        office = win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
        wb = office.Workbooks.Open(Path(excel).absolute().__str__())
        wb.RefreshAll()
        office.CalculateUntilAsyncQueriesDone()
        wb.Save()
        wb.Close(SaveChanges=False)
        office.Quit()
        '''
        
        import xlwings as xw
        # open Excel app in the background
        app_excel = xw.App(visible = False)

        wbk = xw.Book(Path(excel).absolute().__str__())
        wbk.api.RefreshAll()
        logger.debug(f'{log_space}Excel refreshed: {excel}')

        # two options to save
        wbk.save(Path(excel).absolute().__str__()) # this will overwrite the file
        #wbk.save( 'D:\stuff\name1.xlsx' ) # this will save the file with a name
        wbk.close()

        # kill Excel process
        app_excel.kill()
        del app_excel
        #app_excel.quit()
        
        processName = "Excel"
        import subprocess
        command = "Get-Process | Where-Object {{$_.Name -Like '{}'}} ".format(processName)
        result = subprocess.run(["powershell.exe", command], capture_output=True)
        if len(result.stdout.decode('ASCII')) > 0:
            logger.warning("process killed" + result.stdout.decode('ASCII'))
            #print("process killed" + result.stdout.decode('ASCII'))

    df = pd.read_excel(excel, sheet_name=sheet)
    #df = df[['Type','Object','Key','Value']][df.Key.notna()]
    df = df[df.Key.notna()]     # do not only filter key and value columns
    df[['Type','Object']] = df[['Type','Object']].fillna(method='ffill')
    constants['iterationCount'] = 0     # reset iterationCount when running a new sheet
    return df
    #else:
    #    exit(2)

#dfmain = readExcelConfig('DCLICK2')

from pathlib import Path, PureWindowsPath
def refreshExcel(excel = ''):
    # overwrite logic to test
    #return True
    ''' if excel is open with workbooks: do not quit excel
            if workbook matches target excel: do not close workbook
            if workbook does not match target excel: close workbook           
        if excel is not open or without open workbooks: close workbook, quit excel
    '''
    #logger = get_run_logger()
    #logger.info(f"refreshExcel {excel} {__name__} {__file__}")

    if excel == '':
        return False
    workBookName = Path(excel).name
    fileIsOpen = checkIfFileOpen(excel)
    excel = Path(excel).absolute()
    #print('excel value', excel)
    #print('refresh', workBookName, excel)

    #logger.info(f"refreshExcel workbookname:{workBookName}  {excel}")

    import pythoncom
    import win32com.client
    #xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
    # https://stackoverflow.com/questions/61071022/pywintypes-com-error-2147221008-coinitialize-has-not-been-called-none-n
    office = win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
    #office.Visible = True             #xl.Visible = True is not necessary, used just for convenience'
    excelQuit = True
    wbClose = True

    #logger.info(f"refreshExcel - open count:{office.Workbooks.Count}")
    if office.Workbooks.Count > 0:  # excel open with workbooks - do not quit excel
        #if fileIsOpen:
        #for i in office.Workbooks: print('list of open workbooks',i.Name)
        excelQuit = False
        # target workbook is open - do not close the workbook
        #if any(i.Name == workBookName for i in office.Workbooks): 
        for i in office.Workbooks:
            if i.Name == workBookName:
                wb = i
                #print('do not close workbook')
                #logger.info(f"Do not close:{i.Name}")
                wbClose = False
        wb = office.Workbooks.Open(excel.__str__())
    else:
        #logger.info(f"Opening workbook {excel}")
        #logger.info(f"Path is: {Path(excel).is_file()}")        

        import os
        f = excel #'C:/test.xlsx'
        if os.path.exists(f):
            try:
                os.rename(f, f)
                logger.debug(f'{log_space}Access on file "' + f.name +'" is available!')
            except OSError as e:
                logger.critical('Access-error on file "' + f.name + '"! \n' + str(e))
        wb = office.Workbooks.Open(excel.__str__())
        #wb = office.Workbooks.Open('D:\Optimus-Prefect-Test1\scripts\cscKPI.xlsm')
    #wb = office.Workbooks.Open(workBookName)
    logger.debug(f"{log_space}Refreshing workbook")        
    wb.RefreshAll()
    office.CalculateUntilAsyncQueriesDone()
    wb.Save()
    #logger.info(f"Refreshed workbook")        
    if wbClose: wb.Close(SaveChanges=False)
    #if wbClose: wb.Close()
    if excelQuit: office.Quit()

    #logger.info(f"check 2")

    return True


# ***********************************************************************************************************************

def dfKey_value(df, key, offset = 1):
    '''# return value given object and key
        #def dfKey_value(df, object, key):
    '''
    try:
        # retrieve all URLs as a list
        #df = df[(df.Type == 'key') & (df.Object == object)][['Key', 'Value']]
        #df = df[(df.Type == 'key')][['Key', 'Value']]
        df = df[(df.Type == 'key')].reset_index(drop=True)
        #print(df)
        #df.set_index("Key", inplace = True) # setting first name as index column
        #print(df.loc[key]['Value']) # return specific value of key
        x = df.index[(df['Key']==key)].tolist()[0]
        y = df.columns.get_loc('Key')+offset
        #print(key,x,y)
        #print(df)
        result = df.iloc[x,y]
        #print(result)
        #df.loc[key]['Value']
        return result 
    except KeyError:
        print('Key does not exist - key error:', key)
        #pass
        return None
    except IndexError:
        print('Key does not exist - index error:', key)
        #pass
        return None
#print(dfKey_value(df, 'URL', 'url1'))


def dfObjList(df, object_value, withHeader=0):
    '''# return list of "key" values for given object'''
    try:
        #list = df[((df.Type == 'list') | (df.Type == 'key')) & (df.Object == parameter)]['Key'].values.tolist()
        if object_value in df['Object'].unique().tolist():
            list = df[(df.Object == object_value)]['Key'].values.tolist()
            if withHeader: list = list[1:]
            return list
        else:
            # get first rows of each group of table            
            result = df[(df.Type=='table')].groupby('Object', as_index=False)
            final = result.nth(0) # Selecting 1st row of group by result
            #list = []
            for i in range(len(final)):
                #list = list + final.iloc[i].values.tolist()
                if object_value in final.iloc[i].values.tolist():
                    objTable = final.iloc[i].values.tolist()[1]
                    objTableSet = df[(df.Type == 'table') & ((df.Object == objTable))]
                    new_header = objTableSet.iloc[0] #grab the first row for the header
                    objTableSet = objTableSet[1:] #take the data less the header row
                    #objTableSet.set_axis(new_header, axis=1, inplace=True)
                    objTableSet.columns = new_header #set the header row as the df header
                    list = objTableSet[object_value].values.tolist()                    
                    print(objTableSet)
                    print(list)
                    return list
            return None
    except:
        return None

def updateConstants(df, code):
    '''Search and replace special characters and values i.e. <template values> or {{ template values }} in the code'''
    logger = get_run_logger()
    import re
    matchConstants = re.findall( r'<(.*?)>', code) + re.findall( r'{{(.*?)}}', code)     # Output: ['cats', 'dogs']
    if not matchConstants: return code
    #logger.info(f"   updateConstants ...', code = {code}, matchConstants = {matchConstants}")

    for item in matchConstants:                
        #logger.info(f"    process item {item}")
        evalValue=re.findall( r'[eE][vV][aA][lL]\((.*)\)', item.strip()) # greedy mode without ?, instead of lazy mode
        if len(evalValue)>0:                                  #evaluate contents
            from datetime import datetime
            evalStr = str(evalValue[0])
            print("evalValue:",evalValue, evalStr)
            value = eval(evalStr)
            code = code.replace("<" + item + ">", str(value))  # replace templated values
            code = code.replace("{{" + item + "}}", str(value))  # replace templated values
        elif item in df[(df.Object == 'constants')]['Key'].values.tolist(): #Constants defined by user in excel
            value = dfKey_value(df[(df.Object == 'constants')], item)
            #logger.info(f"   match constants >>> key: {item}, value: {str(value)}")            
            code = code.replace("<" + item + ">", str(value))  # replace templated values
            code = code.replace("{{" + item + "}}", str(value))  # replace templated values
        elif item in constants: #system constants e.g. ['yesterdayYYYYMMDD', 'yesterdayDDMMYYYY', 'todayDDMMYYYY', 'todayYYYYMMDD', 'iterationCount']:
            if item == 'iterationCount':
                #logger.info(f"   match iterationCount >>> count = {constants['iterationCount']}")                
                value = constants['iterationCount']
                #code = code.replace("<iterationCount>", str(constants['iterationCount']))  
                code = code.replace("<" + item + ">", str(value))  # replace templated values
                code = code.replace("{{" + item + "}}", str(value))  # replace templated values
            else:               
                #logger.info(f"   match system constants >>> key: {item}, value: {str(constants[item])}")                
                value = constants[item]                
                #code = code.replace("<" + item + ">", str(constants[item]))  
                code = code.replace("<" + item + ">", str(value))  # replace templated values
                code = code.replace("{{" + item + "}}", str(value))  # replace templated values
        elif item in variables.keys() or item in df[(df.Object == 'variables')]['Key'].values.tolist():  # variables defined by user in excel
            # or item in df[(df.Object == 'variables')]['Key'].values.tolist(): 
            #logger.info(f"   match variables >>> key: {item}, variables: {variables}")
            if item in variables.keys():
                value = variables[item]
                code = code.replace("<" + item + ">", str(value))
                code = code.replace("{{" + item + "}}", str(value))  # replace templated values
            else:
                value = dfKey_value(df[(df.Object == 'variables')], item)
                # check if value is nan (when not defined in excel).  And if so, patch it as blank
                import math
                if math.isnan(value):
                    #print('dfkey', type(value), value)
                    value = ''                
                #logger.info(f"   match constants >>> key: {item}, value: {str(value)}")            
                code = code.replace("<" + item + ">", str(value))  # replace templated values
                code = code.replace("{{" + item + "}}", str(value))  # replace templated values
        elif len(re.findall( r'@(.*?)\((.*?)\)', item))>=1:     # formulas
            value = ''
            formula = re.findall( r'@(.*?)\((.*?)\)', item) # returns tuple with formula name and parameters
            import traceback
            try:
                name = formula[0][0].strip()
                parameters = formula[0][1].strip()
                value = _formula(name, parameters)
                logger.info(f"   match formula >>> item: {item} formula: {name}, parameters: {parameters}, result: {value}")
                code = code.replace("<" + item + ">", str(value))
                code = code.replace("{{" + item + "}}", str(value))  # replace templated values
            except Exception as e:
                logger.info(traceback.format_exc())     # Logs the error appropriately. 
        elif len(item.split(':')) == 2: # objects with key value pair defined in excel e.g. code has <obj:attribute> 
            ''' objItem:key or objItem:value like <URL_pages:key> <URL_pages:value> <URL_pages:4> where 4 is offset from key, <URL_pages:@custom_header> '''
            obj = item.split(':')[0].strip()
            attribute = item.split(':')[1].strip()
            # handle table objects - old legacy syntax - see below for new syntax
            if obj[:4]=='tbl@':
                obj = obj[4:]
                withHeader = 1
            else:
                withHeader = 0
            #logger.info(f"   match obj >>> item: {item}, key: {obj}, attribute: {attribute}, iterationCount: {str(constants['iterationCount'])}")
            if obj in df[(df.Type == 'key')]['Object'].dropna().values.tolist():
                # and attribute.lower() in ['key','value','0','1','2','3','4','5','6','7','8','9','10','11']:
                #objLists = df[(df.Type == 'key') & ((df.Object == obj))][['Key','Value']].dropna().values.tolist()
                if withHeader==1:       # table objects with header
                    #logger.info("A1")
                    custom_header_field = attribute
                    objTableSet = df[(df.Type == 'key') & ((df.Object == obj))]
                    new_header = objTableSet.iloc[0] #grab the first row for the header
                    objTableSet = objTableSet[1:] #take the data less the header row
                    #objTableSet.set_axis(new_header, axis=1, inplace=True)
                    objTableSet.columns = new_header #set the header row as the df header
                    objLists = objTableSet[custom_header_field].values.tolist()                    
                elif attribute.lower() == 'key':
                    #logger.info("A2")
                    objLists = df[(df.Type == 'key') & ((df.Object == obj))]['Key'].values.tolist()
                elif attribute.lower() == 'value':
                    #logger.info("A3")
                    objLists = df[(df.Type == 'key') & ((df.Object == obj))]['Value'].values.tolist()
                elif attribute.lower() in ['0','1','2','3','4','5','6','7','8','9','10','11']: # '0', '1', ....
                    #logger.info("A4")
                    offset = int(attribute.lower())
                    columnIndex = df.columns.get_loc('Key')+offset
                    objLists = df[(df.Type == 'key') & ((df.Object == obj))].iloc[:,columnIndex].values.tolist()
                elif attribute.lower()[:1] == '@': # table with custom header
                    #logger.info("A5")
                    custom_header = attribute[1:]
                    objTableSet = df[(df.Type == 'key') & ((df.Object == obj))]
                    new_header = objTableSet.iloc[0] #grab the first row for the header
                    objTableSet = objTableSet[1:] #take the data less the header row
                    #objTableSet.set_axis(new_header, axis=1, inplace=True)
                    objTableSet.columns = new_header #set the header row as the df header
                    objLists = objTableSet[custom_header].values.tolist()
                if 'iterationCount' in constants:
                    #logger.info("A6")
                    value = objLists[constants['iterationCount']]
                    #logger.info(f"   replace <item> with value in code >>> item: {item}, value: {str(value)}, iterationCount: {str(constants['iterationCount'])}")
                    code = code.replace("<" + item + ">", str(value))
                    code = code.replace("{{" + item + "}}", str(value))  # replace templated values
            elif obj in df[(df.Type == 'table')]['Object'].dropna().values.tolist():  # HANDLE Table Objects
                #logger.info("A7")
                custom_header_field = attribute
                objTableSet = df[(df.Type == 'table') & ((df.Object == obj))]
                new_header = objTableSet.iloc[0] #grab the first row for the header
                objTableSet = objTableSet[1:] #take the data less the header row
                #objTableSet.set_axis(new_header, axis=1, inplace=True)
                objTableSet.columns = new_header #set the header row as the df header
                objLists = objTableSet[custom_header_field].values.tolist()                    
                if 'iterationCount' in constants:
                    #logger.info("A8")
                    value = objLists[constants['iterationCount']]
                    #logger.info(f"   replace <item> with value in code >>> item: {item}, value: {str(value)}, iterationCount: {str(constants['iterationCount'])}")
                    code = code.replace("<" + item + ">", str(value))
                    code = code.replace("{{" + item + "}}", str(value))  # replace templated values

    #logger.info(f"   Updated Code >>> code: {code}")
    return code


def _formula(name:str, code:str = ''):
    logger = get_run_logger()
    if name.lower() == 'fileuptodate':
        try:
            param1 = code.split(',')[0].strip()
            date_string = code.split(',')[1].strip()
            logger.info(param1 + " | " + date_string)
            param2 = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            logger.info(f'formula .... name {name} param1 {param1} param2 {param2}')
            return _fileuptodate(param1, param2)
        except Exception as e:
            logger.info(traceback.format_exc())     # Logs the error appropriately. 
            return None
    elif False:
        pass
    return None

def _fileuptodate(path_to_file: str, date: float):
    import datetime
    serial = date     #43111.0
    seconds = (serial - 25569) * 86400.0
    comparetime = datetime.datetime.utcfromtimestamp(seconds)
    return datetime.datetime.fromtimestamp(file_date(path_to_file)) >= comparetime

import os
import platform

def file_date(path_to_file, type:str = 'm') -> 'float':
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        if type == 'm':
            return os.path.getmtime(path_to_file)
        elif type == 'c':
            return os.path.getctime(path_to_file)
        elif type == 'a':
            return os.path.getatime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            if type == 'm':
                return stat.st_mtime
            elif type == 'c' or type == 'a':            
                return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


'''
Not used

# sub all blocks in the list
def updateListBlockCodes(df, run_label):
    itemPos = 0
    main = dfObjList(df, run_label)
    #print('main',main)
    for i in main:
        itemPos += 1
        #print('i', i)
        if i in parameterObjs(df):
            #print('found', i)
            #print('position', main.index(i))
            #print('itemPos', itemPos)
            main[itemPos-1:itemPos] = dfObjList(df, i) #['a','b','c']
    #print('inserted',main)
    return main
#run_code = updateListBlockCodes(df, 'logon_OKTA')
#print('update ******', run_code)

# return all available parameter objects
def parameterObjs(df):
    parameterObjs = df[(df.Type == 'list')]['Object'].dropna().values.tolist()
    return parameterObjs
#print('parameterObjs', parameterObjs(df))


'''

# ***********************************************************************************************************************

class CriticalAccessFailure(Exception):
    def __init__(self, err):
        print('a: critical')
        Exception.__init__(self)
        self.error = err
    def __str__(self):
        print('b: critical')
        return "%r" % self.error

# Wrapper for catching exceptions
def try_catch(func, comment=''):
    #logger = get_run_logger()
    try:
        #print('try',func)
        #logger.info(f"'entering try catch func call ', comment = {comment}")
        result = func
    except CriticalAccessFailure as caf:
        #snapImage('Snap picture - Critical Failure - at', '_Fail.PNG')
        print('Critical Error')
        logger.info(f"'Critical failure', level = 'critical', caf = {caf}")
        logging.critical(caf)
        #AutoCloseMessageBoxW('Citrical failure ... ','TEST_CLOSE',3)
        #copyfile(srcLog, dstLog)
        r.close()
        sys.exit(3)
        #exit(3)
    except Exception as e:
        print('Exception error')
        logger.info(f"'exception', e = {e}, level = 'error'")
        r.close()
        sys.exit(4)
        pass
    except:
        print('Except error')
        logger.info(f"'except', level = 'error'")
        r.close()
        sys.exit(5)
        #exit(3)
        pass
    finally:
        #print('catch finally')
        #logger.info(f"try_catch finally")
        return result

