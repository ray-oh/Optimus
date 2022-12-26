<#
    Script: sync 2 directories

    https://serverfault.com/questions/129098/how-to-get-robocopy-running-in-powershell
#>

param(
    # source and destination folders
    [String] $source = $pwd + '\Output\Images',   #'D:\DClick\Output\Images',
    [String] $dest = 'D:\OneDrive-Sync\Christian Dior Couture\APAC Management - Reports - Reports',
    [String] $files = '*.png'
)


function syncFolders {
    param(
        # source and destination folders
        [String] $source = $pwd + '\Output\Images', #'D:\DClick\Output\Images',
        [String] $dest = 'D:\OneDrive-Sync\Christian Dior Couture\APAC Management - Reports - Reports',
        [String] $files = '*.png'
    )

    #robocopy $source $dest /COPYALL /B /SEC /MIR /R:0 /W:0 /NFL /NDL
    #robocopy D:\DClick\Output\Images "%oneDriveReportPath%"\DClick\Images *.png /mt /z
    robocopy $source $dest $files /mt /z

    Start-Sleep -s 2

}

cd $PSScriptRoot\..              # e.g. D:\DClick\AddOn to D:\DClick
$pwd = (pwd).Path                # D:\DClick
$folder = $pwd.split("\")[-1]    # DClick or FoundationReport
$oneDrive = 'D:\OneDrive-Sync\Christian Dior Couture\RPA Project - Report Automation\'

syncFolders -source $source -dest $dest -files $files

