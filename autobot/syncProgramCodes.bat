set destSync=D:\OneDrive-Sync\Christian Dior Couture\RPA Project - Report Automation
rem dir "%oneDriveReportPath%"\DClick
rem dir "%oneDriveReportPath%"\iCristal
rem dir .\Output\Images
rem syncs png files multithreaded and restartable
robocopy .\ "%destSync%"\AutoTagUI /XD Output __pycache__ Lib venv log /e /copy:DAT /mt /z