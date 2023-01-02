# OPTIMUS
RPA solution with Excel front end for creating flows.  
Designed with the typical data analyst who is not technical savy but comfortable using Excel in mind.  
The solution makes it really easy for beginners to develop your own flows, especially with templates.  
Users can easily share and reuse modular Excel based scripts to speed up flow creation or create sophisticated automation flows.

## Optimus RPA Package
- Optimus RPA solution is built from 2 core solutions
  - TagUI is the core RPA engine
  - Prefect is the orchestration / workflow engine  
  
Much easier to learn and develop than UiPath.  But without compromising on the power of a full RPA solution.  
OPTIMUS leverages the full power of python with its flexible and extensible architecture
- Incoporates other python libraries including pandas and jupyter notebooks support for data analysis and processing.
- Enterprise level security by design with TagUI's decentralized architecture.  No sensitive user data is stored in the cloud.
- Refer to DOCUMENTATION below for further information.

### INSTALLATION
- 2 methods to install and use optimus RPA
  1. Git clone this repo
     - run install-optimus.bat to setup required libraries
  2. Install from zipped package file
    - Requires: install-optimus.bat and a optimus_package*.zip file.
    - optimus_package is in continuous release and new releases are versioned in YYYYMMDD format.
      It is advisable you use the latest version available.  Check the release notes on what is included in the version.
    - Each new release can also be installed over a previous release as an upgrade.  
      Normally, an upgrade installation will not remove existing user files.  But it may overwrite existing scripts files with same name.
      Backup your scripts folder to avoid problems.
    - Downloadable from: [RPA Project Team Site](https://christiandior.sharepoint.com/:f:/s/Grp_RPAProject-KBQuest/ErGLyzBc3QtKj9WzjxDuik0BsuRiyPJB3DHKq-X091PuOg?e=fmxPRt)

### USAGE
- Use runRPA.bat to launch RPA program.  Requires to specify an Excel script file.
- Example with Excel script file sample.xlsm :   >> runRPA -f sample  
- Sample script files "sample" available to test various RPA functionality
- All excel script files are to be placed in \scripts
    And they can include RPA images (for Visual automation of your desktop and websites)

- To launch the Prefect workflow engine, run startOrion.bat to launch the orion workflow server in background.
  - And open the [Prefect dashboard](http://127.0.0.1:4200) in your browser

### DOCUMENTATION
- Documentation available in: \autobot\docs
- Optimus is based on TagUI for RPA automation.  Almost all of TagUI's features are ported and available in Optimus. And some have also been enhanced.
  - A good reference for the key RPA features available in Optimus is available from the TagUI official sites, in particular:
    - [Official TagUI site](https://aisingapore.org/tagui/)
    - And [the python version of TagUI](https://github.com/tebelorg/RPA-Python)
    - [Review of top 5 opensource RPA solutions including TagUI](https://techbeacon.com/enterprise-it/top-5-open-source-rpa-frameworks-how-choose)
    - TagUI by design does not deploy or save any user data on the cloud.  Passwords or credentials are not saved in the scripts, but cached in the browser or secret files on the user's local computer.
- Optimus also utilizes many other python packages for including:
  - [Jupyter](https://pypi.org/project/jupyter/): Native support for Jupyter Notebooks
    - [Installing Jupyter Notebook](https://docs.jupyter.org/en/latest/install/notebook-classic.html)
    - [Setup Jupyter to use installed virtual env](https://janakiev.com/blog/jupyter-virtual-envs/)
      - pip install ipykernel (included in installation libraries)
      - python -m ipykernel --name=myenv (Run this command in venv. Replace myenv with any name for kernel in Jupyter.)
      - jupyter kernelspec uninstall myenv (to remove the virtual env)
    - [Papermill](https://netflixtechblog.com/scheduling-notebooks-348e6c14cfd6): Parameterization and automation of Jupyter Notebooks
    - [scrapbook](https://github.com/nteract/scrapbook): Persist and recall data and visual content in Jupyter notebook
      - [Building jupyter notebook workflows with scrapbook](https://www.wrighters.io/building-jupyter-notebook-workflows-with-scrapbook/)
  - [Prefect](https://www.prefect.io/opensource/): Orchestration workflow engine
    - Prefect is chosen over other orhestration tools as the workflow engine.  [Comparison of Prefect vs Airbnb's Airflow and Spotify's Luigi](https://medium.datadriveninvestor.com/the-best-automation-workflow-management-tool-airbnb-airflow-vs-spotify-luigi-5f4c9832e9fd)
  - [PyPDF4](https://pypi.org/project/PyPDF4/): for PDF merging, splitting, cropping, encryption
  - [Pandas](https://pypi.org/project/pandas/): for data analysis
    - [Matplotlib](https://pypi.org/project/matplotlib/): comprehensive library for creating static, animated, and interactive visualizations in Python
  - [Pillow](https://pypi.org/project/Pillow/): for image processing
  - [dataframe-image](https://pypi.org/project/dataframe-image/): to export dataframe output as image files
  - [xlwings](https://www.xlwings.org/): for Excel automation 
  - it also leverages common windows COM components for Outlook integration, OneDrive Sync Client for OneDrive / Sharepoint / Teams integration.
  - OPTIMUS currently does not have a cloud enabled service option.  But it is possible deploy OPTIMUS on a cloud virtual machine to run the automation in unattended mode.
    - It is also possible to federate an automation task across multiple deployments of OPTIMUS using OneDrive Sync Client or a shared network drive (if running within an enterprise network) to share data, status, and scripts.
    - The current release of OPTIMUS does not provide this capability out of the box and requires some setup to achieve the federation.  Future releases may make this easier by leveraging the cloud enabled capabilities of Prefect workflow.


### PROGRAM TECHNICAL INFORMATION
- Pre-requisites:
- Windows 10 and Windows 10 Enterprise Server on VM
- Python 3.9 and above.  Recommend to install with Anaconda package which will also install Jupyter Notebook.
- Autobot (RPA component) - based on TagUI and various addon python packages
- Prefect (workflow orchestration) - full fledged orchestration package for dataflow automation
    https://www.prefect.io/ - official site
    Currently in pre-Alpha stage for integration with Autobot.

### RELEASE NOTES:

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

### CONTACT
Raymond Oh - for reporting of bugs, questions, requests etc

## CLONING REPO, CONTRIBUTION AND LICENSE

### Clone git repository

```sh
    $ git clone "https://github.com/ray-oh/tutorialGitHub"
```

You can run and edit the content or contribute to them using [Gitpod.io](https://www.gitpod.io/), a free online development environment, with a single click.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](http://gitpod.io/#https://github.com/ray-oh/tutorialGitHub)

### Contributing New Content
	
* Make your pull requests to be **specific** and **focused**. Instead of contributing "several content" all at once contribute them all one by one separately (i.e. one pull request for "VS Code new link", another one for "Jupyter Notebook link" and so on).

* Every new content must have:
	* **Source link** with comments and readable namings
	* **Background** being explained in README.md along with the content
	
If you're adding new **files** they need to be saved in the `/data` folder. The size of the file should not be greater than `30Mb`.

### Contributing

Before removing any bug, or adding new contributions please do the following: **[Check Contribution Guidelines Before Contribution](Contributing.md)** and also please read **[CODE OF CONDUCT](CODE_OF_CONDUCT.md)**.

### License

Licensed under the [BSD 3-Clause License](LICENSE) 


## Ideas scrap book
Python web scraping - processing CAPTCHA
https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_processing_captcha.htm


### To dos:
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
