#!/usr/bin/env python
# coding: utf-8

"""
Module:         auto_utility_browser.py
Description:    Utilities for browser automation
Created:        30 Jul 2022

Versions:
20210216    Reorganize utility file
"""
import config
from auto_utility_logging import *
from auto_utility_file import GetRecentCreatedFile
import rpa as r
from pathlib import Path, PureWindowsPath    


def chromeZoom(factor):
    # zoom -75% = minus, zoom factor of 3 times
    #ahk.send_input('{Ctrl down}0{Ctrl up}')  # reset to 100%
    logg('chromeZoom', factor = factor)
    try:
        int(factor)
    except ValueError:
        # not int
        logg('Not int', factor = factor, level = 'error')
        return
    #isNaN = pd.isna(factor)
    #if isNaN:
    #    print('isNaN')
    #    return
    #if not factor.isnumeric():
    #    print('Not numeric') 
    #    return
    factor = int(factor)
    if factor < 0:
        zoom_plus_minus = '-'
    elif factor > 0:
        zoom_plus_minus = '+'
    elif factor == 0:
        zoom_plus_minus = '0'
    else:
        return
    logg('zoom plus minus', zoom_plus_minus = zoom_plus_minus)
    r.keyboard('[ctrl]0')
    for i in range(int(abs(factor))):
        #ahk.send_input('{Ctrl down}' + zoom_plus_minus + '{Ctrl up}')  # zoom -90%, -80%, -75%
        r.keyboard('[ctrl]' + zoom_plus_minus) 
        logg('zoom', i = i)
    return


import sys
def exitProg():
    '''Close RPA browser'''
    r.close()
    sys.exit(config.EX_OK) # code 0, all ok    
    #exit()

def exitProgWError(errorCode: int):
    '''Close RPA browser'''
    r.close()
    sys.exit(errorCode) # code 0, all ok        
    #exit(errorCode)

from datetime import date
from datetime import datetime
# requires: r.init(visual_automation = True)
# use:      snapImage()
def snapImage(msg="Snap picture at " + datetime.now().strftime("%Y%m%d_%H%M%S"), file_suffix="_Check.PNG", time_snap = datetime.now().strftime("%Y%m%d_%H%M%S") ):
        #logging.info(msg + " " + time_snap + ".PNG")
        print(msg + " " + time_snap + ".PNG")
        r.snap("(0,0)-(1920,1080)", config.LOG_DIR + "/"+time_snap+file_suffix)
        #r.snap("(0,0)-(1920,1080)",time_snap+file_suffix)


import time
#waitIdentifierExist(identifier, time_seconds, interval)
# check and wait for image to appear - True when appear, False when not exist after X seconds
def waitIdentifierExist(identifier, time_seconds = 10, interval = 5, snapPic = True):
    #image = 'Image/' + image
    #identifier

    start_time = time.time()
    if type(identifier) == list:
        #identifier_list = map(lambda x: Path(config.IMAGE_DIR + '/' + x).absolute().__str__() \
        #    if x.lower().endswith(('.png', '.jpg', '.jpeg')) else x, identifier)
        #identifier_list = identifier
        identifier_list = list(map(lambda x: Path(config.IMAGE_DIR + '/' + x).absolute().__str__() \
            if x.lower().endswith(('.png', '.jpg', '.jpeg')) else x, identifier))
        #print('size',len(identifier_list))
        #print('size 2',len(identifier))
        elapsed_time = int(time.time() - start_time)
        while True:
            print('..... true ..... ', list(identifier_list), len(list(identifier_list)), type(list(identifier_list)))
            #idx = 0
            for idx, x in enumerate(identifier_list):
                #for x in list(identifier_list):
                print('loop', x, idx, 'elapsed time', str(elapsed_time), 's ')
                #identifier = "FILE=filepath|filepattern|inLastNumOfSec" eg. FILE=
                if x.startswith("FILE="):
                    identifierParamList = x.split('=')
                    identifierParamList = identifierParamList[1].split('|')
                    sourcePath = identifierParamList[0].strip()
                    filePattern = identifierParamList[1].strip()
                    withinLastSec = float(identifierParamList[2].strip())
                    downloadedFile = GetRecentCreatedFile(sourcePath, filePattern, withinLastSec) # get most recent file of pdf format in last 120 sec in path
                    #logg('renameFile parameters', targetPath = targetPath, saveName = saveName, fileExtension = fileExtension, level = 'debug')
                    #logg('Recent Download file : none', level = 'error') if downloadedFile is None else logg('Recent Download file:', downloadFile = downloadedFile, targetPath = targetPath, saveName = saveName, fileExtension = fileExtension, level = 'info')
                    if downloadedFile is not None: return True, idx
                    #renameFile(downloadedFile, targetPath + saveName + '.' + fileExtension)
                else:
                    bImageFound = r.present(x)
                    if bImageFound:
                        elapsed_time = int(time.time() - start_time)
                        logg('SUCCESS - found: ' + str(elapsed_time) + 's ' + x, level = 'info')
                        print('SUCCESS', x, idx, 'elapsed time', str(elapsed_time), 's ')
                        return True, idx
                #idx += 1
            #idx = 0
            elapsed_time = int(time.time() - start_time)
            if elapsed_time > time_seconds:
                logg('FAIL - Not found: ' + str(elapsed_time) + 's ', level = 'info')
                print('FAIL', 'elapsed time', str(elapsed_time), 's ')
                if snapPic:
                    snapImage()
                return False, idx
            else:
                logg('Checking Image: ' + str(elapsed_time) + 's ', level = 'info')
                print('loop wait', 'elapsed time', str(elapsed_time), 's ')
                r.wait(interval)

    # type is not list
    else:
        if identifier.lower().endswith(('.png', '.jpg', '.jpeg')): identifier = Path(config.IMAGE_DIR + '/' + identifier).absolute().__str__()

        while True:
            #identifier = "FILE=filepath|filepattern|inLastNumOfSec" eg. FILE=
            if identifier.startswith("FILE="):
                identifierParamList = identifier.split('=')
                identifierParamList = identifierParamList[1].split('|')
                sourcePath = identifierParamList[0].strip()
                filePattern = identifierParamList[1].strip()
                withinLastSec = float(identifierParamList[2].strip())
                downloadedFile = GetRecentCreatedFile(sourcePath, filePattern, withinLastSec) # get most recent file of pdf format in last 120 sec in path
                #logg('renameFile parameters', targetPath = targetPath, saveName = saveName, fileExtension = fileExtension, level = 'debug')
                #logg('Recent Download file : none', level = 'error') if downloadedFile is None else logg('Recent Download file:', downloadFile = downloadedFile, targetPath = targetPath, saveName = saveName, fileExtension = fileExtension, level = 'info')
                if downloadedFile is not None: return True
                #renameFile(downloadedFile, targetPath + saveName + '.' + fileExtension)
            else:
                bImageFound = r.present(identifier)
                if bImageFound:
                    elapsed_time = int(time.time() - start_time)
                    logg('SUCCESS - found: ' + str(elapsed_time) + 's ' + identifier, level = 'info')
                    return True

            elapsed_time = int(time.time() - start_time)
            if elapsed_time > time_seconds:
                logg('FAIL - Not found: ' + str(elapsed_time) + 's ' + identifier, level = 'info')
                if snapPic:
                    snapImage()
                return False
            else:
                logg('Checking Image: ' + str(elapsed_time) + 's ' + identifier, level = 'info')
                r.wait(interval)

    return False


def waitIdentifierDisappear(identifier, time_seconds = 10, interval = 5, snapPic = True):
    start_time = time.time()
    if identifier.lower().endswith(('.png', '.jpg', '.jpeg')): identifier = Path(config.IMAGE_DIR + '/' + identifier).absolute().__str__()

    while True:        
        bImageFound = r.present(identifier)
        elapsed_time = int(time.time() - start_time)
        #r.hover(10+elapsed_time*5,500)
        if not bImageFound:
            logg('SUCCESS - disappeared: ' + str(elapsed_time) + 's ' + identifier, level = 'info')
            return True
        elif elapsed_time > time_seconds:
            logg('FAIL - still exist: ' + str(elapsed_time) + 's ' + identifier, level = 'info')
            if snapPic:
                snapImage()
            return False
        else:
            logg('Checking Image: ' + str(elapsed_time) + 's ' + identifier, level = 'info')
            r.wait(interval)
    return False

