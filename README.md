# OPTIMUS
RPA solution with **Excel front end** for creating flows.  
Designed with the typical data analyst who is not technical savy but comfortable using Excel in mind.  
The solution makes it really **easy for beginners** to develop your own flows, especially with templates.  
Users can easily share and reuse modular Excel based scripts to speed up flow creation or create sophisticated automation flows.  

![logo](https://user-images.githubusercontent.com/115925194/210501100-910d4f94-10cd-428a-980a-c2984a7ed739.png)   
[Demo of a basic script in Optimus](https://youtu.be/AqnQwkjb1n0)  
![Sample Optimus script](https://user-images.githubusercontent.com/115925194/210494451-2b3fc373-04a0-4a5e-860e-73921fd89340.png)

## COMPARISON WITH OTHER RPA SOLUTIONS
OPTIMUS differentiates itself from other RPA solutions including market leading commercial packages like UiPath in terms of its ease of use and extensibility.  
But at the sametime, it does not compromise on features and capabilities.

At the core of OPTIMUS is the TagUI RPA engine.
> ***TagUI*** is a multilayered and sophisticated tool with a rich scripting language that supports complete complex RPA instructions. The richness of TagUI's scripting language is a reason why its one of the top opensource RPA solutions at the moment for mid-level or advanced teams implementing RPA. Here is a review from Matthew David (Digital Leader at Accenture) on [comparison of TagUI with other top 5 opensource RPA solutions](https://techbeacon.com/enterprise-it/top-5-open-source-rpa-frameworks-how-choose)  

> ***OPTIMUS*** enhances TagUI's ease of use with an Excel front end for creation of automation flows.  No special development tools are required - just basic Excel and keywords to define various automation steps.  
The solution is also built with ***Enterprise Level Security*** by design due to the decentralized architecture of TagUI.  User has full control on how his/her data is stored and managed.

The second core component of OPTIMUS is the PREFECT workflow engine
> ***PREFECT*** is a *second-generation* open source orchestration platform that has been developed specifically with dataflow automation in mind.  It provides OPTIMUS with powerful and scalable capabilities for workflow orchestration, management and monitoring.

And finally, as OPTIMUS is developed in Python - *the language for data analytics* - you have easy access to the rich set of libraries that Python has to offer
> ***Flexible and extensible architecture***. An example is the built in support for Jupyter Notebooks.  - Jupyter notebooks can be easily called and run from OPTIMUS with different parameters.  And can extend OPTIMUS capability through installation of additional python libraries for machine learning or data analysis.  
And by design, OPTIMUS Excel front end is designed to easily allow modularisation and reuse of your automation flows.  Allowing creation of sophisticated and powerful automation flows.  

***Typical data analytics and automation use case***
![Typical data use case](https://user-images.githubusercontent.com/115925194/210479085-36019993-4048-47a5-a5ee-9baf6d3bffe9.png)


Some example use cases implemented with OPTIMUS in enterprise setting:
> - ***Generate email reports*** out of a legacy reporting solution.  The legacy system did not support email out of the box and also did not support scheduled download of data. Optimus was used to automate of data from the system in Excel, and further processing data and formatting the report before sending as an email to users.
> - ***Automate and extend functionality of legacy Excel macro files***.  These files were originally designed for manual run and had plenty of business logic embedded.  The original business developer for the macro has left, and it was risky and would take time to rewrite the entire solution on another platform.  As volume increased, the Excel would take many hours to run on the users laptop. Optimus was used to automate the refresh of the Excel macro with minimal modification to the original macro apart from exposing some key parameter fields.  Entire automation was deployed to a VM on the cloud.  And results from the macro were further transformed for downstream analysis.
> - ***Extract incident and support request data from serviceNow***.  Optimus was used to combine the different datasets into a harmonized data set for monitoring both incident and request trends. The transformed dataset is passed to PowerBI for interactive visualization by users.
> - Automate the monitoring of a website for downtime and failure.  Setting thresholds to trigger alert via email or telegram messaging.
> - Periodically checking a competitor website for pricing updates, and extracting the data to Excel for further analysis.

Refer to the DOCUMENTATION section below for further technical information on the solution.  

### INSTALLATION
2 methods to install and use optimus RPA:
1. Git clone this repo
    - From this Github page (https://github.com/ray-oh/Optimus.git) - click *Code* and *Download ZIP*  
      ![download the zipped package](https://user-images.githubusercontent.com/115925194/212074132-7e504cc0-d24c-4262-b9cf-e5734f7c827e.png)
    - Create a folder for your Optimus program.  And extract the content to the folder  
      ![image](https://user-images.githubusercontent.com/115925194/212080421-f3b20b76-4f13-4dce-9950-6f6946b7d808.png)
    - Multiple copies of Optimus program can be installed one a computer.  Typically, you could have one instance for PRODUCTION and another instance for TESTING / QUALITY ASSURANCE.  For the PRODUCTION instance, it is recommended to use the name `Optimus` for the program directory.  And for testing, you could give a name like `Optimus_QA`.  If you were setting the TEST/QA environment, it should look like the following with the zipped file content extracted:    
      ![image](https://user-images.githubusercontent.com/115925194/212081617-9c9cb96f-8fd2-43c3-8c9a-b2133d78ed02.png)
    - Finally, run the `install.bat` to setup required libraries for TagUI, PREFECT, JUPYTER NOTEBOOK etc.
2. Install from zipped package file
    - Requires: `install.bat` and a `optimus_package*.zip` file.
    - optimus_package is in continuous release and new releases are versioned in YYYYMMDD format.
      It is advisable you use the latest version available which should be in the *installation* folder.  Check the release notes on what is included in the version.
    - Each new release can also be installed over a previous release as an upgrade.  
      Normally, an upgrade installation will not remove existing user files.  But it may overwrite existing scripts files with same name.
      Backup your scripts folder to avoid problems.
    - Click here for the latest stable [installation package](./installation).  And run the installation batch file with the package directly in the root directory of the folder where you wish to install OPTIMUS.  We recommend to keep the name of the program folder as Optimus.  
#### Installation issues
- [SQLite ‘no such table: json_each’](https://github.com/PrefectHQ/prefect/issues/5970) - potential issue with python / SQLite version.  Ensure python version 3.9 or 3.10 is used.  

### USAGE
- Use `runRPA.bat` to launch RPA program.  Requires to specify an Excel script file.
- Example with Excel script file sample.xlsm :   >> `runRPA -f sample`  
- Sample script files "sample" available to test various RPA functionality
- All excel script files are to be placed in `\scripts`
    And they can include RPA images (for Visual automation of your desktop and websites)

- To launch the Prefect workflow engine, run startOrion.bat to launch the orion workflow server in background.
  - And open the [Prefect dashboard](http://127.0.0.1:4200) in your browser
  - Refer to the documentation here for more details on [managing automation flows and deployments in the workflow dashboard](./docs/ORCHESTRATION.md).

### DOCUMENTATION
OPTIMUS is based on TagUI for RPA automation.  Almost all of TagUI's features are ported and available in Optimus.  And some have also been enhanced.
- As many of OPTIMUS core RPA functionality is based on TagUI, a good reference on the core RPA functionality is available from the TagUI official sites, in particular:
  - [Official TagUI site](https://aisingapore.org/tagui/) and [the python version of TagUI](https://github.com/tebelorg/RPA-Python)
  - The list of keywords and commands currently supported by OPTIMUS Excel script can be [referenced from here](./docs/scriptKeywords.xlsx).
  > TagUI by design does not deploy or save any user data on the cloud.  Passwords or credentials are not saved in the scripts, but cached in the browser or secret files on the user's local computer.  

OPTIMUS also natively leverages many other python packages for additional features, including:
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
- [dataframe-image](https://pypi.org/project/dataframe-image/) / [Github](https://github.com/dexplo/dataframe_image): to export dataframe output as image files
  - [HTML2Image](https://pypi.org/project/html2image/) / [Github](https://github.com/vgalin/html2image) - alternative.  Also relies on [chrome browser application](https://www.bleepingcomputer.com/news/software/chrome-and-firefox-can-take-screenshots-of-sites-from-the-command-line/)
  - [Visualize and save full dataframes as images](https://randomds.com/2021/12/23/visualize-and-save-full-pandas-dataframes-as-images/)
  - [IMGKit](https://pypi.org/project/imgkit/)
- [xlwings](https://www.xlwings.org/): for Excel automation 
  - it also leverages common windows COM components for Outlook integration, OneDrive Sync Client for OneDrive / Sharepoint / Teams integration.

There are some on-going enhancements of OPTIMUS that have yet to be fully incorporated into the solution.  Please contact the developer for further details:
- integrate [data exploration tools like mitos, DTale, Lux](https://github.com/ray-oh/Optimus/blob/master/docs/DATA_EXPLORATION.md).  These are tools that simplify working with Pandas by offering a GUI front end.
- components that allow further [scaling of the solution to handle big data e.g > 10TB without resorting to Spark](https://github.com/ray-oh/Optimus/blob/master/docs/SCALING.md)
- building a GUI front end for writing OPTIMUS RPA commands

### PROGRAM TECHNICAL INFORMATION
Pre-requisites:
- Windows 10 or Windows 10 Enterprise Server.
> OPTIMUS currently does not have a cloud enabled service option.  But it is possible deploy OPTIMUS on a cloud virtual machine to run the automation in unattended mode.
>- It is also possible to federate an automation task across multiple deployments of OPTIMUS using OneDrive Sync Client or a shared network drive (if running within an enterprise network) to share data, status, and scripts.  
>- The current release of OPTIMUS does not provide this capability out of the box and requires some setup to achieve the federation.  Future releases may make this easier by leveraging the cloud enabled capabilities of Prefect workflow.  
>***Typical cloud deployment architecture***
>![Typical cloud deployment architecture](https://user-images.githubusercontent.com/115925194/210483008-d9d9687f-2602-4ded-bb3d-90d1c8cce8b4.png)

- Python
> Version 3.10.9 (or any version < 3.11 and > 3.9) is the recommended ?version for use with OPTIMUS for compatibility with current libraries.   
>- [Download Python 3.10.9](https://www.python.org/downloads/release/python-3109/)
> For future release, we will keep the library list updated to make it compatible with latest python release or anaconda package.
>- You can [follow this guide](https://docs.jupyter.org/en/latest/install/notebook-classic.html) for installing Jupyter separately from Python.  In future release, Jupyter Notebook will be included in the default installation package.  

All other program libraries will be installed automatically by the installation package, including:
- Autobot (RPA component) - based on TagUI and various addon python packages
- Prefect (workflow orchestration) - full fledged orchestration package for dataflow automation.

### RELEASE NOTES:

20220710 - Optimus 1.1.
        Stable release.
        Package and installation scripts.
        Separate autobot and prefect installation folders.
        Separate scripts folder.

20221006 - Stable release. New features: Installation scripts and package updates. Scripts (user files) folders separated from Autobot program folder.

20221018 - Updated installation scripts. Added [python-minifier](https://pypi.org/project/python-minifier/) [github](https://dflook.github.io/python-minifier/installation.html).

### CONTACT
Raymond Oh - for reporting of bugs, questions, requests etc

## CLONING REPO, CONTRIBUTION AND LICENSE

### Clone git repository

```sh
    $ git clone "https://github.com/ray-oh/Optimus"
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
