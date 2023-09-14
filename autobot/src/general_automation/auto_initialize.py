"""
Module:         auto_initialize.py
Description:    Initialize upon first run
Created:        30 Jul 2022

Versions:
20210216        Refactor code

"""
#from config import EX_CONFIG, constants
#import config
from pathlib import Path, PureWindowsPath
from auto_utility_file import renameFile
import configparser
from auto_utility_parsers import parseArg
import sys, os

def checkWorkDirectory(strpath: str):
    # Check working directory
    W_DIR = Path(strpath).resolve().absolute().__str__()
    #print('Current working path ',CWD_DIR)  # ./autobot
    return W_DIR

def changeWorkingDirectory(NEW_DIR):
    import os
    # Change the current working directory
    os.chdir(NEW_DIR)

    # Print the current working directory
    CWD_DIR = Path('.').absolute().__str__()
    #print("Current working directory changed to: {0}".format(os.getcwd()))
    #exit()
    return CWD_DIR    

def checkSettingsPath(SETTINGS_PATH):
    if not Path(SETTINGS_PATH).is_file():
        print('Missing file: settings.ini')
        from config import EX_CONFIG
        sys.exit(EX_CONFIG)

def initializeFromSettings(SETTINGS_PATH, deploymentRun=False):
    #print('initialize from settings ...')
    # Load SYSTEM CONSTANTS from settings.ini
    configObj = configparser.ConfigParser()
    configObj.read(SETTINGS_PATH)

    # Setup SYSTEM CONSTANTS from command line arguments
    program_args = parseArg(configObj, deploymentRun)
    #print(program_args)
    return configObj, program_args

def runBatchCommand(commandStr : str):
    #https://riptutorial.com/python/example/5714/more-flexibility-with-popen
    #from pathlib import Path, PureWindowsPath
    import subprocess
    import sys

    #result = subprocess.run([sys.executable, "-c", "print('ocean')"])
    #commandStr = Path(script).absolute().__str__() + ' ' + arguments
    print('Run command string:',commandStr)
    result = subprocess.run(commandStr,
        capture_output=True, text=True
    )

    print('Batch command working directory', Path('.').absolute().__str__())

    print('      ', 'Run batch command: ', commandStr, 'Return code:', result.returncode) #, result.stderr)

    print('Results of batch run *********************************************************')
    print(result.stdout)
    print('Results of batch run *********************************************************')

    return result

def setEnvVar(env_var = "OPTIMUS_DIR", env_val = Path('.').resolve().parents[0].absolute().__str__()):
    # update Windows environment variable permanently with setx
    import os
    #print('before',os.environ["OPTIMUS_DIR"])
    #env_var = "OPTIMUS_DIR" #"BUILD_NUMBER"
    #env_val = PROGRAM_DIR #"D:\Optimus1.1.2.5" #"3.1.3.3.7"
    #os.system("SETX {0} {1} /M".format(env_var,env_val))
    os.system("SETX {0} {1}".format(env_var,env_val))
    #print('after', os.environ["OPTIMUS_DIR"])
    '''
    import os
    os.environ["OPTIMUS_DIR"]="D:\Optimus1.1"
    print(os.environ["OPTIMUS_DIR"])

    # update OS environment variable
    #runBatchCommand("set OPTIMUS_DIR=" + PROGRAM_DIR)
    import subprocess
    #subprocess.run(["set", "OPTIMUS_DIR=" + PROGRAM_DIR])
    #subprocess.run(["set", "OPTIMUS_DIR=D:\Optimus1.1"])
    commandstr = f'set OPTIMUS_DIR={PROGRAM_DIR}'
    print('command is', commandstr)
    return_code = subprocess.call("echo Hello World", shell=True)
    return_code = subprocess.call(commandstr, shell=True)
    print('command run', return_code)
    '''


def updateDependentFolders(field, PROGRAM_DIR:str, configObj, section):
    SCRIPTS_DIR = Path(PROGRAM_DIR + '/scripts').absolute().__str__()
    if not configObj.has_section(section): configObj.add_section(section)
    configObj[section][field] = str(field)
    return SCRIPTS_DIR

def configValidation(configObj, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, SETTINGS_PATH, INITIALIZATION, FLOWRUN=0, DEPLOYMENTNAME = ''):
    #STARTFILE, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, CWD_DIR, SETTINGS_PATH
    # Validation and correction of SETTINGS
    #if not (Path(PROGRAM_DIR).exists() and Path(AUTOBOT_DIR).exists() and Path(PREFECT_DIR).exists() and AUTOBOT_DIR == CWD_DIR):
    #AUTOBOT_DIR = CWD_DIR
    #PROGRAM_DIR = Path(AUTOBOT_DIR).resolve().parents[0].absolute().__str__()
    SCRIPTS_DIR = Path(PROGRAM_DIR + '/scripts').absolute().__str__()
    PREFECT_DIR = Path(PROGRAM_DIR + '/prefect').absolute().__str__()
    AUTOBOT_DIR = Path(PROGRAM_DIR + '/autobot').absolute().__str__()

    if INITIALIZATION==1:
        if not configObj.has_section('settings'): configObj.add_section('settings') 
        configObj['settings']['AUTOBOT_DIR'] = str(AUTOBOT_DIR)
        #configObj['settings']['PROGRAM_DIR'] = str(PROGRAM_DIR)
        configObj['settings']['SCRIPTS_DIR'] = str(SCRIPTS_DIR)
        configObj['settings']['PREFECT_DIR'] = str(PREFECT_DIR)
        setEnvVar("OPTIMUS_DIR", PROGRAM_DIR)

    if FLOWRUN ==2:

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

    print("update: AUTOBOT_DIR, PROGRAM_DIR, SCRIPTS_DIR, PREFECT_DIR", AUTOBOT_DIR, PROGRAM_DIR, SCRIPTS_DIR, PREFECT_DIR)

    # INITIALIZATION SETTING always default 0
    configObj['settings']['INITIALIZATION'] = str(0)
    configObj['settings']['FLOWRUN'] = str(0)
    save_settings(SETTINGS_PATH, configObj)

    return configObj, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR

def checkStartFile(STARTFILE: Path, SCRIPTS_DIR: Path):
    #check if file name is fully formed with extension
    if not STARTFILE.endswith((".xls", ".xlsm")): STARTFILE = STARTFILE + ".xlsm"

    # check if startfile is a file name (0) or directory (1)
    import os
    if len(os.path.dirname(STARTFILE)) == 0:
        STARTFILE = Path(SCRIPTS_DIR, STARTFILE)
    else:
        STARTFILE = Path(STARTFILE)

    #print('startfile',STARTFILE.absolute())
    return STARTFILE.absolute().__str__()


def checkFileValid(file : Path):
    if not file.is_file():
        print('Warning - Invalid file or path: ', file.absolute())
        return False
        #sys.exit(config.EX_CONFIG)     
    return True


def checkSaveSettings(SETTINGS, SETTINGS_PATH, configObj):
    if SETTINGS == 2:
        pass
    elif SETTINGS == 1 or SETTINGS == 0:
        # update log
        if SETTINGS == 1:
            ''' 
            if not configObj.has_section('settings'): configObj.add_section('settings') 
            configObj['settings']['STARTFILE'] = str(STARTFILE)
            configObj['settings']['STARTCODE'] = str(STARTCODE)
            configObj['settings']['STARTSHEET'] = str(STARTSHEET)
            configObj['settings']['BACKGROUND'] = str(BACKGROUND)
            configObj['settings']['LOGPRINT'] = str(LOGPRINT)
            configObj['settings']['LOGPRINTLEVEL'] = str(LOGPRINTLEVEL)
            configObj['settings']['DEFAULTLOGLEVEL'] = str(DEFAULTLOGLEVEL)
            configObj['settings']['SRCLOGFILE'] = str(SRCLOGFILE)
            configObj['settings']['SRCLOGPATH'] = str(SRCLOGPATH)
            '''
            save_settings(SETTINGS_PATH, configObj)

def setup_assetDirectories(STARTFILE, SCRIPTS_DIR, OUTPUT_PATH, IMAGE_PATH, LOG_PATH, ADDON_PATH, SRCLOGFILE):
    SCRIPT_NAME = Path(STARTFILE).name.__str__()  # stem - without extension
    SCRIPT_NAME_WO_EXT = Path(STARTFILE).stem.__str__()  # stem - without extension
    ASSETS_DIR = (Path(STARTFILE).parents[0] / SCRIPT_NAME_WO_EXT).resolve().absolute().__str__()
    #ASSETS_DIR = Path(SCRIPTS_DIR + '/' + SCRIPT_NAME.split('.')[0]).absolute().__str__()
    #print(SCRIPT_NAME.split('.')[0])
    #print(ASSETS_DIR + '/' + SCRIPT_NAME.split('.')[0] + '/' + OUTPUT_PATH)
    OUTPUT_DIR = Path(ASSETS_DIR + '/' + OUTPUT_PATH).absolute().__str__()
    IMAGE_DIR = Path(ASSETS_DIR  + '/' + IMAGE_PATH).absolute().__str__()
    LOG_DIR = Path(ASSETS_DIR + '/' + LOG_PATH).absolute().__str__()
    ADDON_DIR = Path(ASSETS_DIR + '/' + ADDON_PATH).absolute().__str__()
    SRCLOG = Path(LOG_DIR + '/' + SRCLOGFILE).absolute().__str__()
    #print('ASSETS', ASSETS_DIR, IMAGE_DIR, LOG_DIR, OUTPUT_DIR, SCRIPT_NAME, SRCLOG)
    if not(Path(ASSETS_DIR).exists() and Path(OUTPUT_DIR).exists() and Path(IMAGE_DIR).exists() and Path(LOG_DIR).exists() and Path(ADDON_DIR).exists()): 
        if not Path(ASSETS_DIR).exists(): os.mkdir(ASSETS_DIR)
        if not Path(OUTPUT_DIR).exists(): os.mkdir(OUTPUT_DIR)
        if not Path(OUTPUT_DIR).exists(): os.mkdir(OUTPUT_DIR)
        if not Path(IMAGE_DIR).exists(): os.mkdir(IMAGE_DIR)
        if not Path(LOG_DIR).exists(): os.mkdir(LOG_DIR)
        if not Path(ADDON_DIR).exists(): os.mkdir(ADDON_DIR)
        print('Script Directories created ...')
    return SCRIPT_NAME, ASSETS_DIR, OUTPUT_DIR, IMAGE_DIR, LOG_DIR, ADDON_DIR, SRCLOG 

def save_settings(SETTINGS_PATH, configObj):
    from config import constants
    SETTINGS_PATH_BAK = SETTINGS_PATH + "_" + constants['todayYYYYMMDD'] + "_" + constants['now_hhmmss']+".bak"
    print(SETTINGS_PATH_BAK)
    renameFile(SETTINGS_PATH, SETTINGS_PATH_BAK)
    with open(SETTINGS_PATH, 'w') as configfile:
        configObj.write(configfile)
    print('Settings updated and saved:', SETTINGS_PATH, ' Backup:',SETTINGS_PATH_BAK)

# Import the os module
#import os
# Get the current working directory
#cwd = os.getcwd()

# Print the current working directory
#print("Current working directory: {0}".format(cwd))

# Print the type of the returned object
#print("os.getcwd() returns an object of type: {0}".format(type(cwd)))

# Check working directory

##import sys
##print(sys.executable)
##sysexec = Path(str(sys.executable)).parent.parent.parent.absolute()
#  sysexec = str(sys.executable).split('\\venv\\scripts\\')
#  sysexec = sys.executable.split('\\venv\\scripts\\')[0]
#print(sysexec)
# Change the current working directory
#os.chdir('/tmp')
#os.chdir(sysexec)

'''
print(configObj['flag'])
#print(configObj['help'].keys[1])
print('sections',configObj.sections())
print('items',configObj.items('help')[1][1])
print([option for option in configObj['flag']][1])
for key in configObj['help']:  
    print(key)

print('options', configObj.options('help'))
'''

# mainparseArguments
'''setup the values from settings.ini
list of values from settings.ini - flag, help
for each of items in flag, in its order,
populate the function

terminate if not right - settings.ini not well formed

'''

'''
print('has section', configObj.has_section('help'))
print('help items',configObj.items('help'))
print('help items',configObj.items('help').__len__())

print('flag items',configObj.items('flag'))
print('flag items',configObj.items('flag').__len__())

'''

'''
from auto_utility_parsers import mainparseArguments
program_args = mainparseArguments()
#print('outside parsearg',startfile, startcode, startsheet, logPrint, logPrintLevel, defaultLogLevel, srcLog, srcLogPath)
#print(program_args)
'''
#settings = program_args["settings"]
#config_file = program_args["configfile"]     #r".\config.json"

# Settings INI is a mandatory file

# Load from settings.ini
# read config.json parameters

# Import settings ini
#configObj.read(SETTINGS_PATH)
#config.read_dict(cfg_data)



'''
STARTFILE = configObj['settings']['STARTFILE']
STARTCODE = configObj['settings']['STARTCODE']
STARTSHEET = configObj['settings']['STARTSHEET']
BACKGROUND = configObj['settings']['BACKGROUND']

# global config for logging
if configObj['settings']['LOGPRINT'].strip().lower() in ['true', '1']:
    LOGPRINT = True                    # print log to console
else:
    LOGPRINT = False

LOGPRINTLEVEL = int(configObj['settings']['LOGPRINTLEVEL'])         # Default value 30.  Print to console if level is above or equals this level
DEFAULTLOGLEVEL = configObj['settings']['DEFAULTLOGLEVEL']      # if level is not defined when calling logg function.  INFO, DEBUG etc
SRCLOG = configObj['settings']['SRCLOG']
SRCLOGPATH = configObj['settings']['SRCLOGPATH']
# whether it is logged depends on above setting of level=logging.INFO etc. under basicConfig.
#srcLogPath = r'D:\OneDrive-Sync\Christian Dior Couture\APAC Management - Reports - Reports\log\DClick'
#srcLog = r'D:\OneDrive-Sync\Christian Dior Couture\APAC Management - Reports - Reports\log\DClick\generalAutomation.log'
#srcLog = "D:\\OneDrive-Sync\\Christian Dior Couture\\APAC Helpdesk - Report\\serviceNow\\log\\generalAutomation.log"
CONFIGFILE = configObj['settings']['CONFIGFILE']
SETTINGS = configObj['settings']['SETTINGS']
print(STARTFILE, STARTCODE, STARTSHEET)
'''


# from default or user parameters

#print(("." / Path(STARTFILE)).is_dir())
#print('dd', len(os.path.dirname(".\\main.xls")))
#print('d', len(os.path.dirname(".xls")))


'''
STARTCODE = program_args['startcode']
STARTSHEET = program_args['startsheet']
BACKGROUND = program_args['background']        
LOGPRINT = program_args['logprint']       # print log to console
LOGPRINTLEVEL = program_args['logprintlevel']  # Default value 30.  Print to console if level is above or equals this level
DEFAULTLOGLEVEL = program_args['defaultloglevel']  # if level is not defined when calling logg function.  INFO, DEBUG etc
SRCLOG = program_args['srclog']
SRCLOGPATH = program_args['srclogpath']
'''


#print('SUCCESSFUL')

'''
startcode = program_args['startcode']
startsheet = program_args['startsheet']
background = program_args['background']
logPrint = program_args['logPrint']       # print log to console
logPrintLevel = program_args['logPrintLevel']  # Default value 30.  Print to console if level is above or equals this level
defaultLogLevel = program_args['defaultLogLevel']  # if level is not defined when calling logg function.  INFO, DEBUG etc

srcLogPath = LOG_DIR #program_args['srcLogPath']
srcLog = Path(SCRIPTS_DIR, program_args['srcLog'])

'''
# declaring some global constants
'''
PROGRAM_DIR = 'D:\Optimus'
AUTOBOT_DIR = 'D:\Optimus\autobot'
SCRIPTS_DIR = 'D:\Optimus\scripts'
PREFECT_DIR = 'D:\Optimus\prefect'
IMAGE_PATH = '/rpa'
OUTPUT_PATH = '/output'
LOG_PATH = '/log'
ADDON_PATH = '/addon'
'''




