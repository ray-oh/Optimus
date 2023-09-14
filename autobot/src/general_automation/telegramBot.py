# Setup a telegramBot program and a prefect Query API for job status and running jobs
# Batch file setup to run this program as an agent to hook up with telegram bot
# Bot token/password is stored in Chrome and retrieved with passwords library
# Refer to below on how to setup the batch file to run in minimized mode from windows task scheduler
# https://datacornering.com/run-batch-file-minimized/#:~:text=Here%20is%20a%20simple%20example,adjustments%20in%20the%20Actions%20tab.&text=%E2%80%9C%5E%26%20exit%E2%80%9D%20at%20the,the%20batch%20file%20is%20executed.
'''
https://levelup.gitconnected.com/fixing-your-ssl-verify-errors-in-python-71c2201db4b2
certificate verify failed: unable to get local issuer certificate (_ssl.c:1007)
How to fix your SSL Errors - because your company is using SSL Decryption and you are on windows:
python -m pip install python-certifi-win32
'''
# Uses asynchronous code - https://superfastpython.com/async-await-python/

# Asynchronous client implementation for communicating with the Prefect REST API.
# https://docs.prefect.io/2.11.0/api-ref/prefect/client/orchestration/
from prefect import get_client
from prefect.server.schemas.core import FlowRun
from prefect.server.schemas.filters import (
    FlowFilter,
    FlowFilterName,    
    FlowRunFilter,
    FlowRunFilterName,
    FlowRunFilterState,    
    FlowRunFilterStateName, 
    FlowRunFilterStartTime,    
    DeploymentFilter,
    DeploymentFilterName,
    FlowRunFilterId,
    FlowFilterId,
)

import asyncio
from prefect.client import get_client


async def remove_all_flows():
    orion_client = get_client()
    flows = await orion_client.read_flows(
            #flow_filter=FlowFilter(name=FlowFilterName(like_=flowname)),       #{"any_": ["serviceNow"]}),
            limit=15,
            flow_run_filter=FlowRunFilter(
                state=FlowRunFilterState(
                    type=FlowRunFilterStateName(any_=["RUNNING"])
                ),
                #start_time=FlowRunFilterStartTime(
                #    after_=start_time
                #)
            ))
    result = ''
    for flow in flows:
        flow_id = flow.id
        #print(f"Deleting flow: {flow.name}, UUID {flow_id}")
        await orion_client._client.delete(f"/flows/{flow_id}")
        #print(f"Flow with UUID {flow_id} deleted")
        if result != '': result = result + '\n'
        result = result + f"Deleted flow: {flow.name}, UUID {flow_id}"
    return result


def localTime(st_utc, _timezone):
    #https://stackoverflow.com/questions/1111317/how-do-i-print-a-datetime-in-the-local-timezone
    #https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568  timezone list
    import pytz
    from datetime import datetime, timezone
    from tzlocal import get_localzone            
    #st_utc = flow.start_time  #.strftime("%d/%m %H:%M") #/%Y  :%S")  uiversal time
    HKT = pytz.timezone(_timezone) #"Asia/Hong_Kong")
    st = st_utc.astimezone(HKT).strftime("%d/%m %H:%M")  #.isoformat()
    return st

async def prefectQuery(hours=24*1, flowname="", param="J"):
    from datetime import datetime, timedelta
    start_time = datetime.now() - timedelta(hours=hours)  # minutes

    if "J" in param:
        _flow_run_filter=FlowRunFilter(
        #    state=FlowRunFilterState(
        #        type=FlowRunFilterStateName(any_=["RUNNING", "COMPLETED", "FAILED"])    # "COMPLETED"
        #    ),
            start_time=FlowRunFilterStartTime(
                after_=start_time
            )
        )
        pass
    elif "R" in param:
        _flow_run_filter=FlowRunFilter(
            state=FlowRunFilterState(
                type=FlowRunFilterStateName(any_=["RUNNING"])    # "COMPLETED"
            ),
            start_time=FlowRunFilterStartTime(
                after_=start_time
            )
        )
    elif "F" in param:
        _flow_run_filter=FlowRunFilter(
            state=FlowRunFilterState(
                type=FlowRunFilterStateName(any_=["FAILED", "CRASHED"])    # "COMPLETED"
            ),
            start_time=FlowRunFilterStartTime(
                after_=start_time
            )
        )

    async with get_client() as client:
        r = await client.read_flow_runs(
            flow_filter=FlowFilter(name=FlowFilterName(like_=flowname)),       #{"any_": ["serviceNow"]}),
            limit=50,
            flow_run_filter=_flow_run_filter)
        import socket
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname) 
        result = f"{hostname} VM{IPAddr.split('.')[3]}"
        def myFunc(e):
            print(e)
            return len(e) #e['start_time']
        #r.sort() #key=myFunc)
        # sort list by `name` in the natural order
        r.sort(key=lambda x: x.start_time)
        for flow in r:
            #pass
            td = flow.total_run_time # timedelta object
            
            st = localTime(flow.start_time, "Asia/Hong_Kong")

            duration = ':'.join(str(td).split(':')[:2])
            if 'Completed' in flow.state_name:
                status = ' ✅'
            elif 'Failed' in flow.state_name:
                status = '❌'
            elif 'Crashed' in flow.state_name:
                status = '⛔️'
            elif 'Running' in flow.state_name:
                status = '⚡️'            
            else:
                status = '⚠️' #'✋🆗👉'❕⚠️⛔️⚡️🔥
            
            # use flow id from flow run, to get flow name from read flows
            f = await client.read_flows(
                limit=50,
                flow_run_filter=FlowRunFilter(
                    #state=FlowRunFilterState(
                    #    type=FlowRunFilterStateName(any_=["COMPLETED"])
                    #),
                    #flow_run_filter_id=FlowRunFilterId(id=FlowRunFilterId(any_=[flow.id])),
                    #flow_run_filter_id=FlowRunFilterId(id=FlowRunFilterId(any_=[flow.id])),
                    #flow_filter=FlowFilter(id=FlowFilterId(any_=[flow_id])),
                    #flow_filter=FlowFilter(id=FlowFilterId(any_=[flow.id])),
                    id=FlowFilterId(any_=[flow.id]),  
                    # refer to link below on documentation for how to use FlowRunFilter:
                    #https://docs.prefect.io/2.10.12/api-ref/server/schemas/filters/#prefect.server.schemas.filters.FlowRunFilter
                    start_time=FlowRunFilterStartTime(
                        after_=start_time
                    )
            ))
            zflowName = f[0].name  # flow.parameters['deploymentname'].split('-C')[0][:8]  Instead of using the deployment name, get actual flow name
            # note this flow name is different from flow.name below which is name of the instance of flow run
            text = [st, f'({duration})', status, zflowName[:8] , flow.name.split('-')[1][:7]  ] #flow.state_name[:3]
            text = " ".join(text)
            result = result + '\n' + text
            
            #print(flow.name, flow.state_name, flow.parameters['deploymentname'],
            #      flow.start_time.strftime("%m/%d/%Y, %H:%M:%S"), flow.total_run_time)
            #print(flow.name, flow.flow_id, flow.created)    #https://discourse.prefect.io/t/flow-run-filter-with-flowrunfilterstarttime-doesnt-return-all-runs/2486
        #print(r)
        return result #+ str(r[0])

if __name__ == "__mainXXX__":
    import asyncio
    #asyncio.run(demo())  # replace this with next statement when running asyncio in jupyter notebook
    #https://stackoverflow.com/questions/55409641/asyncio-run-cannot-be-called-from-a-running-event-loop-when-using-jupyter-no
    print(asyncio.run(prefectQuery()))


# https://github.com/python-telegram-bot/python-telegram-bot
# python-telegram-bot added to requirements.txt


# https://github.com/erdewit/nest_asyncio
# https://github.com/python-telegram-bot/python-telegram-bot/issues/3251
# when using jupyter notebook to run this - add the following 2 lines
import nest_asyncio
nest_asyncio.apply()

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

validUser = ['raymondoh097']
# validUser should be read from a safe cache not published to github.
# user excel list
# user can submit name for approval by someone with access
# upon approval, move name to valid list

def userAuthorized(user):
    return user in validUser

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    #user2 = update.message.from_user
    print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))

    global token
    token='start'
    #await update.message.reply_html(
    #    rf"Hi {user.mention_html()}!",
    #    reply_markup=ForceReply(selective=True),
    #)
    if not(userAuthorized(user['username']) or userAuthorized(str(user['id']))):
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! You are not authorized",
        )
        return

    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to Optimus V5.  You can check status of jobs(list) or run specific jobs",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    global token
    token='help'    
    await update.message.reply_text("Help!")

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""
    global token
    token='list'

    # authorization checks
    user = update.effective_user    
    if not(userAuthorized(user['username']) or userAuthorized(str(user['id']))):
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! You are not authorized",
        )
        return

    await update.message.reply_html(
        rf"What do you want to list: type J (job status - optional hours e.g. J24), R (running), F (fail, crashed) or S (available scripts) or D (delete running flow runs)",
        reply_markup=ForceReply(selective=True),
    )
    print(token)
    
async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /run is issued."""
    #await update.message.reply_text("Run!")
    global token
    token='run'

    # authorization checks
    user = update.effective_user    
    if not(userAuthorized(user['username']) or userAuthorized(str(user['id']))):
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! You are not authorized",
        )
        return

    await update.message.reply_html(
        rf"Enter name of flow to run: (shortcut:1=prefectdashboard)",
        reply_markup=ForceReply(selective=True),
    )
    print(token)
    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    global token
    print(f'echo {token}')
    def runRPA(script):
        from pathlib import Path
        currentPath = Path().resolve().parent / "runRPA.bat"   #Path().resolve().parent.parent / "runRPA.bat"
        scriptFile = Path().resolve().parent / "scripts" / f"{script}.xlsm"
        runBatchCommand = rf'{str(currentPath)} -f {script}'
        #currentPath = pathlib.Path().parent.resolve() #.parent[1]
        #await update.message.reply_text(rf'run: {update.message.text} | {os.getcwd()} | {str(currentPath)}')    
        if currentPath.exists() and scriptFile.exists():
            #await update.message.reply_text(rf'run: {str(currentPath)} -f {update.message.text}')
            #https://stackoverflow.com/questions/21936597/blocking-and-non-blocking-subprocess-calls
            import subprocess
            proc = subprocess.Popen(runBatchCommand, shell=True)
            return True
        else:
            return False

    if token=='run':
        import os
        print("Path at terminal when executing this file")
        print(os.getcwd() + "\n")

        if update.message.text == "1":
            script="prefectdashboard"
        else:
            script=update.message.text            
        if runRPA(script=script):
            await update.message.reply_text(rf'Processed script: {script}')
        else:
            await update.message.reply_text(rf'run file does not exist: {update.message.text}')
    elif token=='list':
        if update.message.text.upper()[:1] in 'JRF' or update.message.text=='':
            import asyncio
            param = update.message.text.upper()
            h=int('0'+param[1:])
            if h==0: h=24*1  # default 24 hours
            result = await prefectQuery(hours=h, param=param)
            await update.message.reply_text(result)
        elif update.message.text.upper() == 'D':
            import asyncio
            result = await remove_all_flows()   # remove all running flow runs
            #result = await prefectQuery()
            await update.message.reply_text(result)
        elif update.message.text.upper() == 'P':
            # print screen
            def printscreen():
                # Importing Image and ImageGrab module from PIL package 
                from PIL import Image, ImageGrab                    
                # creating an image object
                #im1 = Image.open(r"C:\Users\sadow984\Desktop\download2.JPG")
                    
                # using the grab method
                im2 = ImageGrab.grab(bbox = None)
                #im2.show()
                # save a image using extension
                im2 = im2.save("D:\OneDrive-Sync\OneDrive - Christian Dior Couture\Shared Documents - RPA Project-APAC_FIN\screen.jpg")
            printscreen()
            await update.message.reply_text('Print screen')
        elif update.message.text.upper() == 'S':
            import os
            from pathlib import Path
            scriptPath = Path().resolve().parent / "scripts"
            dir_path = str(scriptPath) # folder path #r'E:\account'
            res = []                # list to store files
            # Iterate directory
            for file in os.listdir(dir_path):
                if file.endswith('.xlsm'):                  # check only text files
                    res.append(file[:-5])
            #print(res)
            await update.message.reply_text(rf'Scripts: {res}')            
        else:
            await update.message.reply_text(rf'Did not understand your command: {update.message.text}')
    else:
        await update.message.reply_text(rf'Normal echo: {update.message.text}') 
        #await update.message.reply_text(update.message.text)
    token='echo'    

async def echo2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(rf'echo 2: {update.message.text}')    
    global token
    token='echo2'    
    
from passwords import returnPassword

#BOT_TOKEN = is stored in chrome browser password manager "5918xxxxxx" #os.environ.get('BOT_TOKEN')
BOT_TOKEN = returnPassword(username_value="optimusRPA_bot")

#async 
def main() -> None:
    # Run the bot until the user presses Ctrl-C
    #await
    application.run_polling()

token = 0

if __name__ == "__main__":
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("run", run_command))    

    # on non command i.e message - echo the message on Telegram
    # https://docs.python-telegram-bot.org/en/stable/telegram.ext.filters.html
    #application.add_handler(MessageHandler(filters.REPLY & ~filters.COMMAND, echo2))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    main()


