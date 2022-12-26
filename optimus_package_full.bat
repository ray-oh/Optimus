@echo off
for /f "skip=1" %%x in ('wmic os get localdatetime') do if not defined MyDate set MyDate=%%x
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set fmonth=00%Month%
set fday=00%Day%
set today=%Year%%fmonth:~-2%%fday:~-2%
rem echo %today%

rem echo on
REM Copy to a tmp folder
rmdir tmp /S /Q
robocopy . .\tmp /XD __pycache__ Lib venv .git deployment temp /XF install-optimus.bat /e /copy:DAT /mt /z

REM minify scripts
REM .\autobot\venv\Scripts\pyminify .\tmp\autobot\src\general_automation --in-place  --remove-literal-statements
REM .\autobot\venv\Scripts\pyminify .\tmp\prefect\src\workflow --in-place  --remove-literal-statements

rem for /f "tokens=3,2,4 delims=/- " %%x in ("%date%") do set d=%%y%%x%%z
rem set data=%d%
if exist .\optimus_package_%today%_mini.zip (
	rmdir .\optimus_package_%today%_mini.zip /S /Q
)
Echo zipping...
"C:\Program Files\7-Zip\7z.exe" a -tzip ".\optimus_package_%today%_full.zip" ".\tmp\*" -mx0 -xr!install -xr!.git -xr!deployment -x!tmp -x!src -xr!venv -xr!__pycache__ -xr!pyc -xr!bak -xr!old -xr!temp -xr0!optimus_package*.zip -xr0!optimus_package*.bat
rmdir tmp /S /Q
echo Done!
Pause
exit /b


