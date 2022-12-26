set oneDriveReportPath=D:\OneDrive-Sync\Christian Dior Couture\APAC Management - Reports - Reports
dir "%oneDriveReportPath%"\DClick\Images
dir "%oneDriveReportPath%"\iCristal
dir .\Output\Images
rem syncs png files multithreaded and restartable
robocopy D:\DClick\Output\Images "%oneDriveReportPath%"\DClick\Images *.png /mt /z