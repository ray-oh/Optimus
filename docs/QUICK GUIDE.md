# Quick Usage Guide
Assumes that your computer has already been installed and setup with Optimus.
Follow the usage guide below on how to use Optimus RPA.

## Navigating Optimus Program

### Optimus Program Folder
Optimus is installed by default to your root directory e.g. `D:\Optimus`  
`runRPA.bat` is used to launch the RPA program.
![Optimus folder](https://github.com/ray-oh/Optimus/assets/115925194/04de44d5-d496-4e1c-b2a7-21ea4968ba6d)

### Useful shortcuts
As a best practice, you can place shortcuts to frequently used Optimus programs on the desktop for easy access.  Here are some of the useful shortcuts for Optimus:
- open `Optimus folder`
- launch `Jupyter notebook`
- launch `Prefect Orion dashboard` - which is used for monitor and manage your automation flows
- `Quit VM` - to quit your current virtual machine session without logging off the computer. This is necessary if you are running Optimus on an "always on" computer.
  If the computer is logged off, Optimus will not be able to launch the automations properly especially if the automation flow requires visual automation.

![Desktop shortcuts](https://github.com/ray-oh/Optimus/assets/115925194/526682f0-7dd9-43b9-8845-a12c19f48222)

### Scripts Folder
Optimus automation scripts are created in Excel and do not require any programming skills.  
These scripts are stored in the `scripts` folder.  
A `test-sample` script is available in the `scripts` folder for you to learn how to write Optimus automation scripts.

![Scripts folder](https://github.com/ray-oh/Optimus/assets/115925194/23cf3b34-307b-453c-b6b5-521934a973d7)

### How to run a RPA script
You can run the "test-sample" script as follows:  
`runRPA -f test-sample`  
![Running a script](https://github.com/ray-oh/Optimus/assets/115925194/8239b111-d2e8-4c23-b517-288f329a8fe5)

For help on how to use runRPA utility: `runRPA -help` or `runRPA -h`
![runRPA help](https://github.com/ray-oh/Optimus/assets/115925194/b381cde0-4ec8-491e-b809-c7faf63bc127)

### Outputs from the execution of RPA script
Each step of the script that is executed is displayed in the output for reference.
![Standard script run log](https://github.com/ray-oh/Optimus/assets/115925194/5d41acbb-1c68-4d90-8746-782f2417f56e)

Additional DEBUG details in the output can be shown by activating `D:\Optimus\autobot\setLogLevelDEBUG.bat`
![Script run log with DEBUG info](https://github.com/ray-oh/Optimus/assets/115925194/1d046b31-6719-4b99-a0da-d9cec6ed68ef)

### Monitoring automation flows
All executed flows can be monitored in the `Prefect Orion Dashboard`
![Workflow dashboard](https://github.com/ray-oh/Optimus/assets/115925194/446396b7-05d9-4cdb-bdd0-4bac404e7c59)

Details of the execution logs of each flow can be drilled down from the dashboard.
![Flow run details](https://github.com/ray-oh/Optimus/assets/115925194/96a7029d-f0c4-4206-a3a8-e462607d1e93)

### Working with Jupyter Notebook
Juypter notebook can be launched from the shortcut.
An example of how the jupyter notebook can be executed from the automation script is shown below:
`runJupyterNb:DataPreparationv3.ipynb, {"forceRun":"True","strSearch":"<strSearch>", "runDownload":"FALSE", "runJupyter":"FALSE", "generatedDateTime":"19/10/2023 14:01:16"}`  
runJupyterNb is the action keyword.  
First parameter is the notebook file name.  
And the next parameter are the parameters to be passed to the notebook in JSON format e.g.  `{key1:value1, key2:value2}`

![image](https://github.com/ray-oh/Optimus/assets/115925194/c27fd5c6-4d5d-4e38-a14a-1f8efafcbbd6)

![Launch Jupyter](https://github.com/ray-oh/Optimus/assets/115925194/723a5a0f-a211-4653-a25b-a94329d427e5)



