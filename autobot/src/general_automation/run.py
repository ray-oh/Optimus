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

script_version = '2022.10.27'
log_space = "          "

from pathlib import Path, PureWindowsPath
import sys, os
from datetime import datetime

from sys_variables import newVariables
from auto_utility_file import killprocess

if __name__ == '__prefect_loader__':
    PREFECT_DEPLOYMENT_RUN = True
    newVariables['DRUN']=True
else:
    PREFECT_DEPLOYMENT_RUN = False
    newVariables['DRUN']=False

HEADER = "Deployment Run=" + str(PREFECT_DEPLOYMENT_RUN)

from prefect import task, flow, get_run_logger, context
from prefect.task_runners import SequentialTaskRunner

def main_flow(startfile, startsheet, startcode, background, program_dir):
    """ main flow to run RPA """
    logger = get_run_logger()

    #logger.info(f"DEBUG run.py/main_flow Starting RPA flow. File: {startfile} | Sheet code: {startsheet}, {startcode} | Background: {background} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
    from auto_utility_file import runInBackground
    if int(background) == 1 : runInBackground(program_dir)
    #import rpa as r

    from auto_helper_lib import try_catch, readExcelConfig, dfKey_value, dfObjList
    from auto_core_lib import runCodelist #, trial
    # default: excel file from config.json, firstSheetModeule = main
    dfmain = try_catch(readExcelConfig(startsheet))
    #print(dfmain[:20])

    browserDisable = False if dfKey_value(dfmain, 'browserDisable') == None else dfKey_value(dfmain, 'browserDisable')
    instantiatedRPA = False

    # run the main code block
    main_code = dfObjList(dfmain, startcode)

    #logger.info(f"DEBUG run.py/main_flow ----- run main sheet ----- main_code = {main_code}")

    from auto_core_lib import runCodelist
    try_catch(runCodelist(dfmain, main_code))

    import rpa as r
    if not browserDisable and not instantiatedRPA:
        instantiatedRPA = r.close()    
        #logger.info(f"'DEBUG run.py/main_flow Close RPA ', result = {instantiatedRPA}, level = 'info'")
    #logger.info(f"DEBUG run.py/main_flow Complete RPA flow:{startcode}")
    from auto_helper_lib import Window, process_list
    processResult = process_list(name='', minutes=30)
    #selectedWindows = Window()

    return


@flow(name='launch-autobot', 
      description='launch autobot rpa flow', version=script_version)
def run(file = '', flowrun = 1, deploymentname = '', PROGRAM_DIR = '', startcode = '', startsheet = '', background = ''):
    ''' Deployment run or normal run or deploy to prefect '''
    #print("running run flow")
    logger = get_run_logger()
    startTime = datetime.now()

    current_DIR = Path('.').resolve().absolute().__str__()
    # disable use of OPTIMUS_DIR env var
    #OPTIMUS_DIR = os.getenv('OPTIMUS_DIR')  #D:\Optimus-Prefect-Test1
    # deployment run or normal run or deploy to prefect
    # module paths
    MODULE_PATH_file = Path(__file__).parents[0].resolve().absolute().__str__()
    MODULE_PATH_lib = Path(f"{PROGRAM_DIR}/autobot/venv/Lib/site-packages").resolve().absolute().__str__()  #OPTIMUS_DIR
    sys.path.append(MODULE_PATH_file)
    sys.path.append(MODULE_PATH_lib)
    logger.debug(f"{log_space}RPA start {startTime.strftime('%m/%d/%Y, %H:%M:%S')} | {HEADER} | \
        Version={script_version} | PROGRAM_DIR={PROGRAM_DIR}, current_DIR={current_DIR}, __file__={__file__} | \
            flowExecute file={file}, flowrun={flowrun}, deploymentname={deploymentname} | \
                Module path: {MODULE_PATH_lib} and {MODULE_PATH_file}")  # and  OPTIMUS_DIR={OPTIMUS_DIR}, 
    #logger.debug(f"Module path: {MODULE_PATH_file} | {MODULE_PATH_lib}")
    #logger.info(f"sys path: {sys.path}")

    from auto_helper_lib import Window, process_list
    processResult = process_list(name='', minutes=30)
    #selectedWindows = windows_getTitle(name='')
    selectedWindows = Window()
    #logger.debug(f'{log_space}Windows: {selectedWindows.title}')

    # if not deployment run i.e. normal run
    #print(f"Context ... {context.get_run_context().flow_run.deployment_id}")
    if context.get_run_context().flow_run.deployment_id == None:
        import config
        #from auto_utility_dates import getDuration
        #from auto_utility_file import runInBackground
        if file == '': file = deploymentname + ".xlsm" #config.FLOW_NAME
        if startsheet == '': startsheet = config.STARTSHEET
        if startcode == '': startcode=config.STARTCODE
        if background == '': background=config.BACKGROUND
        if PROGRAM_DIR == '': PROGRAM_DIR = config.PROGRAM_DIR

        #logger.info(f"DEBUG run.py/run OPTIMUS_DIR: {os.getenv('OPTIMUS_DIR')} | SETTINGS_PATH {config.SETTINGS_PATH} | FLOW_NAME {config.FLOW_NAME}")
        #logger.info(f"DEBUG run.py/run Current Directory: {current_DIR} CWD_DIR: {config.CWD_DIR} | __file__ {__file__} | __name__ {__name__}")

        from auto_initialize import checkFileValid
        
        #if PREFECT_DEPLOYMENT_RUN:
        #    config.STARTFILE = file

        # Check if start file is valid - but this code probably not needed here as its included in CONFIG file executed by import config
        if not checkFileValid(Path(config.STARTFILE)):
            logger.critical(f"SCRIPT START FILE INVALID - Check file path: {Path(config.STARTFILE)}")            
            raise ValueError(f"Start File Error {config.STARTFILE}")
            exit

        flowname = Path(config.STARTFILE).stem.__str__() + "-" + config.STARTSHEET + "-" + config.STARTCODE
        #logger.info(f"DEBUG run.py/run STARTFILE:{config.STARTFILE} {flowname}")
        #logger.info("DEBUG run.py/run Version: 22.10.26.1")

    try:
        #print('Command:',file)
        #logger.info(f"DEBUG run.py/run Current directory {Path('.').resolve().absolute().__str__()}")
        #result = main_flow.with_options(name=flowname, retries=1)(startfile=file, startsheet=config.STARTSHEET, startcode=config.STARTCODE, \
        #    background=config.BACKGROUND, program_dir=config.PROGRAM_DIR)
        result = main_flow(startfile=file, startsheet=startsheet, startcode=startcode, \
            background=background, program_dir=PROGRAM_DIR)

    #except:
    except Exception as e: 
        #print('Exception', e, "Excel.Application.Workbooks", type(e), e.__str__(), e.__str__() == "Excel.Application.Workbooks")
        #print('Exception')
        #sys.exit(config.EX_SOFTWARE)
        if e.__str__() == "Excel.Application.Workbooks":
            logger.critical(f"kiil process: {killprocess('excel')}")
        raise ValueError(f"Software Error: {e}")

    selectedWindows.getNew()
    selectedWindows.closeNew()

    from auto_utility_dates import getDuration
    endTime = getDuration(startTime, datetime.now())
    # logger.info(f"Completed RPA flow. File: {config.STARTFILE} | Sheet: {config.STARTCODE} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {endTime}")
    logger.info(f"Completed RPA flow. File: {file} | Sheet: {startsheet} {startcode} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {endTime}")
    return result

#if __name__ == '__prefect_loader__':   # deployment run
#    new_flow = flowExecute.with_options(name="My new flow")()

if __name__ == "__main__":
    print('main ...')
    result = run()
