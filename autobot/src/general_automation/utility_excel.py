# Is file1 newer, return True or False
import os.path
import datetime
import time
def isFileNewer(file1, file2, type="m"):
    # m = modified, c = creation date
    if type == "m":
        #local_time_file1 = time.ctime(os.path.getmtime(file1))
        #local_time_file2 = time.ctime(os.path.getmtime(file2))            
        #print("mtime (Local time):", local_time_file1, local_time_file2)
        return os.path.getmtime(file1) > os.path.getmtime(file2)
    elif type == "c":
        #local_time_file1 = time.ctime(os.path.getctime(file1))
        #local_time_file2 = time.ctime(os.path.getctime(file2))            
        #print("ctime (Local time):", local_time_file1, local_time_file2)
        return os.path.getctime(file1) > os.path.getctime(file2)
    else:
        return

# Use pickle file for caching
# Instead of this - use pd.read_pickle
import pickle    
def pickle_storeData(db={}, dbfilename='example.pickle'):
    if db=={}: return
    #print(db)
    # Its important to use binary mode
    dbfile = open(dbfilename, 'ab')
    
    # source, destination
    pickle.dump(db, dbfile)                   
    dbfile.close()
    return

def pickle_loadData(dbfilename='example.pickle'):
    # for reading also binary mode is important
    dbfile = open(dbfilename, 'rb')   
    db = pickle.load(dbfile)
    #for keys in db:
    #    print(keys, '=>', db[keys])
    dbfile.close()
    return db

# Check if cache exist - use cache, else keep a cache
import pandas as pd
from pathlib import Path
from auto_helper_lib import try_catch, readExcelConfig
from sys_variables import log_space
def cacheScripts(script='OptimusLib.xlsm', df=pd.DataFrame(), program_dir = "D:/optimus/", startsheet = "main", refresh=False, msgStr=''):
    script_name = Path(script).stem   # without extension     
    scriptPath = Path(program_dir).joinpath( 'scripts', script )
    scriptPathCache = Path(program_dir).joinpath( 'scripts', '_cache', script_name + '.pickle' )        
    if scriptPath.exists():
        if scriptPathCache.exists() and isFileNewer(scriptPathCache.__str__(), scriptPath.__str__()) and not refresh:
            # use cache file if cache file is newer
            df_script = pd.read_pickle(scriptPathCache.__str__())
            if not msgStr == '': msgStr = msgStr + "\n"
            msgStr = msgStr + f"     {log_space}{script_name} ---- from Cache"
            #logger.debug(f"{msgStr}")
        else:
            df_script = try_catch(readExcelConfig(sheet=startsheet, excel=str(scriptPath) , refresh=refresh )) #Path(program_dir).stem.__str__() + "OptimusLib"))
            #logger.debug(f"{log_space}{script_name} ---- read from Excel")
            if not msgStr == '': msgStr = msgStr + "\n"
            msgStr = msgStr + f"     {log_space}{script_name} ---- from Excel"
            #logger.debug(f"{msgStr}")                
            #pickle_storeData(dfmain_lib, optimusLibraryPathCache.__str__())
            pd.to_pickle(df_script, scriptPathCache.__str__())
        if df.empty:
            df = df_script
        else:
            df = pd.concat([df, df_script], ignore_index=True, sort=False)    # append optimus library commands
    return df, msgStr
