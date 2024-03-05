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
import requests
from datetime import datetime
from telethon import TelegramClient, events, utils
from client import run_client
import sqlite3
import json
import time

AppRunning = True

gui_launched = False
session_validated = False

client = None
phone = None
phone_code_hash = None
session = "user"
api_id = int(os.environ.get("TG_API_ID"))
api_hash = os.environ.get('TG_API_HASH')

currentList = list()
MQL4_paths = list()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, queue_in, queue_out):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1312, 666)
        MainWindow.setStyleSheet("background-color:gray;")
        self.AppRunning = True
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.token_expires_in = None
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
        # self.checkBox = QtWidgets.QCheckBox(parent=self.page)
        # self.checkBox.setGeometry(QtCore.QRect(600, 500, 181, 41))
        # self.checkBox.setStyleSheet("")
        # self.checkBox.setObjectName("checkBox")
        self.server_logout = QtWidgets.QPushButton(parent=self.page)
        self.server_logout.setGeometry(QtCore.QRect(600, 500, 100, 31))
        self.server_logout.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));color:rgba(255, 255, 255, 210);border-radius:5px;")
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
        self.backend_password.setParent
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

        
        self.session_info = None
        self.initSessionRefreshTimer()

        #Auto login if client did not log out on previous session
        self.login_if_return()


        #Connect functions to corresponding buttons
        self.backend_login.clicked.connect(self.handle_backend_login)
        self.tg_code_request_2.clicked.connect(self.handle_tg_code_request)
        self.tg_login_2.clicked.connect(self.handle_tg_login)
        self.chatButton.clicked.connect(self.add_chats)
        self.server_logout.clicked.connect(self.logout)
        self.terminalButton.clicked.connect(self.updateTerminalList)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)
    
    def show_popup(self, title, text, mode=0):
        try:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle(title)
            msg.setText(text)

            if mode == 0:
                msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            elif mode == 1:
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            elif mode == 2:
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)

            x = msg.exec()
        except Exception as e:
            print(f'Failed to show messagebox. Reason: {e}')
            return
    
    def login_if_return(self):
        try:
            session_file = 'session_info.txt'
            session_info = None
            if os.path.exists(session_file):
                with open(session_file, 'r') as f:
                    saved = f.read()
                    session_info = json.loads(saved)
                self.initialize_ui(session_info)
            else:
                print('User logged out on last close.')
        except Exception as e:
            self.show_popup('Auto login failed', f'Failed to execute auto login. Reason: {e}. Please close application and relaunch.', 2)
            
    
    def save_session_info(self, session_info):
        try:
            with open('session_info.txt', 'w') as f:
                f.write(json.dumps(session_info))
        except Exception as e:
            self.show_popup('Session save failed', f'Could not save session info file. Reason: {e}', 1)
    
    def initialize_ui(self, session_info):
        try:
            self.openBotGUI(session_info)

            twelve_days_in_milliseconds = 12 * 24 * 60 * 60 * 1000

            if not self.timer.isActive():
                self.timer.start(twelve_days_in_milliseconds)

            self.queue_in.put('start')

            if os.path.exists('user.session'):
                self.stackedWidget.setCurrentIndex(0)
            else:
                self.stackedWidget.setCurrentIndex(3)
        except Exception as e:
            self.show_popup('UI initialization failed', f'Could not initialize UI. Reason: {e}. Please relaunch application', 1)
    
    def handle_backend_login(self):
        username = self.backend_username.text()
        password = self.backend_password.text()
        
        if len(username) == 0 or len(password) == 0:
            self.show_popup('Invalid username and/or password', f'Please ensure username and passwords are valid and retry.', 2)
            return
        try:
            response = requests.post("https://masterwithjosh.com/login", json={"username": username, "password": password}, timeout=5)
            if response.status_code == 200:
                session_info = response.json()
                self.show_popup('Login Successful', "You are now logged in.", 1)
                self.AppRunning = True
                self.authWarning.setText(f"Logged in with session ID: {session_info['session_id']}")
                self.authWarning.setStyleSheet("font:bold;color:green")
                self.save_session_info(session_info)
                self.initialize_ui(session_info)

            else:
                self.show_popup('Login Failed', "Invalid credentials or server error.", 2)
        except requests.exceptions.RequestException as e:
            self.show_popup('Login Failed', "Could not connect to server.", 0)
        
    def logout(self, force=False):
        if not force:
            try:
                if not self.session_info:
                    print('Session info has no value')
                    return
                
                response = requests.post("https://masterwithjosh.com/logout", json={"session_id": self.session_info['session_id']}, timeout=5)
                if response.status_code != 200:
                    self.show_popup('Logout Failed', 'An error occurred while trying to log out.', 2)
                    return
            except requests.exceptions.RequestException:
                self.show_popup('Logout Failed', 'Could not connect to server.', 0)
                return
        
        try:
            self.timer.timeout.disconnect(self.refreshToken)
            session_file = 'session_info.txt'
            if os.path.exists(session_file):
                os.remove(session_file)
            
            self.AppRunning = False
            self.show_popup('Logout Successful', 'You have been logged out.', 1)
            self.stackedWidget.setCurrentIndex(2)
        except Exception as e:
            self.show_popup('Logout failed', f'Some error occurred while logging out: {e}')

        
        
    
    def openBotGUI(self, session_info):
        try:
            self.session_info = session_info
            self.initSessionRefreshTimer()
        except Exception as e:
            self.show_popup('Session initialization failed', 'Some error occured while initializing session: {e}')
    
    def initSessionRefreshTimer(self):
        try:
            twelve_days_in_milliseconds = 12 * 24 * 60 * 60 * 1000  # 12 days
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.refreshToken)
            self.timer.start(twelve_days_in_milliseconds)
        except Exception as e:
            self.show_popup('Session refresh timer failed', 'Could not refresh session timer. Reason: {e}')
    
    
    def validateSession(self):
        try:
            if not self.session_info:
                return
            
            response = requests.post("https://masterwithjosh.com/session/validate", json={"session_id": self.session_info['session_id']}, timeout=5)
            if response.status_code != 200:
                self.show_popup('Session Ended', "Your session has ended. Please log in again.", 2)
                #QtWidgets.QMessageBox.warning(self, 'Session Ended', 'Your session has ended. Please log in again.')
                self.logout(force=True)
        except requests.exceptions.RequestException as e:
            self.show_popup('Session Validation Failed', "Could not validate session with server.", 2)
            #QtWidgets.QMessageBox.critical(self, 'Session Validation Failed', 'Could not validate session with server.')
    
    def refreshToken(self):
        if not self.session_info:
            return
        

        try:
            # Replace with the actual URL of your refresh endpoint
            refresh_url = 'https://masterwithjosh.com/token/refresh'
            headers = {'Content-Type': 'application/json'}
            # Assuming 'token' is the correct key for the JWT token in your session_info
            data = {'token': self.session_info['token'], 'session_id': self.session_info['session_id']}

            response = requests.post(refresh_url, json=data, headers=headers)
            if response.status_code == 200:
                new_token_info = response.json()
                # Update the token in session info with the new token
                prev_token = self.session_info['token']
                self.session_info['token'] = new_token_info.get('access_token')
                new_token = self.session_info['token']
                #print(f'Previous token: {prev_token}, New token: {new_token}')
                # Optionally, update the token expiration time if it's included in the response
                # self.session_info['expires_in'] = new_token_info.get('expires_in', self.session_info.get('expires_in'))
                if prev_token != new_token:
                    self.show_popup('Session Refreshed', "Session has been successfully refreshed.", 1)
                else:
                    self.show_popup('Session Not Refreshed', "Could not refresh session. Token remains the same.", 1)
            else:
                self.show_popup('Session Refresh Failed', "Failed to refresh your session. Please login again.", 2)
        except requests.exceptions.RequestException as e:
            self.show_popup('Network Error', "Unable to connect to the server to refresh the session.", 0)

    
    def refreshSessionIfNeeded(self):
        try:
            # Assuming the server provides the expiry time as a UNIX timestamp
            print('Attempting session validation')
            self.validateSession()
            if self.token_expires_in and datetime.now().timestamp() >= self.token_expires_in - 300:  # Refresh if within 5 minutes of expiry
                print('Attempting token refresh.')
                self.refreshToken()
            if self.token_expires_in:
                print('Token expires in ',self.token_expires_in)
        except Exception as e:
            self.show_popup('Session refresh failed', 'Could not refresh session. Reason: {e}')
    
    def handle_tg_code_request(self):
        try:
            self.queue_in.put('get tg code')
            self.show_popup('Code request sent', 'Telegram code request sent', 1)
        except Exception as e:
            self.show_popup(f'Code request queue failed', 'Could not queue telegram code request. Reason: {e}')
    
    def handle_tg_login(self):
        try:
            self.queue_in.put('login to tg')
        except Exception as e:
            self.show_popup(f'Login request queue failed', 'Could not queue telegram login request. Reason: {e}')
    
    def add_chats(self):
        try:
            current_chat = self.chatSelect.currentText()
            already_added = list()
            for i in range(self.chatList.count()):
                already_added.append(self.chatList.item(i).text())

            if current_chat not in already_added:
                self.chatList.addItem(current_chat)
        except Exception as e:
            self.show_popup('Chat add failed', f'Could not add {current_chat} to chat. Reason: {e}')
    
    def updateTerminalList(self):
        try:
            global currentList
            home = os.path.expanduser('~')
            starting_directory = os.path.join(home, 'AppData','Roaming','MetaQuotes','Terminal')
            currentTerminal = self.terminalEdit.currentText()
            for i in range(self.terminalList.count()):
                if str(self.terminalList.item(i).text()) not in currentList:
                    currentList.append(str(self.terminalList.item(i).text()))
            
            full_path = os.path.join(starting_directory, currentTerminal)

            if len(currentTerminal) > 0 and currentTerminal != "Select MT4 terminal path here..." and full_path not in currentList:
                currentList.append(full_path)
            
            self.terminalList.clear()
            self.terminalList.addItems(currentList)
        except Exception as e:
            self.show_popup('Terminal list update failed', f'Could not update terminal list. Reason: {e}')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.config_label.setText(_translate("MainWindow", "CONFIGURE TERMINALS"))
        self.config_label_2.setText(_translate("MainWindow", "CONFIGURE CHATS"))
        self.signalText.setText(_translate("MainWindow", "Message"))
        self.server_logout.setText(_translate("MainWindow", "LOGOUT"))
        self.terminalListLabel.setText(_translate("MainWindow", "Terminal list"))
        self.terminalButton.setText(_translate("MainWindow", "Add Terminal"))
        self.chatButton.setText(_translate("MainWindow", "Add Chat"))
        #self.checkBox.setText(_translate("MainWindow", "LOGOUT ON EXIT"))
        self.terminalEdit.setPlaceholderText(_translate("MainWindow", "Select MT4 terminal path here"))
        self.chatSelect.setPlaceholderText(_translate("MainWindow", "------Select chats to scan for messages-----"))
        self.signalLabel.setText(_translate("MainWindow", "LAST SIGNAL RECEIVED:"))
        self.chatListLabel.setText(_translate("MainWindow", "Chat list"))
        self.label.setText(_translate("MainWindow", "LOADING..."))
        self.backend_username.setPlaceholderText(_translate("MainWindow", "Username"))
        self.backend_password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.backend_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.backend_login.setText(_translate("MainWindow", "Login"))
        self.tg_phone_2.setPlaceholderText(_translate("MainWindow", "Telegram number (+XYZ...)"))
        self.tg_password_2.setPlaceholderText(_translate("MainWindow", "Password (if none, leave empty)"))
        self.tg_code_request_2.setText(_translate("MainWindow", "Request code"))
        self.tg_code_2.setPlaceholderText(_translate("MainWindow", "Enter code"))
        self.tg_login_2.setText(_translate("MainWindow", "Connect to Telegram"))

def run_bot(queue_in, queue_out):
    global client

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = TelegramClient(session=session, api_id=api_id, api_hash=api_hash)

    async def sendToMT4(data):
        global currentList
        for i in currentList:
            terminal = os.path.join(i, "MQL4", "Files")
            if os.path.exists(terminal) == True:
                print(f'Sending {data} to {terminal}')
                if os.path.exists(os.path.join(terminal, "lastsignal.txt")) == False:
                    p = open(os.path.join(terminal, "lastsignal.txt"), "x")
                with open(
                    os.path.join(terminal, "lastsignal.txt"), "w", encoding="utf-8"
                ) as f:
                    f.write(data)
    
    async def validate_client():
        global gui_launched
        global session_validated
        while AppRunning:
            await asyncio.sleep(1)
            await client.connect()
            if not await client.is_user_authorized():
                if gui_launched:
                    # if os.path.exists('user.session'):
                    #     os.remove('user.session')
                    ui.stackedWidget.setCurrentIndex(3)
            else:
                ui.stackedWidget.setCurrentIndex(0)
                print('Session is valid')
            session_validated = True
            break

    async def set_start_page():
        while AppRunning:
            await asyncio.sleep(1)
            try:
                global gui_launched
                global session_validated

                if not session_validated:
                    continue

                if gui_launched:
                    print('Setting start page')
                    print('Ui launched')

                    try:
                        if not os.path.exists('session_info.txt'):
                            ui.stackedWidget.setCurrentIndex(2)
                        else:
                            if await client.is_user_authorized():
                                ui.stackedWidget.setCurrentIndex(0)
                            else:
                                ui.stackedWidget.setCurrentIndex(3)
                    except Exception as e:
                        print(f'Could not set start page.{e}')
                        continue
                    
                    break
                else:
                    continue
            except Exception as e:
                print('Failed to set start page: ', e)
                continue
    
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
                    
                    #client = TelegramClient('user', api_id=api_id, api_hash=api_hash)
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
                continue
    
    async def handle_tg_login():
        while AppRunning:
            await asyncio.sleep(1)
            try:
                global phone_code_hash
                global client
                global phone
                if not queue_in.empty() and queue_in.get() == 'login to tg':
                    code = ui.tg_code_2.text()
                    print('Attempting telegram sign in')
                    print('Phone number on sign in: ',phone)
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
                continue
    
    async def update_terminals():
        global MQL4_paths
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
                print('Failed to get MQL4 paths. Error = ',e)
    
    async def update_chats():
        start = time.time()
        while AppRunning:
            await asyncio.sleep(1)
            try:
                global client
                global session
                global api_id
                global api_hash
                global gui_launched
                

                if gui_launched and ui.stackedWidget.currentIndex() == 0:
                    database_locked = False

                    try:
                       async with client:
                            pass
                    except sqlite3.OperationalError as e:
                        print('Database is locked. Will re-attempt chats update')
                        database_locked = True
                    
                    if database_locked:
                        continue
                    
                    try:
                     await client.connect()
                    except Exception as e:
                     print('Could not connect client. Error = ',e)
                     continue
                   
                    if await client.is_user_authorized():
                        async for dialog in client.iter_dialogs():
                            if not dialog.is_user:
                                ui.chatSelect.addItem(dialog.title)
                        #client.disconnect()
                        await run_client()
                        break

                    else:
                        print('Not logged in')
                        continue
                    
                else:
                    continue
            except Exception as e:
                print('Failed to load chats. Error = ',e)
                ui.stackedWidget.setCurrentIndex(3)
                
    
    async def check_termination():
        while AppRunning:
            await asyncio.sleep(1)

           
            try:
                if not queue_in.empty() and queue_in.get() == 'stop':
                    print('Stopping app.')
                    if client:
                        print('Disconnecting client.')
                        await client.disconnect()
                    close_app()
                elif not queue_in.empty() and queue_in.get() == 'start':
                    print('Starting app')
                    #AppRunning = True
                else:
                    continue
            except Exception as e:
                print('Failed to terminate application. Error = ',e)
    
    @client.on(events.NewMessage())
    async def handler(event):
        try:
            if not ui:
                return
            
            if not ui.AppRunning:
                return
            
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

            allowed_chats = list()

            for i in range(ui.chatList.count()):
                allowed_chats.append(ui.chatList.item(i).text())

            
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
            print('Message: ',msg)
            await sendToMT4(f'CH{allowed_chats.index(name) + 1}: {name}' + "\n" + msg)
            MSG = msg.upper()
            ui.signalText.setText(msg[: msg.find("{")] + "\n\nFROM: " + name)
        except Exception as e:
            print("Failed to process last message. Error = ", e)

    
    @client.on(events.MessageEdited)
    async def handler(event):
        try:
            if not ui:
                return
            
            if not ui.AppRunning:
                return
            
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

            allowed_chats = list()

            for i in range(ui.chatList.count()):
                allowed_chats.append(ui.chatList.item(i).text())

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
            await sendToMT4(f'CH{allowed_chats.index(name) + 1}: {name}' + "\n" + msg + '\n\nEdited')
            MSG = msg.upper()
            ui.signalText.setText(msg[: msg.find("{")] + "\n\nFROM: " + name)
        except Exception as e:
            print("Failed to process last message. Error = ", e)
    
    async def run_client():
        global session_validated

        while not client:
            await asyncio.sleep(1)

        while not client.is_connected():
            await asyncio.sleep(1)
       
        print('Client exists and is connected.')

        try:
            await client.start()
            await client.run_until_disconnected()
            print("Client disconnected.")
        except asyncio.CancelledError:
            print("Bot task was cancelled.")
                
        except Exception as e:
            print("Failed to run bot. Error = ", e)
        
    #loop.create_task(run_client())
    loop.run_until_complete(asyncio.gather(update_chats(), update_terminals(), check_termination()))

    
        


def close_app():
    global AppRunning
    print('Closing app')
    #ui.queue_in.put('stop')
    
    #ui.logout()
    ui.timer.stop()
    AppRunning = False

queue_in = Queue()
queue_out = Queue()

bot_thread = Thread(target=run_bot, args=(queue_in, queue_out))
bot_thread.start()

# client_thread = Thread(target=run_client, args=(client,))
# client_thread.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: close_app())
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, queue_in, queue_out)
    queue_in.put('ui launched')
    gui_launched = True
    MainWindow.show()
    sys.exit(app.exec())