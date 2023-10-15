'''
The canonical way to share information across modules within a single program is to create a special module (often called config or cfg). 
Just import the config module in all modules of your application; the module then becomes available as a global name. 
Because there is only one instance of each module, any changes made to the module object get reflected everywhere.
'''
##################### Global Variables ###################################

#from sys_variables import log_space, 

#Exit codes
EX_CONFIG = 1
EX_SOFTWARE = 2
EX_OK = 0

#logging
log_space = "          "
FLOW_COUNT = 0
TASK_COUNT = 0

from datetime import datetime, timedelta
startTime = datetime.now()

#from run import PREFECT_DEPLOYMENT_RUN #, TEST1VAR, TEST2VAR
#from sys_variables import newVariables

# define a 3am cut off
if int(datetime.now().strftime('%H%M'))>=300:
    yesterday = datetime.today() - timedelta(days=1)
else:
    yesterday = datetime.today() - timedelta(days=2)
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
variables['sentEmailCheck_hour']=3  # used by email program to check if email has already been sent (duplicate subject since this cut off time for the day)
variables['sentEmailCheck_min']=15  # default value can be overwritten in excel script: e.g. set:sentEmailCheck_min=0
variables['headless_mode']=False # '{"visual_automation":True, "chrome_browser":True, "headless_mode":False, "turbo_mode":False}' # default browser mode

variables['rpaBrowser']=False

#variables['codeVersion']=str(flow_run_name)  #'test-codeVersion'
#variables['flowrun']='test-flow'
#variables['arguments']=program_args['arguments']
#variables['flow_run_name']=flow_run_name
#variables['flowrun']=flow_run_name

codeVersion = 'version 23.8.22'
variables['codeVersion']=codeVersion

#script_version = '2022.10.27'
flow_run_name = ''
BACKGROUND = ''
UPDATE = ''
RETRIES = ''
STARTFILE = ''
STARTCODE = ''
STARTSHEET = ''
RPABROWSER = 0 # 0 = TagUI (default) 1=playwright
VERSION = ''

#from job_monitor import memoryPath
# MEMORYPATH = "D:\OneDrive-Sync\OneDrive\Shared Documents - RPA Project-APAC_FIN\Status"
MEMORYPATH = ''    #r"\Optimus\memory"
#D:\OneDrive-Sync\OneDrive\Shared Documents - RPA Project-APAC_FIN\Status"

##################### Global Functions ###################################
from job_monitor import touchFile, stateChange, write_yaml, read_yaml, triggerRPA

######################## Initialize SETTINGS #######################

from auto_initialize import setEnvVar, checkFileValid, checkWorkDirectory, configValidation, initializeFromSettings, setup_assetDirectories, checkSettingsPath, \
                checkSaveSettings, checkStartFile, save_settings, changeWorkingDirectory
from pathlib import Path, PureWindowsPath
from prefect import task, flow, get_run_logger, context

try:
    isDeploymentFlowRun = not context.get_run_context().flow_run.deployment_id == None
    logger = get_run_logger()
    #logger.info(f"CONTEXT {context.get_run_context().flow_run.parameters['file']}  {context.get_run_context().flow_run.parameters} {context.get_run_context().flow_run}")
except Exception as e:
    if "No run context" in str(e):
        #print('error in context - not a deployment run')
        isDeploymentFlowRun = False
    else:
        print('Unknown error', e)
        exit()

CWD_DIR = checkWorkDirectory('.')  # directory of run.bat in /autobot
# Not deployment run scenario / NORMAL RUN
#if context.get_run_context().flow_run.deployment_id == None:
if not isDeploymentFlowRun:
    #logger.info(f"DEBUG config.py NORMAL RUN")

    #if not PREFECT_DEPLOYMENT_RUN:
    AUTOBOT_DIR = CWD_DIR

    #logger.info(f"DEBUG config.py Config __file__: {Path(__file__).name.__str__()} CWD_DIR: {CWD_DIR}")

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
    #logger.info(f"DEBUG config.py CURRENT DIR:', {CWD_DIR}, '| OPTIMUS_DIR: ', {os.getenv('OPTIMUS_DIR')}, '| SETTINGS_PATH',{SETTINGS_PATH}") # os.environ['OPTIMUS_DIR']

    #checkSettingsPath(SETTINGS_PATH)
    if not checkFileValid(Path(SETTINGS_PATH)):
        raise ValueError(f"Software Error: settings.ini")
        import sys
        sys.exit(EX_CONFIG)

    #configObj, STARTFILE, STARTCODE, STARTSHEET, LOGPRINT, LOGPRINTLEVEL, DEFAULTLOGLEVEL, SRCLOGFILE, CONFIGFILE, SETTINGS, BACKGROUND, \
    #    PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, IMAGE_PATH, OUTPUT_PATH, LOG_PATH, SRCLOGPATH, ADDON_PATH, INITIALIZE = initialize(SETTINGS_PATH)
    configObj, program_args = initializeFromSettings(SETTINGS_PATH, deploymentRun=False)

    # Create Deployment 
    if program_args['flowrun'] == 2:
        print("CREATE DEPLOYMENT")
        import socket
        computername = socket.gethostname()
        #deploymentname = config.FLOW_NAME + "-"+ str(computername)
        #parametervalue = {"commandStr": Path(config.PROGRAM_DIR + '/runRPA.bat -f ' + Path(config.STARTFILE).name.__str__()).absolute().__str__()}
        deploymentname = program_args['startfile'] + "-"+ str(computername)
        if '4' in str(program_args['background']):
            prefectdeploymentname=program_args['startfile'] + "-TRIGGER-"+ str(computername)
        else:
            prefectdeploymentname=deploymentname
        parametervalue = {"file": program_args['startfile'] +".xlsm", "flowrun": 1, "deploymentname": deploymentname, \
            "PROGRAM_DIR": Path(AUTOBOT_DIR).parents[0].resolve().absolute().__str__(), \
            "update": program_args['update'], \
            "retries": program_args['retries'], \
            "startcode": program_args['startcode'], \
            "startsheet": program_args['startsheet'], \
            "background": str(program_args['background'])} 

        from deployment import workflowDeployment
        workflowDeployment(prefectdeploymentname, parametervalue)
        exit()


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
    #logger.info(f"'FLOW RUN', {FLOWRUN}")
    #logger.info(f"DEBUG configObj options {PROGRAM_DIR} {STARTFILE}, {SCRIPTS_DIR}, {OUTPUT_PATH}, {IMAGE_PATH}, {LOG_PATH}, {ADDON_PATH}, {SRCLOGFILE}")

    # overwrite optimus_dir env with current directory if manual run
    PROGRAM_DIR = Path(CWD_DIR).parent.absolute().__str__()
    #logger.info(f"DEBUG program_dir {PROGRAM_DIR}")

    # overwrite from settings file with default parameter values - if commented means its defined from settings.ini
    # STARTFILE = context.get_run_context().flow_run.parameters['file']
    SCRIPTS_DIR = Path(PROGRAM_DIR + "/scripts").resolve().absolute().__str__()
    OUTPUT_PATH = '/output'
    IMAGE_PATH = '/rpa'
    LOG_PATH = '/log'
    ADDON_PATH = '/addon'
    SRCLOGFILE = 'generalAutomation.log'

    BACKGROUND = program_args['background']
    UPDATE = program_args['update']
    RETRIES = program_args['retries']
    STARTFILE = program_args['startfile']
    STARTCODE = program_args['startcode']
    STARTSHEET = program_args['startsheet']


#elif PREFECT_DEPLOYMENT_RUN:    
else:
    #logger.info(f"DEBUG config.py - DEPLOYMENT RUN")
    #logger.info(f"Context parameters ... {context.get_run_context().flow_run.parameters} {context.get_run_context().flow_run.parameters['PROGRAM_DIR']}")

    import os
    #SETTINGS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/settings.ini").resolve().absolute().__str__()
    SETTINGS_PATH = Path(context.get_run_context().flow_run.parameters['PROGRAM_DIR'] + "/autobot/settings.ini").resolve().absolute().__str__()    
    #COMMANDS_PATH = Path(os.environ['OPTIMUS_DIR'] + "/autobot/commands.xlsx").resolve().absolute().__str__()

    #checkSettingsPath(SETTINGS_PATH)
    if not checkFileValid(Path(SETTINGS_PATH)):
        raise ValueError(f"Software Error: settings.ini")
    #logger.info(f"DEBUG SETTINGS_PATH {SETTINGS_PATH}")

    configObj, program_args = initializeFromSettings(SETTINGS_PATH, deploymentRun=True)
    #print('configObj:',configObj)
    #print('program_args:',program_args)
    #logger.info(f"SETTINGS_PATH {SETTINGS_PATH} configObj: {configObj} | program_args: {program_args}") # | flowrun {flowrun} | deploymentname {deploymentname}")

    # INSTANTIATE configObj
    # declaring SYSTEM CONSTANTS from intialization step
    '''
    #optionsStatic = (option for option in configObj.options('settings') if option not in configObj.options('flag'))
    configSection = context.get_run_context().flow_run.parameters['deploymentname']
    #logger.info(f"configSection {configSection}")
    options = (option for option in configObj.options(configSection)) #if option not in configObj.options('flag'))
    for option in options:
        optionValue = configObj[configSection][option]
        #logger.info(f"{option.upper()} = '{optionValue}'")
        #logger.info(f"{option.upper()} = configObj[configSection]['{option.upper()}']")        
        exec(f"{option.upper()} = configObj[configSection]['{option.upper()}']")
    '''
    #logger.info(f"DEBUG configSection options {STARTFILE}, {SCRIPTS_DIR}, {OUTPUT_PATH}, {IMAGE_PATH}, {LOG_PATH}, {ADDON_PATH}, {SRCLOGFILE}")

    # overwrite from settings file with default parameter values
    PROGRAM_DIR = Path(context.get_run_context().flow_run.parameters['PROGRAM_DIR']).resolve().absolute().__str__()
    #STARTFILE = context.get_run_context().flow_run.parameters['file']
    SCRIPTS_DIR = Path(context.get_run_context().flow_run.parameters['PROGRAM_DIR'] + "/scripts").resolve().absolute().__str__()
    OUTPUT_PATH = '/output'
    IMAGE_PATH = '/rpa'
    LOG_PATH = '/log'
    ADDON_PATH = '/addon'
    SRCLOGFILE = 'generalAutomation.log'

    if 'background' in context.get_run_context().flow_run.parameters: BACKGROUND = context.get_run_context().flow_run.parameters['background']
    if 'update' in context.get_run_context().flow_run.parameters: UPDATE = context.get_run_context().flow_run.parameters['update']
    if 'retries' in context.get_run_context().flow_run.parameters: RETRIES = context.get_run_context().flow_run.parameters['retries']    
    if 'file' in context.get_run_context().flow_run.parameters: STARTFILE = context.get_run_context().flow_run.parameters['file']
    if 'startsheet' in context.get_run_context().flow_run.parameters: STARTSHEET = context.get_run_context().flow_run.parameters['startsheet']
    if 'startcode' in context.get_run_context().flow_run.parameters: STARTCODE = context.get_run_context().flow_run.parameters['startcode']

    deployment_id = context.get_run_context().flow_run.deployment_id

    #logger.info(f"DEBUG overwrite configSection options {STARTFILE}, {SCRIPTS_DIR}, {OUTPUT_PATH}, {IMAGE_PATH}, {LOG_PATH}, {ADDON_PATH}, {SRCLOGFILE}")

    # normal 0, flow execute 1, flow deploy 2
    #logger.info(f"FLOW RUN, {FLOWRUN}")
    
#print(PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR)
#print(CWD_DIR, PROGRAM_DIR, LOG_PATH)
#return configObj, STARTFILE, STARTCODE, STARTSHEET, LOGPRINT, LOGPRINTLEVEL, DEFAULTLOGLEVEL, SRCLOGFILE, CONFIGFILE, SETTINGS, BACKGROUND, \
#    PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, IMAGE_PATH, OUTPUT_PATH, LOG_PATH, SRCLOGPATH, ADDON_PATH, INITIALIZE

#configObj, STARTFILE, STARTCODE, STARTSHEET, LOGPRINT, LOGPRINTLEVEL, DEFAULTLOGLEVEL, SRCLOGFILE, CONFIGFILE, SETTINGS, BACKGROUND, \
#        PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, IMAGE_PATH, OUTPUT_PATH, LOG_PATH, SRCLOGPATH, ADDON_PATH, INITIALIZE \
#        = declareConstants(program_args, configObj)


#==================================================================
# COMMON for both deployment and manual run
#==================================================================

# some global variables from SETTINGS file
VERSION = configObj['settings']['version']
if not configObj['settings']['memoryPath'] == '':
    MEMORYPATH = configObj['settings']['memoryPath']
if MEMORYPATH == '':
    MEMORYPATH = rf"{PROGRAM_DIR}\memory"

from pathlib import Path, PureWindowsPath
import socket
hostname = str(socket.gethostname())
#print(hostname)
'''
# declare CONSTANTS for prefect flow - FLOW_NAME, FLOW_DESCRIPTION, TASK_NAME, TASK_DESCRIPTION, TAG_NAME, DEPLOYMENT_NAME, PARAMETER_VALUE, COMPUTERNAME
options = (option for option in configObj.options('prefect'))  # if option not in configObj.options('flag'))
for option in options:
    optionValue = configObj['prefect'][option]
    #print(f"{option.upper()} = '{optionValue}'")
    #print(f"{option.upper()} = configObj['settings']['{option.upper()}']")        
    #logger.info(f"DEBUG option prefect values {option.upper()} = configObj['settings']['{option.upper()}']")
    exec(f"{option.upper()} = configObj['prefect']['{option.upper()}']")
FLOW_NAME = Path(STARTFILE).name.__str__().rsplit('.',1)[0] + "-"+ hostname
#logger.info(f"FLOW_NAME: {FLOW_NAME}")
TASK_NAME = FLOW_NAME
TAG_NAME = "TEST"
'''
'''
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
'''
# Return absolute path of start file in scripts folder
STARTFILE = checkStartFile(STARTFILE, Path(PROGRAM_DIR) / "scripts") 
#logger.info(f"DEBUG config.py STARTFILE {STARTFILE}")

if not checkFileValid(Path(STARTFILE)):
    try:
        #touchFile(rf"{memoryPath}\fail\sensetime.txt")        
        print('####',STARTFILE, Path(STARTFILE).stem)
        if not stateChange(Path(STARTFILE).stem,"start","fail",'',MEMORYPATH): 
            state="fail"
            touchFile(rf"{MEMORYPATH}\{state}\{Path(STARTFILE).stem}.txt")
            print(f"#### {STARTFILE}: fail")
    except Exception as e:
        print('#### Fail to touch file in fail')
        pass
    if isDeploymentFlowRun: logger.critical(f"SCRIPT START FILE INVALID - Check file path: {Path(STARTFILE)}")            
    raise ValueError(f"Start File Error {STARTFILE} PROGRAM DIR {PROGRAM_DIR} {MEMORYPATH} ")
    exit
else:
    # setup working directories for script file if they don't exist
    SCRIPT_NAME, ASSETS_DIR, OUTPUT_DIR, IMAGE_DIR, LOG_DIR, ADDON_DIR, SRCLOG = \
        setup_assetDirectories(STARTFILE, SCRIPTS_DIR, OUTPUT_PATH, IMAGE_PATH, LOG_PATH, ADDON_PATH, SRCLOGFILE)
    '''
    logger.info(f"'SCRIPT_NAME', {SCRIPT_NAME}, \
                'PROGRAM_DIR', {PROGRAM_DIR}, \
                'ASSETS_DIR', {ASSETS_DIR}, \
                    'OUTPUT_DIR',{OUTPUT_DIR}, \
                        'IMAGE_DIR',{IMAGE_DIR}, \
                            'LOG_DIR',{LOG_DIR}, \
                                'ADDON_DIR',{ADDON_DIR}, \
                                    'SRCLOG',{SRCLOG}")
    '''
    ###########
    #print(SCRIPTS_DIR, ASSETS_DIR)


#checkSaveSettings(SETTINGS, SETTINGS_PATH, configObj)  # save settings file if SETTINGS parameter = 1
def configuResultMsg():
    if isDeploymentFlowRun:
        #logger.debug(
        #{log_space}CONFIGURATION SETTINGS completed ... \n     
        configResultMsg = f"\
            {log_space}RPA start  :{startTime.strftime('%m/%d/%Y, %H:%M:%S')}, {codeVersion}, \n \
            {log_space}Deployment :{isDeploymentFlowRun}, Id({deployment_id}), \n \
            {log_space}Program dir:{PROGRAM_DIR}, \n \
            {log_space}Start file :{STARTFILE}, \n \
            {log_space}Start sheet:{STARTSHEET}, \n \
            {log_space}Start code :{STARTCODE}, \n \
            {log_space}Scripts dir:{SCRIPTS_DIR}, \n \
            {log_space}Output dir :{OUTPUT_PATH}, \n \
            {log_space}Image dir  :{IMAGE_PATH}, \n \
            {log_space}Log dir    :{LOG_PATH}, \n \
            {log_space}Addon Dir  :{ADDON_PATH}, \n \
            {log_space}SrcLog file:{SRCLOGFILE}, \n \
            {log_space}Memory path:{MEMORYPATH}, \n \
            {log_space}Others     :Update({UPDATE}) retries({RETRIES}) background({BACKGROUND}) flow run name({flow_run_name}),\n \
            {log_space}Prog Args  :{program_args}" #)
    else:
        #print(
        #{log_space}CONFIGURATION SETTINGS completed ... \n     
        #    {log_space}Background :{BACKGROUND}, \n \
        #    {log_space}Update     :{UPDATE}, \n \
        configResultMsg = f"\
            {log_space}RPA start  :{startTime.strftime('%m/%d/%Y, %H:%M:%S')}, {codeVersion}, \n \
            {log_space}Deployment :{isDeploymentFlowRun}, Id(None), \n \
            {log_space}Program dir:{PROGRAM_DIR}, \n \
            {log_space}Start file :{STARTFILE}, \n \
            {log_space}Start sheet:{STARTSHEET}, \n \
            {log_space}Start code :{STARTCODE}, \n \
            {log_space}Scripts dir:{SCRIPTS_DIR}, \n \
            {log_space}Output dir :{OUTPUT_PATH}, \n \
            {log_space}Image dir  :{IMAGE_PATH}, \n \
            {log_space}Log dir    :{LOG_PATH}, \n \
            {log_space}Addon Dir  :{ADDON_PATH}, \n \
            {log_space}SrcLog file:{SRCLOGFILE}, \n \
            {log_space}Memory path:{MEMORYPATH}, \n \
            {log_space}Others     :Update({UPDATE}) retries({RETRIES}) background({BACKGROUND}) flow run name({flow_run_name}),\n \
            {log_space}Prog Args  :{program_args}" #)
    return configResultMsg

