@echo off
SET progpath=%~dp0
REM Change prog directory
Pushd %progpath:~0,-1%

CALL ".\venv\Scripts\activate.bat"
rem set "http_proxy=<proxyserver1>:80"
rem set "https_proxy=<proxyserver12>:80"
rem py start.py
rem prefect orion start
prefect server start

popd
