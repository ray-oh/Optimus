<#
    Script: call VBA_Email.xlsm to send email

    uses cleanProcesses.ps1 script to clean up processes

    windows shortcuts and environment variables
    # https://superuser.com/questions/217504/is-there-a-list-of-windows-special-directories-shortcuts-like-temp

    $command = “C:\Temp\Test2.ps1” –Computer L014 –User User1
    Invoke-Expression $command
#>

param(
    # working dir of script
    [String] $scriptDir = 'D:\DClick\AddOn', 

    # logFile name
    [String] $logFile = 'D:\DClick\log\process.txt'
)


function emailSend {
    param(
        # working dir of script
        [String] $scriptDir = 'D:\DClick\AddOn', 

        # logFile name
        [String] $logFile = 'D:\DClick\log\process.txt'
    )

    Write-Host "Email script"
    echo "************************ EMAIL PROCESSES ****************************** Date and time : $((Get-Date).ToString())"  >> $logFile

    #cd D:\DClick\AddOn
    #. .\cleanProcesses.ps1 # include functions content of script

    $currentDir = (Get-Item .).FullName  # get current script directory

    #cleanProcess -msg $msg -cleanName $cleanName -cleanWinTitle $cleanWinTitle -logFile $logFile -period $period
    #cleanProcess -msg ' VBA EMAIL JOB ' -cleanName EXCEL -cleanWinTitle NONE

    #.\cleanProcesses.ps1
    #."D:\DClick\cleanProcesses.ps1"
    #.".\cleanProcesses.ps1"   # clean up processes, log process to log\process.txt

    # start Excel
    $excel = New-Object -comobject Excel.Application
    #open file
    #$FilePath = 'D:\DClick\VBA_Email.xlsm'
    $FilePath = "$($scriptDir.ToString())\VBA_Email.xlsm"
    Write-Host $($FilePath.ToString())
    $workbook = $excel.Workbooks.Open($FilePath)
    ##If you will like to check what is happend
    $excel.Visible = $true
    #$excel.Visible = $false

    ## Here you can "click" the button
    $app = $excel.Application
    $app.Run("RunSendMail")
    #Start-Sleep -s 15

    $workbook.Close($true)  #wb.Close(SaveChanges=1) #ActiveWorkbook.Close SaveChanges:=True

    $excel.quit()

    echo "------------------------- Email Complete ----------------------- Date and time : $((Get-Date).ToString())"  >> $logFile

    Start-Sleep -s 3

    #.".\cleanProcesses.ps1"   # clean up processes, log process to log\process.txt
    # cleanProcess -msg ' POST VBA EMAIL '
}

emailSend -scriptDir $scriptDir -logFile $logFile 
