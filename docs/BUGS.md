# KNOWN BUGS OR ISSUES

This is a list to track some known bugs and current resolution.

- [Aw, Snap! error on Chrome](https://github.com/aisingapore/TagUI/issues/1116)
  - Intermittent error on Chrome.  Chrome browser is not closed cleanly by Optimus/TagUI.
  - Issue does not impact the automation as the next automation launch will kill the open browser window and relauch a new RPA browser.
  - ![Bug screenshot](https://user-images.githubusercontent.com/115925194/210700087-664ecd86-48db-4cf4-a08c-7c33f039dd78.png)
  - Temporary fix in latest version.  Any open Chrome browser sessions will be terminated if not closed after the completion of the RPA flow run

- [refreshenv - to refresh the path environment if program fails with message of file not found](https://thecategorizer.com/windows/how-to-refresh-environment-variables-in-windows/)
  - Optimus will call some powershell commands.  Or some of the libraries will use the "where" system command to locate path of a program.  And this sometimes fails if the path variable is not working correctly.  Call this command could resolve the problem.
  - if path variable is corrupted, refreshenv, echo %path%, copy result and reapply it in the windows to [recover the path variable](https://stackoverflow.com/questions/32015759/how-to-recover-deleted-environment-variables)



