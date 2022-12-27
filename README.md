# optimus
RPA solution with Excel front end


Optimus RPA Package

INSTALLATION
git clone from this repo
install-bat to setup the libraries
runrpa to use




- Requires: install-optimus.bat and a optimus_package*.zip file.
- optimus_package is in continuous release and new releases are versioned in YYYYMMDD format.
  It is advisable you use the latest version available.  Check the release notes on what is included in the version.
- Each new release can also be installed over a previous release as an upgrade.  
  Normally, an upgrade installation will not remove existing user files.  But it may overwrite existing scripts files with same name.
  Backup your scripts folder to avoid problems.
- Downloadable from: RPA Project Team Site: 
    https://christiandior.sharepoint.com/:f:/s/Grp_RPAProject-KBQuest/ErGLyzBc3QtKj9WzjxDuik0BsuRiyPJB3DHKq-X091PuOg?e=fmxPRt

USAGE
- Use runRPA.bat to launch RPA program.  Requires to specify an Excel script file.
- Example:   >> runRPA -f main-test  
- Sample script files "main-test" available to test various RPA functionality
- All excel script files are to be placed in \scripts
    And they can include RPA images (for Visual automation of your desktop and websites)

DOCUMENTATION
- Documentation available in: \autobot\docs
- Optimus is based on TagUI for RPA automation.  Almost all of TagUI's features are ported and available in Optimus.
    And some have also been enhanced.
    A good reference for the key RPA features available in Optimus is available from the TagUI official sites, in particular: 
    https://aisingapore.org/tagui/ - official TagUI site.
    And https://github.com/tebelorg/RPA-Python - the python version of TagUI

PROGRAM TECHNICAL INFORMATION
- Pre-requisites:
- Windows 10 and Windows 10 Enterprise Server on VM
- Python 3.9 and above
- Autobot (RPA component) - based on TagUI and various addon python packages
- Prefect (workflow orchestration) - full fledged orchestration package for dataflow automation
    https://www.prefect.io/ - official site
    Currently in pre-Alpha stage for integration with Autobot.

RELEASE NOTES:

20220710 - Optimus 1.1
        Stable release
        Package and installation scripts
        Separate autobot and prefect installation folders
        Separate scripts folder

20221006 - Stable release
        New features:
        Installation scripts and package updates.
        scripts (user files) folders separated from Autobot program folder.

20221018 - Updated installation scripts
        Added python-minifier  https://pypi.org/project/python-minifier/
        https://dflook.github.io/python-minifier/installation.html

CONTACT
Raymond Oh - for reporting of bugs, questions, requests etc

Ideas scrap book
Python web scraping - processing CAPTCHA
https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_processing_captcha.htm


To dos:
Prefect workflow
Arbitrary parameters not allowed in flows with `validate_parameters=False` #5663
https://bytemeta.vip/repo/PrefectHQ/prefect/issues/5663
python exception Dict key must be str
https://docs.prefect.io/api-ref/prefect/flows/#prefect.flows.Flow.validate_parameters

prefect localfilesystem block
Unable to find block document named for block type LocalFileSystem
https://docs.prefect.io/tutorials/storage/
Upgrade to Prefect 2.0: Running flows with Local Agent and Storage
https://www.youtube.com/watch?v=T53JRD1LA68&list=PLZfWmQS5hVzF3u9FY4-43U4UoTblFgC2l&index=17

prefect __prefect_loader__
https://www.geeksforgeeks.org/how-to-import-a-python-module-given-the-full-path/
https://stackoverflow.com/questions/56687346/python-importing-from-same-module-importerror-cannot-import-name-blah-na
Inheritance allows us to define a class that inherits all the methods and properties from another class.
https://www.w3schools.com/python/python_inheritance.asp
python multiple interitence class
https://www.pythonmorsels.com/inheriting-one-class-another/

https://stackoverflow.com/questions/1210664/no-module-named-sqlite3
https://github.com/PrefectHQ/prefect/issues/5970
https://community.chocolatey.org/packages?q=tag%3Asqlite&moderatorQueue=&moderationStatus=all-statuses&prerelease=false&sortOrder=package-download-count
https://docs.chocolatey.org/en-us/choco/setup#install-with-cmd.exe
https://stackoverflow.com/questions/41309722/error-no-such-function-json-each-in-sqlite-with-json1-installed

https://www.thecodeship.com/patterns/guide-to-python-function-decorators/


Obsufication
https://askubuntu.com/questions/153823/how-to-run-a-pyc-compiled-python-file
Python-minifier
https://medium.com/geekculture/python-source-code-obfuscation-6b97f88a460d
https://stackabuse.com/differences-between-pyc-pyd-and-pyo-python-files/

Command Line Application and Python Package to Add/Append/Remove environment variables on Windows systems
Current package allows to precisely control and differentiate user and system variables
https://github.com/beliaev-maksim/py_setenv#how-to-use-as-python-package


Batch Script - return code
https://www.tutorialspoint.com/batch_script/batch_script_return_code.htm

Resize display resolution using python with cross platform support
https://stackoverflow.com/questions/20838201/resize-display-resolution-using-python-with-cross-platform-support


How to install Python package from GitHub? [duplicate]
https://stackoverflow.com/questions/15268953/how-to-install-python-package-from-github
pip install git+https://github.com/jkbr/httpie.git#egg=httpie



Airflow, Prefect, and Dagster: An Inside Look
https://towardsdatascience.com/airflow-prefect-and-dagster-an-inside-look-6074781c9b77
prefect vs airflow vs argo
Running Workflows on Docker, Kubernetes or Locally with Prefect
https://www.youtube.com/watch?v=-eZlKa7ggvo&list=PLZfWmQS5hVzFmPh4hVj9ijtl-jRhsWD6E&index=23


Structuring python project
https://docs.python-guide.org/writing/structure/
structure python resuable libraries
https://towardsdatascience.com/learn-python-modules-and-packages-in-5-minutes-bbdfbf16484e

https://towardsdatascience.com/how-to-build-and-distribute-a-python-package-using-venv-and-pypi-d17dade7f8c2

Match case statement
https://learnpython.com/blog/python-match-case-statement/


python call virtual environment from script
Installing python 3 on windows
https://python-docs.readthedocs.io/en/latest/starting/install3/win.html
Manage multiple Python versions on Windows with py.exe
https://changhsinlee.com/windows-py-launcher/
python setup.py requirements.txt

https://realpython.com/python-virtual-environments-a-primer/


How to Throw Exceptions in Python
https://rollbar.com/blog/throwing-exceptions-in-python/


How To Compare Contents Of Two Files In Visual Studio Code?
https://www.mytecbits.com/microsoft/dot-net/compare-contents-of-two-files-in-vs-code


The 6 Best Python GUI Frameworks for Developers
https://medium.com/teamresellerclub/the-6-best-python-gui-frameworks-for-developers-7a3f1a41ac73



Incremental data load using pandas
https://stackoverflow.com/questions/45247500/incremental-data-load-using-pandas

python whatsapp
whatsapp to myself
Automate WhatsApp Messages With Python using Pywhatkit module
https://www.geeksforgeeks.org/automate-whatsapp-messages-with-python-using-pywhatkit-module/



AutoHotkey Beginner Tutorial
https://www.autohotkey.com/docs/Tutorial.htm#s3
Send, SendRaw, SendInput, SendPlay, SendEvent
https://www.autohotkey.com/docs/commands/Send.htm



https://info.nrao.edu/computing/guide/file-access-and-archiving/7zip/7z-7za-command-line-guide
https://superuser.com/questions/97342/7zip-command-line-exclude-folders-by-wildcard-pattern

python on multiple lines
https://developer.rhino3d.com/guides/rhinopython/python-statements/#:~:text=You%20cannot%20split%20a%20statement%20into%20multiple%20lines%20in%20Python,continued%20on%20the%20next%20line.


Exit codes in python
https://stackoverflow.com/questions/285289/exit-codes-in-python


configparser vs decouple
https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file

python os environ not permanent
https://pybit.es/articles/how-to-handle-environment-variables-in-python/
https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5
https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5
https://stackoverflow.com/questions/3575165/what-is-the-correct-way-to-unset-a-linux-environment-variable-in-python

How To: Run multiple Python scripts from a single primary script
https://support.esri.com/en/technical-article/000010647

https://stackoverflow.com/questions/3827567/how-to-get-the-path-of-the-batch-script-in-windows
