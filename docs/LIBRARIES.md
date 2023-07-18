Library of reusable function scripts
Loaded in sequence of 'optimus script', 'optimusLib.xlsm', 'optimusLibPublic.xlsm' - if the file exist.
optimusLibPublic.xlsm - exposed to public and downloadable from github.  User contributed content validated by publisher.  This file is published to Github and not ignored by .gitignore
Some reusable functions:
shareX - using shareX utility (separately download and installed, and operated using default hotkeys)
  - launch, screen record, screenshot 
win - general window automation
  - minimize.all, close, switch, undo, copy, paste, desktop.show.hide, maximize, minimize.alterative, minimize, restore
whatsapp - web automation
   - launch (using url), focuslaunch (using pywinauto keyboard)
okta
   - logon

qlik
- logon

chrome.password.change({"chrome.password.change.duration"="60"})
servicenow
- logon
- 




optimusLib.xlsm - private to installed optimus program.  Shared library of functions accessible by all script runs.  Can also store private library of constants, variables.


function({json string})

New functions
keyboard_pwa:key string  - using pywinauto.  Does not require tagui RPA intialization.
keyboard:key string - using tagui RPA.  Needs Intitializing of RPA to work.

focus: application name     - focus and activate application for RPA.  Uses tagui RPA.


chrome password management


variables declared in Optimus Excel script with 'variables' Object.
Templated or subtitued in Excel script using syntax {{variable name}} or <variable name>
Declared in python script using variables dictionary.
Modify or create in Excel script using 'set:variable name=value'
