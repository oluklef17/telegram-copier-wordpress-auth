# Form implementation generated from reading ui file 'copierbot.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from queue import Queue
from threading import Thread
import asyncio
import os
import re
from telethon import TelegramClient, events, utils

AppRunning = True

gui_launched = False

client = None
phone = None
phone_code_hash = None
session = "user"
api_id = int(os.environ.get("TG_API_ID"))
api_hash = os.environ.get('TG_API_HASH')

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
        self.terminalEdit = QtWidgets.QLineEdit(parent=self.page)
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
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.label = QtWidgets.QLabel(parent=self.page_3)
        self.label.setGeometry(QtCore.QRect(370, 230, 291, 71))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.stackedWidget.addWidget(self.page_3)
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
        self.backend_login.clicked.connect(self.handle_backend_login)
        self.tg_code_request_2.clicked.connect(self.handle_tg_code_request)
        self.tg_login_2.clicked.connect(self.handle_tg_login)
        self.chatButton.clicked.connect(self.add_chats)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def handle_backend_login(self):
        username = self.backend_username.text()
        password = self.backend_password.text()
        print('Username is ',username)
        print('Password is ',password)
        if username == 'Yemi' and password == 'admin':
            if os.path.exists('user.session'):
                #self.queue_in.put('logged in')
                self.stackedWidget.setCurrentIndex(0)
            else:
                self.stackedWidget.setCurrentIndex(3)
        else:
            print('Username or password incorrect.')
    
    def handle_tg_code_request(self):
        self.queue_in.put('get tg code')
    
    def handle_tg_login(self):
        self.queue_in.put('login to tg')
    
    def add_chats(self):
        current_chat = self.chatSelect.currentText()
        already_added = list()
        for i in range(self.chatList.count()):
            already_added.append(self.chatList.item(i).text())

        #print('Chats: ',already_added)

        if current_chat not in already_added:
            self.chatList.addItem(current_chat)

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
        self.label.setText(_translate("MainWindow", "LOADING..."))
        self.backend_username.setPlaceholderText(_translate("MainWindow", "Username"))
        self.backend_password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.backend_login.setText(_translate("MainWindow", "Login"))
        self.tg_phone_2.setPlaceholderText(_translate("MainWindow", "Telegram number (+XYZ...)"))
        self.tg_password_2.setPlaceholderText(_translate("MainWindow", "Password (if none, leave empty)"))
        self.tg_code_request_2.setText(_translate("MainWindow", "Request code"))
        self.tg_code_2.setPlaceholderText(_translate("MainWindow", "Enter code"))
        self.tg_login_2.setText(_translate("MainWindow", "Connect to Telegram"))

def run_bot(queue_in, queue_out):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def set_start_page():
        while AppRunning:
            await asyncio.sleep(1)
            try:
                global gui_launched
                if not queue_in.empty() and queue_in.get() == 'ui launched':
                    ui.stackedWidget.setCurrentIndex(2)
                    gui_launched = True
                    break
                else:
                    continue
            except Exception as e:
                print('Failed to set start page: ', e)
                break
    
    async def handle_tg_code_request():
        while AppRunning:
            await asyncio.sleep(1)
            try:
                global phone_code_hash
                global client
                global phone
                if not queue_in.empty() and queue_in.get() == 'get tg code':   
                    phone = ui.tg_phone_2.text()
                    password = ui.tg_password_2.text()
                    pattern = r'\+\d+'
                    if re.search(pattern=pattern, string=phone):
                        print('Phone number is: ',phone)
                    else:
                        print('Invalid phone format. Must be +XXX...')
                    
                    client = TelegramClient('user', api_id=api_id, api_hash=api_hash)
                    await client.connect()

                    if not await client.get_me():
                        result = await client.send_code_request(phone)
                        phone_code_hash = result.phone_code_hash
                        break
                    else:
                        continue
                else:
                    continue
            except Exception as e:
                print('TG login failed. Error = ',e)
                break
    
    async def handle_tg_login():
        while AppRunning:
            await asyncio.sleep(1)
            try:
                global phone_code_hash
                global client
                global phone
                if not queue_in.empty() and queue_in.get() == 'login to tg':
                    code = ui.tg_code_2.text()
                    await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)

                    if client.is_user_authorized:
                        ui.stackedWidget.setCurrentIndex(0)
                        break
                    else:
                        continue
                else:
                    continue
            
            except Exception as e:
                print('Failed to login to telegram. Error = ',e)
                break
    
    async def update_chats():
        while AppRunning:
            await asyncio.sleep(1)
            try:
                global session
                global api_id
                global api_hash
                global gui_launched
                if gui_launched and ui.stackedWidget.currentIndex() == 0:
                    client = TelegramClient(session=session, api_id=api_id, api_hash=api_hash)
                    await client.connect()
                    await client.start()
                    if await client.is_user_authorized():
                        async for dialog in client.iter_dialogs():
                            if not dialog.is_user:
                                ui.chatSelect.setPlaceholderText("------Select chats to scan for messages-----")
                                ui.chatSelect.addItem(dialog.title)
                        break

                    else:
                        print('Not logged in')
                        continue
                    
                else:
                    continue
            except Exception as e:
                print('Failed to load chats. Error = ',e)
                break


    
    loop.run_until_complete(asyncio.gather(set_start_page(),handle_tg_code_request(),handle_tg_login(),update_chats()))
    

def close_app():
    global AppRunning
    print('Closing app')
    AppRunning = False

queue_in = Queue()
queue_out = Queue()

bot_thread = Thread(target=run_bot, args=(queue_in, queue_out))
bot_thread.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: close_app())
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, queue_in, queue_out)
    queue_in.put('ui launched')
    MainWindow.show()
    sys.exit(app.exec())