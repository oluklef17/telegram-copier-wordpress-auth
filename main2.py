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
        MainWindow.resize(1312, 666)
        MainWindow.setStyleSheet("background-color:gray;")
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 10, 1211, 591))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.authWarning = QtWidgets.QLabel(parent=self.page)
        self.authWarning.setGeometry(QtCore.QRect(350, 50, 631, 61))
        self.authWarning.setStyleSheet("font:bold;color:#8B0000")
        self.authWarning.setText("")
        self.authWarning.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.authWarning.setObjectName("authWarning")
        self.config_label = QtWidgets.QLabel(parent=self.page)
        self.config_label.setGeometry(QtCore.QRect(120, 170, 281, 20))
        self.config_label.setStyleSheet("font-size:15px")
        self.config_label.setObjectName("config_label")
        self.config_label_2 = QtWidgets.QLabel(parent=self.page)
        self.config_label_2.setGeometry(QtCore.QRect(930, 170, 281, 16))
        self.config_label_2.setStyleSheet("font-size:15px")
        self.config_label_2.setObjectName("config_label_2")
        self.signalText = QtWidgets.QLabel(parent=self.page)
        self.signalText.setGeometry(QtCore.QRect(490, 200, 351, 261))
        self.signalText.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.signalText.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.signalText.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.signalText.setObjectName("signalText")
        self.terminalListLabel = QtWidgets.QLabel(parent=self.page)
        self.terminalListLabel.setGeometry(QtCore.QRect(120, 310, 281, 16))
        self.terminalListLabel.setStyleSheet("font-size:15px")
        self.terminalListLabel.setObjectName("terminalListLabel")
        self.chatSelect = QtWidgets.QComboBox(parent=self.page)
        self.chatSelect.setGeometry(QtCore.QRect(930, 200, 281, 41))
        self.chatSelect.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.chatSelect.setObjectName("chatSelect")
        self.terminalButton = QtWidgets.QPushButton(parent=self.page)
        self.terminalButton.setGeometry(QtCore.QRect(210, 250, 111, 23))
        self.terminalButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.terminalButton.setObjectName("terminalButton")
        self.chatButton = QtWidgets.QPushButton(parent=self.page)
        self.chatButton.setGeometry(QtCore.QRect(1010, 250, 111, 23))
        self.chatButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.chatButton.setObjectName("chatButton")
        self.checkBox = QtWidgets.QCheckBox(parent=self.page)
        self.checkBox.setGeometry(QtCore.QRect(600, 500, 181, 41))
        self.checkBox.setStyleSheet("")
        self.checkBox.setObjectName("checkBox")
        self.terminalEdit = QtWidgets.QComboBox(parent=self.page)
        self.terminalEdit.setGeometry(QtCore.QRect(120, 200, 281, 41))
        self.terminalEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.terminalEdit.setObjectName("terminalEdit")
        self.signalLabel = QtWidgets.QLabel(parent=self.page)
        self.signalLabel.setGeometry(QtCore.QRect(490, 170, 281, 16))
        self.signalLabel.setStyleSheet("font-size:15px")
        self.signalLabel.setObjectName("signalLabel")
        self.chatListLabel = QtWidgets.QLabel(parent=self.page)
        self.chatListLabel.setGeometry(QtCore.QRect(930, 310, 281, 16))
        self.chatListLabel.setStyleSheet("font-size:15px")
        self.chatListLabel.setObjectName("chatListLabel")
        self.terminalList = QtWidgets.QListWidget(parent=self.page)
        self.terminalList.setGeometry(QtCore.QRect(120, 330, 281, 131))
        self.terminalList.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.terminalList.setObjectName("terminalList")
        self.chatList = QtWidgets.QListWidget(parent=self.page)
        self.chatList.setGeometry(QtCore.QRect(930, 330, 281, 131))
        self.chatList.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.chatList.setObjectName("chatList")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.layoutWidget = QtWidgets.QWidget(parent=self.page_2)
        self.layoutWidget.setGeometry(QtCore.QRect(660, 130, 181, 251))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.backend_username = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.backend_username.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.backend_username.setObjectName("backend_username")
        self.verticalLayout.addWidget(self.backend_username)
        self.backend_password = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.backend_password.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.backend_password.setObjectName("backend_password")
        self.verticalLayout.addWidget(self.backend_password)
        self.backend_login = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.backend_login.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.backend_login.setObjectName("backend_login")
        self.verticalLayout.addWidget(self.backend_login)
        self.stackedWidget.addWidget(self.page_2)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.layoutWidget_5 = QtWidgets.QWidget(parent=self.page_6)
        self.layoutWidget_5.setGeometry(QtCore.QRect(600, 90, 211, 291))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tg_phone_2 = QtWidgets.QLineEdit(parent=self.layoutWidget_5)
        self.tg_phone_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.tg_phone_2.setObjectName("tg_phone_2")
        self.verticalLayout_5.addWidget(self.tg_phone_2)
        self.tg_password_2 = QtWidgets.QLineEdit(parent=self.layoutWidget_5)
        self.tg_password_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.tg_password_2.setObjectName("tg_password_2")
        self.verticalLayout_5.addWidget(self.tg_password_2)
        self.tg_code_request_2 = QtWidgets.QPushButton(parent=self.layoutWidget_5)
        self.tg_code_request_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.tg_code_request_2.setObjectName("tg_code_request_2")
        self.verticalLayout_5.addWidget(self.tg_code_request_2)
        self.tg_code_2 = QtWidgets.QLineEdit(parent=self.layoutWidget_5)
        self.tg_code_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.tg_code_2.setObjectName("tg_code_2")
        self.verticalLayout_5.addWidget(self.tg_code_2)
        self.tg_login_2 = QtWidgets.QPushButton(parent=self.layoutWidget_5)
        self.tg_login_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
        self.tg_login_2.setObjectName("tg_login_2")
        self.verticalLayout_5.addWidget(self.tg_login_2)
        self.stackedWidget.addWidget(self.page_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1312, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.config_label.setText(_translate("MainWindow", "CONFIGURE TERMINALS"))
        self.config_label_2.setText(_translate("MainWindow", "CONFIGURE CHATS"))
        self.signalText.setText(_translate("MainWindow", "Message"))
        self.terminalListLabel.setText(_translate("MainWindow", "Terminal list"))
        self.terminalButton.setText(_translate("MainWindow", "Add Terminal"))
        self.chatButton.setText(_translate("MainWindow", "Add Chat"))
        self.checkBox.setText(_translate("MainWindow", "LOGOUT ON EXIT"))
        self.terminalEdit.setPlaceholderText(_translate("MainWindow", "Paste MT4/MT5 terminal path here"))
        self.signalLabel.setText(_translate("MainWindow", "LAST SIGNAL RECEIVED:"))
        self.chatListLabel.setText(_translate("MainWindow", "Chat list"))
        self.backend_username.setPlaceholderText(_translate("MainWindow", "Username"))
        self.backend_password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.backend_login.setText(_translate("MainWindow", "Login"))
        self.tg_phone_2.setPlaceholderText(_translate("MainWindow", "Telegram number (+XYZ...)"))
        self.tg_password_2.setPlaceholderText(_translate("MainWindow", "Password (if none, leave empty)"))
        self.tg_code_request_2.setText(_translate("MainWindow", "Request code"))
        self.tg_code_2.setPlaceholderText(_translate("MainWindow", "Enter code"))
        self.tg_login_2.setText(_translate("MainWindow", "Connect to Telegram"))

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
                    ui.stackedWidget.setCurrentIndex(2)
                else:
                    #ui.authWarning.setText("")
                    ui.stackedWidget.setCurrentIndex(1)
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