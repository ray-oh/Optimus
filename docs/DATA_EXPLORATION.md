# Data Exploration

Data exploration involves data cleansing, transformation, wrangling and quick profiling and visualizations.
All these can be done with python pandas.  But there are a number of tools that make this easier without need for knowledge on python coding.
Commercial equivalents of such tools would be alteryx, tableau prep.  Which are proprietary and have a high license cost.

There are some a number of alternative open source options - which come at zero cost - and are more open in integration with python and pandas.  In fact many of such solutions are built upon standard pandas and other python libraries.
The following open source data exploration tools have been evaluated for integration with OPTIMUS, including:
- [mito](https://www.trymito.io/) This solution has been selected for inclusion in the OPTIMUS package as its the most mature among the evaluated tools in terms of user interface and features.  Here is an youtube video [review on mito](https://www.youtube.com/watch?v=js4iaGQvTAo&list=PLtqF5YXg7GLkskjS9D2PSIwKV6HUuWkXo&index=14)
- [bamboolib](https://docs.bamboolib.8080labs.com/)
- [pandas GUI](https://github.com/adamerose/PandasGUI).  
    - Youtube [Video](https://www.youtube.com/watch?v=F8mSlETrcl8&list=PLtqF5YXg7GLkskjS9D2PSIwKV6HUuWkXo&index=20) on how to use PandasGUI for Exploratory Data Analysis and Data Science
    - [Analysing data with pandas gui](https://flowygo.com/en/blog/pandasgui-graphical-user-interface-for-analyzing-data-with-pandas/)
- [pandas ui](https://github.com/arunnbaba/pandas_ui) 
- [pandas table data explore application](https://pypi.org/project/pandastable/) - useful for data analysts and programmers who want to get an initial interactive look at their tabular data without coding

Some other reviews on data exploratory solutions for reference:
- [4 Python Tools Every Data Scientist Should Start Using - pandas GUI, mito, lux, bokeh](https://medium.com/trymito/4-python-tools-every-data-scientist-should-start-using-f1a3be18d2c9)
- [3 Python Packages for Low Code Data Science](https://medium.com/geekculture/3-python-packages-for-low-code-data-science-5dfec9b0acc)
- [Pandas DataFrame Visualization Tools](https://pbpython.com/dataframe-gui-overview.html)
- [Dtale - easy way to view & analyze Pandas data structures](https://github.com/man-group/dtale) 
    - [D-Tale The Best Library To Perform Exploratory Data Analysis Using Single Line Of Code](https://towardsdatascience.com/d-tale-for-fast-and-easy-exploratory-data-analysis-of-well-log-data-a2ffca5295b6)
- [LUX - A Python API for Intelligent Visual Discovery](https://github.com/lux-org/lux)

# mito - automate entire spreadsheet workflows without having to learn Python

[mito](https://www.trymito.io/) is a GUI front end to python pandas for data analysis.  It provides a familiar EXCEL spreadsheet interface for automating python data analysis, without need to learn coding in python and pandas.

## Installing mito
Install the Mito installer:
```
python -m pip install mitoinstaller
```
Run installer:
```
python -m mitoinstaller install
```
Copy and run this in Jupyter Notebook:
```
import mitosheet
mitosheet.sheet()
```
Installation log.  Potential delay in installation due to [SSL certificate warning](https://github.com/segmentio/analytics-python/issues/142)
```
D:\Optimus\autobot>.\venv\Scripts\activate

(venv) D:\Optimus\autobot>python -m pip install mitoinstaller
Requirement already satisfied: mitoinstaller in d:\optimus\autobot\venv\lib\site-packages (0.0.199)
Requirement already satisfied: analytics-python in d:\optimus\autobot\venv\lib\site-packages (from mitoinstaller) (1.4.0)
Requirement already satisfied: colorama in d:\optimus\autobot\venv\lib\site-packages (from mitoinstaller) (0.4.6)
Requirement already satisfied: termcolor in d:\optimus\autobot\venv\lib\site-packages (from mitoinstaller) (2.2.0)
Requirement already satisfied: six>=1.5 in d:\optimus\autobot\venv\lib\site-packages (from analytics-python->mitoinstaller) (1.16.0)
Requirement already satisfied: monotonic>=1.5 in d:\optimus\autobot\venv\lib\site-packages (from analytics-python->mitoinstaller) (1.6)
Requirement already satisfied: requests<3.0,>=2.7 in d:\optimus\autobot\venv\lib\site-packages (from analytics-python->mitoinstaller) (2.28.1)
Requirement already satisfied: python-dateutil>2.1 in d:\optimus\autobot\venv\lib\site-packages (from analytics-python->mitoinstaller) (2.8.2)
Requirement already satisfied: backoff==1.10.0 in d:\optimus\autobot\venv\lib\site-packages (from analytics-python->mitoinstaller) (1.10.0)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in d:\optimus\autobot\venv\lib\site-packages (from requests<3.0,>=2.7->analytics-python->mitoinstaller) (1.26.12)
Requirement already satisfied: charset-normalizer<3,>=2 in d:\optimus\autobot\venv\lib\site-packages (from requests<3.0,>=2.7->analytics-python->mitoinstaller) (2.1.1)
Requirement already satisfied: certifi>=2017.4.17 in d:\optimus\autobot\venv\lib\site-packages (from requests<3.0,>=2.7->analytics-python->mitoinstaller) (2022.9.24)
Requirement already satisfied: idna<4,>=2.5 in d:\optimus\autobot\venv\lib\site-packages (from requests<3.0,>=2.7->analytics-python->mitoinstaller) (3.4)

(venv) D:\Optimus\autobot>python -m mitoinstaller install
Starting Mito install. This make take a few moments.

In the meantime, check out a 2 minute intro to Mito: https://www.youtube.com/watch?v=LFfWfqzdKyE

Upgrade mitoinstaller
Setting up environment
Check dependencies
Remove mitosheet3 if present
Install mitosheet
This may take a few moments...
Activate extension
error uploading: HTTPSConnectionPool(host='api.segment.io', port=443): Max retries exceeded with url: /v1/batch (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')))
Create import mito startup file
Creating a Mitosheet starter notebook
Start Jupyter
error uploading: HTTPSConnectionPool(host='api.segment.io', port=443): Max retries exceeded with url: /v1/batch (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')))
error uploading: HTTPSConnectionPool(host='api.segment.io', port=443): Max retries exceeded with url: /v1/batch (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')))

(venv) D:\Optimus\autobot>[I 2023-03-04 06:15:08.940 ServerApp] jupyter_server_fileid | extension was successfully linked.
[I 2023-03-04 06:15:08.956 ServerApp] jupyter_server_ydoc | extension was successfully linked.
[I 2023-03-04 06:15:08.987 ServerApp] jupyterlab | extension was successfully linked.
[I 2023-03-04 06:15:09.003 ServerApp] nbclassic | extension was successfully linked.
[I 2023-03-04 06:15:09.503 ServerApp] notebook_shim | extension was successfully linked.
[I 2023-03-04 06:15:09.612 ServerApp] notebook_shim | extension was successfully loaded.
[I 2023-03-04 06:15:09.612 FileIdExtension] Configured File ID manager: ArbitraryFileIdManager
[I 2023-03-04 06:15:09.612 FileIdExtension] ArbitraryFileIdManager : Configured root dir: D:/Optimus/autobot
[I 2023-03-04 06:15:09.612 FileIdExtension] ArbitraryFileIdManager : Configured database path: C:\Users\svc_supplychain\AppData\Roaming\jupyter\file_id_manager.db
[I 2023-03-04 06:15:09.612 FileIdExtension] ArbitraryFileIdManager : Successfully connected to database file.
[I 2023-03-04 06:15:09.612 FileIdExtension] ArbitraryFileIdManager : Creating File ID tables and indices with journal_mode = DELETE
[I 2023-03-04 06:15:09.612 ServerApp] jupyter_server_fileid | extension was successfully loaded.
[I 2023-03-04 06:15:09.612 ServerApp] jupyter_server_ydoc | extension was successfully loaded.
[I 2023-03-04 06:15:09.612 LabApp] JupyterLab extension loaded from D:\Optimus\autobot\venv\lib\site-packages\jupyterlab
[I 2023-03-04 06:15:09.612 LabApp] JupyterLab application directory is D:\Optimus\autobot\venv\share\jupyter\lab
[I 2023-03-04 06:15:09.628 ServerApp] jupyterlab | extension was successfully loaded.
[I 2023-03-04 06:15:09.643 ServerApp] nbclassic | extension was successfully loaded.
[I 2023-03-04 06:15:09.643 ServerApp] Serving notebooks from local directory: D:\Optimus\autobot
[I 2023-03-04 06:15:09.643 ServerApp] Jupyter Server 1.23.3 is running at:
[I 2023-03-04 06:15:09.643 ServerApp] http://localhost:8888/lab?token=6f04ec2bc19b2bab6f8c322f17f1c3a286cc6b86bd64d9e6
[I 2023-03-04 06:15:09.643 ServerApp]  or http://127.0.0.1:8888/lab?token=6f04ec2bc19b2bab6f8c322f17f1c3a286cc6b86bd64d9e6
[I 2023-03-04 06:15:09.643 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2023-03-04 06:15:09.753 ServerApp]

    To access the server, open this file in a browser:
        file:///C:/Users/svc_supplychain/AppData/Roaming/jupyter/runtime/jpserver-1136-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/lab?token=6f04ec2bc19b2bab6f8c322f17f1c3a286cc6b86bd64d9e6
     or http://127.0.0.1:8888/lab?token=6f04ec2bc19b2bab6f8c322f17f1c3a286cc6b86bd64d9e6
[W 2023-03-04 06:15:14.737 ServerApp] 404 GET /api/me?1677881714013 (::1) 288.85ms referer=http://localhost:8888/lab/tree/mito-starter-notebook.ipynb
[W 2023-03-04 06:15:15.983 LabApp] Could not determine jupyterlab build status without nodejs
[I 2023-03-04 06:15:17.957 ServerApp] Kernel started: f203d1e0-305e-44d0-8bfc-fb0e79cfe295
[W 2023-03-04 06:15:22.314 ServerApp] Got events for closed stream <zmq.eventloop.zmqstream.ZMQStream object at 0x0000013A78C1F0D0>
[I 2023-03-04 06:17:17.731 ServerApp] Saving file at /mito-starter-notebook.ipynb
[I 2023-03-04 06:17:32.795 ServerApp] Starting buffering for f203d1e0-305e-44d0-8bfc-fb0e79cfe295:9db3962e-dbb2-48e8-b0a1-069fbfbed05d
```

