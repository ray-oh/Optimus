#!/usr/bin/env python
# coding: utf-8

"""
Module:         auto_utility_logging.py
Description:    library for logging
Created:        30 Jul 2022

Versions:
20210216    Reorganize utility files
"""
import config

import logging
# define all the srcLog parameters in config.json

#srcLog = r'.\log\generalAutomation.log'

#srcLogPath = r'D:\OneDrive-Sync\APAC Management - Reports - Reports\log\DClick'
#srcLog = r'D:\OneDrive-Sync\APAC Management - Reports - Reports\log\DClick\generalAutomation.log'

logging.basicConfig(filename= config.SRCLOG ,  ##"./log/output.log"
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s') 
    #format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

'''
def logg(text,**kwargs):                    # kwargs is a dict of the keyword args passed to the function
    if("level" in kwargs):
        level = kwargs['level'].upper()     # CRITICAL	50, ERROR	40, WARNING	30, INFO	20, DEBUG	10
    else:
        level = config.DEFAULTLOGLEVEL
    logLevelDictionary = {
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10        
        }
    logLevel = logLevelDictionary[level]
    arguments = ''
    if len(kwargs) > 0: arguments = str(kwargs)
    result = "{} {}".format(text, arguments)
    if config.LOGPRINT and logLevel >= int(config.LOGPRINTLEVEL):
        #print('LOG kwargs:', kwargs)
        print(text, arguments)
    if level == 'INFO': logging.info(result)
    if level == 'DEBUG': logging.debug(result)
    if level == 'WARNING': logging.warning(result)
    if level == 'ERROR': logging.error(result)    
    if level == 'CRTICAL': logging.critical(result)    
'''