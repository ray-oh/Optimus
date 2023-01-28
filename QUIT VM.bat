:: =========================================================================================
:: When using Remote Desktop to connect to a remote computer, closing Remote Desktop locks out the computer and displays the login screen. 
:: In the locked mode, the computer does not have GUI, so any currently running or scheduled GUI automation will fail.
:: To avoid problems with GUI automation, run this batch file to use the tscon utility to disconnect from Remote Desktop. 
:: tscon returns the control to the original local session on the remote computer, bypassing the logon screen. All programs on the remote computer continue running normally, including GUI automation.
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do (
  %windir%\System32\tscon.exe %%s /dest:console
)