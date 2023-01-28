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
#from prefect import flow, task
#from prefect.task_runners import SequentialTaskRunner
#from prefect import flow, get_run_logger # task, 
from prefect import task, flow, get_run_logger, context
from prefect.task_runners import SequentialTaskRunner

import config
from pathlib import Path, PureWindowsPath

from auto_helper_lib import *
from auto_utility_PDF_Image import *
#from auto_utility_logging import *
#from auto_utility_file import GetRecentCreatedFile, runInBackground
from auto_utility_browser import *
from auto_utility_parsers import *


#@flow(validate_parameters=False)
#def runCodelist(request: CodeObject, codeList: list, run_code_until: str = '', objVar: str = '') -> 'Jounes':

#@flow(task_runner=SequentialTaskRunner(), validate_parameters=False)
#def runCodelist(request: CodeObject, codeList: list, run_code_until: str = '', objVar: str = ''):
def runCodelist(df: pd.DataFrame, codeList: list, run_code_until: str = '', objVar: str = ''):    
    DFlist = [df] * len(codeList)
    objVarList = [objVar] * len(codeList)
    logger = get_run_logger()
    #logger.info(f"RunCodeList checking ...:  {codeList} ")
    if run_code_until != '':
        codeList = codeList[:int(run_code_until)]
        print('******************************ERROR !!!!! **************************************')
        logger.debug(f"{log_space}DEBUG *** codeList sliced ****', codeList = {codeList}, level = 'WARNING'")
    while len(codeList) > 0:
        x = codeList[0]
        df = DFlist[0]
        objVar = objVarList[0]
        #logger = get_run_logger()
        #logger.info(f">>>>>runCodelist ...:  {x} {df.__len__()} {objVar}")

        codeList.pop(0)
        DFlist.pop(0)
        objVarList.pop(0)
        #prefix = x.split(':',1)
        #logger.info(f">>>>>runCodelist ... popped :  {x} {df.__len__()} {objVar}")
         
        if isinstance(x, list):
            logger.debug(f"{log_space}click', codeInCodeList = {x[0]}")
            #hoverClick(x[0], 2, 1, x[1], x[2]) # if a list is defined, call with offset x and y
        else:
            #try_catch(runCode(df, x, objVar), x)
            #logger.info(f">>>>>runCodelist ... before runCode :  {x} {df.__len__()} {objVar}")

            additionalCodeList, additionalDFlist, additionalobjVarList = runCode(df, x, objVar)

            #logger = get_run_logger()
            if not (additionalCodeList == None or additionalCodeList == []):
                #logger.info(f"additional CodeList:{additionalCodeList} DFlist: {additionalDFlist.__len__()} objVarList:{additionalobjVarList} ")

                codeList = additionalCodeList + codeList
                DFlist = additionalDFlist + DFlist
                objVarList = additionalobjVarList + objVarList

                #logger.info(f"codeList ...:{codeList} DFlist ...:{DFlist.__len__()} objVarList ...:{objVarList}")

            #try_catch(runCodeFlow.with_options(name=flowname, validate_parameters=False)(CodeObject(df)))
            #try_catch(runCodeFlow.with_options(name=flowname, validate_parameters=False)(CodeObject(df), x, objVar))

            import re
            flowname = re.sub('[^a-zA-Z0-9 \n\.]', '_', x)
            #try_catch(runCodeFlow.with_options(name=flowname)(CodeObject(df), x, objVar))
            #logger.info(f"CHECK codeList ...:{codeList} {codeList.__len__()} DFlist ...:{DFlist.__len__()} objVarList ...:{objVarList}")

        #r.wait(2)
    return



# run Code - single line of code
#runCode('url:https://bear.com')
#runCode('read:checkUserName=okta-signin-username')
#print(tmpObj['checkUserName'])
#tmpObj = {}
def runCode(df, code, objVar=''):
    logger = get_run_logger()
    #logger.info(f".... start runcode .... code:{code} objVar:{objVar} df:{df.shape}")
    from pathlib import Path, PureWindowsPath    
    prefix = code.split(':',1)
    codeID = prefix[0].strip()
    if codeID == 'rem': return [], [], []                     # remarks - do nothing
    codeBeforeTemplateUpdate = code
    variables['codeBeforeTemplateUpdate'] = codeBeforeTemplateUpdate
    #logg('### runCode before replacing templated values ###:', CODE = code, OBJVAR = objVar) 
    code = updateConstants(df, code.strip())  # replace templated values
    #logg('### runCode after update template values ###:', CODE = code, OBJVAR = objVar)  
    prefix = code.split(':',1)
    codeID = prefix[0].strip()
    if len(prefix) > 1: 
        codeValue = prefix[1].strip() 
    else: 
        codeValue = None
    print('RUN STEP | ',codeBeforeTemplateUpdate)  # prints code after templated values update
    if not 'iterationCount' in codeBeforeTemplateUpdate:
        logger.info(f"RUN STEP | {codeBeforeTemplateUpdate}")
    if codeBeforeTemplateUpdate.strip() != code.strip():
        #print('       updated:', code)
        logger.debug(f"{log_space}updated:{code}")
    if False: pass
        #elif codeID in commands_df['commands'].dropna().values.tolist():           #run Block of Code
        #pass
    else:
        flowname = re.sub('[^a-zA-Z0-9 \n\.]', '_', code)
        #try_catch(runCodeFlow.with_options(name=flowname)(CodeObject(df), x, objVar))
        #return _otherRunCode.with_options(name=flowname)(df, code, codeID, codeValue, objVar)
        from auto_core_lib_helper import _otherRunCode
        return _otherRunCode(df, code, codeID, codeValue, objVar)

    return [], [], []

#############################################################################################################################
# obsolete code - not used below

'''
# run a sub_code iteratively over a objVar e.g. a URL list like iterate: URL_pages , codeList:<URL_runprocess:key>
def temprunIterate(df, objVar, sub_code, withHeader=0):
    objVarList = dfObjList(df, objVar, withHeader)
    print('      Iteration list:', objVar, ', ', objVarList)
    logg('******** runIterate objVar:', objVar = objVar) # e.g. URL_Dclick_Pages
    logg('******** runIterate sub_code:', sub_code = sub_code) # e.g. openPages
    logg('******** runIterate objVarList:', objVarList = objVarList) # e.g. ['wBags', 'wRTW', 'wShoes']
    #logg('******** runIterate codeList:', codeList = codeList) # e.g. codelist of openPages i.e.['print ...' , 'urls...']
    i = 0
    for x in objVarList:
        constants['iterationCount'] = i
        logg('runIterate objVarList[i],', i = i , objVarList = objVarList[i], constantsIterationCount = constants['iterationCount'], level = 'info')
        print('ITERATION **************************************** ', 'COUNT', i+1, objVarList[i]) #, ', STEP', sub_code)
        runCode(df, sub_code, objVarList[i])
        i = i + 1
    return
'''

'''
            additionalCodeList = runCode(df, x, objVar)
            if additionalCodeList != None:
                codeList = additionalCodeList + codeList
'''

