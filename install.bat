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
SET /P AREYOUSURE=Reinstall python libraries - Are you sure (Y/[N])
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END1
echo ... Reinstalling libraries ...
if exist .\autobot\venv (
	rmdir .\autobot\venv /S /Q
)
PAUSE
rem python -m venv .\autobot\venv
rem https://stackoverflow.com/questions/1534210/use-different-python-version-with-virtualenv
rem where python
C:\Python310\python.exe -m venv .\autobot\venv
.\autobot\venv\Scripts\pip --version
PAUSE
@echo ================ INSTALL PREFECT ==========================
.\autobot\venv\Scripts\pip install -U prefect
@echo ================ INSTALL JUPYTER NOTEBOOK =================
pip install jupyter
.\autobot\venv\Scripts\pip install ipykernel
for %%I in (.) do set CurrDirName=%%~nxI
rem echo %CurrDirName%
.\autobot\venv\Scripts\python -m ipykernel install --user --name=%CurrDirName%
@echo ================ INSTALL AUTOBOT ==========================
.\autobot\venv\Scripts\pip install -r .\autobot\requirements.txt
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
@echo ================ LIBRARIES INSTALLED - INITIALIZE ==========================
rem @echo ================ INSTALL PREFECT ==========================
rem .\autobot\venv\Scripts\pip install -U prefect
.\autobot\venv\Scripts\prefect version
@echo ================ INSTALL PLAYWRIGHT =================
.\autobot\venv\Scripts\playwright install
@echo ================ INSTALL ROBOTFRAMEWORK BROWSER =================
rem Need to install NPM to complete the browser initizliation - https://kinsta.com/blog/how-to-install-node-js/
.\installation\node-v18.18.0-x64.msi
rem https://stackoverflow.com/questions/39764302/npm-throws-error-unable-to-get-issuer-cert-locally-while-installing-any-package
npm set strict-ssl=false
.\autobot\venv\Scripts\rfbrowser init --skip-browsers

goto :eof
:usage
@echo ================ OPTIMUS INSTALLATION ============================
@echo Install / upgrade optimus software with optimus_package*.zip files
@echo Usage: %0 ^<OptimusPackageFile^>
@echo ==================================================================
pause
exit /B 1

