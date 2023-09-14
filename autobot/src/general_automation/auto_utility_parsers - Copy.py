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


import sys
import time

program_message = \
    '''
Thanks for checking out out Gooey!

This is a sample message to demonstrate Gooey's functionality.

Here are the arguments you supplied:

{0}

-------------------------------------

Gooey is an ongoing project, so feel free to submit any bugs you find to the
issue tracker on Github[1], or drop me a line at audionautic@gmail.com if ya want.

[1](https://github.com/chriskiehl/Gooey)

See ya!

^_^

'''


def display_message():
    message = program_message.format('\n'.join(sys.argv[1:])).split('\n')
    delay = 1.8 / len(message)

    for line in message:
        print(line)
        time.sleep(delay)

import argparse
@Gooey(
    optional_cols=2, 
    program_name='Advanced Layout Groups',
    menu=[{
        'name': 'File',
        'items': [{
                'type': 'AboutDialog',
                'menuTitle': 'About',
                'name': 'Gooey Layout Demo',
                'description': 'An example of Gooey\'s layout flexibility',
                'version': '1.2.1',
                'copyright': '2018',
                'website': 'https://github.com/chriskiehl/Gooey',
                'developer': 'http://chriskiehl.com/',
                'license': 'MIT'
            }, {
                'type': 'MessageDialog',
                'menuTitle': 'Information',
                'caption': 'My Message',
                'message': 'I am demoing an informational dialog!'
            }, {
                'type': 'Link',
                'menuTitle': 'Visit Our Site',
                'url': 'https://github.com/chriskiehl/Gooey'
            }]
        },{
        'name': 'Help',
        'items': [{
            'type': 'Link',
            'menuTitle': 'Documentation',
            'url': 'https://www.readthedocs.com/foo'
        }]
    }]
)
def parseArgGUI2(configObj):
    print('xxxxxxxxxxxxxxxxxxxxx 1')
    settings_msg = 'Subparser example demonstating bundled configurations ' \
                   'for Siege, Curl, and FFMPEG'
    parser = GooeyParser(description=settings_msg)
    parser.add_argument('--verbose', help='be verbose', dest='verbose',
                        action='store_true', default=False)
    subs = parser.add_subparsers(help='commands', dest='command')

    curl_parser = subs.add_parser(
        'curl', help='curl is a tool to transfer data from or to a server')
    curl_parser.add_argument('Path',
                             help='URL to the remote server',
                             type=str, widget='FileChooser')
    #curl_parser.add_argument('--connect-timeout', default=13, choices=[13,14],
    #                         help='Maximum time in seconds that you allow curl\'s connection to take', required=True)
    curl_parser.add_argument('--user-agent', widget="PasswordField",
                             help='Specify the User-Agent string ')
    curl_parser.add_argument('--cookie',
                             help='Pass the data to the HTTP server as a cookie')
    curl_parser.add_argument('--dump-header', type=argparse.FileType(),
                             help='Write the protocol headers to the specified file')
    curl_parser.add_argument('--progress-bar', action="store_true", default=False,
                             help='Make curl display progress as a simple progress bar')
    #curl_parser.add_argument('--progress-bar1', widget="CheckBox", default=True,
    #                         help='Make1 curl display progress as a simple progress bar')
    curl_parser.add_argument('--http2', action="store_true",
                             help='Tells curl to issue its requests using HTTP 2')
    #curl_parser.add_argument('--ipv4', action="store_true", default=True,
    #                         help=' resolve names to IPv4 addresses only')

    # ########################################################
    siege_parser = subs.add_parser(
        'siege', help='Siege is an http/https regression testing and benchmarking utility')
    siege_parser.add_argument('--get',
                              help='Pull down headers from the server and display HTTP transaction',
                              type=str)
    siege_parser.add_argument('--concurrent',
                              help='Stress the web server with NUM number of simulated users',
                              type=int)
    siege_parser.add_argument('--time',
                              help='allows you to run the test for a selected period of time',
                              type=int)
    siege_parser.add_argument('--delay',
                              help='simulated user is delayed for a random number of seconds between one and NUM',
                              type=int)
    siege_parser.add_argument('--message',
                              help='mark the log file with a separator',
                              type=int)

    # ########################################################
    ffmpeg_parser = subs.add_parser(
        'ffmpeg', help='A complete, cross-platform solution to record, convert and stream audio and video')
    ffmpeg_parser.add_argument('Output',
                               help='Pull down headers from the server and display HTTP transaction',
                               widget='FileSaver', type=argparse.FileType())
    ffmpeg_parser.add_argument('--bitrate',
                               help='set the video bitrate in kbit/s (default = 200 kb/s)',
                               type=str)
    ffmpeg_parser.add_argument('--fps',
                               help='set frame rate (default = 25)',
                               type=str)
    ffmpeg_parser.add_argument('--size',
                               help='set frame size. The format is WxH (default 160x128)',
                               type=str)
    ffmpeg_parser.add_argument('--aspect',
                               help='set aspect ratio (4:3, 16:9 or 1.3333, 1.7777)',
                               type=str)
    ffmpeg_parser.add_argument('--tolerance',
                               help='set video bitrate tolerance (in kbit/s)',
                               type=str)
    ffmpeg_parser.add_argument('--maxrate',
                               help='set min video bitrate tolerance (in kbit/s)',
                               type=str)
    ffmpeg_parser.add_argument('--bufsize',
                               help='set ratecontrol buffere size (in kbit)',
                               type=str)

    parser.parse_args()
    print('ARGS######----', parser)

    display_message()
    return ffmpeg_parser

from gooey import Gooey, GooeyParser
from pathlib import Path
@Gooey(
    program_name='Optimus RPA - do more with less',
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
    #parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description= 'Optimus ' + version + '\n' +  'Utility to process RPA scripts with steps defined from an Excel input.')
    parserGUI = GooeyParser(description=f"Automate more with less!") 
    #parser.add_argument('Filename', widget="FileChooser")
    #parser.add_argument('Date', widget="DateChooser")
    return parserGUI

@Gooey
def parseArg(configObj):
    # Parse command line arguments
    version = configObj['settings']['version']
    #parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description= 'Optimus ' + version + ' \r\n sdfsdfsdfsdfsdfds Utility to process RPA scripts with steps defined from an Excel input.')
    #parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description= 'Optimus ' + version + '\n' +  'Utility to process RPA scripts with steps defined from an Excel input.')

    #import sys
    #if True: #len(sys.argv) > 1 and False:
    print('>1 arg#####')
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
        typeValue = eval(configObj['type'][key])
        defaultValue = configObj['settings'][key]
        help = configObj['help'][key]
        #print(flag, flagLong, help, typeValue, 'DEFAULT:',defaultValue )
        parser.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)

    if False: #else:  # if no command line arguments specified, activate GUI
        print('trigger parser gui', configObj)        
        parser = parseArgGUI(configObj)

        config_keys = configObj.options('flag')
        flags_items = configObj.items('flag')
        help_items = configObj.items('help')
        #type_items = configObj.items('type')
        #print(config_keys)
        #print(flags_items)
        #print(help_items)
        print(len(config_keys), config_keys)
        required = parser.add_argument_group('Required arguments')
        optional = parser.add_argument_group('Optional arguments')

        def addArg(op):  # used below to setup gooey
            if 'choices[' in widget_action:   #type(widget_action) is list: # choice
                op.add_argument(flag, flagLong, help=help, default=defaultValue, choices=eval(widget_action[7:]))                
            elif str(widget_action).lower() in ['dirchooser','filechooser','integerfield']: # widget
                op.add_argument(flag, flagLong, help=help, default=defaultValue, widget=widget_action, required=True)
            elif str(widget_action).lower() in ['store','count']: # action
                op.add_argument(flag, flagLong, help=help, action=widget_action, default=defaultValue)
            elif str(widget_action).lower() in ['store_true', 'store_false']: # action
                op.add_argument(flag, flagLong, help=help, action=widget_action, default=defaultValue)
            else:
                op.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
            return op

        for key in config_keys:
            #print(key, configObj['flag'][key])
            flag = "-" + configObj['flag'][key]
            flagLong = "--" + key
            typeValue = eval(configObj['type'][key])
            defaultValue = configObj['settings'][key]
            if defaultValue in ['True','False'] and typeValue==bool: defaultValue=eval(defaultValue)
            help = configObj['help'][key]
            widget_action = configObj['widget'][key]
            if typeValue==list: widget_action=eval(widget_action)
            #print(flag, flagLong, 'DEFAULT:',defaultValue, help, typeValue)
            if key in ['startfile','program_dir']: # required
                required = addArg(required)
            else:
                optional = addArg(optional)

                '''
                if type(widget_action) is list: # choice
                    required.add_argument(flag, flagLong, help=help, default=defaultValue, choices=widget_action)                
                elif str(widget_action).lower() in ['dirchooser','filechooser','integerfield']: # widget
                    required.add_argument(flag, flagLong, help=help, default=defaultValue, widget=widget_action, required=True)
                elif str(widget_action).lower() in ['store','count']: # action
                    required.add_argument(flag, flagLong, help=help, action=widget_action, default=defaultValue)
                elif str(widget_action).lower() in ['store_true', 'store_false']: # action
                    required.add_argument(flag, flagLong, help=help, action=widget_action, default=defaultValue)
                else:
                    required.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
            else:
                if type(widget_action) is list: # choice
                    optional.add_argument(flag, flagLong, help=help, default=defaultValue, choices=widget_action)                
                elif str(widget_action).lower() in ['dirchooser','filechooser','integerfield']: # widget
                    optional.add_argument(flag, flagLong, help=help, widget=widget_action, required=True)
                elif str(widget_action).lower() in ['store_true', 'store_false', 'store','count']: # action
                    optional.add_argument(flag, flagLong, help=help, action=widget_action)
                else:
                    optional.add_argument(flag, flagLong, default=defaultValue, type=typeValue, help=help)
            '''
            print(key, flag, flagLong, defaultValue, help, widget_action, typeValue, type(defaultValue))
                
    args = vars(parser.parse_args())
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



