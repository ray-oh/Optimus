echo on
REM Copy to a tmp folder
rmdir tmp /S /Q
robocopy . .\tmp /XD __pycache__ Lib venv /XF install-optimus.bat /e /copy:DAT /mt /z

REM minify scripts
.\autobot\venv\Scripts\pyminify .\tmp\autobot\src\general_automation --in-place  --remove-literal-statements
.\autobot\venv\Scripts\pyminify .\tmp\prefect\src\workflow --in-place  --remove-literal-statements

REM Compile scripts to pyc
rmdir tmp\autobot\src\general_automation\__pycache__
rmdir tmp\prefect\src\workflow\__pycache__
.\autobot\venv\Scripts\python.exe -m compileall .\tmp\autobot\src\general_automation
.\autobot\venv\Scripts\python.exe -m compileall .\tmp\prefect\src\workflow

REM Rename pyc files
rem change directory
Pushd tmp\autobot\src\general_automation\__pycache__
ren *.pyc *.
ren *.cpython-310 *.pyc
rem ren tmp\autobot\src\general_automation\__pycache__\*.pyc tmp\autobot\src\general_automation\__pycache__\*.
rem ren tmp\autobot\src\general_automation\__pycache__\*.cpython-310 tmp\autobot\src\general_automation\__pycache__\*.pyc
popd

rem change directory
Pushd tmp\prefect\src\workflow\__pycache__
ren *.pyc *.
ren *.cpython-310 *.pyc
rem ren tmp\prefect\src\workflow\__pycache__\*.pyc tmp\prefect\src\workflow\__pycache__\*.
rem ren tmp\prefect\src\workflow\__pycache__\*.cpython-310 tmp\prefect\src\workflow\__pycache__\*.pyc
popd

REM Swap src and pyc files
move .\tmp\autobot\src\general_automation\__pycache__\*.pyc .\tmp\autobot\src\general_automation
move .\tmp\autobot\src\general_automation\*.py .\tmp\autobot\src\general_automation\__pycache__

move tmp\prefect\src\workflow\__pycache__\*.pyc .\tmp\prefect\src\workflow
move .\tmp\prefect\src\workflow\*.py .\tmp\prefect\src\workflow\__pycache__

rem .\autobot\venv\Scripts\python.exe -m compileall .\tmp\prefect\src\workflow

for /f "tokens=3,2,4 delims=/- " %%x in ("%date%") do set d=%%y%%x%%z
set data=%d%
Echo zipping...
rem "C:\Program Files\7-Zip\7z.exe" a -tzip ".\Test_Zipping_%d%.zip" ".\*"
"C:\Program Files\7-Zip\7z.exe" a -tzip ".\optimus_package_%d%_pyc.zip" ".\tmp\*" -mx0 -xr!install -x!tmp -x!src -xr!venv -xr!__pycache__ -xr!pyc -xr!bak -xr!old -xr!temp -xr0!optimus_package*.zip -xr0!optimus_package*.bat
rmdir tmp /S /Q
echo Done!
exit /b


