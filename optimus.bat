if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
@echo off
rem This script opens the optimus program launcher
set scriptpath=%~dp0
Pushd %scriptpath:~0,-1%

rem call %scriptpath%autobot\run.bat %*

cd autobot

rem .\venv\Scripts\python.exe .\src\general_automation %*
.\venv\Scripts\python.exe .\src\general_automation\launcher.py

popd

IF %ERRORLEVEL% NEQ 0 ( 
   echo ERROR %ERRORLEVEL%
   EXIT /B %ERRORLEVEL%
)
exit
