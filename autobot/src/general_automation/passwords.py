# Extracts password word from Chrome browser password manager
# https://www.thepythoncode.com/article/extract-chrome-passwords-python
# Required libraries
# pip3 install pycryptodome pypiwin32
# Added pycryptodome and pypiwin32 to requirements.txt

# Other methods
# https://pythonhow.com/how/store-python-passwords-securely-on-windows-mac-and-linux/


import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

# local sqlite Chrome database path
chromePath = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    #local_state_path = os.path.join(os.environ["USERPROFILE"],
    #                                "AppData", "Local", "Google", "Chrome",
    #                                "User Data", "Local State")
    local_state_path = os.path.join(chromePath, "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""

#username_value="optimusRPA_bot"
def returnPassword(**kwargs):
    # site username password
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    #db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
    #                        "Google", "Chrome", "User Data", "default", "Login Data")
    db_path = os.path.join(chromePath, "default", "Login Data")
    #print(db_path, chromePath, os.path.join(chromePath, "default", "Login Data"))
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    condition = ''
    if "username" in kwargs:
        if not kwargs['username']=='':
            condition = f'username_value="{kwargs["username"]}"'
    if "site" in kwargs:
        if condition != '': condition = condition + ' and'
        condition = f'{condition} origin_url like "%{kwargs["site"]}%"'
    condition = 'where ' + condition
    print(condition)
    statement = f'select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins {condition} order by date_created'
    print(statement)
    cursor.execute(statement)
    #cursor.execute('select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins where username_value="optimusRPA_bot" and origin_url like "%telegram%" order by date_created')    
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            #print(f"Password: {password}")
            print(f"Password: *************")

            cursor.close()
            db.close()
            try:
                # try to remove the copied db file
                os.remove(filename)
            except:
                pass
            return password
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass

#username_value="optimusRPA_bot"
def retrieveSecret(**kwargs):
    # site username password
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    #db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
    #                        "Google", "Chrome", "User Data", "default", "Login Data")
    db_path = os.path.join(chromePath, "default", "Login Data")
    #print(db_path, chromePath, os.path.join(chromePath, "default", "Login Data"))
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    condition = ''
    if "username" in kwargs:
        if not kwargs['username']=='':        
            condition = f'username_value="{kwargs["username"]}"'
    if "site" in kwargs:
        if condition != '': condition = condition + ' and'
        condition = f'{condition} origin_url like "%{kwargs["site"]}%"'
    condition = 'where ' + condition
    #print(condition)
    statement = f'select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins {condition} order by date_created'
    #print(statement)
    cursor.execute(statement)
    #cursor.execute('select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins where username_value="optimusRPA_bot" and origin_url like "%telegram%" order by date_created')    
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            #print(f"Password: {password}")
            print(f"Password: *************")

            Secret = {
                'site':f'{origin_url}',
                'key':f'{username}',
                'value':f'{password}'
                }
            #print(Secret)
            cursor.close()
            db.close()
            try:
                # try to remove the copied db file
                os.remove(filename)
            except:
                pass
            return Secret #password
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass

def domain(url):
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    return domain


def retrieveHttpCredentials(url, user='', origin=''):
    from passwords import returnPassword, retrieveSecret
    if not origin=='': url=origin
    _domain = domain(url)
    print('_domain', _domain.__str__())
    #BOT_TOKEN = returnPassword(username="optimusRPA_bot", site="telegram")
    SECRET = retrieveSecret(site=_domain, username=user) #"https://qliksense.fashion/")
    if SECRET==None: return {'username': '', 'password': ''}
    http_credentials = {}
    http_credentials['username'] = SECRET['key']
    http_credentials['password'] = SECRET['value']
    #http_credentials['origin'] = SECRET['site']
    #print(http_credentials)
    return http_credentials

def main():
    print(returnPassword(username_value="optimusRPA_bot"))

def testmain():
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute('select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins where username_value="optimusRPA_bot" and origin_url like "%telegram%" order by date_created')
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass

if __name__ == "__main__":
    main()


