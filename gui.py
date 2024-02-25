# Form implementation generated from reading ui file 'copierbot.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


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

