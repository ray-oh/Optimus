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
from prefect import task, flow, get_run_logger, context
from prefect.task_runners import SequentialTaskRunner

from config import variables, constants, STARTFILE, CWD_DIR, IMAGE_DIR, yesterdayYYYYMMDD
from pathlib import Path, PureWindowsPath
import rpa as r

from auto_helper_lib import dfObjList, dfKey_value, readExcelConfig, updateConstants, CriticalAccessFailure
from auto_utility_PDF_Image import cropImage, createPDFfromImages, addContentPDF
from auto_utility_file import GetRecentCreatedFile, runInBackground, renameFile
from auto_utility_browser import chromeZoom, waitIdentifierExist, waitIdentifierDisappear, exitProg, snapImage
from auto_utility_parsers import parseArguments, regexSearch
from auto_utility_email import EmailsSender

def _otherRunCode(df, code, codeID, codeValue, objVar):   
    if False: pass
    # ------------------ code processing functions ------------------------------
    elif codeID.lower() == 'rem'.lower():   pass                    # remarks - do nothing
    elif codeID.lower() == 'print'.lower():  _print(codeValue)
    elif codeID.lower() == 'log':  _log(codeValue)
    elif codeID.lower() == 'exit'.lower():    _exit()
    elif codeID.lower() == 'exitError'.lower():    _exitError(codeValue)                 # exit with an error code e.g. exitError:2
    elif codeID.lower() == 'raiseError'.lower():    _raiseError(codeValue)                 # exit with an error code e.g. exitError:2
    elif codeID.lower() == 'if'.lower(): return _if(codeValue, df, objVar)
    elif code in df[(df.Type == 'list')]['Object'].dropna().values.tolist(): return _isCodeList(df, code, objVar)          #run Block of Code
    elif codeID.lower() == 'runModule'.lower(): return _runModule(codeValue, df, objVar)                  #runModule:sheet, excelfile
    elif codeID.lower() == 'codeList'.lower(): return _codeList(codeValue, df, objVar)
    elif codeID.lower() == 'wait'.lower():  return _wait(codeValue, df, objVar)                        # wait:time_sec,identifier,run_code
    elif codeID.lower() == 'waitDisappear'.lower(): return _waitDisappear(codeValue, df, objVar)                        # waitDisappear:time_sec,identifier,run_code
    elif codeID.lower() == 'iterate'.lower(): return _iterate(codeValue, df, objVar)                    # iterate: objlists, runCodelist e.g. iterate: @url_pages : openPage
    elif codeID.lower() == 'iterationCount'.lower(): _iterationCount(codeValue, df, objVar)
    elif codeID.lower() == 'test'.lower(): _test(codeValue, df, objVar)

    # ------------------ Custom functions ------------------------------
    elif codeID.lower() == 'regexSearch'.lower():        _regexSearch(codeValue)                           # regexSearch:strPattern, strSearch, variable_name e.g. regexSearch:PACIFIC.ASIA.(..........),Last data was imported at,lastDataUpdate
    elif codeID.lower() == 'createPDF'.lower():   _createPDF(codeValue, df)

    #add_page_numbers(saveFile, pageTitles)
    #addContentPDF(pdf_path, pageTitles, file_extension = '_' + yesterdayYYYYMMDD + '.pdf')
    #addContentPDF:pageTitles,sourcePDF,targetPDF
    elif codeID.lower() == 'addContentPDF'.lower():  _addContentPDF(codeValue, df)
    elif codeID.lower() == 'cropImage'.lower():     _cropImage(codeValue, df)                              # cropImage:files, savefiles, left, top, right, bottom, boolPercentage = True/False
    elif codeID.lower() == 'runExcelMacro'.lower():       _runExcelMacro(codeValue)                          # runExcelMacro:excel, macro
    elif codeID.lower() == 'runPowerShellScript'.lower():       _runPowerShellScript(codeValue)                          # runExcelMacro:excel, macro
    elif codeID.lower() == 'runBatchScript'.lower():       _runBatchScript(codeValue)                          # runExcelMacro:excel, macro
    elif codeID.lower() == 'runJupyterNb'.lower():       _runJupyterNb(codeValue)                          # runJupyterNb:notebook_file, parameters
    elif codeID.lower() == 'mergeFiles'.lower():    _mergeFiles(codeValue, df)                               # mergeFiles: fileList, keep, uniqueColumnsList, fileName, encoding 
    elif codeID.lower() == 'dropNRowsExcel'.lower():   _dropNRowsExcel(codeValue)                                # merge files.  merge:newFile,oldFile,olderFile
    elif codeID.lower() == 'DFpromoteHeader'.lower(): _DFpromoteHeader(codeValue) # merge files.  merge:newFile,oldFile,olderFile
    elif codeID.lower() == 'DFsaveToExcel'.lower():   _DFsaveToExcel(codeValue)  # merge files.  merge:newFile,oldFile,olderFile
    elif codeID.lower() == 'DFreadExcel'.lower():     _DFreadExcel(codeValue) # read Excel to dataframe.  DFreadExcel:filename, variableDataFrameName
    elif codeID.lower() == 'DFsort'.lower():      _DFsort(codeValue) # merge files.  merge:newFile,oldFile,olderFile
    elif codeID.lower() == 'DFdropDuplicates'.lower():    _DFdropDuplicates(codeValue) # merge files.  merge:newFile,oldFile,olderFile
    elif codeID.lower() == 'DFconcatenate'.lower():    _DFconcatenate(codeValue)    # merge files.  merge:newFile,oldFile,olderFile
    elif codeID.lower() == 'DFcreate'.lower(): _DFcreate(codeValue)
    # ------------------ Browser / Windows functions ------------------------------
    elif codeID.lower() == 'chromeZoom'.lower():  _chromeZoom(codeValue)
    elif codeID.lower() == 'copyFile'.lower():   _copyFile(codeValue)       # copyFile:source,dest  e.g. copy file to one drive sync folder
    elif codeID.lower() == 'moveFile'.lower():    _moveFile(codeValue)    # moveFile:source,dest  e.g. copy file to one drive sync folder
    elif codeID.lower() == 'makeDir'.lower():     _makeDir(codeValue)     # makeDir:pathname
    elif codeID.lower() == 'removeFile'.lower():  _removeFile(codeValue)        # removeFile:source,dest  e.g. copy file to one drive sync folder
    elif codeID.lower() == 'renameRecentDownloadFile'.lower(): _renameRecentDownloadFile(codeValue) # renameRecentDownloadFile:saveName,path,fileExtension,withinLastSec

    # ------------------ RPA functions ------------------------------
    elif codeID.lower() == 'runInBackground'.lower():   _runInBackground()  # run automation in background mode without user attendance
    elif codeID.lower() == 'initializeRPA'.lower(): _initializeRPA()
    elif codeID.lower() == 'closeRPA'.lower():  _closeRPA()
    elif codeID.lower() == 'url'.lower():       _url(codeValue, df)         # url:OKTA or url:<URL_Dclick_Pages:key> or url:@<URL_Dclick_Pages:@columnHeader>
    elif codeID.lower() == 'urls'.lower():   _urls(codeValue, objVar)        # No longer required - can remove
    elif codeID.lower() == 'read'.lower():      _read(codeValue)        # read:checkUserName=okta-signin-username
    elif codeID.lower() == 'checkVariable'.lower(): _checkVariable(codeValue)    # checkVariable:checkUserName
    elif codeID.lower() == 'set'.lower():       _set(codeValue)             # set:checkUserName=value
    elif codeID.lower() == 'increment'.lower():       _increment(codeValue)             # increment:counter, 1    
    elif codeID.lower() == 'urlcontains'.lower(): _urlcontains(codeValue)   # urlcontains:value_to_search,variable_result_true_false
    elif codeID.lower() == 'keyboard'.lower():  _keyboard(codeValue)        # key press e.g. [home] [end] [insert] [f1] .. [f15] [shift] [ctrl] [alt] [win] [cmd] [enter] [space] [tab] [esc] [backspace] [delete] [clear]
    elif codeID.lower() == 'rclick'.lower():    _rclick(codeValue)          # right click
    elif codeID.lower() == 'present'.lower():   _present(codeID, codeValue) # right click
    elif codeID.lower() == 'exist'.lower():     _exist(codeID, codeValue)   # Waits until the timeout for an element to exist and returns a JavaScript true or false
    elif codeID.lower() == 'count'.lower():     _count(codeID, codeValue)   # right click
    elif codeID.lower() == 'select'.lower():    _select(codeValue)  # Selects a dropdown option in a web input. select:dropdown,option
    elif codeID.lower() == 'type'.lower():    _type(codeValue)  # type:identifier,value
    elif codeID.lower() == 'snap'.lower():      _snap(codeValue)    # snap:page,saveFile   Snap entire web page
    elif codeID.lower() == 'telegram'.lower():  _telegram(codeValue)
    elif codeID.lower() == 'email'.lower():  _email(codeValue, df)
    elif codeID.lower() == 'waitEmailComplete'.lower():  _waitEmailComplete(codeValue, df)
    else:                       _click(code)        # normal left click
    return [], [], []

# used by tagui to redirect console output to a variable
def consoleOutput(runStatement):
    from io import StringIO
    import sys
    old_stdout = sys.stdout # reference current console std out
    buffer = StringIO()     
    sys.stdout = buffer     # redirect std out to buffer
    exec(runStatement)
    buffer_output = buffer.getvalue()   # assign buffer to variable
    sys.stdout = old_stdout   # reset std out
    #sys.stdout = sys.__stdout__
    return buffer_output

from io import StringIO
import sys
def redirectConsole():
    old_stdout = sys.stdout # reference current console std out
    buffer = StringIO()     
    sys.stdout = buffer     # redirect std out to buffer
    return buffer, old_stdout

def resetConsole(buffer, old_stdout):
    buffer_output = buffer.getvalue()   # assign buffer to variable
    sys.stdout = old_stdout   # reset std out
    #sys.stdout = sys.__stdout__
    return buffer_output
    
def _iterate(codeValue, df, objVar):
    '''  Defines iteration steps and appends to runcode list to handle loops over object list or tables.  Syntax: iterate: obj or table list, codelist to run '''
    logger = get_run_logger()
    #logger.info(f">>>>ITERATION ==================== {codeValue}")
    objVar = codeValue.split(',',1)[0].strip()
    sub_code = codeValue.split(',',1)[1].strip()
    worksheetTable = False
    if objVar.lower()[:4]=='tbl@':  # special table object with headers
        withHeader = 1
        objVar = objVar[4:]
    elif objVar in df[(df.Type == 'table')]['Object'].dropna().values.tolist():  # special table object with headers
        withHeader = 1
        #objVar = objVar[4:]
    else:
        # check if its a worksheet name
        result, objTableSet = _isWorkSheetName(objVar, excelfile=STARTFILE)
        if result == True:
            # is a table from a worksheet with name = objVar
            withHeader = 0 #1  Does not support 2 table headers.  Apply a rename instead to align names to function param
            worksheetTable = True
        else:
            # not a table - just normal list.  No header.
            withHeader = 0
    #print('check iterate', objVar, sub_code, withHeader)
    if objVar.isdigit():   # is integer - just standard loop
        totalCount = int(objVar)
        codeBeforeTemplateUpdate = variables['codeBeforeTemplateUpdate']
        sub_code = codeBeforeTemplateUpdate.split(',')[1].strip()
        if len(codeBeforeTemplateUpdate.split(','))==3:
            startCount = codeBeforeTemplateUpdate.split(',')[2].strip()
            startCount = int(startCount) if startCount.isdigit() else 0 
        else:
            startCount = 0
        #print('check .... ' , startCount, totalCount)
        n = 1
        additionalCodeList = []
        additionalDFlist = []
        additionalobjVarList = []
        for i in range(startCount, startCount + totalCount):
            #variables['loopCount'] = i
            #print('ITERATION ---------------------------------------- ', 'LOOP', n)                
            logger.info(f"'ITERATION ---------------------------------------- LOOP {n}")
            #runCode(df, sub_code)
            increment = 'set:loopCount=' + str(i)
            additionalCodeList = additionalCodeList + [increment] + [sub_code]
            additionalDFlist = additionalDFlist + [df, df]
            additionalobjVarList = additionalobjVarList + [objVar, objVar]
            #return [increment, sub_code], [df, df], [objVar, objVar]
            n += 1
        return additionalCodeList, additionalDFlist, additionalobjVarList 
    else:
        #runIterate(df, objVar, sub_code, withHeader)

        # run a sub_code iteratively over a objVar e.g. a URL list like iterate: URL_pages , codeList:<URL_runprocess:key>
        #def runIterate(df, objVar, sub_code, withHeader=0):
 
        if worksheetTable:
            objVarList = objTableSet.iloc[withHeader:, 0].values.tolist() # row and column           
            #logger.info(f"      objTableSet: {objTableSet.iloc[withHeader:3, 0].head(5)}")
            #logger.info(f"      objTableSet: {objTableSet.iloc[withHeader:, 0].values.tolist()}")
        else:
            objVarList = dfObjList(df, objVar, withHeader)
        logger.debug(f"      LOOP over {codeValue}.  {objVar}:{objVarList}")
        #print(f"      Iteration list: {objVar}, {objVarList}")
        #logg('******** runIterate objVar:', objVar = objVar) # e.g. URL_Dclick_Pages
        #logg('******** runIterate sub_code:', sub_code = sub_code) # e.g. openPages
        #logg('******** runIterate objVarList:', objVarList = objVarList) # e.g. ['wBags', 'wRTW', 'wShoes']
        #logg('******** runIterate codeList:', codeList = codeList) # e.g. codelist of openPages i.e.['print ...' , 'urls...']
        i = 0
        rtn_code = []
        rtn_df = []
        rtn_obj = []
        for x in objVarList:
            #constants['iterationCount'] = i
            # set: iterationCount=i
            rtn_code = rtn_code + [f"iterationCount:{i},{objVarList[i]}"]  # inserts a interationCount step to increase interatation counter
            rtn_df = rtn_df + [df]
            rtn_obj = rtn_obj+ [objVarList[i]]

            #logg('runIterate objVarList[i],', i = i , objVarList = objVarList[i], constantsIterationCount = constants['iterationCount'], level = 'info')
            #print('ITERATION **************************************** ', 'COUNT', i+1, objVarList[i]) #, ', STEP', sub_code)
            #runCode(df, sub_code, objVarList[i])
            rtn_code = rtn_code + [sub_code]
            rtn_df = rtn_df + [df]
            rtn_obj = rtn_obj+ [objVarList[i]]
            i = i + 1
        #logger.info('_iterate complete iteration step preparations.  Next run steps.')
        return rtn_code, rtn_df, rtn_obj



#@task
def _if(codeValue, df, objVar):
    condition = codeValue.split(':',1)[0]
    codeBlock = codeValue.split(':',1)[1]
    if objVar == None or objVar =="": objVar = " "
    #logg('if condition:', condition = condition, codeBlock = codeBlock)
    print('      ', str(eval(condition)).upper(), ' : ', codeBlock)
    if eval(condition):
        #logg('condition is true -----')
        #runCode(df, codeBlock)
        return [codeBlock], [df], [objVar]
        #codeList = dfObjList(df, codeBlock)
        #runCodelist(df, codeList)
    return [], [], []

def _isCodeList(df, code, objVar):
    # parameterObjs(df)
    sub_code = dfObjList(df, code)
    #logg('Run Code Block - user defined objects in sheet - ParameterObjs: ', code = code, sub_code = sub_code, level = 'info')
    #runCodelist.with_options(name=code)(df, sub_code)
    #runCodelist(CodeObject(df), sub_code)
    n = len(sub_code)
    logger = get_run_logger()
    logger.debug(f"   Steps:{sub_code}")
    return sub_code, [df] * n, [objVar] * n

#@task
def _runModule(codeValue, df, objVar):
    #logger = get_run_logger()
    sheet = codeValue.split(',')[0]
    num_arg = len(codeValue.split(','))
    if num_arg==1: 
        codeBlock = 'main'
        excelfile = ''
    elif num_arg==2: 
        codeBlock = codeValue.split(',')[1]
        excelfile = ''
    elif num_arg==3:
        codeBlock = codeValue.split(',')[1]
        excelfile = codeValue.split(',')[2]

    #excelfile = '' if len(codeValue.split(','))==1 else codeValue.split(',',1)[1]
    #logg('runModule: ', excelfile = excelfile, sheet = sheet, isExcelFileStringValue = str(excelfile==''))
    if excelfile=='': excelfile = STARTFILE
    #logger.info(f".... runModule .... sheet:{sheet} excelfile:{excelfile} df:{df.shape}")

    new_df = readExcelConfig(sheet, excelfile)
    #logger.info(f".... runModule .... new_df sheet:{sheet} excelfile:{excelfile} df:{df.shape}")

    run_code = dfObjList(new_df, codeBlock)               # run the main code block
    #logger.info(f".... runModule .... run_code:{run_code}")

    #runCodelist.with_options(name=sheet)(df, run_code)
    #runCodelist(CodeObject(df), run_code)
    n = len(run_code)
    return run_code, [new_df] * n, [objVar] * n

#@task
def _codeList(codeValue, df, objVar):
    codeList = codeValue.split(',')
    constants['lastCodelist'] = codeList
    #runCodelist(CodeObject(df), codeList)
    n = len(codeList)
    return codeList, [df] * n, [objVar] * n

#@task
import time
def _wait(codeValue, df, objVar):
    tmpDict = parseArguments('time_sec,identifier,run_code,run_code_until',codeValue)  #items = 'wait:15:ID:codeA'
    time_sec = int(tmpDict['time_sec'])
    if 'identifier' in tmpDict:                 # do while identifier is found - r.exist
        #logg('identifier', identifier = tmpDict['identifier'])
        print('wait identifier', tmpDict['identifier'])
        # identifier is a special object list
        if tmpDict['identifier'] in df[(df.Type == 'list')]['Object'].dropna().values.tolist():
            tmpDict['identifier'] = dfObjList(df, tmpDict['identifier'])
            if 'run_code' in tmpDict:                                           #run code if time out
                tmpDict['run_code'] = dfObjList(df, tmpDict['run_code'])
            print('wait identifier list', tmpDict['identifier'])
            print('wait run code list', tmpDict['run_code'])

            logger = get_run_logger()
            logger.debug(f"   Scenario list:{tmpDict['identifier']} Action list:{tmpDict['run_code']}")

            matchBool, index = waitIdentifierExist(tmpDict['identifier'], time_sec, 1, False)         #waitIdentifierExist(identifier, time_seconds, interval) - returns true or false
            if not matchBool:
                #logg('      Time out from waiting', level = 'warning')                    #raise CriticalAccessFailure("TXT logon window did not appear")
                logger.warning(f"Time out from waiting ...")
                return [], [], []
            else:
                if 'run_code' in tmpDict:                                           #run code if time out
                    print('      Run code from wait:', tmpDict['run_code'][index])

                    run_code = dfObjList(df, tmpDict['run_code'][index])
                    #logg('      Run code:', run_code = run_code)

                    #runCodelist(CodeObject(df), run_code)
                    n = len(run_code)
                    logger.debug(f"   Action:{tmpDict['run_code'][index]}, {n} steps:{run_code} {[objVar] * n}")

                    return run_code, [df] * n, [objVar] * n
                    #return run_code, [df], [objVar]
                else:
                    return [], [], []

        else: # not a special object list
            if not waitIdentifierExist(tmpDict['identifier'], time_sec, 1, False):         #waitIdentifierExist(identifier, time_seconds, interval) - returns true or false
                #logg('      Time out from waiting', level = 'warning')                    #raise CriticalAccessFailure("TXT logon window did not appear")
                if 'run_code' in tmpDict:                                           #run code if time out
                    run_code = dfObjList(df, tmpDict['run_code'])
                    if 'run_code_until' in tmpDict:
                        #logg('Time out - run code:', run_code = run_code, run_code_until = tmpDict['run_code_until'], level = 'debug')
                        #runCodelist(CodeObject(df), run_code, '', tmpDict['run_code_until'])
                        n = len(run_code)
                        return run_code, [df] * n, [objVar] * n                        
                    else:                                                           
                        #logg('      Time out - run code:', run_code = run_code, level = 'error')
                        #runCodelist(CodeObject(df), run_code)
                        n = len(run_code)
                        return run_code, [df] * n, [objVar] * n
            else:
                return [], [], []

    # no identifier - normal wait
    else:
        #logg('wait', time_sec = time_sec)
        time.sleep(time_sec)
        # r.wait(time_sec)
        return [], [], []

#@task
def _waitDisappear(codeValue, df, objVar):
    logger = get_run_logger()
    tmpDict = parseArguments('time_sec,identifier,run_code,run_code_until',codeValue)  #items = 'wait:15:ID:codeA'
    time_sec = int(tmpDict['time_sec'])
    logger.debug('checking 1...')
    if 'identifier' in tmpDict:                 # do while identifier is found - r.exist
        logger.debug(f"   identifier = {tmpDict['identifier']}")
        if not waitIdentifierDisappear(tmpDict['identifier'], time_sec, 1, False):         #waitIdentifierExist(identifier, time_seconds, interval) - returns true or false
            logger.warning(f"   Time out from waiting', level = 'warning'")                    #raise CriticalAccessFailure("TXT logon window did not appear")
            if 'run_code' in tmpDict:                                           #run code if time out
                run_code = dfObjList(df, tmpDict['run_code'])
                if 'run_code_until' in tmpDict:
                    logger.debug(f"'Time out - run code:', run_code = {run_code}, run_code_until = {tmpDict['run_code_until']}, level = 'debug'")
                    #runCodelist(CodeObject(df), run_code, '', tmpDict['run_code_until'])
                    n = len(run_code)
                    return run_code, [df] * n, [objVar] * n
                else:                                                           
                    logger.warning(f"'      Time out - run code:', run_code = {run_code}, level = 'warning'")
                    #runCodelist(CodeObject(df), run_code)
                    n = len(run_code)
                    return run_code, [df] * n, [objVar] * n
        else:
            return [], [], []
    else:
        logger.debug(f"'wait', time_sec = {time_sec}")
        time.sleep(time_sec)
        # r.wait(time_sec)
        return [], [], []

#@task
def _print(codeValue):
    #logg('print:', codeValue = codeValue, level = 'info')
    print(codeValue)

def _log(codeValue):
    #logg('log:', errorMsg = codeValue)
    pass

def _exit():
    exitProg()

def _exitError(codeValue):
    if codeValue.isdigit():
        if int(codeValue) in [1,2,3,4,5,6,7,8,9,10]:                
            exitProgWError(errorCode=int(codeValue))

def _raiseError(codeValue):
    raise ValueError(f"Raise Error: {codeValue}")

def _regexSearch(codeValue):
    #regexSearch:PACIFIC.ASIA.(..........),<strSearch>,lastDataUpdate
    strPattern = codeValue.split(',')[0]
    strSearch = codeValue.split(',')[1]
    variable_name = codeValue.split(',')[2]
    variables[variable_name] = regexSearch(strPattern, strSearch)
    #logg('regexSearch', strPattern = strPattern, strSearch = strSearch, variable_name = variable_name, result = variables[variable_name])


def _createPDF(codeValue, df):
    logger = get_run_logger()
    tmpDict = parseArguments('imagelist,outputPath,saveFileName',codeValue)
    if 'imagelist' in tmpDict:
        #logg('imagelist', content = tmpDict['imagelist'].strip())
        imagelist = tmpDict['imagelist'].strip()
        imagelist = dfObjList(df, imagelist)

        #logg('imagelist', imagelist = imagelist)
        #if imagelist == '': imagelist = ''
        if imagelist == None:
            #imagelist = ''
            logger.error('Error - no imagelist ...')
        else:
            if 'outputPath' in tmpDict:
                #logg('outputPath', content = tmpDict['outputPath'])  # D:\\iCristal\\
                outputPath = tmpDict['outputPath'].strip()
                if outputPath == '': outputPath = './' #'.\\' #'D:\\iCristal\\'
            if 'saveFileName' in tmpDict:
                #logg('saveFileName', content = tmpDict['saveFileName'])  # 'D:/iCristal/Output/APAC_Daily_Sales/'
                saveFileName = tmpDict['saveFileName'].strip()
                if saveFileName == '': saveFileName = './savefile.pdf' #'./Output/APAC_Daily_Sales/' #'D:/iCristal/Output/APAC_Daily_Sales/'
            createPDFfromImages(imagelist, outputPath, saveFileName)


def _addContentPDF(codeValue, df):
    tmpDict = parseArguments('pageTitles,sourcePDF,targetPDF',codeValue)
    if 'pageTitles' in tmpDict:
        #logg('pageTitles', content = tmpDict['pageTitles'].strip())
        pageTitles = tmpDict['pageTitles'].strip()
        pageTitlesList = dfObjList(df, pageTitles)
        #logg('pageTitlesList', pageTitlesList = pageTitlesList)
        if not len(pageTitlesList) : return # error - no pageTitles provided
    if 'sourcePDF' in tmpDict:
        #logg('sourcePDF', content = tmpDict['sourcePDF'])  # D:\\iCristal\\
        sourcePDF = tmpDict['sourcePDF'].strip()
        if sourcePDF == '': return # error - no pdf_path defined
    if 'targetPDF' in tmpDict:
        #logg('targetPDF', content = tmpDict['targetPDF'])  # 'D:/iCristal/Output/APAC_Daily_Sales/'
        targetPDF = tmpDict['targetPDF'].strip()
        file_extension = '_' + yesterdayYYYYMMDD + '.pdf'
        if targetPDF == '': targetPDF = sourcePDF + file_extension #'./Output/APAC_Daily_Sales/' #'D:/iCristal/Output/APAC_Daily_Sales/'
    addContentPDF(pageTitlesList, sourcePDF, targetPDF)

def _cropImage(codeValue, df):
    tmpDict = parseArguments('files, savefiles, left, top, right, bottom, boolPercentage',codeValue)
    # cropImage - num or pct - percentage
    tmpDict['files'] = [updateConstants(df, s) for s in dfObjList(df, tmpDict['files'])]
    tmpDict['savefiles'] = [updateConstants(df, s) for s in dfObjList(df, tmpDict['savefiles'])]        
    #print(tmpDict['files'], tmpDict['savefiles'], tmpDict['left'], tmpDict['top'], tmpDict['right'], tmpDict['bottom'], tmpDict['boolPercentage'])
    cropImage(tmpDict['files'], tmpDict['savefiles'], tmpDict['left'], tmpDict['top'], tmpDict['right'], tmpDict['bottom'], tmpDict['boolPercentage'])

def _runExcelMacro(codeValue):
    logger = get_run_logger()
    excel = codeValue.split(',')[0].strip()
    macro = codeValue.split(',')[1].strip()
    import win32com.client
    xl = win32com.client.Dispatch("Excel.Application")          #instantiate excel app
    #xl.Visible = True is not necessary, used just for convenience'

    workBookName = Path(excel).name
    excel = Path(excel).absolute()

    if excel == '': return
    excelQuit = True
    wbClose = True
    if xl.Workbooks.Count > 0:  # excel open with workbooks - do not quit excel
        #for i in office.Workbooks: print('list of open workbooks',i.Name)
        excelQuit = False
        # target workbook is open - do not close the workbook
        if any(i.Name == workBookName for i in xl.Workbooks): 
            #print('do not close workbook')
            wbClose = False

    xl.Visible = False
    logger.debug(f"   excel {excel.__str__()} workBookName {workBookName.__str__()} macro {macro}")
    wb = xl.Workbooks.Open(excel)
    xl.Application.Run(macro)
    wb.Save()
    if wbClose: wb.Close(SaveChanges=False)
    #xl.Visible = True
    if excelQuit: xl.Application.Quit()


def _runPowerShellScript(codeValue):
    script = codeValue #.split(',')[0].strip()
    #macro = codeValue.split(',')[1].strip()
    import subprocess, sys
    #p = subprocess.Popen(['powershell.exe', '.\AddOn\cleanProcesses.ps1 -msg " Testing 123 v5 " '], stdout=sys.stdout)
    p = subprocess.Popen(['powershell.exe', 
        script], 
        stdout=sys.stdout)
    p.communicate()
    #logg('runPowerShellScript:', returnCode = p.returncode, stderr = p.stderr, stdout = p.stdout)

def _runBatchScript(codeValue):
    script = codeValue.split(',')[0].strip()
    if len(codeValue.split(','))>1:
        workingDir = codeValue.split(',')[1].strip()
    else:
        workingDir = CWD_DIR
    #https://riptutorial.com/python/example/5714/more-flexibility-with-popen
    from subprocess import Popen
    #p = Popen("test.bat", cwd=r".\AddOn")
    p = Popen(script, cwd=workingDir)
    stdout, stderr = p.communicate()
    #logg('runBatchScript:', returnCode = p.returncode, stderr = p.stderr, stdout = p.stdout)
    #print(p.returncode)
    #print("An error occured: %s", p.stderr)
    #print("Output %s", p.stdout)

def _runJupyterNb(codeValue):
    logger = get_run_logger()
    nb_file = codeValue.split(',', 1)[0].strip()
    jsonString = codeValue.split(',', 1)[1].strip()

    logger.debug(f"       Run Jupyter Notebook = {nb_file}, Parameters = {jsonString}")

    from auto_initialize import checkWorkDirectory
    from pathlib import Path, PureWindowsPath

    CWD_DIR = checkWorkDirectory('.')
    #logger.info(f"curDIR = {CWD_DIR}")

    #print(jsonString)
    import papermill as pm

    #file = r'C:\Users\roh\Downloads\d5c7a4f7-b9a7-4d1e-904e-ce7349e0f27c.xlsx'
    #country = 'All'

    import json

    #jsonString = '{"file":"C:\\Users\\roh\\Downloads\\d5c7a4f7-b9a7-4d1e-904e-ce7349e0f27c.xlsx", "country": "All"}'
    #jsonString = '{"file": "C:/Users/roh/Downloads/d5c7a4f7-b9a7-4d1e-904e-ce7349e0f27c.xlsx", "country": "All"}'

    paramDict = json.loads(jsonString)
    #logger.info(f"parameter dictionary = {paramDict}")    
    #print(paramDict['file'])
    #print(paramDict['country'])

    #res = pm.execute_notebook(
    #    'C:\\Users\\roh\Documents\\python\\Optimus\\autobot\\DClickReport.ipynb',
    #    'C:\\Users\\roh\\Documents\\python\\Optimus\\autobot\\DClickReport_output.ipynb',
    #    parameters = paramDict
    #)

    res = pm.execute_notebook(
        nb_file, nb_file.replace('.ipynb', '_output.ipynb'),
        parameters = paramDict
    )



def _mergeFiles(codeValue, df):
    # e.g. mergeFiles: mergeFilelist, first, deDuplicationColumnList, ./merged.csv,  latin-1 .... Handles csv or excel
    tmpDict = parseArguments('fileList, keep, uniqueColumnsList, fileName, encoding',codeValue)
    #print(tmpDict)
    if tmpDict == {}: return

    if tmpDict['fileList'] in df[(df.Type == 'list')]['Object'].dropna().values.tolist():           #run Block of Code
        tmpDict['fileList'] = dfObjList(df, tmpDict['fileList'])
        tmpDict['fileList'] = [updateConstants(df, s) for s in tmpDict['fileList']]
        tmpDict['fileList'] = [s.strip() for s in tmpDict['fileList']]        # using list comprehension to trim spaces of every element in list

    if tmpDict['uniqueColumnsList'] in df[(df.Type == 'list')]['Object'].dropna().values.tolist():           #run Block of Code
        tmpDict['uniqueColumnsList'] = dfObjList(df, tmpDict['uniqueColumnsList'])
        tmpDict['uniqueColumnsList'] = [updateConstants(df, s) for s in tmpDict['uniqueColumnsList']]

    #logg('tmpDict', tmpDict = tmpDict, level = 'info')
    #logg('fileList', fileList = tmpDict['fileList'], level = 'info')

    df_merged = pd.concat(map(lambda x: pd.read_csv(x, encoding=tmpDict['encoding']) if x.upper().endswith('.CSV') else pd.read_excel(x), tmpDict['fileList']), ignore_index=True)        
    df_merged = df_merged.drop_duplicates(tmpDict['uniqueColumnsList'], keep=tmpDict['keep'])
    saveFile = tmpDict['fileName']
    df_merged.to_csv(saveFile, index=False) if saveFile.upper().endswith('CSV') else df_merged.to_excel(tmpDict['fileName'], index=False)
    print('      ', 'Merge Files:', tmpDict['fileList'], ' Save to:', saveFile)


def _dropNRowsExcel(codeValue):
    tmpDict = parseArguments('Nrows, variableDataFrameName',codeValue)
    # Drop first N rows
    # by selecting all rows from 4th row onwards
    N = variables[tmpDict['Nrows']]
    variables[tmpDict['variableDataFrameName']] = variables[tmpDict['variableDataFrameName']].iloc[N: , :]

def _DFpromoteHeader(codeValue):
    tmpDict = parseArguments('variableDataFrameName',codeValue)
    new_header = variables[tmpDict['variableDataFrameName']].iloc[0] #grab the first row for the header
    variables[tmpDict['variableDataFrameName']] = variables[tmpDict['variableDataFrameName']][1:] #take the data less the header row
    variables[tmpDict['variableDataFrameName']].columns = new_header #set the header row as the df header

def _DFsaveToExcel(codeValue):
    tmpDict = parseArguments('filename, variableDataFrameName, mode, sheet',codeValue)
    filename = tmpDict['filename']
    dataFrameName = tmpDict['variableDataFrameName']
    if 'sheet' in tmpDict: 
        _sheet = tmpDict['sheet']
    else:
        _sheet = 'Sheet1'
    _ifsheetexist = None
    if 'mode' in tmpDict:
        _mode = tmpDict['mode'] # write w or append a
        if _mode.lower() == 'a': 
            _ifsheetexist = 'overlay'
            append_df_to_excel(filename, variables[dataFrameName], sheet_name=_sheet,
                        index=False)
    else:
        _mode = 'w'  # write
        #variables[tmpDict['variableDataFrameName']].to_excel(tmpDict['filename'], index=False)
        with pd.ExcelWriter(filename, if_sheet_exists=_ifsheetexist, engine="openpyxl",
                            mode=_mode) as writer:  
            variables[dataFrameName].to_excel(writer, sheet_name= _sheet, index=False)
        #    #variables[dataFrameName].to_excel(writer, index=False)
        print(_ifsheetexist, _sheet, _mode)

from pathlib import Path
from copy import copy
from typing import Union, Optional
import numpy as np
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


def copy_excel_cell_range(
        src_ws: openpyxl.worksheet.worksheet.Worksheet,
        min_row: int = None,
        max_row: int = None,
        min_col: int = None,
        max_col: int = None,
        tgt_ws: openpyxl.worksheet.worksheet.Worksheet = None,
        tgt_min_row: int = 1,
        tgt_min_col: int = 1,
        with_style: bool = True
) -> openpyxl.worksheet.worksheet.Worksheet:
    """
    copies all cells from the source worksheet [src_ws] starting from [min_row] row
    and [min_col] column up to [max_row] row and [max_col] column
    to target worksheet [tgt_ws] starting from [tgt_min_row] row
    and [tgt_min_col] column.

    @param src_ws:  source worksheet
    @param min_row: smallest row index in the source worksheet (1-based index)
    @param max_row: largest row index in the source worksheet (1-based index)
    @param min_col: smallest column index in the source worksheet (1-based index)
    @param max_col: largest column index in the source worksheet (1-based index)
    @param tgt_ws:  target worksheet.
                    If None, then the copy will be done to the same (source) worksheet.
    @param tgt_min_row: target row index (1-based index)
    @param tgt_min_col: target column index (1-based index)
    @param with_style:  whether to copy cell style. Default: True

    @return: target worksheet object
    """
    if tgt_ws is None:
        tgt_ws = src_ws

    # https://stackoverflow.com/a/34838233/5741205
    for row in src_ws.iter_rows(min_row=min_row, max_row=max_row,
                                min_col=min_col, max_col=max_col):
        for cell in row:
            tgt_cell = tgt_ws.cell(
                row=cell.row + tgt_min_row - 1,
                column=cell.col_idx + tgt_min_col - 1,
                value=cell.value
            )
            if with_style and cell.has_style:
                # tgt_cell._style = copy(cell._style)
                tgt_cell.font = copy(cell.font)
                tgt_cell.border = copy(cell.border)
                tgt_cell.fill = copy(cell.fill)
                tgt_cell.number_format = copy(cell.number_format)
                tgt_cell.protection = copy(cell.protection)
                tgt_cell.alignment = copy(cell.alignment)
    return tgt_ws


def append_df_to_excel(
        filename: Union[str, Path],
        df: pd.DataFrame,
        sheet_name: str = 'Sheet1',
        startrow: Optional[int] = None,
        max_col_width: int = 30,
        autofilter: bool = False,
        fmt_int: str = "#,##0",
        fmt_float: str = "#,##0.00",
        fmt_date: str = "yyyy-mm-dd",
        fmt_datetime: str = "yyyy-mm-dd hh:mm",
        truncate_sheet: bool = False,
        storage_options: Optional[dict] = None,
        **to_excel_kwargs
) -> None:
    """
    Append a DataFrame [df] to existing Excel file [filename]
    into [sheet_name] Sheet.
    If [filename] doesn't exist, then this function will create it.

    @param filename: File path or existing ExcelWriter
                     (Example: '/path/to/file.xlsx')
    @param df: DataFrame to save to workbook
    @param sheet_name: Name of sheet which will contain DataFrame.
                       (default: 'Sheet1')
    @param startrow: upper left cell row to dump data frame.
                     Per default (startrow=None) calculate the last row
                     in the existing DF and write to the next row...
    @param max_col_width: maximum column width in Excel. Default: 40
    @param autofilter: boolean - whether add Excel autofilter or not. Default: False
    @param fmt_int: Excel format for integer numbers
    @param fmt_float: Excel format for float numbers
    @param fmt_date: Excel format for dates
    @param fmt_datetime: Excel format for datetime's
    @param truncate_sheet: truncate (remove and recreate) [sheet_name]
                           before writing DataFrame to Excel file
    @param storage_options: dict, optional
        Extra options that make sense for a particular storage connection, e.g. host, port,
        username, password, etc., if using a URL that will be parsed by fsspec, e.g.,
        starting “s3://”, “gcs://”.
    @param to_excel_kwargs: arguments which will be passed to `DataFrame.to_excel()`
                            [can be a dictionary]
    @return: None

    Usage examples:

    >>> append_df_to_excel('/tmp/test.xlsx', df, autofilter=True,
                           freeze_panes=(1,0))

    >>> append_df_to_excel('/tmp/test.xlsx', df, header=None, index=False)

    >>> append_df_to_excel('/tmp/test.xlsx', df, sheet_name='Sheet2',
                           index=False)

    >>> append_df_to_excel('/tmp/test.xlsx', df, sheet_name='Sheet2',
                           index=False, startrow=25)

    >>> append_df_to_excel('/tmp/test.xlsx', df, index=False,
                           fmt_datetime="dd.mm.yyyy hh:mm")

    (c) [MaxU](https://stackoverflow.com/users/5741205/maxu?tab=profile)
    """
    def set_column_format(ws, column_letter, fmt):
        for cell in ws[column_letter]:
            cell.number_format = fmt
    filename = Path(filename)
    file_exists = filename.is_file()
    # process parameters
    # calculate first column number
    # if the DF will be written using `index=True`, then `first_col = 2`, else `first_col = 1`
    first_col = int(to_excel_kwargs.get("index", True)) + 1
    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')
    # save content of existing sheets
    if file_exists:
        wb = load_workbook(filename)
        sheet_names = wb.sheetnames
        sheet_exists = sheet_name in sheet_names
        sheets = {ws.title: ws for ws in wb.worksheets}

    with pd.ExcelWriter(
        filename.with_suffix(".xlsx"),
        engine="openpyxl",
        mode="a" if file_exists else "w",
        if_sheet_exists="new" if file_exists else None,
        date_format=fmt_date,
        datetime_format=fmt_datetime,
        storage_options=storage_options
    ) as writer:
        if file_exists:
            # try to open an existing workbook
            writer.book = wb
            # get the last row in the existing Excel sheet
            # if it was not specified explicitly
            if startrow is None and sheet_name in writer.book.sheetnames:
                startrow = writer.book[sheet_name].max_row
            # truncate sheet
            if truncate_sheet and sheet_name in writer.book.sheetnames:
                # index of [sheet_name] sheet
                idx = writer.book.sheetnames.index(sheet_name)
                # remove [sheet_name]
                writer.book.remove(writer.book.worksheets[idx])
                # create an empty sheet [sheet_name] using old index
                writer.book.create_sheet(sheet_name, idx)
            # copy existing sheets
            writer.sheets = sheets
        else:
            # file doesn't exist, we are creating a new one
            startrow = 0

        # write out the DataFrame to an ExcelWriter
        df.to_excel(writer, sheet_name=sheet_name, **to_excel_kwargs)
        worksheet = writer.sheets[sheet_name]

        if autofilter:
            worksheet.auto_filter.ref = worksheet.dimensions

        for xl_col_no, dtyp in enumerate(df.dtypes, first_col):
            col_no = xl_col_no - first_col
            width = max(df.iloc[:, col_no].astype(str).str.len().max(),
                        len(df.columns[col_no]) + 6)
            width = min(max_col_width, width)
            column_letter = get_column_letter(xl_col_no)
            worksheet.column_dimensions[column_letter].width = width
            if np.issubdtype(dtyp, np.integer):
                set_column_format(worksheet, column_letter, fmt_int)
            if np.issubdtype(dtyp, np.floating):
                set_column_format(worksheet, column_letter, fmt_float)

    if file_exists and sheet_exists:
        # move (append) rows from new worksheet to the `sheet_name` worksheet
        wb = load_workbook(filename)
        # retrieve generated worksheet name
        new_sheet_name = set(wb.sheetnames) - set(sheet_names)
        if new_sheet_name:
            new_sheet_name = list(new_sheet_name)[0]
        # copy rows written by `df.to_excel(...)` to
        copy_excel_cell_range(
            src_ws=wb[new_sheet_name],
            tgt_ws=wb[sheet_name],
            tgt_min_row=startrow + 1,
            with_style=True
        )
        # remove new (generated by Pandas) worksheet
        del wb[new_sheet_name]
        wb.save(filename)
        wb.close()

def _DFreadExcel(codeValue):
    tmpDict = parseArguments('filename, variableDataFrameName',codeValue)
    variables[tmpDict['variableDataFrameName']] = pd.read_excel(tmpDict['filename'])

def _DFsort(codeValue):
    tmpDict = parseArguments('sortFieldList, boolAscending, variableDataFrameName',codeValue)

    columnList = tmpDict['sortFieldList']
    boolAscending = tmpDict['boolAscending']
    variables[tmpDict['variableDataFrameName']].sort_values(by=columnList, ascending = boolAscending, inplace = True)

def _DFdropDuplicates(codeValue):
    tmpDict = parseArguments('uniqueColumnList, keep, variableDataFrameName',codeValue)

    uniqueColumnList = tmpDict['uniqueColumnList']
    keep = tmpDict['keep']
    variables[tmpDict['variableDataFrameName']] = variables[tmpDict['variableDataFrameName']].drop_duplicates(uniqueColumnList, keep=keep)

def _DFconcatenate(codeValue):
    tmpDict = parseArguments('dataFrameList, mergedDataFrameName',codeValue)
    dataFrameList = tmpDict['dataFrameList']
    variables[tmpDict['mergedDataFrameName']] = pd.concat(map(lambda x: variables[x], dataFrameList), ignore_index=True)

def _DFcreate(codeValue):
    tmpDict = parseArguments('dataFrameName, columnslist',codeValue)
    dataFrameName = tmpDict['dataFrameName']
    columnslist = tmpDict['columnslist'].strip('\"')
    elementlist = list(map(lambda x: x.strip(), columnslist.split(',')))
    dictionary = variables
    print('1', dataFrameName, elementlist, dictionary)
    dictresult = dict((k, dictionary[k]) for k in elementlist
            if k in dictionary)
    print('2', dictresult)
    if not dataFrameName in variables:
        #n == 0:
        variables[dataFrameName] = pd.DataFrame(dictresult, index=[0])
    else:
        n = variables[dataFrameName].__len__()
        variables[dataFrameName] = pd.concat([variables[dataFrameName], pd.DataFrame(dictresult, index=[n])])
    print('3', variables[dataFrameName])

def _chromeZoom(codeValue):
    chromeZoom(codeValue)

def _copyFile(codeValue):
    source = codeValue.split(',',1)[0]
    dest = codeValue.split(',',1)[1]
    #logg('copyFile:', source = source, dest = dest)
    import os
    import shutil
    destination = shutil.copyfile(source, dest)
    #logg("Path of copied file:", destination = destination)

def _moveFile(codeValue):
    source = codeValue.split(',',1)[0]
    dest = codeValue.split(',',1)[1]
    #logg('moveFile:', source = source, dest = dest)
    import os
    import shutil
    destination = shutil.move(source, dest)
    #logg("Path of moved file:", destination = destination)

def _makeDir(codeValue):
        path = codeValue.split(',',1)[0]
        import pathlib
        p = pathlib.Path(path)
        p.mkdir(parents=True, exist_ok=True)
        print("      ","Directory created", path)

def _removeFile(codeValue):
    filePattern = codeValue
    #logg('removeFile:', filePattern = filePattern)
    import os, glob
    # Getting All Files List
    fileList = glob.glob(filePattern, recursive=True)
    # Remove all files one by one
    for file in fileList:
        try:
            os.remove(file)
        except OSError:
            print("      ","Error while deleting file")
    #logg("Removed all matched files!")
    print("      ","Removed all matched files!")


#@task
def _renameRecentDownloadFile(codeValue):
    # e.g. codeValue = 'renameRecentDownloadFile:D:/iCristal/Output/APAC_Daily_Sales/,D:\\iCristal\\,*.pdf,120'
    tmpDict = parseArguments('saveName,saveName_suffix,sourcePath,targetPath,fileExtension,withinLastSec',codeValue)
    print('renameRecentDownloadFile','saveName,saveName_suffix,sourcePath,targetPath,fileExtension,withinLastSec', tmpDict)
    if 'saveName' in tmpDict:
        #logg('saveName', saveName = tmpDict['saveName'].strip())
        saveName = tmpDict['saveName'].strip()
        if saveName == '': saveName = variables['url']
    if 'saveName_suffix' in tmpDict:
        #logg('saveName_suffix',saveName_suffix = tmpDict['saveName_suffix'].strip())
        saveName_suffix = tmpDict['saveName_suffix'].strip()
        if saveName_suffix == '': saveName_suffix = ''
    if 'sourcePath' in tmpDict:
        #logg('sourcePath',sourcePath = tmpDict['sourcePath'])  # D:\\iCristal\\
        sourcePath = tmpDict['sourcePath'].strip()
        if sourcePath == '': sourcePath = './' #'.\\' #'D:\\iCristal\\'
    if 'targetPath' in tmpDict:
        #logg('targetPath', targetPath = tmpDict['targetPath'])  # 'D:/iCristal/Output/APAC_Daily_Sales/'
        targetPath = tmpDict['targetPath'].strip()
        if targetPath == '': targetPath = './' #'./Output/APAC_Daily_Sales/' #'D:/iCristal/Output/APAC_Daily_Sales/'
    if 'fileExtension' in tmpDict:
        #logg('fileExtension', fileExtension = tmpDict['fileExtension'])
        fileExtension = tmpDict['fileExtension'].strip()
        if fileExtension == '': fileExtension = 'pdf'
    if 'withinLastSec' in tmpDict:
        #logg('withinLastSec', withinLastSec = tmpDict['withinLastSec'])
        withinLastSec = tmpDict['withinLastSec'].strip()
        if withinLastSec == '':
            withinLastSec = 12000
        else:
            withinLastSec = int(withinLastSec)
    saveName = saveName + saveName_suffix
    downloadedFile = GetRecentCreatedFile(sourcePath,'*.' + fileExtension, withinLastSec) # get most recent file of pdf format in last 120 sec in path
    #logg('renameFile parameters', targetPath = targetPath, saveName = saveName, fileExtension = fileExtension, level = 'debug')
    #logg('Recent Download file : none', level = 'error') if downloadedFile is None else #logg('Recent Download file:', downloadFile = downloadedFile, targetPath = targetPath, saveName = saveName, fileExtension = fileExtension, level = 'info')
    if downloadedFile is not None: renameFile(downloadedFile, targetPath + saveName + '.' + fileExtension)


def _runInBackground():
    #script = codeValue.split(',')[0].strip()
    #workingDir = codeValue.split(',')[1].strip()
    runInBackground()

#@task
def _initializeRPA():
    logger = get_run_logger()
    #if not browserDisable:
    #r.init()
    instantiatedRPA = r.init(visual_automation = True)
    #logg('Initialize RPA', result = instantiatedRPA, level = 'info')
    logger.debug(f"       Initialize RPA = {instantiatedRPA}")


#@task
def _closeRPA():
    logger = get_run_logger()
    #if not browserDisable:
    instantiatedRPA = r.close()    
    logger.debug(f"       Close RPA = {instantiatedRPA}")
    #logg('Close RPA ', result = instantiatedRPA, level = 'info')

#@task
def _url(codeValue, df):
    logger = get_run_logger()
    key = codeValue.strip()
    #print('check key', key)

    if isinstance(key, str) and key[:4]=='http':  # value given is a URL value
        #logger.info(f"      Valid URL")
        url_value = key
    elif key[:1]=='@':                            # value given is a URL value with special prefix @
        url_value = key[1:]
    else:                                         # name of list (key value pair) expected
        #print('check df',df)
        url_value = dfKey_value(df, key)
        #print('      ','URL:',key, url_value) #, type(url_value))
        #logger.info(f"      DEBUG url: ', VARIABLE_TYPE = {type(url_value)}, key = {key}, url_value = {url_value}")
        logger.debug(f"      Open URL: {url_value}")

    import math
    #x = float('nan')
    #math.isnan(x)

    if url_value==None or url_value!=url_value:  #df key value returns empty value
        logger.info(f"      Not a valid key value pair. url_value = {url_value} key = {key}, level = 'warning'")            
    elif not(isinstance(url_value, str)):
        url_value = url_value[0]
        #logg('IsInstanceOfStr', key = key, url_value = url_value)
    if isinstance(url_value, str) and url_value[:4]=='http':
        #runStatement = \
        #                '''
        #                result = r.url(url_value) # true if run is successful
        #                '''
        #print(consoleOutput(runStatement))
        buffer, old_stdout = redirectConsole()
        result = r.url(url_value) # true if run is successful
        consoleOutput = resetConsole(buffer, old_stdout)
        if not result:
            logger.info(f"      RPA ERROR: {consoleOutput}")
        else:
            #logger.info(f"      Valid URL")
            pass
    else:
        logger.info(f"      ERROR: Not http address, url_value = {url_value}, key = {key}, level = 'warning'")
    constants['url'] = key          # set the URL key/name to a temp varaible with label url

def _urls(codeValue, objVar):
    #logg('urls',codeValue = codeValue, objVar = objVar)
    url = dfKey_value(df, objVar).strip()                
    #logg('url', objVar = objVar, url = url)
    r.url(url)
    constants['url'] = objVar.strip()

#@task
def _read(codeValue):
    key = codeValue.split('=',1)[0]
    value = codeValue.split('=',1)[1]
    #logg('read:', key = key, value = value)
    variables[key] = r.read(value)  # print('variables(', key, ')=', variables[key])

#@task
def _checkVariable(codeValue):
    logger = get_run_logger()
    variableValue = variables[codeValue]
    logger.info(f"checkVariable:', key = {codeValue}, variableValue = {variableValue}")

#@task
def _set(codeValue):
    key = codeValue.split('=',1)[0].strip()
    value = codeValue.split('=',1)[1].strip()
    if key == 'iterationCount':
        # special case iteration count
        constants[key] = int(value)
    else:
        variables[key] = value
        #logg('set: ', key = key, variablesValue = variables[key])        

def _increment(codeValue):
    key = codeValue.split(',',1)[0].strip()
    value = codeValue.split(',',1)[1].strip()
    if key == 'iterationCount':
        # special case iteration count
        constants[key] = int(value) + int(constants[key])
    else:
        variables[key] = int(value) + int(variables[key])
        #logg('set: ', key = key, variablesValue = variables[key])        

#@task
def _iterationCount(codeValue, df, objVar):
    # ['iterationCount:' + str(i) + ',' + objVarList[i]]
    countValue = codeValue.split(',',1)[0].strip()
    #objVarListDesc = codeValue.split(',',1)[1].strip()
    constants['iterationCount'] = int(countValue)  
    logger = get_run_logger()
    logger.info(f">>>>>>>>>>>>>>>>>>>> ITERATION:{int(countValue)+1}, {objVar} <<<<<<<<<<<<<<<<<")


def _urlcontains(codeValue):
    search = codeValue.split('=',1)[0]
    result_name = codeValue.split('=',1)[1]
    variables[result_name] = search in r.url()
    #logg('urlcontains: ', search = search, result_name = variables[result_name])        
    print('      ',codeID,codeValue,variables[result_name])

#@task
def _rclick(codeValue):
    if codeValue.lower().endswith(('.png', '.jpg', '.jpeg')): codeValue = Path(IMAGE_DIR + '/' + codeValue).absolute().__str__() 
    r.rclick(codeValue)             # print('rclick',prefix[1])
    print('      ','rclick',codeValue)

#@task
def _present(codeID, codeValue):
    variables[codeID] = r.present(codeValue)             # print('rclick',prefix[1])
    print('      ',codeID,variables[codeID])

#@task
def _exist(codeID, codeValue):
    variables[codeID] = r.exist(codeValue)             # print('rclick',prefix[1])
    print('      ',codeID,variables[codeID])

def _count(codeID, codeValue):
    variables[codeID] = r.count(codeValue)             # print('rclick',prefix[1])
    print('      ',codeID,variables[codeID])

#@task
def _keyboard(codeValue: str):
    r.keyboard(codeValue)           # print('keyboard',prefix[1])

def _type(codeValue: str):
    identifier = codeValue.split(',',1)[0].strip()
    value = codeValue.split(',',1)[1].strip()
    r.type(identifier,value)

def _select(codeValue: str):
    key = codeValue.split(',',1)[0]
    value = codeValue.split(',',1)[1]
    #print("select", key, value)
    #logg('select:', select = key, option = value)
    r.select(key,value)             # print('select',prefix[1])
    #print("select done")

def _snap(codeValue):
    page = codeValue.split(',',1)[0]        
    if page=='':
        page = 'page'
    elif page =='log':
        snapImage()
        return
    saveFile = codeValue.split(',',1)[1]
    if saveFile=='': saveFile = './Output/Images/' + saveFile
    #logg('######### snap ###########', page = page, saveFile = saveFile, level = 'debug')
    r.snap(page, saveFile)          

def _telegram(codeValue):
    id = codeValue.split(',',1)[0].strip()
    msg = codeValue.split(',',1)[1].strip()
    flow_run_name = context.get_run_context().flow_run.dict()['name']
    r.telegram(int(id),f"{flow_run_name}-{msg}")

def selectTable(codeValue: str, df):
    # Returns a objTableSet (table object) with parameter which is either a table object in the list or a worksheet
    logger = get_run_logger()
    # table specified
    obj = codeValue
    #from openpyxl import load_workbook
    #wb = load_workbook(STARTFILE, read_only=True)   # open an Excel file and return a workbook
    if obj in df[(df.Type == 'table')]['Object'].dropna().values.tolist():
        #objTableSet = df[(df.Type == 'key') & ((df.Object == obj))]
        objTableSet = df[(df.Type == 'table') & ((df.Object == obj))]   # filter for specified object
        objTableSet = objTableSet.dropna(axis=1, how='all')  # drop all columns where values are nan
        #objTableSet = objTableSet.loc[:, ~objTableSet.columns.str.contains('^Unnamed')]  # remove unnamed columns
        #objTableSet.set_index("Type", inplace = True)
        objTableSet = objTableSet.reset_index(drop=True)    # remove index
        objTableSet = objTableSet.drop(['Type', 'Object'], axis=1)  # drop Type and Object column  
        #logger.info(objTableSet.head())
        objTableSet.columns = objTableSet.iloc[0]   # promote 1st row to header
        objTableSet = objTableSet[1:] #take the data less the header row
        #objTableSet = objTableSet.drop(columns=[0])

        #new_header = objTableSet.iloc[0] #grab the first row for the header
        #objTableSet = objTableSet[1:] #take the data less the header row
        #objTableSet.set_axis(new_header, axis=1, inplace=True)
        #objTableSet.columns = new_header #set the header row as the df header
        #logger.info(objTableSet.head())
        return True, objTableSet
    else:
        result, objTableSet = _isWorkSheetName(obj, excelfile=STARTFILE)
        return result, objTableSet

def _isWorkSheetName(obj, excelfile):
    #check if obj is a worksheet in excelfile and returns result of sheet as dataframe
    logger = get_run_logger()
    try:
        #elif obj in wb.sheetnames:
        sheet = obj
        #excelfile = STARTFILE
        objTableSet = pd.read_excel(excelfile, sheet_name=sheet)
        #logger.info('sheet exists')
        #logger.info(objTableSet)
        return True, objTableSet
    except ValueError as e:
        pass
    return False, None

def _test(codeValue, df, objVar):
    logger = get_run_logger()
    result, objTableSet = selectTable(codeValue, df)  # returns objTableSet from worksheet name
    if result: logger.info(objTableSet.head())

def _ifObjectExist(var:str):
    var_exists = var in locals() or var in globals()
    #try:
    #    exec(var)
    #except NameError:
    #    var_exists = False
    #else:
    #    var_exists = True
    print(f"====================================================== {var} {var_exists}")
    #print(locals())
    #print(globals())
    return var_exists

def _email(codeValue, df):
    import json
    logger = get_run_logger()
    #logger.info(f"Email codeValue: {codeValue}")

    # parse codeValue:
    try:
        emailObj = json.loads(codeValue)    # if codeValue is a Json object
        #logger.info(emailObj)
        #logger.info(emailObj['To'])

    except ValueError as e:
        #logger.info(f"ValueError")
        # not a json format - i.e. assume its a table
        # raise ValueError(f"Raise Error: incorrect json format, {codeValue}")
        if len(codeValue.split(',')) > 1:
            colsMapping = codeValue.split(',',1)[1].strip()
            codeValue = codeValue.split(',',1)[0].strip()
            #logger.info(f"colsMapping:{colsMapping}, codeValue: {codeValue}")
        result, objTableSet = selectTable(codeValue, df)
        #if _ifObjectExist('colsMapping'): # rename columns to names required by email send function
        if 'colsMapping' in locals(): #or var in globals()
            #logger.info(f"Rename cols: {json.loads(colsMapping)}")
            #logger.info(json.loads(colsMapping))
            objTableSet.rename(columns = json.loads(colsMapping), inplace = True)
        mailfieldlst = ['To', 'CC', 'Subject', 'Body', 'HTMLBody', 'Attachment', 'boolDisplay', 'boolRun', 'boolForce']
        objTableSet = objTableSet[objTableSet.columns.intersection(mailfieldlst)]  # select columns for mailing
        if result == True:  # is a table
            n = constants['iterationCount']
            #logger.info('iterationCount ' + str(n))
            objTableSet = objTableSet.iloc[n]  # fiter tableset for current iteration row
            #logger.info(objTableSet)
            #logger.info('columns')
            emailObj = json.loads(objTableSet.to_json(orient="columns"))
            logger.debug(f"   {emailObj}")
    #logger.info(type(emailObj)) # dictionary object

    # Send email
    #print('*******************************************************************')
    #logger.info(f"****** Send Email - emailObj:{emailObj}")
    import traceback
    try:
        To = emailObj['To']
        Subject = emailObj['Subject']
        #HTMLBody = emailObj['HTMLBody']
        #Attachment = emailObj['Attachment']
        #email_sender.send_email(boolDisplay=False, To=To, Subject=Subject, HTMLBody=HTMLBody, Attachment=Attachment)
        #logger.info(f"******** Email To:{To} Subject:{Subject}")

        boolRun = emailObj['boolRun'] if 'boolRun' in emailObj else True 
        boolDisplay = emailObj['boolDisplay'] if 'boolDisplay' in emailObj else False
        boolForce = emailObj['boolForce'] if 'boolForce' in emailObj else False        

        if boolRun: 
            #logger.info(emailObj)
            email_sender = EmailsSender()

            #from auto_utility_email import sentEmailSubjectList
            #logger.info(f"#####>>>> sentEmailSubList, {len(sentEmailSubjectList)}")
            import datetime
            sentEmailSubjectList = email_sender.getSentEmailSubjectList(sentEmailSubjectList = [], cutOffDateTme=datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
            if not Subject in sentEmailSubjectList or boolForce:
                email_sender.send_email(boolDisplay=boolDisplay, boolRun=boolRun, EmailObj = emailObj)
                logger.debug('   email SENT')
            else:
                logger.debug('   email NOT SENT - already sent')
        else:
            logger.debug('   boolRun is FALSE')
        #result = email_sender.wait_send_complete()
    except ValueError as e:
        logger.error('error --', e)
    except Exception as e:
        logger.error(traceback.format_exc())
        #logger.info('error --', e)
    #print('complete')

def _waitEmailComplete(codeValue, df):
    logger = get_run_logger()
    email_sender = EmailsSender()
    result = email_sender.wait_send_complete()
    #import datetime
    #today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) #.strftime('%Y-%m-%d')

    #print(today.strftime('%d/%m/%Y %H:%M %p'))
    #result2 = email_sender.folderItemsList(ofolder=5,dateRange_StartOn=today)          #.sentFolderList()
    #print(result2)
    
    from auto_utility_email import today, sentEmailSubjectList
    #global today
    #global sentEmailSubjectList
    #print(today.strftime('%d/%m/%Y %H:%M %p'), sentEmailSubjectList)
    #print(sentEmailSubjectList)
 
    #email_sender.refreshMail()
 
    logger.debug('   Email complete = ' + str(result))


def etest():    
    logger = get_run_logger()

    lst = codeValue.split(',')
    #code_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    code_dct = {lst[i].split('=')[0]: lst[i].split('=')[1] for i in range(0, len(lst))}           
    
    # Driver code
    #lst = ['a', 1, 'b', 2, 'c', 3]
    logger.info(lst)
    logger.info(code_dct)


    #logger.info(f"   email:{id} msg:{msg}")
    email_sender = EmailsSender()
    #attachment=[r"C:\Users\roh\OneDrive\Personal\TravelPlan\Raymond's KR and SG visit agenda_v3.xlsx"] #"Path to the attachment"
    #email_sender.send_email(To="tsoh20@gmail.com", Subject="Test", HTMLBody="test", attachment=attachment)
    #print('Email', email_sender.wait_send_complete())


#@task
def _click(code:str):
    try:
        int(len(code))
    except ValueError:
        # not int
        #logg('Not int - code is nan', level = 'error')
        return

    if not waitIdentifierExist(code, 30, 1):        # identifier, time_sec, interval
            #logg('      Time out - unable to process step', level = 'critical')           #constants['lastCodelist'] = codeList  
            raise CriticalAccessFailure("Exception critical failure")              
            return
    if code.lower().endswith(('.png', '.jpg', '.jpeg')): code = Path(IMAGE_DIR + '/' + code).absolute().__str__() 
    r.click(code)
    print('      ','click',code)
    #logg('click', code = code, level = 'debug')


