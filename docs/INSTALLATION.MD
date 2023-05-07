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

