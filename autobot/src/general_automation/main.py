#!/usr/bin/env python
# coding: utf-8

"""
Module:         general_automation/_main_.py
Description:    RPA automation with Excel front end
Created:        30 Jul 2022

Versions:
20210216    Refactor KB Quest code - reusable sub routines - sub_TXT_*
            helper functions - hoverClick, hoverRclick, waitImage, waitImageDisappear, try_catch
            Logging
            Reorganize assets - image, log, output folders

"""

# In[1]:

#from prefect import task, get_run_logger
from prefect import tags, task, flow, get_run_logger
import time

from run import run

def main():
    #print("running main option")
    #if __name__ == "__main__":    
    #print(__name__)
    from auto_initialize import checkWorkDirectory
    from pathlib import Path, PureWindowsPath
    CWD_DIR = checkWorkDirectory('.')  # directory of run.bat in /autobot
    AUTOBOT_DIR = CWD_DIR

    #print(f"Config __file__: {Path(__file__).name.__str__()} CWD_DIR: {CWD_DIR}")
    from auto_initialize import checkFileValid, checkWorkDirectory, initializeFromSettings, setEnvVar

    # get program dir from windows environment
    import os
    # change logic - always use current program dir for settings path instead from the OPTIMUS_DIR env var
    if True:    #os.getenv('OPTIMUS_DIR') is None:
        SETTINGS_PATH = Path(CWD_DIR + "/settings.ini").resolve().absolute().__str__()
        COMMANDS_PATH = Path(CWD_DIR + "/commands.xlsx").resolve().absolute().__str__()
        # Disable to set OPTIMUS_DIR env var
        #setEnvVar("OPTIMUS_DIR", Path(AUTOBOT_DIR).resolve().parents[0].absolute().__str__())
    else:
        SETTINGS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/settings.ini").resolve().absolute().__str__()
        COMMANDS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/commands.xlsx").resolve().absolute().__str__()
        # if the settings path for optimus_dir is not valid, then pick the current directory
        if not checkFileValid(Path(SETTINGS_PATH)):
            SETTINGS_PATH = Path(CWD_DIR + "/settings.ini").resolve().absolute().__str__()
            COMMANDS_PATH = Path(CWD_DIR + "/commands.xlsx").resolve().absolute().__str__()
    #print('CURRENT DIR:', CWD_DIR, '| OPTIMUS_DIR: ', os.getenv('OPTIMUS_DIR'), '| SETTINGS_PATH',SETTINGS_PATH) # os.environ['OPTIMUS_DIR']
    #checkSettingsPath(SETTINGS_PATH)
    if not checkFileValid(Path(SETTINGS_PATH)):
        raise ValueError(f"Software Error: settings.ini")
        import sys
        EX_CONFIG = 1
        sys.exit(EX_CONFIG)

    configObj, program_args = initializeFromSettings(SETTINGS_PATH)
    #print(configObj, program_args)
    #print('marker', program_args)
    #codeValue = f"501259457, {__file__} {program_args['startfile']}"
    #from auto_core_lib import _telegram
    #_telegram(codeValue)

    if program_args['initialization'] == 1:
        # initialization is current not used - can pass
        print("running initialization option")
        pass

        '''
        PROGRAM_DIR = Path(AUTOBOT_DIR).parents[0].resolve().absolute().__str__()
        SCRIPTS_DIR = Path(PROGRAM_DIR + '/scripts').absolute().__str__()
        PREFECT_DIR = Path(PROGRAM_DIR + '/prefect').absolute().__str__()
        AUTOBOT_DIR = Path(PROGRAM_DIR + '/autobot').absolute().__str__()
        setEnvVar("OPTIMUS_DIR", PROGRAM_DIR)

        configObj['settings']['PROGRAM_DIR'] = str(PROGRAM_DIR)
        configObj['settings']['AUTOBOT_DIR'] = str(AUTOBOT_DIR)
        configObj['settings']['SCRIPTS_DIR'] = str(SCRIPTS_DIR)
        configObj['settings']['PREFECT_DIR'] = str(PREFECT_DIR)
        #configObj['settings']['startfile'] = program_args['startfile']
        #configObj['settings']['startcode'] = program_args['startcode']
        #configObj['settings']['startsheet'] = program_args['startsheet']
        #configObj['settings']['initialization'] = str(0) #program_args['initialization']
        #configObj['settings']['flowrun'] = str(1) #program_args['flowrun']

        from auto_initialize import save_settings
        #save_settings(SETTINGS_PATH, configObj)
        from datetime import datetime, timedelta
        todayYYYYMMDD = datetime.today().strftime('%Y%m%d')
        now_hhmmss = datetime.now().strftime('%H%M%S')
        SETTINGS_PATH_BAK = SETTINGS_PATH + "_" + todayYYYYMMDD + "_" + now_hhmmss + ".bak"
        print(SETTINGS_PATH_BAK)
        from auto_utility_file import renameFile
        renameFile(SETTINGS_PATH, SETTINGS_PATH_BAK)
        with open(SETTINGS_PATH, 'w') as configfile:
            configObj.write(configfile)
        print('Settings updated and saved:', SETTINGS_PATH, ' Backup:',SETTINGS_PATH_BAK)
    '''

    # Create Deployment 
    elif program_args['flowrun'] == 2:
        print("Create deployment")
        import socket
        computername = socket.gethostname()
        #deploymentname = config.FLOW_NAME + "-"+ str(computername)
        deploymentname = program_args['startfile'] + "-"+ str(computername)
        #parametervalue = {"commandStr": Path(config.PROGRAM_DIR + '/runRPA.bat -f ' + Path(config.STARTFILE).name.__str__()).absolute().__str__()}
        parametervalue = {"file": program_args['startfile'] +".xlsm", "flowrun": 1, "deploymentname": deploymentname, \
            "PROGRAM_DIR": Path(AUTOBOT_DIR).parents[0].resolve().absolute().__str__(), \
            "startcode": program_args['startcode'], \
            "startsheet": program_args['startsheet'], \
            "background": str(program_args['background'])} 

        from deployment import workflowDeployment
        workflowDeployment(deploymentname, parametervalue)
        '''
        # save settings
        DEPLOYMENTNAME = deploymentname
        PROGRAM_DIR = Path(AUTOBOT_DIR).parents[0].resolve().absolute().__str__()
        SCRIPTS_DIR = Path(PROGRAM_DIR + '/scripts').absolute().__str__()
        PREFECT_DIR = Path(PROGRAM_DIR + '/prefect').absolute().__str__()
        AUTOBOT_DIR = Path(PROGRAM_DIR + '/autobot').absolute().__str__()


        # save deploymentname settings under deploymentname section
        if configObj.has_section(DEPLOYMENTNAME):
            configObj.remove_section(DEPLOYMENTNAME)
        configObj.add_section(DEPLOYMENTNAME) 

        configObj[DEPLOYMENTNAME] = configObj['settings']

        if not configObj.has_section(DEPLOYMENTNAME): configObj.add_section(DEPLOYMENTNAME) 
        configObj[DEPLOYMENTNAME]['AUTOBOT_DIR'] = str(AUTOBOT_DIR)
        #configObj['settings']['PROGRAM_DIR'] = str(PROGRAM_DIR)
        configObj[DEPLOYMENTNAME]['SCRIPTS_DIR'] = str(SCRIPTS_DIR)
        configObj[DEPLOYMENTNAME]['PREFECT_DIR'] = str(PREFECT_DIR)
        configObj[DEPLOYMENTNAME]['startfile'] = program_args['startfile']
        configObj[DEPLOYMENTNAME]['startcode'] = program_args['startcode']
        configObj[DEPLOYMENTNAME]['startsheet'] = program_args['startsheet']
        configObj[DEPLOYMENTNAME]['initialization'] = str(0) #program_args['initialization']
        configObj[DEPLOYMENTNAME]['flowrun'] = str(2) #program_args['flowrun']
        configObj[DEPLOYMENTNAME]['background'] = str(1) #default run in background mode

        #print("update: AUTOBOT_DIR, PROGRAM_DIR, SCRIPTS_DIR, PREFECT_DIR", AUTOBOT_DIR, PROGRAM_DIR, SCRIPTS_DIR, PREFECT_DIR)

        # INITIALIZATION SETTING always default 0
        #configObj['settings']['INITIALIZATION'] = str(0)
        #configObj['settings']['FLOWRUN'] = str(0)
        from auto_initialize import save_settings
        #save_settings(SETTINGS_PATH, configObj)
        from datetime import datetime, timedelta
        todayYYYYMMDD = datetime.today().strftime('%Y%m%d')
        now_hhmmss = datetime.now().strftime('%H%M%S')
        SETTINGS_PATH_BAK = SETTINGS_PATH + "_" + todayYYYYMMDD + "_" + now_hhmmss + ".bak"
        print(SETTINGS_PATH_BAK)
        from auto_utility_file import renameFile
        renameFile(SETTINGS_PATH, SETTINGS_PATH_BAK)
        with open(SETTINGS_PATH, 'w') as configfile:
            configObj.write(configfile)
        print('Settings updated and saved:', SETTINGS_PATH, ' Backup:',SETTINGS_PATH_BAK)
        '''

        '''
        [diorOrder-CDAPHKGRPA03]
        startfile = diorOrder
        startcode = main
        startsheet = main
        logprint = True
        logprintlevel = 30
        defaultloglevel = DEBUG
        srclogfile = generalAutomation.log
        configfile = .\\settings.ini
        settings = 0
        background = 0
        program_dir = D:\Optimus-Prefect-Test1
        autobot_dir = D:\Optimus-Prefect-Test1\autobot
        scripts_dir = D:\Optimus-Prefect-Test1\scripts
        prefect_dir = D:\Optimus-Prefect-Test1\prefect
        image_path = /rpa
        output_path = /output
        log_path = /log
        srclogpath = /log
        addon_path = /addon
        initialization = 0
        flowrun = 2
        version = 2022.10.09
        '''

    # running from runrpa.bat
    else:
        #print("running from runrpa.bat")
        #result = run()
        deploymentname = program_args['startfile'] #+ "-"+ str(computername)  "launch-" + 
        #print(f"deploymentname .... {program_args['startfile']}   {program_args}")

        timeout = 60*50 #3 * 60  # 1 hour = 60 min x 60 sec
        #parametervalue = {"commandStr": Path(config.PROGRAM_DIR + '/runRPA.bat -f ' + Path(config.STARTFILE).name.__str__()).absolute().__str__()}
        #parametervalue = {"file": program_args['startfile'] +".xlsm", "flowrun": 1, "deploymentname": deploymentname} 
        #result = run.with_options(name=deploymentname, timeout_seconds = timeout, retries = 1)()
        #print(f"Retries .... {program_args['retries']}")
        retries = int(program_args['retries'])
        tag = program_args['tag']
        #print(tag, retries)
        with tags(tag):   #("production", "test"):
            #run()  # has tags: a, b
            result = run.with_options(name=deploymentname, retries=retries)() #, timeout_seconds=timeout)()



