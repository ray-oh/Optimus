#!/usr/bin/env python
"""
    Application launcher for Optimus.
    Allows following actions:
        Run RPA scripts
        Settings
        And more!

    Copyright 2021, 2022, 2023 Optimus
"""
# default program path
from pathlib import Path
prog_path = Path.cwd().parent.__str__() # d:\optimus
scriptKeywordsDefn = f'{prog_path}\\autobot\keywords.xlsx' #f'D:\Optimus\docs\scriptKeywordsDefn.xlsx'

# Utility libraries
import PySimpleGUI as sg

# Resize image
from io import BytesIO
from pathlib import Path
from PIL import Image, UnidentifiedImageError
def resize(image_file, new_size, encode_format='PNG'):
    im = Image.open(image_file)
    #new_im = im.resize(new_size, Image.ANTIALIAS)
    new_im = im.resize((128, 128), Image.Resampling.LANCZOS)
    with BytesIO() as buffer:
        new_im.save(buffer, format=encode_format)
        data = buffer.getvalue()
    return data

# Optimus keyword command definition library and other utility

import pandas as pd
# read optimus script keyword definitions
def readfile(filepath = scriptKeywordsDefn, sheet_name=0):
    df = pd.read_excel(filepath, sheet_name) # can also index sheet by name or fetch all sheets
    if sheet_name=="Commands":
        df['Type']=df['Type'].fillna(method="ffill")
        df['Description']=df['Description'].astype(str)
        df['Command']=df['Command'].astype(str)
    if sheet_name=="Apps":
        df['Description']=df['Description'].astype(str)
        df['Label']=df['Label'].astype(str)        
    return df

df = readfile(filepath = scriptKeywordsDefn, sheet_name="Apps")
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

def launcher_window():
    # PARAMETERS    
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']] ]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing','More Nothing','Exit']]
    fcolor = 'dark slate gray'

    # LAYOUT COMPONENTS
    menu_bar = [ [sg.MenubarCustom(menu_def, key='-MENU-', tearoff=True)] ] #font='Courier 15',
    
    banner_textblock = [ [sg.Text('OPTIMUS RPA',background_color='white', text_color=fcolor, font=("Helvetica", 12, "bold"))],
            [sg.Text('Select required action ...',background_color='white', text_color=fcolor, font=("Helvetica", 11))] ]
    top_bar_banner = [[sg.Column(banner_textblock, background_color='white'), sg.Push(background_color='white'), 
                  sg.Image(data=resize('program_icon2.png', (150,60)), background_color='white')]]
    top_bar = [[sg.Frame('', top_bar_banner, background_color='white', size=(480,70) )]]
    
    # tab1 layout
    button_bar = [[]]
    tab = 'tab1'
    for idx, i in enumerate(df[df['Tab']==tab]["Label"].tolist()):
        #print(df["Label"][idx], df["Row"][idx], df["Col"][idx], df["Description"][idx], df["Launcher"][idx])
        button_bar +=  [[sg.Button(f"{i}", size=(16, 1), font=("Helvetica", 12, "bold"), 
                             k=f"-BUTTON{i}", enable_events=True),
                   sg.Text(f"{df[df['Tab']==tab]['Description'].tolist()[idx]}", size=(30, 1), 
                            justification='center', font=("Helvetica", 10), k=f"-BUTTON DESC{idx}-", enable_events=True)
                  ]] 
    tab1_layout =  button_bar
    
    # tab2 layout
    button2_bar = [[]]
    tab = 'tab2'    
    for idx, i in enumerate(df[df['Tab']==tab]["Label"].tolist()):
        #print(df["Label"][idx], df["Row"][idx], df["Col"][idx], df["Description"][idx], df["Launcher"][idx])
        button2_bar +=  [[sg.Button(f"{i}", size=(16, 1), font=("Helvetica", 12, "bold"), 
                             k=f"-BUTTON{i}", enable_events=True),
                   sg.Text(f"{df[df['Tab']==tab]['Description'].tolist()[idx]}", size=(30, 1), 
                            justification='center', font=("Helvetica", 10), k=f"-BUTTON DESC{idx}-", enable_events=True)
                  ]] 
    tab2_layout =  button2_bar

    # tab3 layout
    button3_bar = [[]]
    tab = 'tab3'    
    for idx, i in enumerate(df[df['Tab']==tab]["Label"].tolist()):
        #print(df["Label"][idx], df["Row"][idx], df["Col"][idx], df["Description"][idx], df["Launcher"][idx])
        button3_bar +=  [[sg.Button(f"{i}", size=(16, 1), font=("Helvetica", 12, "bold"), 
                             k=f"-BUTTON{i}", enable_events=True),
                   sg.Text(f"{df[df['Tab']==tab]['Description'].tolist()[idx]}", size=(30, 1), 
                            justification='center', font=("Helvetica", 10), k=f"-BUTTON DESC{idx}-", enable_events=True)
                  ]] 
    tab3_layout =  button3_bar
    
    #logging_layout = [[sg.Text("Anything printed will display here!")],
    #                  [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
    #                                reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
    #                  ]

    # LAYOUT
    layout = menu_bar + top_bar                
    layout +=[[sg.TabGroup([[  sg.Tab('OPTIMUS CORE', tab1_layout),
                               sg.Tab('SETTINGS', tab2_layout),
                               sg.Tab('AGENTS', tab3_layout),
                            ]], key='-TAB GROUP-', expand_x=True, expand_y=True),
               ]]
    layout[-1].append(sg.Sizegrip())
    
    # WINDOW CREATE / BINDINGS    
    win_title = f'OPTIMUS - Do more with less'
    window = sg.Window(win_title, layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)
    window.set_min_size(window.size)
    window.bind("<Escape>", "_Escape")    
    #return window

    # window = make_window() # sg.theme() 
    
    # EVENT ACTIONS    
    while True: # Event Loop
        event, values = window.read()

        if event in ("-EXIT-", sg.WIN_CLOSED, "_Escape"):
            break

        if '-BUTTON' in event:
            print(event, str(event)[7:]) #, df[df['Label']==str(event)[7:]]['Description'][0])
            label_str = str(event)[7:]
            program = df[df['Label']==label_str]['Launcher'].tolist()[0]            
            type = df[df['Label']==label_str]['Type'].tolist()[0]
            if type in ('win'): 
                command = program.split(" ")
                shell=True
            else: 
                command = [f'{prog_path}\{program}']
                shell=False
            print(program, command)
            import subprocess
            #if len(program.split(" "))>1:
            #    #subprocess.call([program.split(" ")[0], program.split(" ")[1], program.split(" ")[2] ])
            #    subprocess.call(program.split(" "))                
            #elif len(program.split(" "))==1:
            #subprocess.call(["D:\\optimus\\" + program])
            proc = subprocess.Popen(command, shell=shell)   # non blocking

        if event in ("About"):#event == 'About':
            print("MENU Clicked", event)
            #gui(window, key)            
            
    window.close()


if __name__ == '__main__':
    launcher_window()


