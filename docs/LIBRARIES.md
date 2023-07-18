# Library of reusable function scripts
Resuable Excel script steps can be stored in a private (optimusLib.xlsm) or public (optimusLibPublic.xlsm) shared file that is accessible to all scripts in Optimus.

Loaded in sequence of 'optimus script', 'optimusLib.xlsm', 'optimusLibPublic.xlsm' - if the file exist in script folder.

optimusLibPublic.xlsm - exposed to public and downloadable from github.  User contributed content validated by publisher.  This file is published to Github and not ignored by .gitignore
```
Some reusable functions published in optimusLibPublic:
  - for the functions below - call them using dot notation e.g. shareX.screenrecord.start to start screen recording with shareX
  - function({json string}) syntax can be used to pass variables to functions e.g. chrome.password.change({"chrome.password.change.duration"="60"})
      - variables declared in Optimus Excel script with 'variables' Object.
        Templated or subtitued in Excel script using syntax {{variable name}} or <variable name>
        Declared in python script using variables dictionary.
        Modify or create in Excel script using 'set:variable name=value'

shareX - using shareX utility (separately download and installed, and operated using default hotkeys)
  - launch, screen record, screenshot 
win - general window automation
  - minimize.all, close, switch, undo, copy, paste, desktop.show.hide, maximize, minimize.alterative, minimize, restore
whatsapp - web automation
   - launch (using url), focuslaunch (using pywinauto keyboard)
chrome.password.change({"chrome.password.change.duration"="60"})
   - used to access chrome password manager of optimus/tagui's chrome browser automation session.  All passwords cached during automation run are stored and managed here.  You can use this to modify or update your passwords - only accessible locally on your optimus hosted computer, and requires your computer account sign in to access.

Various logon functions.  Called with example syntax - okta.logon.  Available for:
   - okta, qlik, servicenow
```
optimusLib.xlsm - private to installed optimus program.  Shared library of functions accessible by all script runs.  Can also store private library of constants, variables.

# New functions
This is a temporary place for sharing some new functions avaiable in optimus python library
```
keyboard_pwa:key string  - using pywinauto.  Does not require tagui RPA intialization.
keyboard:key string - using tagui RPA.  Needs Intitializing of RPA to work.

focus: application name     - focus and activate application for RPA.  Uses tagui RPA.

```
