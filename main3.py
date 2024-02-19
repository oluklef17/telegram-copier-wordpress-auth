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

assets = dict()

binaryToken = ""

parentDirectory = os.getcwd()


LastTradeInfo = ""

currentList = list()

channel_list = list()

allowed_chats = list()

MQL4_paths = list()

lastWarning = ""


# UI CLASS
class Ui_MainWindow(object):
    def setupUi(self, MainWindow, queue_in, queue_out):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1312, 634)
        MainWindow.setFixedWidth(1312)
        MainWindow.setStyleSheet("background-color:Gray;")
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.logoLabel = QtWidgets.QLabel(self.centralwidget)
        self.logoLabel.setGeometry(QtCore.QRect(510, 30, 361, 51))
        self.logoLabel.setStyleSheet("font-family:'Helvetica';font-size:20px")
        self.logoLabel.setObjectName("logoLabel")
        self.signalLabel = QtWidgets.QLabel(self.centralwidget)
        self.signalLabel.setGeometry(QtCore.QRect(510, 220, 281, 16))
        self.signalLabel.setStyleSheet("font-family:'Helvetica';font-size:15px")
        self.signalLabel.setObjectName("signalLabel")
        self.terminalButton = QtWidgets.QPushButton(self.centralwidget)
        self.terminalButton.setGeometry(QtCore.QRect(230, 300, 111, 23))
        self.terminalButton.setStyleSheet(
            "text-align:center;color:Black;background-color:#46748A"
        )
        self.terminalButton.setObjectName("terminalButton")
        self.terminalList = QtWidgets.QListWidget(self.centralwidget)
        self.terminalList.setGeometry(QtCore.QRect(140, 380, 281, 131))
        self.terminalList.setStyleSheet(
            "text-align:center;color:#46748A;background-color:Black"
        )
        self.terminalList.setObjectName("terminalList")
        self.config_label = QtWidgets.QLabel(self.centralwidget)
        self.config_label.setGeometry(QtCore.QRect(140, 220, 281, 20))
        self.config_label.setStyleSheet("font-family:'Helvetica';font-size:15px")
        self.config_label.setObjectName("config_label")
        self.signalText = QtWidgets.QLabel(self.centralwidget)
        self.signalText.setGeometry(QtCore.QRect(510, 250, 351, 261))
        self.signalText.setStyleSheet(
            "padding:15px;color:#46748A;background-color:Black"
        )
        self.signalText.setTextFormat(QtCore.Qt.AutoText)
        self.signalText.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.signalText.setObjectName("signalText")
        self.terminalEdit = QtWidgets.QComboBox(self.centralwidget)
        self.terminalEdit.setGeometry(QtCore.QRect(140, 250, 281, 41))
        self.terminalEdit.setStyleSheet(
            "text-align:center;color:#46748A;background-color:Black"
        )
        self.terminalEdit.setObjectName("terminalEdit")
        self.terminalListLabel = QtWidgets.QLabel(self.centralwidget)
        self.terminalListLabel.setGeometry(QtCore.QRect(140, 360, 281, 16))
        self.terminalListLabel.setStyleSheet("font-family:'Helvetica';font-size:15px")
        self.terminalListLabel.setObjectName("terminalListLabel")
        self.chatList = QtWidgets.QListWidget(self.centralwidget)
        self.chatList.setGeometry(QtCore.QRect(950, 380, 281, 131))
        self.chatList.setStyleSheet(
            "text-align:center;color:#46748A;background-color:Black"
        )
        self.chatList.setObjectName("chatList")
        self.chatListLabel = QtWidgets.QLabel(self.centralwidget)
        self.chatListLabel.setGeometry(QtCore.QRect(950, 360, 281, 16))
        self.chatListLabel.setStyleSheet("font-family:'Helvetica';font-size:15px")
        self.chatListLabel.setObjectName("chatListLabel")
        self.chatButton = QtWidgets.QPushButton(self.centralwidget)
        self.chatButton.setGeometry(QtCore.QRect(1030, 300, 111, 23))
        self.chatButton.setStyleSheet(
            "text-align:center;color:Black;background-color:#46748A"
        )
        self.chatButton.setObjectName("chatButton")
        self.config_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.config_label_2.setGeometry(QtCore.QRect(950, 220, 281, 16))
        self.config_label_2.setStyleSheet("font-family:'Helvetica';font-size:15px")
        self.config_label_2.setObjectName("config_label_2")
        self.chatSelect = QtWidgets.QComboBox(self.centralwidget)
        self.chatSelect.setGeometry(QtCore.QRect(950, 250, 281, 41))
        self.chatSelect.setStyleSheet(
            "text-align:center;color:#46748A;background-color:Black"
        )
        self.chatSelect.setObjectName("chatSelect")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(620, 550, 181, 41))
        self.checkBox.setStyleSheet("")
        self.checkBox.setObjectName("checkBox")
        self.authWarning = QtWidgets.QLabel(self.centralwidget)
        self.authWarning.setGeometry(QtCore.QRect(370, 100, 631, 61))
        self.authWarning.setStyleSheet("font:bold;color:#8B0000")
        self.authWarning.setText("")
        self.authWarning.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.authWarning.setObjectName("authWarning")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1312, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.terminalButton.clicked.connect(self.updateTerminalList)
        self.chatButton.clicked.connect(self.updateSourceList)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def updateTerminalList(self):
        global currentList
        home = os.path.expanduser('~')
        starting_directory = os.path.join(home, 'AppData','Roaming','MetaQuotes','Terminal')
        currentTerminal = self.terminalEdit.currentText()
        for i in range(self.terminalList.count()):
            if str(self.terminalList.item(i).text()) not in currentList:
                currentList.append(str(self.terminalList.item(i).text()))
        if len(currentTerminal) > 0 and currentTerminal != "Select MT4 terminal path here..." and currentTerminal not in currentList:
            currentList.append(os.path.join(starting_directory, currentTerminal))
        #log("Terminal list is ", currentList)
        self.terminalList.clear()
        self.terminalList.addItems(currentList)

    def updateSourceList(self):
        global allowed_chats
        currentSource = self.chatSelect.currentText()
        # for i in range(self.chatList.count()):
        #     if str(self.chatList.item(i).text()) not in allowed_chats:
        #         allowed_chats.append(str(self.chatList.item(i).text()))
        if len(currentSource) > 0 and currentSource not in allowed_chats:
            allowed_chats.append(currentSource)
        #log("Chat list is ", allowed_chats)
        self.chatList.clear()
        for idx, chat in enumerate(allowed_chats):
            self.chatList.addItem(f'CH{idx + 1}: {chat}')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "SIGNAL COPIER")
        )
        self.signalLabel.setText(_translate("MainWindow", "LAST SIGNAL RECEIVED:"))
        self.logoLabel.setText(_translate("MainWindow", "SIGNAL COPIER"))
        self.terminalButton.setText(_translate("MainWindow", "Add Terminal"))
        self.config_label.setText(_translate("MainWindow", "CONFIGURE TERMINALS"))
        self.signalText.setText(_translate("MainWindow", "Message"))
        self.terminalEdit.addItem("Select MT4 terminal path here...")
        self.terminalListLabel.setText(_translate("MainWindow", "Terminal list"))
        self.chatListLabel.setText(_translate("MainWindow", "Chat list"))
        self.chatButton.setText(_translate("MainWindow", "Add Chat"))
        self.config_label_2.setText(_translate("MainWindow", "CONFIGURE CHATS"))
        self.checkBox.setText(_translate("MainWindow", "LOGOUT ON EXIT"))


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

    print(msg)

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
    if os.path.exists(f"{session}.session") == False:
        log('Not logged in. Will attempt to launch login terminal.')
        login = None
        path = 'login.exe'
        if os.path.exists(path):
            try:
                login = subprocess.Popen(path)
                os._exit(0)
            except Exception as e:
                log('Failed to open login exe. Error = ',e)
            

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
            terminal = os.path.join(i, "MQL5", "Files")
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
            #log('New message received.')
            sender = await event.get_sender()

            #str(type(sender)) != "<class 'telethon.tl.types.User'>"
            
            chat_entity = await client.get_entity(event.message.peer_id)
  
            if str(type(sender)) == "<class 'telethon.tl.types.User'>":
                name = chat_entity.title if hasattr(chat_entity, 'title') else 'Unknown Group'
            else:
                name = utils.get_display_name(sender)
            #print('Group name is ',group_name)
            #print('Sender type ',str(type(sender)))
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
            #log('New message received.')
            sender = await event.get_sender()

            #str(type(sender)) != "<class 'telethon.tl.types.User'>"
            
            chat_entity = await client.get_entity(event.message.peer_id)
  
            if str(type(sender)) == "<class 'telethon.tl.types.User'>":
                name = chat_entity.title if hasattr(chat_entity, 'title') else 'Unknown Group'
            else:
                name = utils.get_display_name(sender)
            #print('Group name is ',group_name)
            #print('Sender type ',str(type(sender)))
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
                    ui.authWarning.setText(
                        "You are not logged in to a Telegram account. Please close this application and run login.exe first."
                    )
                else:
                    ui.authWarning.setText("")
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
                        if path.endswith("MQL5") and 'MQL5' not in root:
                            path = path.replace('MQL5', '')
                            path = path.replace(starting_directory, '')
                            path = path.replace('\\', '')
                            MQL4_paths.append(path)
                if len(MQL4_paths) > 0:
                    #ui.terminalEdit.clear()
                    for p in MQL4_paths:
                        ui.terminalEdit.addItem(p)
                    break
            except Exception as e:
                log('Failed to get MQL5 paths. Error = ',e)
        
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

    try:
        with client:
            # log('[BOT] start')
            client.run_until_disconnected()
            log("Client disconnected.")
    except Exception as e:
        ui.authWarning.setText(
            str(sys.exc_info()[1])
            + ").\n Please check your internet connection\nand restart application."
        )
        log("Failed to run bot. Error = ", e)





queue_in = Queue()  # to send data to bot
queue_out = Queue()  # to receive data from bot
thread2 = Thread(target=run_bot, args=(queue_in, queue_out))
thread2.start()

# tradeinfo = Thread(target=sendTradeInfo)
# tradeinfo.start()


# check_connect_thread = Thread(target=close_on_disconnect, args=(), daemon=True)
# check_connect_thread.start()

try:
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, queue_in, queue_out)
    ui.authWarning.setText(
        "",
    )
    MainWindow.show()
    app.exec_()
    checkState = int(ui.checkBox.checkState())
    if checkState == 0:
        log("User not logged out")
        queue_in.put("stop")
        thread2.join()
        os._exit(0)
    elif checkState == 2:
        queue_in.put("logout")
        thread2.join()
        log("User logged out")
        os._exit(0)
except Exception as e:
    log("Application error = ", e)
    ui.authWarning.setText("Application error = ", e)


