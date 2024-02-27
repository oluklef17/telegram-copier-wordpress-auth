import os
import sys
import time
from threading import Thread
from datetime import datetime, timedelta
from queue import Queue
import asyncio
import os
import socket
import subprocess
from telethon import TelegramClient, events, utils
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import ui, queue_in, queue_out

ui = None

assets = dict()

binaryToken = ""

parentDirectory = os.getcwd()


LastTradeInfo = ""

currentList = list()

channel_list = list()

allowed_chats = list()

MQL4_paths = list()

lastWarning = ""




def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            log(e, file=sys.stderr)
            time.sleep(1)


session = "user"  # os.environ.get('TG_SESSION', 'loger')
api_id = 19533412
api_hash = "244adfc8d6a54f85df6958ac3823e203"
proxy = None  # https://github.com/Anorov/PySocks

# Create and start the client so we can make requests (we don't here)


# `pattern` is a regex, see https://docs.python.org/3/library/re.html
# Use https://regexone.com/ if you want a more interactive way of learning.
#
# "(?i)" makes it case-insensitive, and | separates "options".
def log(*args):
    arguments = list()
    
    for arg in args:
        arguments.append(str(arg))

    msg = ''.join(arguments)

    ui.authWarning.setText(msg)

    current_time = time.time()
    log_text = str(datetime.utcfromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')) + ' - ' + msg
    #ui.logList.addItem(log_text)
    date = str(datetime.utcfromtimestamp(current_time).strftime('%Y-%m-%d'))

    log_file = os.path.join('logs', f'log_{date}.txt')

    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
            with open(log_file, 'w') as f:
                f.write(log_text+'\n')
        else:
            with open(log_file, 'a') as f:
                f.write(log_text+'\n')
    except Exception as e:
        log('Could not write log to file: ',e)

def run_bot(queue_in, queue_out):
    # if os.path.exists(f"{session}.session") == False:
    #     ui.stackedWidget.setCurrentIndex(2)
    #     log('Not logged in. Will attempt to launch login terminal.')
    #     login = None
    #     path = 'login.exe'
    #     if os.path.exists(path):
    #         try:
    #             login = subprocess.Popen(path)
    #             os._exit(0)
    #         except Exception as e:
    #             log('Failed to open login exe. Error = ',e)
    # else:
    #     ui.stackedWidget.setCurrentIndex(0)
            
    global ui
    # log("run_bot()")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # log('loop:', loop)
    
    try:
        client = TelegramClient(session, api_id, api_hash, proxy=proxy)
    except Exception as e:
        log('Failed to log in to client. Error = ', e)

    def sendToMT4(data):
        for i in currentList:
            terminal = os.path.join(i, "MQL4", "Files")
            if os.path.exists(terminal) == True:
                log(f'Sending {data} to {terminal}')
                if os.path.exists(os.path.join(terminal, "lastsignal.txt")) == False:
                    p = open(os.path.join(terminal, "lastsignal.txt"), "x")
                with open(
                    os.path.join(terminal, "lastsignal.txt"), "w", encoding="utf-8"
                ) as f:
                    f.write(data)

    @client.on(events.NewMessage())
    async def handler(event):
        try:
            # log('New message received.')
            sender = await event.get_sender()
            name = utils.get_display_name(sender)
            msg = ""
            if name not in allowed_chats:
                return

            if event.is_reply:
                reply = await event.get_reply_message()
                msg = reply.raw_text
                msg = msg.replace("|", "")
                msg = msg.replace("{", "")
                msg = msg.replace("}", "")
                msg = msg + "|" + event.raw_text + " {" + str(reply.id) + "}"
            else:
                msg = event.raw_text
                msg = msg.replace("|", "")
                msg = msg.replace("{", "")
                msg = msg.replace("}", "")
                msg = msg  + " {" + str(event.id) + "}"
            sendToMT4(f'CH{allowed_chats.index(name) + 1}: {name}' + "\n" + msg)
            MSG = msg.upper()
            ui.signalText.setText(msg[: msg.find("{")] + "\n\nFROM: " + name)
        except Exception as e:
            log("Failed to process last message. Error = ", e)
    
    @client.on(events.MessageEdited)
    async def handler(event):
        try:
            # log('New message received.')
            sender = await event.get_sender()
            name = utils.get_display_name(sender)
            msg = ""
            if name not in allowed_chats:
                return

            if event.is_reply:
                reply = await event.get_reply_message()
                msg = reply.raw_text
                msg = msg.replace("|", "")
                msg = msg.replace("{", "")
                msg = msg.replace("}", "")
                msg = msg + "|" + event.raw_text + " {" + str(reply.id) + "}"
            else:
                msg = event.raw_text
                msg = msg.replace("|", "")
                msg = msg.replace("{", "")
                msg = msg.replace("}", "")
                msg = msg  + " {" + str(event.id) + "}"
            sendToMT4(f'CH{allowed_chats.index(name) + 1}: {name}' + "\n" + msg + '\n\nEdited')
            MSG = msg.upper()
            ui.signalText.setText(msg[: msg.find("{")] + "\n\nFROM: " + name)
        except Exception as e:
            log("Failed to process last message. Error = ", e)

    async def check_queue():
        # log('[BOT] check_queue(): start')
        while True:
            await asyncio.sleep(1)
            # log('[BOT] check_queue(): check')
            if not queue_in.empty():
                cmd = queue_in.get()
                # log('[BOT] check_queue(): queue_in get:', cmd)
                if cmd == "stop":
                    log("Stopping bot...")
                    await client.disconnect()
                    os._exit(0)
                    break
                if cmd == "logout":
                    log("Logging out...")
                    await client.log_out()

    async def auth_warning():
        while True:
            await asyncio.sleep(1)
            try:
                if await client.is_user_authorized() == False:
                    # ui.authWarning.setText(
                    #     "You are not logged in to a Telegram account. Please close this application and run login.exe first."
                    # )
                    print('Not logged in')
                    ui.stackedWidget.setCurrentIndex(0)
                else:
                    #ui.authWarning.setText("")
                    ui.stackedWidget.setCurrentIndex(2)
            except Exception as e:
                log("Failed to warn auth. Error = " + str(e))

    async def update_terminals():
        home = os.path.expanduser('~')
        starting_directory = os.path.join(home, 'AppData','Roaming','MetaQuotes','Terminal')
        while len(MQL4_paths) == 0:
            await asyncio.sleep(1)
            try:
                current_directory = os.path.abspath(starting_directory)
                while current_directory != os.path.dirname(current_directory):
                    current_directory = os.path.dirname(current_directory)
                for root, dirs, files in os.walk(starting_directory):
                    for dir in dirs:
                        path = os.path.join(root, dir)
                        #log('Path: ',path)
                        if path.endswith("MQL4") and 'MQL4' not in root:
                            path = path.replace('MQL4', '')
                            path = path.replace(starting_directory, '')
                            path = path.replace('\\', '')
                            MQL4_paths.append(path)
                if len(MQL4_paths) > 0:
                    #ui.terminalEdit.clear()
                    for p in MQL4_paths:
                        ui.terminalEdit.addItem(p)
                    break
            except Exception as e:
                log('Failed to get MQL4 paths. Error = ',e)
        
    async def update_sources():
        global channel_list
        #log("Channels are " + str(channel_list))
        if len(channel_list) == 0:
            while True:
                await asyncio.sleep(1)
                try:
                    channels = list()
                    await client.connect()
                    if await client.is_user_authorized():
                        async for dialog in client.iter_dialogs():
                            # log('Channel is ',dialog.title)
                            if dialog.is_user == False:
                                channels.append(dialog.title)
                        channel_list = list(channels)
                        
                        ui.chatSelect.clear()
                        ui.chatSelect.addItems(channel_list)
                        #log('Added ',channel_list)
                        if ui.chatSelect.count() > 0:
                            log('Filled chats list.')
                            break
                        else:
                            continue
                # log('Channels are '+str(channel_list))
                except Exception as e:
                    log("Failed to update sources. Error = " + str(e))
                    continue

    loop.create_task(update_sources())
    loop.create_task(update_terminals())
    loop.create_task(auth_warning())
    loop.create_task(check_queue())

    # try:
    #     with client:
    #         # log('[BOT] start')
    #         client.run_until_disconnected()
    #         log("Client disconnected.")
    # except Exception as e:
    #     ui.authWarning.setText(
    #         str(sys.exc_info()[1])
    #         + ").\n Please check your internet connection\nand restart application."
    #     )
    #     log("Failed to run bot. Error = ", e)






thread2 = Thread(target=run_bot, args=(queue_in, queue_out))
thread2.start()

# tradeinfo = Thread(target=sendTradeInfo)
# tradeinfo.start()


# check_connect_thread = Thread(target=close_on_disconnect, args=(), daemon=True)
# check_connect_thread.start()

