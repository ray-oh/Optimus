<#
    Script: launch if process is not running
    Usage : .\launch_agent.ps1 -batchScript startAgent.bat -path D:\Optimus\autobot

    Used to launch prefect agent, orion server, telegram bot and job monitor

    https://stackoverflow.com/questions/5592531/how-can-i-pass-an-argument-to-a-powershell-script
    https://stackoverflow.com/questions/15120597/passing-multiple-values-to-a-single-powershell-script-parameter
#>

param(
    # launch following jobs
    #, "startJobMonitor.bat", "startTelegramBot.bat")
    [String[]] $batchScript = "startAgent.bat",
    [String[]] $path = "D:\Optimus"
)


function numInstances([string]$process)
{
    @(Get-Process | Where-Object {$_.MainWindowTitle -Like "*$($process)*"}).Count
    #@(Get-Process $process -ErrorAction 0).Count
}


#cleanProcess -msg $msg -cleanName $cleanName -cleanWinTitle $cleanWinTitle -logFile $logFile -period $period

$count = numInstances($batchScript)
#$count = [int]$count1
#echo count $count
#echo "process ------" $batchScript
#Get-Process | Where-Object {$_.MainWindowTitle -Like "*startagent.bat*"} | Format-Table Id, Name, mainWindowtitle, Description, StartTime -AutoSize  


if ($count -gt 0) {
    #echo "Process running" > prefectagent.log
    echo "$((Get-Date).ToString()) Process running" >> $path\prefectagent.log
} else {
    #echo "launch"
    #$host.ui.RawUI.WindowTitle = 'startAgent'
    #Start-Process -FilePath "startAgent.bat" -WorkingDirectory "D:\Optimus-Prefect-Test1" -Wait -WindowStyle Minimized

    echo "$((Get-Date).ToString()) Launching process" >> $path\prefectagent.log
    Start-Process -FilePath "cmd.exe" -WorkingDirectory "$($path)" -ArgumentList "/c start /min  $($path)\autobot\$($batchScript) ^& exit" -WindowStyle Minimized

    #Start-Job -FilePath "cmd.exe" -WorkingDirectory "$($path)" -ArgumentList "/c start /min  $($path)\autobot\$($batchScript) ^& exit" -Wait -WindowStyle Minimized

    # Start-Job -WorkingDirectory "$($path)" | Start-Job -FilePath "cmd.exe" -ArgumentList "/c start /min  $($path)\autobot\$($batchScript) ^& exit" 
    #| -Wait -WindowStyle Minimized

    #echo "$((Get-Date).ToString()) Close process" >> D:\Optimus\prefectagent.log
}

