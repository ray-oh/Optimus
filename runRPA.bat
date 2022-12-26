@echo off
rem echo Session Path %cd%		:: path of session from which batch file is called
set scriptpath=%~dp0
rem echo Script Path %scriptpath%   :: batch file path
rem echo %scriptpath:~0,-1%  :: without backslash

rem Pushd %scriptpath:~0,-1%        :: Change working directory to script directory

call %scriptpath%autobot\run.bat %*

IF %ERRORLEVEL% NEQ 0 ( 
   echo ERROR %ERRORLEVEL%
   EXIT /B %ERRORLEVEL%
)

rem popd
rem echo Session Path %cd%
