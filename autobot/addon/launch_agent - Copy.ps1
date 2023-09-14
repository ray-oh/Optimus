<#
    Script: launch if process is not running

    Script: clean up failed processes

    log process before and after run to process.txt in log folder
    https://stackoverflow.com/questions/5592531/how-can-i-pass-an-argument-to-a-powershell-script
    https://stackoverflow.com/questions/15120597/passing-multiple-values-to-a-single-powershell-script-parameter
    .\cleanProcesses.ps1 -msg '[TESTING 123]' -cleanName chrome, chrome Engine, Sikulix Engine

    .\launch_agent.ps1 -batchScript startAgent.bat, startJobMonitor.bat, startTelegramBot.bat -path D:\Optimus\autobot
#>

param(
    # launch following jobs
    #, "startJobMonitor.bat", "startTelegramBot.bat")
    [String[]] $batchScript = "startAgent.bat"
)


function numInstances([string]$process)
{
    @(Get-Process | Where-Object {$_.MainWindowTitle -Like $process}).Count
    #@(Get-Process $process -ErrorAction 0).Count
}

$count = numInstances("*startAgent.bat*")
#$count = [int]$count1
#echo count $count

if ($count -gt 0) {
    #echo "Process running" > prefectagent.log
    echo "$((Get-Date).ToString()) Process running" >> D:\Optimus\prefectagent.log
} else {
    #echo "launch"
    #$host.ui.RawUI.WindowTitle = 'startAgent'
    #Start-Process -FilePath "startAgent.bat" -WorkingDirectory "D:\Optimus-Prefect-Test1" -Wait -WindowStyle Minimized
    echo "$((Get-Date).ToString()) Launching process" >> D:\Optimus\prefectagent.log
    Start-Process -FilePath "cmd.exe" -WorkingDirectory "D:\Optimus" -ArgumentList "/c start /min  D:\Optimus\autobot\startAgent.bat ^& exit" -Wait -WindowStyle Minimized
    echo "$((Get-Date).ToString()) Close process" >> D:\Optimus\prefectagent.log
}

