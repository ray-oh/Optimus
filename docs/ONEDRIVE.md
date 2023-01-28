# ONE DRIVE
OPTIMUS uses ONE DRIVE for storage and exchange of data or files that can be input for a automation process.  Or output or results of the automation process.
Typically in an enterprise context, this data for ONE DRIVE will be part of a Microsoft TEAMS site.  
Access to the data is controlled by TEAMS.  And the data is synced to the RPA VM via the ONE DRIVE client.  
  
ONE DRIVE folders synced to the desktop as seen in windows explorer. ONE DRIVE Enterprise and ONE DRIVE Personal folders are shown in the example.  
![Onedrive explorer](https://user-images.githubusercontent.com/115925194/213614115-c5c2850c-8161-4a2b-9b1c-0e697540b81e.png)

## TIPS
### Managing Storage Space
Typically, the storage on the VM is limited.  And when running an regular daiy automation script downloading data, significant storage space will be used up over time and requires housekeeping.  
Storage space on the local VM can be freed up by removing from the files on the local VM but keeping the backup on the ONE DRIVE cloud as follows:  
  
Open Settings from ONE DRIVE on the windows taskbar  
![image](https://user-images.githubusercontent.com/115925194/213614712-281201cb-441a-444d-babb-b72a278f5f9f.png)
  
Select *Choose Folders* to manage which folders to sync/view on local VM  
Select *Manage Storage* to view and manage storage of ONE DRIVE space  
![image](https://user-images.githubusercontent.com/115925194/213614969-1bab630a-3b1d-4970-b9fd-fb281d7d3d49.png)
  
From *Choose Folders* - select which folders to view on local VM.  
De-selecting the folder removes all local files stored on the VM but keeps the files on ONE DRIVE cloud.
![image](https://user-images.githubusercontent.com/115925194/213615093-0f2da478-e31c-4325-a370-7d6fd2ead968.png)
  
### References
[Add and Sync Shared Folders to OneDrive](https://support.microsoft.com/en-us/office/add-and-sync-shared-folders-to-onedrive-for-home-8a63cd47-1526-4cd8-bd09-ee3f9bfc1504)  
[Save disk space with OneDrive files on demand for windows](https://support.microsoft.com/en-us/office/save-disk-space-with-onedrive-files-on-demand-for-windows-0e6860d3-d9f3-4971-b321-7092438fb38e)
