# Library of reusable function scripts
Resuable Excel script steps can be stored in a private (optimusLib.xlsm) or public (optimusLibPublic.xlsm) shared file that is accessible to all scripts in Optimus.

Loaded in sequence of 'optimus script', 'optimusLib.xlsm', 'optimusLibPublic.xlsm' - if the file exist in script folder.

***optimusLibPublic.xlsm*** - exposed to public and downloadable from github.  User contributed content validated by publisher.  This file is published to Github and not ignored by .gitignore

> Some reusable functions published in optimusLibPublic:
>  - for the functions below - call them using dot notation e.g. shareX.screenrecord.start to start screen recording with shareX
>  - function({json string}) syntax can be used to pass variables to functions e.g. chrome.password.change({"chrome.password.change.duration"="60"})
>      - variables declared in Optimus Excel script with 'variables' Object.
>      - Templated or subtitued in Excel script using syntax `{{variable name}}` or `<variable name>`
>      - Declared in python script using variables dictionary.
>      - Modify or create in Excel script using `set:variable name=value`

> shareX - using shareX utility (separately download and installed, and operated using default hotkeys)
>  - launch, screen record, screenshot 
> win - general window automation
>  - leveraging keyboard shortcuts: [keyboard shortcuts](https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec)
>  - minimize.all, close, switch, undo, copy, paste, desktop.show.hide, maximize, minimize.alterative, minimize, restore

> chrome - browser automation using keyboard shortcuts
>   - zoom.in, zoom.out, zoom.reset, addressbar, window.new, tab.new, tab.switch.up, tab.switch.down, tab.switch, tab.search, reload
>   - https://support.google.com/chrome/answer/157179

> chrome.password.change({"chrome.password.change.duration"="60"})
>   - used to access chrome password manager of optimus/tagui's chrome browser automation session.  All passwords cached during automation run are stored and managed here.  You can use this to modify or update your passwords - only accessible locally on your optimus hosted computer, and requires your computer account sign in to access.

> whatsapp - web automation
>   - keyboard shortcuts https://www.xda-developers.com/whatsapp-keyboard-shortcuts/
>   - launch (using url), focuslaunch (using pywinauto keyboard)

> teams - microsoft teams web automation
>   - using keyboard shortcuts:
>       - [13 best keyboard shortcuts for teams](https://helpdeskgeek.com/office-tips/the-13-best-keyboard-shortcuts-for-microsoft-teams/)
>       - [keyboard shortcuts for teams](https://support.microsoft.com/en-gb/office/keyboard-shortcuts-for-microsoft-teams-2e8e2a70-e8d8-4a19-949b-4c36dd5292d2#bkmk_global)
>   - launch

> Various logon functions.  Called with example syntax - okta.logon.  Available for:
>   - okta, qlik, servicenow

> Most of the above steps leverage pywinauto.keyboard function:
>   - [pywinauto keyboard reference](https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html)
>   - [Get urls of opened tabs in browser with pywinauto](https://stackoverflow.com/questions/72594066/get-urls-of-opened-tabs-in-browser-pywinauto-python)

***optimusLib.xlsm*** - private to installed optimus program.  Shared library of functions accessible by all script runs.  Can also store private library of constants, variables.

# New functions
This is a temporary place for sharing some new functions avaiable in optimus python library
```
keyboard_pwa:key string  - using pywinauto.  Does not require tagui RPA intialization.
keyboard:key string - using tagui RPA.  Needs Intitializing of RPA to work.

focus: application name     - focus and activate application for RPA.  Uses tagui RPA.

```

https://robocorp.com/docs/development-guide/robot-framework/how-to-use-custom-python-libraries-in-your-robots




