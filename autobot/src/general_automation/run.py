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


Usage:
from D:\optimus\autobot
Normal run:         run -f main-test
Deploy:             run -f main-test -o 2
Flow run manual:    run -f main-test -o 1
run with a different installation:  run -f main-test -pd D:\optimus_1.2
initialize seting:  run -i 1 -pd D:\optimus_1.2
"""

# In[1]:
# Deployment flow will run run.py including header section
#print("running run.py module start section")

from sys_variables import log_space, codeVersion, startTime
from job_monitor import touchFile, stateChange, write_yaml, read_yaml, triggerRPA #, memoryPath

#script_version = '2022.10.27'
#log_space = "          "

from pathlib import Path, PureWindowsPath
import sys, os
from datetime import datetime

from auto_utility_file import killprocess

# can remove this code and the module sys_variables.py
'''
from sys_variables import newVariables
if __name__ == '__prefect_loader__':
    PREFECT_DEPLOYMENT_RUN = True
    newVariables['DRUN']=True
else:
    PREFECT_DEPLOYMENT_RUN = False
    newVariables['DRUN']=False

HEADER = "Deployment Run=" + str(PREFECT_DEPLOYMENT_RUN)
'''
from prefect import task, flow, get_run_logger, context
from prefect.task_runners import SequentialTaskRunner

'''
# create or update file
memoryPath = "D:\OneDrive-Sync\OneDrive\Shared Documents - RPA Project-APAC_FIN\Status"
def touchFile(filename):
    from pathlib import Path
    Path(filename).touch()
    return True

# change state of token
def stateChange(token="test", statefrom="start", stateto="stop"):
    try:
        #script="test"
        #statefrom="start"
        #stateto="stop"
        import os
        import shutil
        source=rf"{memoryPath}\{statefrom}\{token}.txt"
        dest=rf"{memoryPath}\{stateto}\{token}.txt"
        destination = shutil.move(source, dest)
    except FileNotFoundError:
        print("Token not found")
        return False
    return True
'''

@task(name="OPEN")
def main_flow(startfile, startsheet, startcode, background, program_dir, update):
    """ main flow to run RPA """
    logger = get_run_logger()

    #logger.info(f"DEBUG run.py/main_flow Starting RPA flow. File: {startfile} | Sheet code: {startsheet}, {startcode} | Background: {background} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
    from auto_utility_file import runInBackground
    if '1' in str(background) : runInBackground(program_dir)
    #import rpa as r

    from utility_excel import isFileNewer, pickle_storeData, pickle_loadData, cacheScripts

    from auto_helper_lib import try_catch, readExcelConfig, dfKey_value, dfObjList
    from auto_core_lib import runCodelist #, trial
    # default: excel file from config.json, firstSheetModeule = main
    #dfmain = try_catch(readExcelConfig(startsheet))
    #print('##########', startfile, startsheet, Path(startfile).name)

    import pandas as pd
    dfmain, msgStr = cacheScripts(script=Path(startfile).name,df=pd.DataFrame(),program_dir=program_dir, startsheet=startsheet, refresh=bool(update), msgStr='')
    dfmain, msgStr = cacheScripts(script='OptimusLib.xlsm',df=dfmain,program_dir=program_dir, startsheet=startsheet, refresh=False, msgStr=msgStr)
    dfmain, msgStr = cacheScripts(script='OptimusLibPublic.xlsm',df=dfmain,program_dir=program_dir, startsheet=startsheet, refresh=False, msgStr=msgStr)
    msgStr = f"{log_space}Start file:{startfile}, Start sheet:{startsheet}, Start file name:{Path(startfile).name}\n{log_space}Scripts files loaded:\n" + msgStr
    logger.debug(f"{msgStr}")
    #print(dfmain[:20])

    browserDisable = False if dfKey_value(dfmain, 'browserDisable') == None else dfKey_value(dfmain, 'browserDisable')
    instantiatedRPA = False

    import config
    #global RPABROWSER
    config.RPABROWSER = 0 if dfKey_value(dfmain, 'RPABROWSER') == None else int(dfKey_value(dfmain, 'RPABROWSER'))    
    logger.error(log_space+f'RPABROWSER: {config.RPABROWSER} | Value in main: '+ str(dfKey_value(dfmain, 'RPABROWSER')))
    #print('*********************************************************', config.RPABROWSER)

    # run the main code block
    main_code = dfObjList(dfmain, startcode)

    #logger.info(f"DEBUG run.py/main_flow ----- run main sheet ----- main_code = {main_code}")

    return browserDisable, instantiatedRPA, dfmain, main_code

#@flow
@task
def launch(browserDisable, instantiatedRPA, dfmain, main_code, file):
    from auto_helper_lib import try_catch
    from auto_core_lib import runCodelist
    print('######################',file)

    # change working directory to Assets directory - downloads etc will be in that folder
    #if FLOWRUN != 2:
    from auto_initialize import changeWorkingDirectory
    from config import ASSETS_DIR, CWD_DIR
    CWD_DIR = changeWorkingDirectory(ASSETS_DIR)

    from config import TASK_COUNT
    TASK_COUNT = context.get_run_context().task_run.run_count #context.get("task_run_count")

    try_catch(runCodelist(dfmain, main_code, file=file))
    return browserDisable, instantiatedRPA

@task
def optimus_close(browserDisable, instantiatedRPA):
    import rpa as r
    if not browserDisable and not instantiatedRPA:
        instantiatedRPA = r.close()    
        #logger.info(f"'DEBUG run.py/main_flow Close RPA ', result = {instantiatedRPA}, level = 'info'")
    #logger.info(f"DEBUG run.py/main_flow Complete RPA flow:{startcode}")
    from auto_helper_lib import Window, process_list
    processResult = process_list(name='', minutes=30) # get list of specific name process or all process (if name = '') started within last X min
    #selectedWindows = Window()
    return

@flow(name='launch-autobot', 
      description='launch autobot rpa flow', version=codeVersion)
def run(file = '', flowrun = 1, deploymentname = '', PROGRAM_DIR = '', update = '', retries = '',
            startcode = '', startsheet = '', background = '', retry_delay_seconds=30, **kwargs):
    logger = get_run_logger()
    logger.debug(f"Run started ... ") #Deployment:{isDeploymentFlowRun}   
    #startTime = datetime.now()

    current_DIR = Path('.').resolve().absolute().__str__()
    # disable use of OPTIMUS_DIR env var
    #OPTIMUS_DIR = os.getenv('OPTIMUS_DIR')  #D:\Optimus-Prefect-Test1
    # deployment run or normal run or deploy to prefect
    # module paths
    MODULE_PATH_file = Path(__file__).parents[0].resolve().absolute().__str__()
    MODULE_PATH_lib = Path(f"{PROGRAM_DIR}/autobot/venv/Lib/site-packages").resolve().absolute().__str__()  #OPTIMUS_DIR
    sys.path.append(MODULE_PATH_file)
    sys.path.append(MODULE_PATH_lib)
    logger.debug(f"Flow Run Parameters: \n \
        {log_space}PROGRAM_DIR={PROGRAM_DIR}, \n \
        {log_space}current_DIR={current_DIR} | \n \
        {log_space}Module path: {MODULE_PATH_lib} and {MODULE_PATH_file} | \n \
        {log_space}__file__={__file__} | flowExecute file={file}, flowrun={flowrun}, deploymentname={deploymentname} ")  # and  OPTIMUS_DIR={OPTIMUS_DIR}, 
    #logger.debug(f"Module path: {MODULE_PATH_file} | {MODULE_PATH_lib}")
    #logger.info(f"sys path: {sys.path}")

    from config import configuResultMsg
    from config import isDeploymentFlowRun

    #(file = '', flowrun = 1, deploymentname = '', PROGRAM_DIR = '', startcode = '', startsheet = '', background = '', update = ''):
    # ['file', 'flowrun', 'deploymentname', 'PROGRAM_DIR', 'startcode', 'startsheet', 
    # 'background', 'update', 'kwargs'] but was provided with parameters ['file', 'flowrun', 
    # 'deploymentname', 'PROGRAM_DIR', 'update', 'retries', 'startcode', 'startsheet', 'background']    
    ''' Deployment run or normal run or deploy to prefect '''
    #print('Is this a PREFECT DEPLOYMENT RUN', PREFECT_DEPLOYMENT_RUN)
    #print("running run flow")
    logger.debug(f"CONFIGURATION SETTINGS completed ... \n{configuResultMsg()}") # log configResults

    logger.debug(f"Flow run param:{context.get_run_context().flow_run.parameters}")

    from auto_helper_lib import Window, process_list, process_kill
    processResult = process_list(name='', minutes=30) # generate list of running process in last x min for info
    #selectedWindows = windows_getTitle(name='')
    selectedWindows = Window()
    #logger.debug(f'{log_space}Windows: {selectedWindows.title}')

    import config

    # if not deployment run i.e. normal run
    #print(f"Context ... {context.get_run_context().flow_run.deployment_id}")
    if context.get_run_context().flow_run.deployment_id == None:
        import config
        #from auto_utility_dates import getDuration
        #from auto_utility_file import runInBackground
        if file == '': file = config.STARTFILE #deploymentname + ".xlsm" #config.FLOW_NAME
        if startsheet == '': startsheet = config.STARTSHEET
        if startcode == '': startcode=config.STARTCODE
        if background == '': background=config.BACKGROUND
        if update == '': update=config.UPDATE
        if PROGRAM_DIR == '': PROGRAM_DIR = config.PROGRAM_DIR

        #logger.info(f"DEBUG run.py/run OPTIMUS_DIR: {os.getenv('OPTIMUS_DIR')} | SETTINGS_PATH {config.SETTINGS_PATH} | FLOW_NAME {config.FLOW_NAME}")
        #logger.info(f"DEBUG run.py/run Current Directory: {current_DIR} CWD_DIR: {config.CWD_DIR} | __file__ {__file__} | __name__ {__name__}")
        '''
        from auto_initialize import checkFileValid
        
        #if PREFECT_DEPLOYMENT_RUN:
        #    config.STARTFILE = file

        # Check if start file is valid - but this code probably not needed here as its included in CONFIG file executed by import config
        # confirm - this code block is useless and can be removed
        if not checkFileValid(Path(config.STARTFILE)):
            try:
                print('####',file, Path(file).stem, config.STARTFILE)
                if not stateChange(Path(file).stem,"start","fail"): 
                    state="fail"
                    touchFile(rf"{memoryPath}\{state}\{Path(file).stem}.txt")
                    print(f"#### {file}: fail")
            except Exception as e:
                pass
            logger.critical(f"SCRIPT START FILE INVALID - Check file path: {Path(config.STARTFILE)}")            
            raise ValueError(f"Start File Error {config.STARTFILE}")
            exit
        '''
        flowname = Path(config.STARTFILE).stem.__str__() + "-" + config.STARTSHEET + "-" + config.STARTCODE
        #logger.info(f"DEBUG run.py/run STARTFILE:{config.STARTFILE} {flowname}")
        #logger.info("DEBUG run.py/run Version: 22.10.26.1")
    else:
        # deployment run - flowExecute file=test.xlsm, flowrun=1, deploymentname=test-CDAPHKGRPA03
        flowname = deploymentname         # e.g. test-CDAPHKGRPA03

        # update config variables
        #config.PROGRAM_DIR =
        config.STARTFILE = file
        #config.SCRIPTS_DIR
        #config.OUTPUT_PATH
        #config.IMAGE_PATH
        #config.LOG_PATH
        #config.ADDON_PATH
        #config.SRCLOGFILE

        config.UPDATE = update
        config.RETRIES = retries
        config.BACKGROUND = background
        #config.flow_run_name

        #file = '', flowrun = 1, deploymentname = '', PROGRAM_DIR = '', update = '', retries = '', startcode = '', startsheet = '', background = ''

    # Clean up processes - either run clean.bat or perform below kill process
    #logger.debug(f"Process_kill xxx")
    logger.debug(f"{log_space}background:{background}, {type(background)}, update:{update}, file:{file}, flowname:{flowname} ")
    #if background == '' or str(background).strip()=="2":
    #    pass
    #else:
    processesToKill=['OUTLOOK.EXE'] #['OUTLOOK.EXE','EXCEL.EXE', 'chrome.exe', 'Sikulix', 'CASPERJS', 'PHANTOMJS']
    if not '2' in str(background): process_kill(process=processesToKill) #int(background) != 2 does not work as background could be blank

    from config import variables # imports system wide variables from config which is run when importing config
    if '3' in str(background): variables['headless_mode']=True  # overwrite default setting if user requests in CLI flag


    # New mode to trigger script using event trigger run.
    if '4' in str(background) or '5' in str(background):
        print(f"background:{background} | Trigger script: {triggerRPA(file, memoryPath=MEMORYPATH)}")        
        '''
        state="pending"

        #write_yaml_to_file(data, 'output.txt')
        token = {}
        token['update']=update
        token['startfile']=file
        token['startsheet']=startsheet
        token['startcode']=startcode
        token['background']=background
        token['program_dir']=PROGRAM_DIR
        print('Token',token)
        print('LAUNCH RPA SCRIPT:', Path(file).stem, write_yaml(token, rf"{memoryPath}\{state}\{Path(file).stem}.txt"))

        result = read_yaml(rf"{memoryPath}\{state}\{Path(file).stem}.txt")
        print(result)
        '''
        #touchFile(rf"{memoryPath}\{state}\{Path(file).stem}.txt")
        #result == None
        return

    config.flow_run_name = context.get_run_context().flow_run.dict()['name']

    logger.debug(f"RUN STAGE - CONFIGURATION SETTINGS completed ... \n{configuResultMsg()}") # log configResults
    '''
    logger.debug(f"{log_space}RUN STAGE: CONFIGURATION SETTINGS completed ... \n \
        {log_space}Deployment :{context.get_run_context().flow_run.deployment_id}, \n \
        {log_space}Program dir:{config.PROGRAM_DIR}, \n \
        {log_space}Start file :{config.STARTFILE}, \n \
        {log_space}Scripts dir:{config.SCRIPTS_DIR}, \n \
        {log_space}Output dir :{config.OUTPUT_PATH}, \n \
        {log_space}Image dir  :{config.IMAGE_PATH}, \n \
        {log_space}Log dir    :{config.LOG_PATH}, \n \
        {log_space}Addon Dir  :{config.ADDON_PATH}, \n \
        {log_space}SrcLog file:{config.SRCLOGFILE}, \n \
        {log_space}Others     :update:{config.UPDATE} retries:{config.RETRIES}  background:{config.BACKGROUND}  flow run name:{config.flow_run_name} , \n \
        {log_space}Prog Args  :{config.program_args}")
    '''
    try:
        #print('Command:',file)
        #logger.info(f"DEBUG run.py/run Current directory {Path('.').resolve().absolute().__str__()}")
        #result = main_flow.with_options(name=flowname, retries=1)(startfile=file, startsheet=config.STARTSHEET, startcode=config.STARTCODE, \
        #    background=config.BACKGROUND, program_dir=config.PROGRAM_DIR)
        from config import MEMORYPATH
        if not stateChange(Path(file).stem+".txt","start","process",'',MEMORYPATH): 
            state="process"
            touchFile(rf"{MEMORYPATH}\{state}\{Path(file).stem}.txt")
            #exit
        #print(f"#### {file}: process")
        browserDisable, instantiatedRPA, dfmain, main_code = main_flow.with_options(name='OPEN', tags=['OPEN_CLOSE'])(startfile=file, startsheet=startsheet, 
            startcode=startcode, background=background, program_dir=PROGRAM_DIR, update=update)
        #print(browserDisable, instantiatedRPA)
        #launch.with_options(name=flowname.split('-')[0] + '_MAIN')(browserDisable, instantiatedRPA, dfmain, main_code, file)

        config.FLOW_COUNT = context.get_run_context().flow_run.run_count #context.get("task_run_count")
        from config import FLOW_COUNT
        logger.info("%s. FlowRun", FLOW_COUNT)

        #launch.with_options(name=Path(file).stem + '_MAIN')(browserDisable, instantiatedRPA, dfmain, main_code, file)


        from auto_helper_lib import try_catch
        from auto_core_lib import runCodelist
        print('######################',file)

        # change working directory to Assets directory - downloads etc will be in that folder
        #if FLOWRUN != 2:
        from auto_initialize import changeWorkingDirectory
        from config import ASSETS_DIR, CWD_DIR
        CWD_DIR = changeWorkingDirectory(ASSETS_DIR)

        #from config import TASK_COUNT
        #TASK_COUNT = context.get_run_context().task_run.run_count #context.get("task_run_count")

        try_catch(runCodelist(dfmain, main_code, file=file))

        optimus_close.with_options(name='CLOSE', tags=['OPEN_CLOSE'])(browserDisable, instantiatedRPA)
        if not stateChange(Path(file).stem+".txt","process","complete",'',MEMORYPATH):
            logger.critical('Error in state change process->complete')
            #exit()
        #print(f"#### {file}: complete")        
    #except:
    except Exception as e: 
        #print('Exception', e, "Excel.Application.Workbooks", type(e), e.__str__(), e.__str__() == "Excel.Application.Workbooks")
        #print('Exception')
        #sys.exit(config.EX_SOFTWARE)
        if e.__str__() == "Excel.Application.Workbooks":
            logger.critical(f"kiil process: {killprocess('excel')}")  # kill process with name using powershell
        try:
            raise ValueError(f"Software Error: {e}")
        finally:
            from auto_utility_file import printscreen
            printscreen(f".\{config.startTime.strftime('%Y%m%d_%H%M%S')}_{config.flow_run_name}_ERROR.jpg")

            print('####### FINALLY #########')
            from config import RPABROWSER
            if RPABROWSER == 0:
                import rpa as r
                #if not browserDisable and not instantiatedRPA:
                instantiatedRPA = r.close()
                print('Close finally', instantiatedRPA)

                selectedWindows.getNew()
                selectedWindows.closeNew()

            from auto_utility_dates import getDuration
            endTime = getDuration(startTime, datetime.now())
            # logger.info(f"Completed RPA flow. File: {config.STARTFILE} | Sheet: {config.STARTCODE} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {endTime}")
            logger.info(f"Completed RPA flow. File: {file} | {flowname} | Sheet: {startsheet} {startcode} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {endTime}")

    from config import RPABROWSER
    if RPABROWSER == 0:
        selectedWindows.getNew()
        selectedWindows.closeNew()

    from auto_utility_dates import getDuration
    endTime = getDuration(startTime, datetime.now())
    # logger.info(f"Completed RPA flow. File: {config.STARTFILE} | Sheet: {config.STARTCODE} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {endTime}")
    logger.info(f"Completed RPA flow. File: {file} | {flowname} | Sheet: {startsheet} {startcode} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {endTime}")
    return True #result

#if __name__ == '__prefect_loader__':   # deployment run
#    new_flow = flowExecute.with_options(name="My new flow")()

if __name__ == "__main__":
    print('main ...')
    result = run()
