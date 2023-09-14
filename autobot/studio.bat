@echo off
rem This script opens the optimus program launcher
set scriptpath=%~dp0
rem Pushd %scriptpath:~0,-1%

rem call %scriptpath%autobot\run.bat %*

rem cd autobot

rem .\venv\Scripts\python.exe .\src\general_automation %*
.\venv\Scripts\python.exe .\src\general_automation\studio.py

rem popd

IF %ERRORLEVEL% NEQ 0 ( 
   echo ERROR %ERRORLEVEL%
   EXIT /B %ERRORLEVEL%
)
