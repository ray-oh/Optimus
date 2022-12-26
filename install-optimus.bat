@echo off

if [%1]==[] goto usage
echo %1
@echo off
@echo ================ UNPACK PACKAGE ==========================
SET /P AREYOUSURE=Unpack package and overwrite existing files - Are you sure (Y/[N])
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END0
echo ... Installing/upgrading package ...
@echo %cd%
if exist tmp (
	rmdir tmp /S /Q
)
if not exist "optimus_package<.zip" (
	@echo Installation aborted - optimus_package.zip not found.
	pause
	EXIT /B
)
powershell Expand-Archive -Path %1 -DestinationPath .\tmp
rem set destSync=.
rem robocopy .\tmp "%destSync%" /XD __pycache__ Lib venv /XF install.bat /e /copy:DAT /mt /z
rem robocopy .\tmp "%destSync%" /XD __pycache__ Lib venv /XF install-optimus.bat /e /copy:DAT /mt /z
robocopy .\tmp . /XD __pycache__ Lib venv /XF install-optimus.bat /e /copy:DAT /mt /z
rmdir tmp /S /Q
:END0

@echo ================ INSTALL AUTOBOT ==========================
cd autobot
setlocal
:PROMPT1
SET /P AREYOUSURE=Reinstall other python libraries - Are you sure (Y/[N])
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END1
echo ... Reinstalling libraries ...
if exist venv (
	rmdir venv /S /Q
)
python -m venv venv
.\venv\Scripts\pip --version
@echo ================ INSTALL PREFECT ==========================
.\venv\Scripts\pip install -U prefect
.\venv\Scripts\prefect version
@echo ================ INSTALL AUTOBOT ==========================
.\venv\Scripts\pip install -r requirements.txt
:END1
endlocal
cd ..
@echo ================ INSTALLATION COMPLETED ==========================
@echo To use Auto RPA - click runRPA.bat or from the command line with parameters
call runRPA -i 1
call runRPA -h
pause

goto :eof
:usage
@echo ================ OPTIMUS INSTALLATION ============================
@echo Install / upgrade optimus software with optimus_package*.zip files
@echo Usage: %0 ^<OptimusPackageFile^>
@echo ==================================================================
pause
exit /B 1

