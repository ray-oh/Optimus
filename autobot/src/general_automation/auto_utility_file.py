#!/usr/bin/env python
# coding: utf-8

"""
Module:         auto_utility_file.py
Description:    file utilities e.g. rename File, get full path of file, getRecentCreatedFile, Json file handling, Excel file handling
Created:        30 Jul 2022

Versions:
20210216        Refactor all utility codes
"""
#from config import *
#from auto_utility_logging import *
from prefect import task, flow, get_run_logger, context
from prefect.task_runners import SequentialTaskRunner

import os

#from config import PROGRAM_DIR
def renameFile(sourceFilePath, targetFilePath):
    #logg('renameFile', sourceFilePath = sourceFilePath, targetFilePath = targetFilePath)
    #rename a file
    if os.path.exists(targetFilePath):
      os.remove(targetFilePath)
    os.rename(sourceFilePath, targetFilePath)

def getFullPath(path):
    #import os
    return os.path.abspath(path)

import time
import glob
import os
from pathlib import Path, PureWindowsPath
def GetRecentCreatedFile(filepath,filetype,inLastNumOfSec):
    #GetRecentCreatedFile('C:/Users/roh/Downloads/','*.png',10)
    #print(filepath,filetype,inLastNumOfSec)
    filepath = Path(filepath)
    #print(filepath.absolute())
    file_pattern = filepath / filetype # filepath + filetype
    #print('GetRecentCreatedFile', str(filepath), filetype, str(file_pattern), inLastNumOfSec)
    list_of_files = glob.glob(str(file_pattern)) # * means all if need specific format then *.csv
    #print(not not list_of_files ) # returns true if empty
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        # time.ctime(c_time)
        print('Latest file', latest_file, 'create', time.ctime(os.path.getctime(latest_file)), '>', time.ctime(time.time()-inLastNumOfSec), os.path.getctime(latest_file) > time.time()-inLastNumOfSec)
        if os.path.getctime(latest_file) > time.time()-inLastNumOfSec:
            print('Time', time.time()-inLastNumOfSec, '|' , latest_file)            
            return latest_file
        else:
            return None
    else:
        return None
#downloadedFile = GetRecentCreatedFile('D:\\iCristal\\','*.pdf',120) # get most recent file of pdf format in last 120 sec in path
#print('none') if downloadedFile is None else print(downloadedFile)
#renameFile(downloadedFile, 'D:/iCristal/Output/APAC_Daily_Sales/' + saveName + '.pdf')


#Helper functions for JSON
#https://tutswiki.com/read-write-json-config-file-in-python/
import json
def jsonWrite(obj, file):
    with open(file, "w") as jsonfile:
        json.dump(obj, jsonfile, indent=4)
        print(file, obj, " : Write successful")
        jsonfile.close()
    return True

def jsonRead(file):
    with open(file, "r") as jsonfile:
        obj = json.load(jsonfile) # Reading the file
        print(file, " : Read successful")
        jsonfile.close()
    return obj

def runInBackground(prog_path):
    #https://riptutorial.com/python/example/5714/more-flexibility-with-popen
    from subprocess import Popen
    from pathlib import Path, PureWindowsPath

    import subprocess
    import sys

    #result = subprocess.run([sys.executable, "-c", "print('ocean')"])
    #print('      ', 'Command:', prog_path + r"\autobot\src\console.bat")

    result = subprocess.run(
        Path(prog_path + r"\autobot\src\console.bat").absolute(),
        capture_output=True, text=True
    )
    print('      ', 'Activate remote console session. Return code:', result.returncode, result.stderr)
    result = subprocess.run(
        str(Path(prog_path + r"\autobot\src\Qres\Qres.exe").absolute()) + " /x:1920 /y:1080",
        capture_output=True, text=True
    )
    #result = subprocess.run(
    #    [sys.executable, "-c", "raise ValueError('oops')"], capture_output=True, text=True
    #)
    #print("stdout:", result.stdout)
    print('      ',"Set screen resolution 1920 x 1080.", result.stderr)
    #stdout=subprocess.DEVNULL,
    #stderr=subprocess.STDOUT, 
    #creationflags=subprocess.CREATE_NO_WINDOW
    return

def killprocess(processName: str):
    logger = get_run_logger()
    import subprocess
    command = "Get-Process | Where-Object {{$_.Name -Like '{}'}} ".format(processName)
    result = subprocess.run(["powershell.exe", command], capture_output=True)
    if len(result.stdout.decode('ASCII')) > 0:
        logger.info("process killed" + result.stdout.decode('ASCII'))
        print("process killed" + result.stdout.decode('ASCII'))
        result = subprocess.run(["powershell.exe", command + " | Stop-Process -force "], capture_output=True)
        return True
    else:
        return False


def checkIfFileOpen(FILENAME: str):
    import os
    import pythoncom
    import win32api
    import win32com.client

    #FILENAME = win32api.GetLongPathName(os.path.join(os.environ["TEMP"], "temp.csv"))
    #open(FILENAME, "wb").write ("1,2,3\n4,5,6\n")
    #obj = win32com.client.GetObject(FILENAME)

    context = pythoncom.CreateBindCtx(0)
    for moniker in pythoncom.GetRunningObjectTable():
        name = moniker.GetDisplayName(context, None)
        if name.endswith(FILENAME):
            print("Found", name)
            #break
            return True
        else:
            #print("Not found")
            pass
    return False


def printscreen(file=".\screen.jpg"):
    # Importing Image and ImageGrab module from PIL package 
    from PIL import Image, ImageGrab                    
    # creating an image object
    #im1 = Image.open(r"C:\Users\sadow984\Desktop\download2.JPG")
        
    # using the grab method
    im2 = ImageGrab.grab(bbox = None)
    #im2.show()
    # save a image using extension
    im2 = im2.save(file)
#printscreen()


'''   
#'subinacl.exe /service "foo" display'

p = Popen(Path(".\src\console.bat").absolute(), cwd=r".\src")
#p = Popen(script, cwd=workingDir)
stdout, stderr = p.communicate()
print('runInBackground:', 'returnCode', p.returncode, 'stderr', p.stderr, 'stdout', p.stdout)
#logg('runBatchScript:', returnCode = p.returncode, stderr = p.stderr, stdout = p.stdout)
p = Popen(str(Path(".\src\Qres\Qres.exe").absolute()) + " /x:1920 /y:1080")                 # set screen resolution
#p = Popen(script, cwd=workingDir)
stdout, stderr = p.communicate()
print('screen resolution:', 'returnCode', p.returncode, 'stderr', p.stderr, 'stdout', p.stdout)
'''