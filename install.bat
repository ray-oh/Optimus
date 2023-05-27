@echo off

if [%1]==[] goto install_autobot 
rem usage
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

:install_autobot
@echo ================ INSTALL AUTOBOT ==========================
:PROMPT1
SET /P AREYOUSURE=Reinstall other python libraries - Are you sure (Y/[N])
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END1
echo ... Reinstalling libraries ...
if exist .\autobot\venv (
	rmdir .\autobot\venv /S /Q
)
python -m venv .\autobot\venv
.\autobot\venv\Scripts\pip --version
@echo ================ INSTALL PREFECT ==========================
.\autobot\venv\Scripts\pip install -U prefect
.\autobot\venv\Scripts\prefect version
@echo ================ INSTALL AUTOBOT ==========================
.\autobot\venv\Scripts\pip install -r .\autobot\requirements.txt
@echo ================ INSTALL JUPYTER NOTEBOOK =================
pip install jupyter
.\autobot\venv\Scripts\pip install ipykernel
for %%I in (.) do set CurrDirName=%%~nxI
rem echo %CurrDirName%
.\autobot\venv\Scripts\python -m ipykernel install --user --name=%CurrDirName%
rem @echo ================ INSTALL wkhtmltoimage =================
rem xcopy .\autobot\wkhtml*.* .\autobot\venv\scripts\.
rem SET PATH=%PATH%;%cd%\autobot
@echo ================ INSTALL MITO =================
SET /P AREYOUSURE=Install Mito sheets for use in Jupyter Notebook - Are you sure (Y/[N])
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END1
echo ... Installing Mito - may take some time ...
.\autobot\venv\Scripts\python -m pip install mitoinstaller
.\autobot\venv\Scripts\python -m mitoinstaller install
@echo ================ INSTALLATION COMPLETED ==========================
@echo To use Auto RPA - click runRPA.bat or from the command line with parameters
call runRPA -i 1
call runRPA -h
pause
:END1

goto :eof
:usage
@echo ================ OPTIMUS INSTALLATION ============================
@echo Install / upgrade optimus software with optimus_package*.zip files
@echo Usage: %0 ^<OptimusPackageFile^>
@echo ==================================================================
pause
exit /B 1

