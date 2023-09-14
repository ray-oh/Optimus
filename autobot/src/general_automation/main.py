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
#import time
from prefect import tags, task, flow, get_run_logger

def main():
    import config    # call config upon startup - required to get background argument to modify flow name before calling run flow
    from config import program_args, AUTOBOT_DIR
    from pathlib import Path

    #check program_args
    #print(f"Check deploymentname .... {config.program_args['startfile']}   {config.program_args}")
    #print(f"Check background .... {config.program_args['background']}")

    if '4' in str(config.program_args['background']):
        deploymentname = config.program_args['startfile'] + "_TRIGGER"
    else:
        deploymentname = config.program_args['startfile']

    #timeout = 60*50 #3 * 60  # 1 hour = 60 min x 60 sec
    retries = int(config.program_args['retries'])
    tag = config.program_args['tag']
    with tags(tag):   #("production", "test"):
        #run()  # has tags: a, b
        from run import run
        result = run.with_options(name=deploymentname, retries=retries)() #, timeout_seconds=timeout)()

#### temp delete below
'''
def main3():
    print('#start#')
    # create or update file
    memoryPath = "D:\OneDrive-Sync\OneDrive - Christian Dior Couture\Shared Documents - RPA Project-APAC_FIN\Status"
    def touchFile(filename):
        from pathlib import Path
        Path(filename).touch()
        return True

    touchFile(rf"{memoryPath}\fail\sense_start_time.txt")        
    exit()

def main2():
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

    # extract program_args from settings.ini and also CLI args or GUI options
    configObj, program_args = initializeFromSettings(SETTINGS_PATH)
    # if no start file specificied, abort
    if program_args['startfile'] == '':
        raise ValueError(f"No script file specified")
        import sys
        EX_CONFIG = 1
        sys.exit(EX_CONFIG)

    #check program_args
    print('##### CHECK ARGS ######', program_args)
    #exit()

    #print(configObj, program_args)
    #print('marker', program_args)
    #codeValue = f"501259457, {__file__} {program_args['startfile']}"
    #from auto_core_lib import _telegram
    #_telegram(codeValue)

    # Create Deployment 
    if program_args['flowrun'] == 2:
        print("Create deployment")
        import socket
        computername = socket.gethostname()
        #deploymentname = config.FLOW_NAME + "-"+ str(computername)
        deploymentname = program_args['startfile'] + "-"+ str(computername)
        #parametervalue = {"commandStr": Path(config.PROGRAM_DIR + '/runRPA.bat -f ' + Path(config.STARTFILE).name.__str__()).absolute().__str__()}
        parametervalue = {"file": program_args['startfile'] +".xlsm", "flowrun": 1, "deploymentname": deploymentname, \
            "PROGRAM_DIR": Path(AUTOBOT_DIR).parents[0].resolve().absolute().__str__(), \
            "update": program_args['update'], \
            "startcode": program_args['startcode'], \
            "startsheet": program_args['startsheet'], \
            "background": str(program_args['background'])} 

        from deployment import workflowDeployment
        workflowDeployment(deploymentname, parametervalue)

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

'''

