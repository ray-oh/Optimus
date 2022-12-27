# deployment.py

from pathlib import Path, PureWindowsPath

from run import run
from prefect.deployments import Deployment

import socket
computername = socket.gethostname()

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
    workflowDeployment()

