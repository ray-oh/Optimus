@echo off
REM echo Arguments %*
REM set arg1=%1
REM set arg2=%2

rem echo Session path: %cd%

SET scriptpath=%~dp0
rem echo %scriptpath:~0,-1%  :: without backslash
rem echo %scriptpath%

REM Change directory to directory of autobot
Pushd %scriptpath:~0,-1%

.\venv\Scripts\python.exe .\src\general_automation\job_monitor.py

popd

rem echo Session path: %cd%

IF %ERRORLEVEL% NEQ 0 ( 
   echo ERROR %ERRORLEVEL%
   EXIT /B %ERRORLEVEL%		:: exit just this batch
   rem EXIT %ERRORLEVEL%	:: exit entire process
   echo %ERRORLEVEL%
)

