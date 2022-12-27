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
print("running run.py module start section")

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

HEADER = "RUN.PY HEADER " + str(PREFECT_DEPLOYMENT_RUN)

from prefect import task, flow, get_run_logger, context
from prefect.task_runners import SequentialTaskRunner

def main_flow(startfile, startsheet, startcode, background, program_dir):
    """ main flow to run RPA """
    print('Starting RPA flow. File:', startfile, ' | Sheet code:', startsheet, startcode, ' | Background:', background, ' | Time:', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
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

    logger = get_run_logger()
    logger.info(f"DEBUG ----- run main sheet ----- main_code = {main_code}")

    from auto_core_lib import runCodelist
    try_catch(runCodelist(dfmain, main_code))

    import rpa as r
    if not browserDisable and not instantiatedRPA:
        instantiatedRPA = r.close()    
        logger.info(f"'DEBUG Close RPA ', result = {instantiatedRPA}, level = 'info'")

    logger.info(f"DEBUG Complete RPA flow:{startcode}")

    return


@flow(name='launch-autobot', 
      description='launch autobot rpa flow', version='2022.10.27')
def run(file = '', flowrun = 1, deploymentname = ''):
    ''' Deployment run or normal run or deploy to prefect '''
    print("running run flow")
    logger = get_run_logger()
    startTime = datetime.now()
    logger.info(f"flowExecute file {file}, flowrun {flowrun}, start {startTime.strftime('%m/%d/%Y, %H:%M:%S')}")
    current_DIR = Path('.').resolve().absolute().__str__()
    OPTIMUS_DIR = os.getenv('OPTIMUS_DIR')  #D:\Optimus-Prefect-Test1
    # deployment run or normal run or deploy to prefect
    logger.info(f"Run type: Deployment_run={PREFECT_DEPLOYMENT_RUN} {HEADER}, OPTIMUS_DIR={OPTIMUS_DIR}, __file__={__file__}")
    logger.info(f"__file__: {__file__} | file parameter: {file} | flowrun {flowrun} | deploymentname {deploymentname}")
    # module paths
    MODULE_PATH_file = Path(__file__).parents[0].resolve().absolute().__str__()
    MODULE_PATH_lib = Path(f"{OPTIMUS_DIR}/autobot/venv/Lib/site-packages").resolve().absolute().__str__()
    sys.path.append(MODULE_PATH_file)
    sys.path.append(MODULE_PATH_lib)
    logger.info(f"Module: {MODULE_PATH_file} {MODULE_PATH_lib}")
    #logger.info(f"sys path: {sys.path}")

    import config
    from auto_utility_dates import getDuration
    #from auto_utility_file import runInBackground
    if file == '': file = config.FLOW_NAME
    logger.info(f"OPTIMUS_DIR: {os.getenv('OPTIMUS_DIR')} | SETTINGS_PATH {config.SETTINGS_PATH} | FLOW_NAME {config.FLOW_NAME}")
    logger.info(f"Current Directory: {current_DIR} CWD_DIR: {config.CWD_DIR} | __file__ {__file__} | __name__ {__name__}")

    from auto_initialize import checkFileValid
    
    #if PREFECT_DEPLOYMENT_RUN:
    #    config.STARTFILE = file
   
    if not checkFileValid(Path(config.STARTFILE)):
        raise ValueError(f"Start File Error {config.STARTFILE}")

    flowname = Path(config.STARTFILE).stem.__str__() + "-" + config.STARTSHEET + "-" + config.STARTCODE
    logger.info(f"STARTFILE:{config.STARTFILE} {flowname}")
    logger.info("Version: 22.10.26.1")

    try:
        #print('Command:',file)
        logger.info(f"Current directory {Path('.').resolve().absolute().__str__()}")
        #result = main_flow.with_options(name=flowname, retries=1)(startfile=file, startsheet=config.STARTSHEET, startcode=config.STARTCODE, \
        #    background=config.BACKGROUND, program_dir=config.PROGRAM_DIR)
        result = main_flow(startfile=file, startsheet=config.STARTSHEET, startcode=config.STARTCODE, \
            background=config.BACKGROUND, program_dir=config.PROGRAM_DIR)

    #except:
    except Exception as e: 
        print('Exception', e, "Excel.Application.Workbooks", type(e), e.__str__(), e.__str__() == "Excel.Application.Workbooks")
        #print('Exception')
        #sys.exit(config.EX_SOFTWARE)
        if e.__str__() == "Excel.Application.Workbooks":
            print("kiil process:",killprocess("excel"))
        raise ValueError(f"Software Error: {e}")

    endTime = getDuration(startTime, datetime.now())
    logger.info(f"Completed RPA flow. File: {config.STARTFILE} | Sheet: {config.STARTCODE} | Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {endTime}")
    return result

#if __name__ == '__prefect_loader__':   # deployment run
#    new_flow = flowExecute.with_options(name="My new flow")()

if __name__ == "__main__":
    print('main ...')
    result = run()
