rmdir tmp /S /Q
powershell Expand-Archive -Path package_latest.zip -DestinationPath .\tmp
set destSync=.
robocopy .\tmp "%destSync%" /XD __pycache__ Lib venv /XF install.bat /e /copy:DAT /mt /z
rmdir tmp /S /Q
rmdir venv /S /Q
python -m venv venv
.\venv\Scripts\pip --version
.\venv\Scripts\pip install -r requirements.txt
@echo ================ INSTALLATION COMPLETED ==========================
@echo To use Auto RPA - click run.bat or from the command line with parameters
call run -h
pause