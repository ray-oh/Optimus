# deployment.py

from pathlib import Path, PureWindowsPath
'''
# appending a path
import sys
MODULE_PATHS = Path(__file__).parents[0].resolve().absolute().__str__()
#print('Import Path', MODULE_PATHS)
sys.path.append(MODULE_PATHS)
print('deployment ... autobot', Path(__file__).name.__str__())

from prefect.filesystems import LocalFileSystem
fs = LocalFileSystem(basepath=f"D:\Optimus-Prefect-Test1\deployment\{deploymentname}")

'''

#from config_deployment import *
#import config
from run import run
from prefect.deployments import Deployment
#from prefect.blocks.core import Block
#storage = Block.load("LocalFileSystem/bumblebee")

import socket
computername = socket.gethostname()

#print('done ...', config.FLOW_NAME, config.STARTFILE, config.PROGRAM_DIR)

#deploymentname = config.FLOW_NAME + "-"+ str(computername)
#deploymentname = Path(config.STARTFILE).name.__str__().rsplit('.',1)[0] + "-"+ str(computername)
#parametervalue = {"commandStr": Path(config.PROGRAM_DIR + '/runRPA.bat -f ' + Path(config.STARTFILE).name.__str__()).absolute().__str__()}
#parametervalue = {"file": config.SCRIPT_NAME, "flowrun": 2, "deploymentname": deploymentname} 

'''
if config.INITIALIZATION==1:
    print('Initializing package ....')
    configObj, STARTFILE, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR = \
        configValidation(configObj, STARTFILE, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR, CWD_DIR, SETTINGS_PATH)
    # reset INITIALIZATION
    configObj['settings']['INITIALIZATION'] = str(0)
    save_settings(SETTINGS_PATH, configObj)
    import sys
    sys.exit(EX_OK) # code 0, all ok
'''

# Initialize deploymentname settings in settings.ini
#from auto_initialize import configValidation, save_settings

#print('Initializing package ....')
#configObj, PROGRAM_DIR, AUTOBOT_DIR, SCRIPTS_DIR, PREFECT_DIR = \
#    configValidation(config.configObj, config.PROGRAM_DIR, config.AUTOBOT_DIR, config.SCRIPTS_DIR, config.PREFECT_DIR, \
#        config.SETTINGS_PATH, config.INITIALIZATION, config.FLOWRUN, deploymentname)


def workflowDeployment(deploymentname, parametervalue):
    deployment = Deployment.build_from_flow(
        flow=run.with_options(name=deploymentname),
        name=deploymentname,
        parameters=parametervalue,
        infra_overrides={"env": {"PREFECT_LOGGING_LEVEL": "DEBUG"}},
        work_queue_name=computername
    )
    #     storage=fs
    deployment.apply()
    print('Deployed ...', deploymentname, 'Parameter:',parametervalue)

if __name__ == "__main__":
    #deployment.apply()
    #print('Deployed ...', deploymentname)
    workflowDeployment()

