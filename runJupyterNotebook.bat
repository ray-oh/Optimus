@echo off
rem echo Session Path %cd%		:: path of session from which batch file is called
set scriptpath=%~dp0
rem echo Script Path %scriptpath%   :: batch file path
rem echo %scriptpath:~0,-1%  :: without backslash

rem Pushd %scriptpath:~0,-1%        :: Change working directory to script directory

%scriptpath%scripts\runJupyterNotebook.bat %*

rem popd
rem echo Session Path %cd%
