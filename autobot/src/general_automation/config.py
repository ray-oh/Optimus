'''
The canonical way to share information across modules within a single program is to create a special module (often called config or cfg). 
Just import the config module in all modules of your application; the module then becomes available as a global name. 
Because there is only one instance of each module, any changes made to the module object get reflected everywhere.
'''
#Exit codes
EX_CONFIG = 1
EX_SOFTWARE = 2
EX_OK = 0

from datetime import datetime, timedelta

from run import PREFECT_DEPLOYMENT_RUN #, TEST1VAR, TEST2VAR
from sys_variables import newVariables

yesterday = datetime.today() - timedelta(days=1)
yesterdayYYYYMMDD = yesterday.strftime('%Y%m%d')
yesterdayDDMMYYYY = yesterday.strftime('%d/%m/%Y')
yesterdayDD_MMY_YYYY = yesterday.strftime('%d/%m/%Y')
now_hhmmss = datetime.now().strftime('%H%M%S')
# system variables
constants = {}
constants['yesterdayYYYYMMDD'] = yesterday.strftime('%Y%m%d')
constants['yesterdayDDMMYYYY'] = yesterday.strftime('%d%m%Y')
constants['todayYYYYMMDD'] = datetime.today().strftime('%Y%m%d')
constants['todayDDMMYYYY'] = datetime.today().strftime('%d/%m/%Y')
constants['yesterdayDD_MM_YYYY'] = yesterday.strftime('%d/%m/%Y')
constants['now_hhmmss'] = datetime.now().strftime('%H%M%S')

#tmpObj = {}
#variables = {}
#tmpObj['iterationCount'] = 0
constants['iterationCount'] = 0
#constant['iterationCount'] = tmpObj['iterationCount']
#variables['iterationCount'] = variables['iterationCount']

# declare user defined variables
variables = {}
#system variables that are pre-declared
variables['i']=None
variables['present']=None
variables['exist']=None
variables['count']=None
variables['loopCount']=None
codeVersion = 'version 1.2'

######################## Initialize SETTINGS #######################

from auto_initialize import setEnvVar, checkFileValid, checkWorkDirectory, configValidation, initializeFromSettings, setup_assetDirectories, checkSettingsPath, checkSaveSettings, checkStartFile, save_settings, changeWorkingDirectory
from pathlib import Path, PureWindowsPath
from prefect import task, flow, get_run_logger, context
logger = get_run_logger()
#logger.info(f"CONTEXT {context.get_run_context().flow_run.parameters['file']}  {context.get_run_context().flow_run.parameters} {context.get_run_context().flow_run}")
#if context.get_run_context().flow_run.deployment_id == None:
#    logger.info(f"deployment id is None")
#else:
#    logger.info(f"deployment id is {context.get_run_context().flow_run.deployment_id}")

#logger.info(f"{TEST1VAR} {TEST2VAR} {newVariables['DRUN']} PREFECT_DEPLOYMENT_RUN {PREFECT_DEPLOYMENT_RUN} __name__ {__name__}")

if context.get_run_context().flow_run.deployment_id == None:
    logger.info(f"NORMAL RUN")

    #if not PREFECT_DEPLOYMENT_RUN:
    CWD_DIR = checkWorkDirectory('.')  # directory of run.bat in /autobot
    AUTOBOT_DIR = CWD_DIR

    logger.info(f"Config __file__: {Path(__file__).name.__str__()} CWD_DIR: {CWD_DIR}")

    # get program dir from windows environment
    import os
    if os.getenv('OPTIMUS_DIR') is None:
        SETTINGS_PATH = Path(CWD_DIR + "/settings.ini").resolve().absolute().__str__()
        COMMANDS_PATH = Path(CWD_DIR + "/commands.xlsx").resolve().absolute().__str__()
        setEnvVar("OPTIMUS_DIR", Path(AUTOBOT_DIR).resolve().parents[0].absolute().__str__())
    else:
        SETTINGS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/settings.ini").resolve().absolute().__str__()
        COMMANDS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/commands.xlsx").resolve().absolute().__str__()
        # if the settings path for optimus_dir is not valid, then pick the current directory
        if not checkFileValid(Path(SETTINGS_PATH)):
            SETTINGS_PATH = Path(CWD_DIR + "/settings.ini").resolve().absolute().__str__()
            COMMANDS_PATH = Path(CWD_DIR + "/commands.xlsx").resolve().absolute().__str__()
    logger.info(f"'CURRENT DIR:', {CWD_DIR}, '| OPTIMUS_DIR: ', {os.getenv('OPTIMUS_DIR')}, '| SETTINGS_PATH',{SETTINGS_PATH}") # os.environ['OPTIMUS_DIR']
    #checkSettingsPath(SETTINGS_PATH)
    if not checkFileValid(Path(SETTINGS_PATH)):
        raise ValueError(f"Software Error: settings.ini")
        import sys
        sys.exit(EX_CONFIG)

    #configObj, STARTFILE, STARTCODE, STARTSHEET, LOGPRINT, LOGPRINTLEVEL, DEFAULTLOGLEVEL, SRCLOGFILE, CONFIGFILE, SETTINGS, BACKGROUND, \
    #    PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, IMAGE_PATH, OUTPUT_PATH, LOG_PATH, SRCLOGPATH, ADDON_PATH, INITIALIZE = initialize(SETTINGS_PATH)
    configObj, program_args = initializeFromSettings(SETTINGS_PATH)

    #logger.info(f"'configObj:',{configObj}")
    #logger.info(f"'program_args:',{program_args}")

    # INSTANTIATE configObj
    # declaring SYSTEM CONSTANTS from intialization step
    #optionsStatic = (option for option in configObj.options('settings') if option not in configObj.options('flag'))
    options = (option for option in configObj.options('settings')) #if option not in configObj.options('flag'))
    for option in options:
        optionValue = configObj['settings'][option]
        #logger.info(f"{option.upper()} = '{optionValue}'")
        #logger.info(f"{option.upper()} = configObj['settings']['{option.upper()}']")        
        exec(f"{option.upper()} = configObj['settings']['{option.upper()}']")

    # INSTANTIATE program_args - overwrite configObj instantiation
    for arg in program_args:
        # update user parameters to configObj    
        configObj['settings'][arg.upper()] = str(program_args[arg.lower()])
        #logger.info(arg.upper(), program_args[arg], type(program_args[arg]))
        #logger.info(f"{arg.upper()} = program_args['{arg.lower()}']")
        exec(f"{arg.upper()} = program_args['{arg.lower()}']")
    #print(STARTFILE, STARTCODE, STARTSHEET, LOGPRINT, LOGPRINTLEVEL, DEFAULTLOGLEVEL, SRCLOGFILE, CONFIGFILE, SETTINGS, BACKGROUND)

    # normal 0, flow execute 1, flow deploy 2
    logger.info(f"'FLOW RUN', {FLOWRUN}")

#elif PREFECT_DEPLOYMENT_RUN:    
else:
    logger.info(f"DEPLOYMENT RUN")

    import os
    SETTINGS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/settings.ini").resolve().absolute().__str__()
    #COMMANDS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/commands.xlsx").resolve().absolute().__str__()

    #checkSettingsPath(SETTINGS_PATH)
    if not checkFileValid(Path(SETTINGS_PATH)):
        raise ValueError(f"Software Error: settings.ini")
    configObj, program_args = initializeFromSettings(SETTINGS_PATH)
    #print('configObj:',configObj)
    #print('program_args:',program_args)
    logger.info(f"SETTINGS_PATH {SETTINGS_PATH} configObj: {configObj} | program_args: {program_args}") # | flowrun {flowrun} | deploymentname {deploymentname}")

    # INSTANTIATE configObj
    # declaring SYSTEM CONSTANTS from intialization step
    #optionsStatic = (option for option in configObj.options('settings') if option not in configObj.options('flag'))
    configSection = context.get_run_context().flow_run.parameters['deploymentname']
    options = (option for option in configObj.options(configSection)) #if option not in configObj.options('flag'))
    for option in options:
        optionValue = configObj[configSection][option]
        #logger.info(f"{option.upper()} = '{optionValue}'")
        #logger.info(f"{option.upper()} = configObj[configSection]['{option.upper()}']")        
        exec(f"{option.upper()} = configObj[configSection]['{option.upper()}']")

    # normal 0, flow execute 1, flow deploy 2
    logger.info(f"FLOW RUN, {FLOWRUN}")


#print(PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR)
#print(CWD_DIR, PROGRAM_DIR, LOG_PATH)
#return configObj, STARTFILE, STARTCODE, STARTSHEET, LOGPRINT, LOGPRINTLEVEL, DEFAULTLOGLEVEL, SRCLOGFILE, CONFIGFILE, SETTINGS, BACKGROUND, \
#    PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, IMAGE_PATH, OUTPUT_PATH, LOG_PATH, SRCLOGPATH, ADDON_PATH, INITIALIZE

#configObj, STARTFILE, STARTCODE, STARTSHEET, LOGPRINT, LOGPRINTLEVEL, DEFAULTLOGLEVEL, SRCLOGFILE, CONFIGFILE, SETTINGS, BACKGROUND, \
#        PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, IMAGE_PATH, OUTPUT_PATH, LOG_PATH, SRCLOGPATH, ADDON_PATH, INITIALIZE \
#        = declareConstants(program_args, configObj)

from pathlib import Path, PureWindowsPath
import socket
hostname = str(socket.gethostname())
#print(hostname)
# declare CONSTANTS for prefect flow
options = (option for option in configObj.options('prefect'))  # if option not in configObj.options('flag'))
for option in options:
    optionValue = configObj['prefect'][option]
    #print(f"{option.upper()} = '{optionValue}'")
    #print(f"{option.upper()} = configObj['settings']['{option.upper()}']")        
    exec(f"{option.upper()} = configObj['prefect']['{option.upper()}']")
FLOW_NAME = Path(STARTFILE).name.__str__().rsplit('.',1)[0] + "-"+ hostname
logger.info(f"FLOW_NAME: {FLOW_NAME}")
TASK_NAME = FLOW_NAME
TAG_NAME = "TEST"

#initalize upon installation
if INITIALIZATION==1:
    print('Initializing package ....')
    #configObj, STARTFILE, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR = \
    configObj, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR = \
        configValidation(configObj, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, SETTINGS_PATH, INITIALIZATION)
    #configObj, STARTFILE, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, CWD_DIR, SETTINGS_PATH)
    # reset INITIALIZATION
    exit()
    import sys
    sys.exit(EX_OK) # code 0, all ok

STARTFILE = checkStartFile(STARTFILE, Path(PROGRAM_DIR) / "scripts") 
logger.info(f"STARTFILE {STARTFILE}")

SCRIPT_NAME, ASSETS_DIR, OUTPUT_DIR, IMAGE_DIR, LOG_DIR, ADDON_DIR, SRCLOG = \
    setup_assetDirectories(STARTFILE, SCRIPTS_DIR, OUTPUT_PATH, IMAGE_PATH, LOG_PATH, ADDON_PATH, SRCLOGFILE)
logger.info(f"'SCRIPT_NAME', {SCRIPT_NAME}, \
            'PROGRAM_DIR', {PROGRAM_DIR}, \
            'ASSETS_DIR', {ASSETS_DIR}, \
                'OUTPUT_DIR',{OUTPUT_DIR}, \
                    'IMAGE_DIR',{IMAGE_DIR}, \
                        'LOG_DIR',{LOG_DIR}, \
                            'ADDON_DIR',{ADDON_DIR}, \
                                'SRCLOG',{SRCLOG}")

# change working directory to Assets directory - downloads etc will be in that folder
if FLOWRUN != 2: CWD_DIR = changeWorkingDirectory(ASSETS_DIR)
#print(SCRIPTS_DIR, ASSETS_DIR)

checkSaveSettings(SETTINGS, SETTINGS_PATH, configObj)

logger.info('SETTINGS CONFIGURATION completed ...')

