#cd D:\DClick\
cd $PSScriptRoot\..              # e.g. D:\DClick\AddOn to D:\DClick
$pwd = (pwd).Path                # D:\DClick
$folder = $pwd.split("\")[-1]    # DClick or FoundationReport
$oneDrive = 'D:\OneDrive-Sync\Christian Dior Couture\RPA Project - Report Automation\'

$logFile = $oneDrive + $folder +'\ps_script_log.txt' # D:\Click\ps_script.log
#$logFile = '.\ps_script.log'
#'D:\OneDrive-Sync\Christian Dior Couture\APAC Management - Reports - Reports\log\DClick\process.txt'

Get-Date >> $logFile

"Path:" + $PSScriptRoot >> $logFile
"Script:" + $PSCommandPath  >> $logFile
"Log File:" + $logFile >> $logFile
"Current working dir:" + $pwd >> $logFile
"foldername:" + $folder >> $logFile

& $pwd\AddOn\to_Console.bat     # exit to console with virtual display
& $pwd\AddOn\1920-res.bat       # set display resolution to 1920

#return
#Start-Sleep -Seconds 60

& $pwd\Scripts\activate.ps1 >> $logFile
#python .\sendAlert.py ':china: iCristal Report start'

& python $pwd\GeneralAutomationScript.py >> $logFile

#python .\sendAlert.py ':china: iCristal Report end'

#.\runVBA_Email.ps1

#Write-Output 
"Completed" >> $logFile
