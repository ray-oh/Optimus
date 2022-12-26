<#
    Script: launch if process is not running
#>

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
    Start-Process -FilePath "cmd.exe" -WorkingDirectory "D:\Optimus" -ArgumentList "/c start /min  D:\Optimus\startAgent.bat ^& exit" -Wait -WindowStyle Minimized
    echo "$((Get-Date).ToString()) Close process" >> D:\Optimus\prefectagent.log
}

