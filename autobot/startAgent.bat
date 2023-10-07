@echo off
SET progpath=%~dp0
REM Change prog directory
Pushd %progpath:~0,-1%

CALL ".\venv\Scripts\activate.bat"
rem set "http_proxy=<proxyserver1>:80"
rem set "https_proxy=<proxyserver12>:80"
rem py start.py
rem https://docs.prefect.io/2.11.4/concepts/agents/
rem something wrong with work queue setup
rem prefect agent start -q %COMPUTERNAME% --prefetch-seconds 60  --limit 1
rem prefect agent start --pool default-agent-pool --prefetch-seconds 60  --limit 1
rem prefect agent start --pool default-agent-pool --work-queue CDAPHKGRPA03 --prefetch-seconds 60  --limit 1
Set PYTHONUTF8=1
rem prefect agent start --pool local-computer --prefetch-seconds 60
prefect agent start --pool default-agent-pool --prefetch-seconds 60

popd
