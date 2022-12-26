echo on
for /f "tokens=3,2,4 delims=/- " %%x in ("%date%") do set d=%%y%%x%%z
set data=%d%
Echo zipping...
rem "C:\Program Files\7-Zip\7z.exe" a -tzip ".\Test_Zipping_%d%.zip" ".\*"
"C:\Program Files\7-Zip\7z.exe" a -tzip ".\package%d%.zip" ".\" -mx0 -xr!install -xr!venv -xr0!*.xlsm
echo Done!