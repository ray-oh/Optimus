<#
    Script: clean up failed processes

    log process before and after run to process.txt in log folder
    https://stackoverflow.com/questions/5592531/how-can-i-pass-an-argument-to-a-powershell-script
    https://stackoverflow.com/questions/15120597/passing-multiple-values-to-a-single-powershell-script-parameter
    .\cleanProcesses.ps1 -msg '[TESTING 123]' -cleanName chrome, chrome Engine, Sikulix Engine
#>

param(
    #force stop processes with name or winTitle as follows
    [String[]] $cleanName = @("EXCEL", "phantomjs", "casperjs"), 
    [String[]] $cleanWinTitle = @("Chrome", "Sikulix"), 

    # logFile name
    #[String] $logFile = 'D:\DClick\log\process.txt',
    #[String] $logFile = $oneDrive + $folder + '\log\process.txt',
    [String] $logFile = 'process.txt',

    # msg to log
    [String] $msg = '',

    # period to check process e.g. in past -1 hr
    [Int] $period = -1
)


function cleanProcess {
    param(
        #force stop processes with name or winTitle as follows
        [String[]] $cleanName = @("EXCEL", "phantomjs", "casperjs"), 
        [String[]] $cleanWinTitle = @("Chrome", "Sikulix"), 

        # logFile name
        # [String] $logFile = 'D:\DClick\log\process.txt',
        # [String] $logFile = 'D:\OneDrive-Sync\Christian Dior Couture\APAC Management - Reports - Reports\log\DClick\process.txt',
        [String] $logFile = $oneDrive + $folder + '\log\process.txt',

        # msg to log
        [String] $msg = '',

        # period to check process e.g. in past -1 hr
        [Int] $period = -1
    )

    #cls
    Write-Host "Clean script"
    #Write-Host cleanName[1]
    echo "************************ CLEANING PROCESSES ***************$($msg)*************** Date and time : $((Get-Date).ToString())"  >> $logFile
    # Get all processes that have a main window title and display them in a table https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-process?view=powershell-7.1
    # Get-Process | Where-Object {$_.mainWindowTitle} | Format-Table Id, Name, mainWindowtitle, Description, SessionId -AutoSize
    #Get-Process | Sort-Object Id -Descending | Where-Object {$_.Description -NotLike "*Tanium*" -and $_.Description -NotLike "*Google*" -and $_.Description -NotLike "*Windows*" -and $_.Description -NotLike "*Microsoft*" -and $_.Description -NotLike "*Citrix*" -and $_.Name -NotLike "svchost" -and $_.Name -NotLike "Runtime*" -and $_.Name -NotLike "Search*" -and $_.Name -NotLike "Wmi*" -and $_.Name -NotLike "vm3*" -and $_.Name -NotLike "ZSA*" -and $_.Name -NotLike "Tanium*" -and $_.Name -NotLike "Sentinel*"} | Format-Table Id, Name, mainWindowtitle, Description, StartTime -AutoSize
    #Get-Process | Sort-Object Id -Descending | Where-Object {$_.StartTime -gt [datetime]::Now.AddHours(-2) -and $_.Description -NotLike "*Tanium*" -and $_.Description -NotLike "*Windows*" -and $_.Description -NotLike "*Microsoft*" -and $_.Description -NotLike "*Citrix*" -and $_.Name -NotLike "svchost" -and $_.Name -NotLike "Runtime*" -and $_.Name -NotLike "Search*" -and $_.Name -NotLike "Wmi*" -and $_.Name -NotLike "vm3*" -and $_.Name -NotLike "ZSA*" -and $_.Name -NotLike "Tanium*" -and $_.Name -NotLike "Sentinel*"} | Format-Table Id, Name, mainWindowtitle, Description, StartTime -AutoSize
    Get-Process | Sort-Object Name -Descending | Where-Object {$_.StartTime -gt [datetime]::Now.AddHours($period) `
    -and $_.Name -NotLike "rdp*" -and $_.Name -NotLike "WUDFHost*" -and $_.Name -NotLike "smartscreen*" -and $_.Name -NotLike "dllhost*" -and $_.Name -NotLike "cscript*" `
    -and $_.Name -notLike "TabTip*" -and $_.Name -notLike "Search*" -and $_.Name -notLike "Wmi*"  -and $_.Name -notLike "pacjsworker" -and `
    $_.Name -notLike "svchost" -and $_.Description -notLike "*Tanium*"} `
    | Format-Table Id, Name, mainWindowtitle, Description, StartTime -AutoSize >> $logFile

    foreach ($cleanItem in $cleanName)
    {
        #Get-Process *Citrix* | Stop-Process -force
        Get-Process | Where-Object {$_.Name -Like $($cleanItem) } | Stop-Process -force

    }

    foreach ($cleanItem in $cleanWinTitle)
    {
        #Get-Process *Citrix* | Stop-Process -force
        #Get-Process | Where-Object {$_.mainWindowTitle} | Where-Object {$_.mainWindowTitle -Like "Chrome Engine" } | Stop-Process -force
        Get-Process | Where-Object {$_.mainWindowTitle} | Where-Object {$_.mainWindowTitle -Like $($cleanItem) } | Stop-Process -force
    }

    Start-Sleep -s 2

    #Get-Process | Sort-Object Id -Descending | Where-Object {$_.Description -NotLike "*Tanium*" -and $_.Description -NotLike "*Google*" -and $_.Description -NotLike "*Windows*" -and $_.Description -NotLike "*Microsoft*" -and $_.Description -NotLike "*Citrix*" -and $_.Name -NotLike "svchost" -and $_.Name -NotLike "Runtime*" -and $_.Name -NotLike "Search*" -and $_.Name -NotLike "Wmi*" -and $_.Name -NotLike "vm3*" -and $_.Name -NotLike "ZSA*" -and $_.Name -NotLike "Tanium*" -and $_.Name -NotLike "Sentinel*"} | Format-Table Id, Name, mainWindowtitle, Description, StartTime -AutoSize >> .\process.txt
    Get-Process | Sort-Object Name -Descending | Where-Object {$_.StartTime -gt [datetime]::Now.AddHours($period) `
    -and $_.Name -NotLike "rdp*" -and $_.Name -NotLike "WUDFHost*" -and $_.Name -NotLike "smartscreen*" -and $_.Name -NotLike "dllhost*" -and $_.Name -NotLike "cscript*" `
    -and $_.Name -notLike "TabTip*" -and $_.Name -notLike "Search*" -and $_.Name -notLike "Wmi*"  -and $_.Name -notLike "pacjsworker" -and `
    $_.Name -notLike "svchost" -and $_.Description -notLike "*Tanium*"} `
    | Format-Table Id, Name, mainWindowtitle, Description, StartTime -AutoSize >> $logFile

    echo "Active Windows: $((Get-Process | Where-Object {$_.mainWindowTitle}).Count)" >> $logFile
    Get-Process | Where-Object {$_.mainWindowTitle} >> $logFile

    echo "------------------------- complete clean ----------------------- Date and time : $((Get-Date).ToString())"  >> $logFile
    #(Get-Item .).FullName
    # Get-ChildItem -Path Env:
    # Get-ChildItem -Path Env:\OneDriveCommercial
}

cd $PSScriptRoot\..              # e.g. D:\DClick\AddOn to D:\DClick
$pwd = (pwd).Path                # D:\DClick
$folder = $pwd.split("\")[-1]    # DClick or FoundationReport
$oneDrive = 'D:\OneDrive-Sync\Christian Dior Couture\RPA Project - Report Automation\'

cleanProcess -msg $msg -cleanName $cleanName -cleanWinTitle $cleanWinTitle -logFile $logFile -period $period
