#!/usr/bin/env python
# coding: utf-8

"""
Module:         auto_utility_parsers.py
Description:    library for parsers
Created:        30 Jul 2022

Versions:
20210216    Reorganize utility files
"""
#import config

from auto_utility_file import jsonRead, jsonWrite
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter

def parseArg(configObj):
    # Parse command line arguments
    version = configObj['settings']['version']
    #parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description= 'Optimus ' + version + ' \r\n sdfsdfsdfsdfsdfds Utility to process RPA scripts with steps defined from an Excel input.')
    #parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description= 'Optimus ' + version + '\n' +  'Utility to process RPA scripts with steps defined from an Excel input.')
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description= 'Optimus ' + version + '\n' +  'Utility to process RPA scripts with steps defined from an Excel input.')

    config_keys = configObj.options('flag')
    flags_items = configObj.items('flag')
    help_items = configObj.items('help')
    #type_items = configObj.items('type')
    #print(config_keys)
    #print(flags_items)
    #print(help_items)
    for key in config_keys:
        #print(key, configObj['flag'][key])
        flag = "-" + configObj['flag'][key]
        flagLong = "--" + key
        defaultValue = configObj['settings'][key]
        help = configObj['help'][key]
        typeValue = eval(configObj['type'][key])
        #print(flag, flagLong, 'DEFAULT:',defaultValue, help, typeValue)
        parser.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
    args = vars(parser.parse_args())
    return args


def mainparseArguments():
    # declare global else startcode will be treated as local variable when assigning a value to variable with this name within function
    #global config.startfile, config.startcode, config.startsheet, config.logPrint, config.logPrintLevel, config.defaultLogLevel, config.srcLog, config.srcLogPath
    #print('after global in parsearg',startfile, startcode, startsheet, logPrint, logPrintLevel, defaultLogLevel, srcLog, srcLogPath)

    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f", "--startfile", default=".\\main.xlsm", type=str, help="Path to Excel file with RPA steps")
    parser.add_argument("-c", "--startcode", default="main", type=str, help="Name of first block of RPA steps to run")
    parser.add_argument("-m", "--startsheet", default="main", help="Name of first sheet or module to run")
    parser.add_argument("-b", "--background", default=0, help="0 = Normal mode, 1 = Background mode")

    parser.add_argument("-p", "--logPrint", default=True, type=bool, help="Print logs to console.")
    parser.add_argument("-a", "--logPrintLevel", default=30, type=int, help="Prints alerts to console - 10 Debug, 20 Info, 30 Warning.")
    parser.add_argument("-d", "--defaultLogLevel", default="DEBUG", type=str, help="Log alert level - DEBUG, INFO, WARNING etc.")
    #parser.add_argument("-l", "--srcLog", default=".\\log\\generalAutomation.log", type=str, help="Path of log file")
    parser.add_argument("-l", "--srcLog", default="generalAutomation.log", type=str, help="Log file name")
    parser.add_argument("-r", "--srcLogPath", default=".\\log", type=str, help="Log Path")

    parser.add_argument("-g", "--config", default="", type=str, help="Path to config file with default run settings. Default config.json")
    parser.add_argument("-s", "--settings", default=2, type=int, help="Settings: 0 = ignore, 1 = save config, 2 = load config")

    args = vars(parser.parse_args())
    '''
    settings = args["settings"]
    config_file = args["config"]     #r".\config.json"
    
    if settings == 2:
        # Load from config.json
        # read config.json parameters
        if config_file == "":
            config_file = r".\config.json"            
        config = jsonRead(config_file)
        #print('config', config)
        #print(config2['VM1']['sheet1']['iterationcount'])

        # Set up parameters
        startfile = config['startfile']
        startcode = config['startcode']
        startsheet = config['startsheet']
        background = config['background']        
        logPrint = config['logPrint']       # print log to console
        logPrintLevel = config['logPrintLevel']  # Default value 30.  Print to console if level is above or equals this level
        defaultLogLevel = config['defaultLogLevel']  # if level is not defined when calling logg function.  INFO, DEBUG etc
        srcLog = config['srcLog']
        srcLogPath = config['srcLogPath']

        #print('Main Excel RPA input: ', startfile)
        #srcLogPath = config['srcLogPath']
        #srcLog = config['srcLog']

    elif settings == 1 or settings == 0:
        # from default or user parameters
        startfile = args['startfile']
        startcode = args['startcode']
        startsheet = args['startsheet']
        background = args['background']        
        logPrint = args['logPrint']       # print log to console
        logPrintLevel = args['logPrintLevel']  # Default value 30.  Print to console if level is above or equals this level
        defaultLogLevel = args['defaultLogLevel']  # if level is not defined when calling logg function.  INFO, DEBUG etc
        srcLog = args['srcLog']
        srcLogPath = args['srcLogPath']

        # save log
        if settings == 1:
            if config_file == "":
                config_file = r".\config.json"
                args["config"] = r".\config.json"                            
            jsonWrite(args, config_file)

    #logging.info('version 1.2')
    #logg(codeVersion, level = 'info')
    '''
    #print('exiting parse arguments', startfile, startcode)
    #print('in parsearg',startfile, startcode, startsheet, logPrint, logPrintLevel, defaultLogLevel, srcLog, srcLogPath)
    return args



#from auto_utility_logging import logg

#import logging

from pyparsing import (printables, originalTextFor, OneOrMore, 
    quotedString, Word, delimitedList)

# Special parser to parse a string by its delimiter except if its encased in quotes
def parseWithQuotes(stringToParse, delimiter = ','):

    #stringToParse = stringToParse.replace(delimiter+delimiter,',[space],')
    stringToParse = searchReplacePattern("(,[\s]*,)", stringToParse, ",[space],")   # ,, or , , or ,    ,

    # unquoted words can contain anything but a delimiter
    printables_less_delimiter = printables.replace(delimiter,'')

    # capture content between ';'s, and preserve original text
    content = originalTextFor(
        OneOrMore(quotedString | Word(printables_less_delimiter)))

    # process the string
    result = delimitedList(content, delimiter).parseString(stringToParse)

    # replace any specific matching item in list with value
    result = searchReplaceList(result, "[space]", "")  #["" if x=="[space]" else x for x in result]

    return result


import re
# called by auto_code command regexSearch:
def regexSearch(strPattern, strSearch):
    ''' search for a pattern in a given string and return the matching pattern value'''
    try:
        # found = re.search('AAA(.+?)ZZZ', str).group(1)
        print('regexSearch .....', strPattern, strSearch)
        found = re.search(strPattern, strSearch).group(1)
        #logg(found)
        return found
    except AttributeError:
        pass
    return None

def searchReplacePattern(pattern, searchStr, replace):  
    #str = '<URL_pages:key>,,./,<outputTempFolder>/,xlsx,600' #"Joe-Kim Ema Max Aby Liza"
    #print(re.sub("(\s) | (-)", ", ", str))
    #print(re.sub("(,[\s]*,)", ",[space],", str))
    return re.sub(pattern, replace, searchStr)

def searchReplaceList(objList, search, replace = ""):
    result = [replace if x==search else x for x in objList]
    return result

# Parse an argment string into a dictionary with argument labels as keys
def parseArguments(labels, argumentStr, delimiter = ',', validate = 1):
    labelsList = [s.strip() for s in labels.split(delimiter)]    
    #argumentsList = [s.strip() for s in argumentStr.split(delimiter)]
    argumentsList = [s.strip() for s in parseWithQuotes(argumentStr)]
    #logg('parseArguments:', labels = labelsList, argumentsList = argumentsList, level = 'debug')
    #if len(argumentsList) != len(labelsList):
    if validate == 2:    # strict validation
        if len(argumentsList) != len(labelsList):
            #logg('parseArguments:Error with number of arguments:', argumentsList = argumentsList, labels = labelsList, level = 'error')
            return {}
    elif validate == 1:  # loose validation - arguments not more than labels
        if len(argumentsList) > len(labelsList):
            #logg('parseArguments:Error with number of arguments:', argumentsList = argumentsList, labels = labelsList, level = 'error')
            return {}        
    elif validate == 0:  # no validation
        pass

    i = 0
    tmpDict = {}
    for argument in argumentsList:
        tmpDict[labelsList[i]] = argument #updateConstants(df, argumentsList[i])
        i = i + 1
    return tmpDict



