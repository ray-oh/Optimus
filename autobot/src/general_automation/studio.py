#!/usr/bin/env python
"""
    Optimus Studio
    Description     Utility to help create Optimus RPA scripts
    Library         PySimpleGui

    Copyright 2021, 2022, 2023 Optimus
"""
# default program path
from pathlib import Path
prog_path = Path.cwd().parent.__str__() # d:\optimus
scriptKeywordsDefn = f'{prog_path}\\autobot\keywords.xlsx' #f'D:\Optimus\docs\scriptKeywordsDefn.xlsx'

# Optimus keyword command definition library and other utility
import pandas as pd
# read optimus script keyword definitions
def readfile(filepath = scriptKeywordsDefn):
    df = pd.read_excel(filepath, sheet_name=0) # can also index sheet by name or fetch all sheets
    df['Type']=df['Type'].fillna(method="ffill")
    df['Description']=df['Description'].astype(str)
    df['Command']=df['Command'].astype(str)    
    return df

df = readfile()
# returns field values of specified command key, and prefix token
def data_desc(key='rem:', field='Description', token=""):
    x = df[df.Command==key][field]
    if len(x)==0: return ""
    result = str(x.iloc[0])
    if result =="nan": 
        result=""
    else:
        result=token+result
    return result

# returns JSON object from string - else None
def readJSON(json_str):
    import json
    try:
        return json.loads(json_str)
    except:
        return None

def arg(values):    
    argstr = data_desc(key=values['listbox'][0], field='Arguments')    
    import json
    y = json.loads(x)
    return

import PySimpleGUI as sg
_width_win = 50 #50
_width_txt = _width_win - 5 #45
_font_header = ("Helvetica", 12, "bold")
_font_txt = ("Helvetica", 12, "bold") #sg.DEFAULT_FONT #("bold")

# Formula window
def formula_window(command):
    # PARAMETERS
    _width_win = 70 #50
    _width_txt = _width_win - 50 #45
    _font_header = ("Helvetica", 12, "bold")
    _font_txt = ("Helvetica", 12, "bold") #sg.DEFAULT_FONT #("bold")

    # LAYOUT COMPONENTS
    bar_command = [[sg.Text(f"{command}", font=_font_header)]] # size=(_width_win, 1), 
    def _bar_parameters():
        arguments_str = data_desc(key=command, field='Arguments',token="")
        args = readJSON(arguments_str)
        if args == None:
            bar_parameters = [[sg.Text(f"No parameters", size=(_width_txt, 1))]] #, font=_font_txt
        else:
            bar_parameters = [[]]
            for idx, arg in enumerate(args): #print(arg, idx)
                bar_parameters+=[[sg.Text(arg, size=(_width_txt, 1)), sg.Input('', enable_events=True, key=f"-INPUT{idx}-")]]
        return bar_parameters, args
    bar_parameters, args = _bar_parameters()
    bar_description = [[sg.Text(data_desc(key=command, field='Description',token="⏰ ")+"\n"+ \
                             data_desc(key=command, field='Syntax',token="✅ ")+"\n"+ \
                             data_desc(key=command, field='Parameters',token="⭐ ")+"\n"+ \
                             data_desc(key=command, field='Arguments',token="⬛ ")+"\n"+ \
                             data_desc(key=command, field='Documentation',token="⚠️ "),\
                               size=(45, 5), key='-DESCRIPTION-')]]
    bar_result = [[sg.Multiline(f"Input parameters and click COPY to generate formula ...\n{command}"\
                               , size=(_width_win, 3), key='-RESULT-')]]
    bar_bottom = [[sg.Push(), sg.Button(' Copy ', key='-COPY-'),sg.Button(' Cancel ', key='-CANCEL-')]]
    
    # LAYOUT
    layout = [[]] + bar_command + [[sg.Text("Parameters", font=_font_header)]] + bar_parameters + \
                [[sg.Text("Description", font=_font_header)]] + bar_description + \
                [[sg.Text("Result", font=_font_header)]] + bar_result + bar_bottom
                #layout.insert(2,parameterlist)
        
    # WINDOW CREATE / BINDINGS
    window = sg.Window("Functional Arguments", layout, modal=True, finalize=True)
    try:
        for idx, arg in enumerate(args):
            window[f"-INPUT{idx}-"].bind("<Return>", "_Enter")    # bind enter key event with input box
    except:
        pass
    window.bind("<Escape>", "_Escape")    
    
    # EVENT ACTIONS
    while True:
        event, values = window.read()
        print('*', event)
        if event == "-CANCEL-" or event == sg.WIN_CLOSED or "_Escape" in event:
            break
        if event == "-COPY-" or "_Enter" in event: #("-INPUT" in event and "_Enter" in event):
            print('COPY', event)
            result_rpa=""
            separator=""            
            try:
                for idx, arg in enumerate(args):
                    if result_rpa!="":separator=", "
                    result_rpa += separator+values[f"-INPUT{idx}-"]
            except:
                pass
            finally:
                result_rpa=f"{command}{result_rpa}"
                window['-RESULT-'].update(result_rpa)
                import pyclip
                pyclip.copy(result_rpa) # copy data to the clipboard
        
    window.close()

# Formula browser window
# main window - search for command
# data input window - update parameters
def search_rpa_commands_window():
    # PARAMETERS
    def strDiffs(oldstr, newstr):
        import difflib
        difflist = [li[2] for li in difflib.ndiff(oldstr, newstr) if li[0] == '+']
        return ''.join(difflist)
    
    # LAYOUT COMPONENTS
    # -SEARCH-, -GO- | dropbox: cmd_combolist, -COMBO- | cmd_list_str, -LISTBOX- | command, -DESCRIPTION- | -OPEN-, -EXIT-

    initialMsg = 'Type a brief description and click Go to search'
    bar_search = [[sg.Input(initialMsg, enable_events=True, key='-SEARCH-'), sg.Button(' Go ', key='-GO-')]]
    cmd_combolist = [''] + ['(Show All)'] + df['Type'].dropna().unique().tolist()
    bar_categorySelection = [[sg.Text('Or select a category:'), sg.Push(), \
                      sg.Combo(tuple(cmd_combolist), enable_events=True, key='-COMBO-')]] #, size=(_width_list, 1)
    command=""
    cmd_list = df[df['Command']!='nan']['Command'].tolist()
    cmd_list_str = tuple([k for k in cmd_list if isinstance(k,str)])
    bar_commandlist = [[sg.Listbox(values=cmd_list_str, size=(_width_win, 7), enable_events=True, key='-LISTBOX-')]]
    
    def cmd_description(command):
        return   data_desc(key=command, field='Description',token="⏰ ")+"\n"+ \
                 data_desc(key=command, field='Syntax',token="✅ ")+"\n"+ \
                 data_desc(key=command, field='Parameters',token="⭐ ")+"\n"+ \
                 data_desc(key=command, field='Arguments',token="⬛ ")+"\n"+ \
                 data_desc(key=command, field='Documentation',token="⚠️ ")
    
    bar_description = [[sg.Text(cmd_description(command), size=(45, 5), key='-DESCRIPTION-')]]    
    bar_bottom = [[sg.Push(), sg.Button(" Ok ", key="-OPEN-"), sg.Button(" Exit ", key="-EXIT-")]]
    
    # LAYOUT    
    layout = [[sg.Text('Search for a function:')]] + bar_search + \
                bar_categorySelection + [[sg.Text('Select a function:')]] + bar_commandlist + \
                bar_description + bar_bottom
    
    # WINDOW CREATE / BINDINGS
    window = sg.Window("Insert Function", layout, finalize=True)  # finalize true modifier required for key binding
    window[f"-SEARCH-"].bind("<Return>", "_Enter")    # bind enter key event with input box    #https://stackoverflow.com/questions/68528274/how-to-raise-an-event-when-enter-is-pressed-into-an-inputtext-in-pysimplegui
    window[f"-LISTBOX-"].bind("<Return>", "_Enter")
    window[f"-SEARCH-"].bind("<Escape>", "_Escape")
    
    prev_input = initialMsg
    prev_event = ''
    
    # EVENT ACTIONS
    # -SEARCH-, -GO- | dropbox: cmd_combolist, -COMBO- | cmd_list_str, -LISTBOX- | command, -DESCRIPTION- | -OPEN-, -EXIT-
    while True:        
        event, values = window.read()
        
        if event == "-EXIT-" or event == sg.WIN_CLOSED:     # or "_Escape" in event:
            break

        if event == '-SEARCH-' or event == '-SEARCH-_Escape': # Update -SEARCH- Search box
            if prev_input == initialMsg or values['-SEARCH-'] == initialMsg: # refresh search box
                incrementalStr = strDiffs(initialMsg, values['-SEARCH-'])
                window['-SEARCH-'].update(incrementalStr)                
            elif event == '-SEARCH-_Escape':                  # clear search box
                window['-SEARCH-'].update("")
            prev_input = values['-SEARCH-']
            
        if event in ['-GO-','-SEARCH-_Enter','-COMBO-']:  # Refresh cmd_list_str, trigger by searchStr or dropdown -COMBO-
            if event in ['-GO-', '-SEARCH-_Enter']:
                searchStr = values['-SEARCH-']
            elif event in ['-COMBO-']:
                searchStr = values['-COMBO-']
                if 'Show All' in searchStr or searchStr=="": searchStr = ''
            df2=df[['Command', 'Type','Description']].dropna()            
            mylist = df2[(df2['Command'].str.contains(searchStr, case=False)| \
                          df2['Description'].str.contains(searchStr, case=False))]['Command'].tolist()
            cmd_list_str = tuple([k for k in mylist if isinstance(k,str)])        
            window['-LISTBOX-'].update(cmd_list_str)            
            
        if event == "-OPEN-" or event=="-LISTBOX-_Enter":    # Launch Formula window
            if len(values['-LISTBOX-']):
                command = values['-LISTBOX-'][0]
                formula_window(values['-LISTBOX-'][0])

        if event == '-LISTBOX-' and not '# ---' in values['-LISTBOX-'][0]: # Refresh -DESCRIPTION- trigger by -LISTBOX- selection
            command = values['-LISTBOX-'][0]
            window['-DESCRIPTION-'].update(cmd_description(command))                        

        if prev_event != event:                             # Refresh prev event if event changed
            print(window.size, prev_event, event, values['-SEARCH-'])            
            prev_event = event
            
        if not event == '-SEARCH-' and values['-SEARCH-']=='':  # Reset Search Box if its blank and focus changed from INPUT
            window['-SEARCH-'].update(initialMsg)
            prev_input = initialMsg
                
    window.close()

# Launch windows
if __name__ == "__main__":
    search_rpa_commands_window()
