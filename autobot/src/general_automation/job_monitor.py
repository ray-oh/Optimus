# Global variables
#from config import memoryPath
# memoryPath = "D:\OneDrive-Sync\OneDrive\Shared Documents - RPA Project-APAC_FIN\Status"

#from config import MEMORYPATH
#memoryPath = MEMORYPATH #r"\Optimus\memory"
#D:\OneDrive-Sync\OneDrive\Shared Documents - RPA Project-APAC_FIN\Status"

# create or update file
#memoryPath = MEMORYPATH
def touchFile(filename):
    from pathlib import Path
    Path(filename).touch()
    return True

#touchFile(rf"{memoryPath}\fail\sense_start_time.txt")        

import yaml
# write python obj to yaml file
def write_yaml(py_obj,filename):
    with open(f'{filename}', 'w',) as f :
        yaml.dump(py_obj,f,sort_keys=False) 
    #print('Written to file successfully')
    return True

# read yaml to python obj/dictionary
def read_yaml(filename):
    with open(f'{filename}','r') as f:
        output = yaml.safe_load(f)
    #print(output)
    return output

# file age in seconds
import os, time
def file_age(filepath):
    seconds = time.time() - os.path.getmtime(filepath)    
    return int(seconds)

# return timestamp in format '230817_141844'
def timestamp():
    import calendar
    import time
    from datetime import datetime      
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(time_stamp)
    return date_time.strftime("%y%m%d_%H%M%S") #("%d-%m-%Y, %H:%M:%S")

# returns list of files in path in sort order by modified datetime
import os
def getfiles(dirpath, reverse=False):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)), reverse=reverse)
    return a

'''
# change state of token
def stateChange(token="test", statefrom="start", stateto="stop"):
    try:
        #script="test"
        #statefrom="start"
        #stateto="stop"
        import os
        import shutil
        source=rf"{memoryPath}\{statefrom}\{token}.txt"
        dest=rf"{memoryPath}\{stateto}\{token}.txt"
        destination = shutil.move(source, dest)
    except FileNotFoundError:
        print("Token not found")
        return False
    return True
'''

# change state of token
def stateChange(token="test.txt", statefrom="start", stateto="stop", changeName='', memoryPath=''):
    try:
        #script="test"
        #statefrom="start"
        #stateto="stop"
        import os
        import shutil

        from pathlib import Path
        if not Path(rf"{memoryPath}\{statefrom}\{Path(token).stem}.txt").exists():
            tokenObj = tokenCreate()
            tokenSave(tokenObj,stateto,token)

        if stateto=="process":
            touchFile(rf"{memoryPath}\{stateto}\{Path(token).stem}.txt")

        if changeName=='': changeName=token
        source=rf"{memoryPath}\{statefrom}\{token}"#".txt"
        dest=rf"{memoryPath}\{stateto}\{changeName}"#".txt"
        destination = shutil.move(source, dest)
    except FileNotFoundError:
        print(f"StateChange from {statefrom} to {stateto}: Token {token} not found")
        return False
    return True

# launch token
from pathlib import Path
def runRPAscript(script="test", flags=""):
    currentPath = Path().resolve().parent / "runRPA.bat"   #Path().resolve().parent.parent / "runRPA.bat"
    scriptFile = Path().resolve().parent / "scripts" / f"{script}.xlsm"
    runBatchCommand = rf'{str(currentPath)} -f {script} {flags}'
    #print(runBatchCommand)
    if currentPath.exists() and scriptFile.exists(): # and False:
        #https://stackoverflow.com/questions/21936597/blocking-and-non-blocking-subprocess-calls
        import subprocess
        proc = subprocess.Popen(runBatchCommand, shell=True)
        print("*** LAUNCH:", script, ' | ' ,runBatchCommand)
        return True
    return False

def tokenCreate():
    from config import STARTFILE, STARTSHEET, STARTCODE, PROGRAM_DIR, UPDATE, BACKGROUND #, RETRIES, MEMORYPATH
    token = {}
    token['update']=UPDATE
    token['startfile']=STARTFILE
    token['startsheet']=STARTSHEET
    token['startcode']=STARTCODE
    token['background']=BACKGROUND
    token['program_dir']=PROGRAM_DIR
    print('Token',token)
    return token

def tokenSave(token, state, file='', memoryPath=''):
    from pathlib import Path
    if file=='': file = token['startfile']
    return write_yaml(token, rf"{memoryPath}\{state}\{Path(file).stem}.txt")

# trigger RPA event by generating token in pending
def triggerRPA(file, memoryPath=''):
    if file =='': return False
    from pathlib import Path, PureWindowsPath
    #print(f"background:{background}")
    state="pending"
    #from config import MEMORYPATH    
    if memoryPath=='': #memoryPath=MEMORYPATH
        return False
    #write_yaml_to_file(data, 'output.txt')
    token = tokenCreate()
    print('LAUNCH RPA SCRIPT:', Path(file).stem, tokenSave(token,state,file))

    result = read_yaml(rf"{memoryPath}\{state}\{Path(file).stem}.txt")
    print(result)
    return True


# Monitor token jobs in pending to activate every 15 seconds.  Only when nothing in start and in process.
# Change token status to start.  And launch job - which will update token status to process and then complete
# Option in script to update status to a parallel run non blocking run.  May be distinguish with prefix or suffix
# Tokens are queued - first in first out.
# Prefect/task scheduler to only touch a token in pending to queue for activation.
# Exception handling for frozen jobs - check age of jobs - if above threshold, delete blocking token, stop/cancel/delete prefect job
def monitor(memoryPath=''):
    import time
    print('''
    ##################################################
            OPTIMUS JOB MONITOR AND QUEUE
    ##################################################
    ''')
    nonBlockingProcessTokens2=[]
    nonBlockingPendingTokens2=[]
    pendingTokens2=[]
    startTokens2=[]
    processTokens2=[]
    completeTokens2=[]
    while True:
        import time
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        #print(curr_time, ': heartbeat')
        #print('test', keepalive)

        nonBlockingProcessTokens=[]
        nonBlockingPendingTokens=[]
        pendingTokens=getfiles(memoryPath+"\pending")
        startTokens=getfiles(memoryPath+"\start")
        processTokens=getfiles(memoryPath+"\process")
        completeTokens=getfiles(memoryPath+"\complete")

        if len(processTokens)>0:
            for item in processTokens:
                state='process'
                token = read_yaml(rf"{memoryPath}\{state}\{item}")
                if not token==None:
                    if 'background' in token:
                        if '5' in token['background']:
                            nonBlockingProcessTokens = nonBlockingProcessTokens + [item]
                            processTokens = processTokens.remove(item)
                            if processTokens == None: processTokens = []

        if len(pendingTokens)>0:
            for item in pendingTokens:
                state='pending'
                token = read_yaml(rf"{memoryPath}\{state}\{item}")
                if not token==None:
                    if 'background' in token:
                        if '5' in token['background']:
                            nonBlockingPendingTokens = nonBlockingPendingTokens + [item]
                            pendingTokens = pendingTokens.remove(item)
                            if pendingTokens == None: pendingTokens = []                        

        pendingTokens=pendingTokens[:1] + nonBlockingPendingTokens

        if nonBlockingProcessTokens2==nonBlockingProcessTokens and nonBlockingPendingTokens2==nonBlockingPendingTokens \
            and pendingTokens2==pendingTokens and startTokens2==startTokens and processTokens2==processTokens and completeTokens2==completeTokens:
            pass
        else:
            print('-----------------------------------------------------------------------------------------------------------------')
            print(curr_time, ': pending:',pendingTokens, 'start:',startTokens, 'process:', processTokens, 'nonBlockingPendingTokens:', 
                        nonBlockingPendingTokens, 'nonBlockingProcessTokens', nonBlockingProcessTokens)
            print('-----------------------------------------------------------------------------------------------------------------')
        if len(pendingTokens)>0 and len(startTokens)==0 and len(processTokens)==0:
            print('=============================================================================')

            from pathlib import Path
            state='pending'

            for item in pendingTokens:
                token = read_yaml(rf"{memoryPath}\{state}\{item}")
                print(token)

                # check if script contains flow run name if yes - append to token
                from pathlib import Path
                script = item
                if len(Path(script).stem.split('='))>1:
                    flow_run_name = Path(script).stem.split('=')[1]
                else:
                    flow_run_name = 'None'
                token['flow_run_name'] = flow_run_name
                write_yaml(token,rf"{memoryPath}\{state}\{item}")
                script = Path(script).stem.split('=')[0]
                
                print("PENDING -> START:",stateChange(item,'pending','start'))

                flags=""
                if not token==None:
                    if 'update' in token:
                        if str(token['update']).strip() in '01234' and not str(token['update']).strip()=='':
                            flags=f"-u {token['update']}"
                            #print(f"-u |{token['update']}| {type(token['update'])}")
                #runRPAscript(script=Path(f"{pendingTokens[0]}").stem, flags=flags)
                runRPAscript(script=Path(f"{script}").stem, flags=flags)        
                print('=============================================================================')        
        for token in processTokens:    # check age of tokens in process
            if not token in nonBlockingProcessTokens:
                state='process'
                token_path = rf"{memoryPath}\{state}\{token}"
                token_age = file_age(token_path)
                age_limit = 60*5 # 5 min
                if token_age>age_limit:
                    #print('token age', token_age, 'remove',token)
                    #os.remove(token_path)
                    print('=============================================================================')            
                    print(rf"FAIL <- {timestamp()}_{state} {token} {int(token_age/60)}min:",
                        stateChange(token,state,'fail',f"{timestamp()}_{state}_{token}"))
                    print('=============================================================================')                              
        for token in startTokens:    # check age of tokens in process
            state='start'
            token_path = rf"{memoryPath}\{state}\{token}"
            token_age = file_age(token_path)
            age_limit = 60*2 # 2 min
            if token_age>age_limit:
                #print('token age', token_age, 'remove',token)
                #os.remove(token_path)
                print('=============================================================================')                        
                print(rf"FAIL <- {timestamp()}_{state} {token} {int(token_age/60)}min:",
                    stateChange(token,state,'fail',f"{timestamp()}_{state}_{token}"))
                print('=============================================================================')

        nonBlockingProcessTokens2=nonBlockingProcessTokens
        nonBlockingPendingTokens2=nonBlockingPendingTokens
        pendingTokens2=pendingTokens
        startTokens2=startTokens
        processTokens2=processTokens
        completeTokens2=completeTokens

        time.sleep(15)

if __name__ == "__main__":
    monitor()