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

from gooey import Gooey, GooeyParser
from pathlib import Path
@Gooey(
    program_name='Optimus RPA - do more with less',
    optional_cols=3,  
    program_description=f"Input RPA script name and other parameters below", 
    image_dir=f'{Path.cwd().__str__()}',
    menu=[{
        'name': 'Help',
        'items': [{
                'type': 'MessageDialog',
                'menuTitle': 'About',
                'caption': 'Inform',
                'message': 'RPA solution with Excel front end for creating flows.\n\
Designed with the typical data analyst who is not technical savy but comfortable using Excel in mind.\n\
The solution makes it really easy for beginners to develop your own flows, especially with templates.\n\
Users can easily share and reuse modular Excel based scripts to speed up flow creation or create sophisticated automation flows.\n\n\
OPTIMUS differentiates itself from other RPA solutions including market leading commercial packages like UiPath in terms of its ease of use and extensibility.\n\
But at the sametime, it does not compromise on features and capabilities.'
            }, {
                'type': 'Link',
                'menuTitle': 'Documentation',
                'url': 'https://github.com/ray-oh/Optimus'
            }, {
                'type': 'AboutDialog',
                'menuTitle': 'Version / License',
                'name': 'Optimus RPA',
                'description': 'Program for running Optimus Automation Scripts',
                'version': '1.2.1',
                'copyright': '2023',
                'website': 'https://github.com/ray-oh/Optimus',
                'developer': 'Raymond Oh (https://github.com/ray-oh)',
                'license': 'BSD-3-Clause license'
            }]
        }]
    )
def parseArgGUI(configObj):
    # Parse command line arguments
    version = configObj['settings']['version']
    parserGUI = GooeyParser(description=f"Automate more with less!") 
    #parser.add_argument('Filename', widget="FileChooser")
    #parser.add_argument('Date', widget="DateChooser")
    return parserGUI


def parseArg(configObj, deploymentRun):
    # Parse command line arguments
    version = configObj['settings']['version']
    #parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description= 'Optimus ' + version + ' \r\n sdfsdfsdfsdfsdfds Utility to process RPA scripts with steps defined from an Excel input.')
    #parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description= 'Optimus ' + version + '\n' +  'Utility to process RPA scripts with steps defined from an Excel input.')

    import sys
    #if len(sys.argv) > 1 or deploymentRun:  # more than 1 arg provided or deployment run, do not activate GUI, run from CLI
    if True:
        activateGooey=False
        #print('>1 arg#####')
        parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description= 'Optimus ' + version + '\n' +  'Utility to process RPA scripts with steps defined from an Excel input.')
    else:  # if no command line arguments specified, activate GUI
        activateGooey=True
        #print('trigger parser gui', configObj)        
        parser = parseArgGUI(configObj)

    required = parser.add_argument_group('Required arguments')
    optional = parser.add_argument_group('Optional arguments')
    def addArg(op, widget_action, activateGooey, defaultValue, typeValue, key):  # used below to setup gooey

        def filelistcheck(value):  # field validation with type in argparse - experimental
            from pathlib import Path
            scripts = [f.stem for f in Path.cwd().parents[0].glob("./scripts/*.xlsm")]  # switch from autobot to optimus dir            
            if value in scripts:
                return value
            else:
                raise TypeError("Incorrect file")

        if not activateGooey:
            #print(key, typeValue, defaultValue, '>>>1')
            op.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
        elif key == 'startfile': # widget
            #print(key, typeValue, defaultValue, '>>>2 startfile')

            # Get list of script file names https://builtin.com/data-science/python-list-files-in-directory
            #files = [f. for f in pathlib.Path().iterdir() if f.is_file()]
            scripts = [f.stem for f in Path.cwd().parents[0].glob("./scripts/*.xlsm")]  # switch from autobot to optimus dir
            #print('scripts', scripts)
            op.add_argument(flag, flagLong, help=help, choices=scripts, widget='FilterableDropdown', type=filelistcheck,  gooey_options={'full_width': True}, required=True)            
            #op.add_argument(flag, flagLong, help=help, choices=scripts, type=filelistcheck, required=True)            
            #op.add_argument(flag, flagLong, help=help, default=defaultValue, widget=widget_action, required=True)
        elif 'choices[' in widget_action:   #type(widget_action) is list: # choice
            #print(key, typeValue, defaultValue, '>>>2')            
            op.add_argument(flag, flagLong, help=help, default=defaultValue, choices=eval(widget_action[7:]))                
        elif str(widget_action).lower() in ['dirchooser','filechooser','integerfield']: # widget
            #print(key, typeValue, defaultValue, '>>>3')            
            op.add_argument(flag, flagLong, help=help, default=defaultValue, widget=widget_action, required=True)
        elif str(widget_action).lower() in ['store','count']: # action
            #print(key, typeValue, defaultValue, '>>>4')            
            op.add_argument(flag, flagLong, help=help, action=widget_action, default=defaultValue)
        elif typeValue==bool: # checkbox
            #print(key, typeValue, defaultValue, '>>>5')
            defaultValue=eval(defaultValue) # force to bool
            #print(key, typeValue, defaultValue, '>>>5.1')            
            op.add_argument(flag, flagLong, help=help, widget='CheckBox', default=defaultValue)
        #elif str(widget_action).lower() in ['store_true', 'store_false']: # action
        #    #defaultValue=eval(defaultValue) # force to bool
        #    op.add_argument(flag, flagLong, help=help, action=widget_action, default=True)
        else:
            #print(key, typeValue, defaultValue, '>>>6')            
            op.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
        return op

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
        typeValue = eval(configObj['type'][key])
        defaultValue = configObj['settings'][key]
        widget_action = configObj['widget'][key]
        help = configObj['help'][key]
        #print(flag, flagLong, help, typeValue, 'DEFAULT:',defaultValue )

        if key in ['startfile','program_dir']: # required
            #required.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
            required = addArg(required, widget_action, activateGooey, defaultValue, typeValue, key)
        else:
            #optional.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
            optional = addArg(optional, widget_action, activateGooey, defaultValue, typeValue, key)


        #parser.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)

    #print('3333333333333333333333')
    args = vars(parser.parse_args())
    #print('44444444444444444444')

    #print('ARGS ####',args)
    return args


# Not used ....
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



