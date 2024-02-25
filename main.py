from gui import Ui_MainWindow
from PyQt6 import QtWidgets
from queue import Queue
import sys
import os
import asyncio
from telethon import TelegramClient
from threading import Thread

session = "user"
api_id = 19533412
api_hash = "244adfc8d6a54f85df6958ac3823e203"
proxy = None

ui = None

async def connect_to_telegram(client):
    await client.start()
    if not await client.is_user_authorized():
        ui.stackedWidget.setCurrentIndex(2)
    else:
        ui.stackedWidget.setCurrentIndex(1)

def run_bot(queue_in, queue_out):
    async def tg_login():
        while True:
            if not queue_in.empty():
                cmd = queue_in.get()
                if cmd == 'tg_login':
                    client = TelegramClient(session, api_id, api_hash, proxy=proxy)
                    await connect_to_telegram(client)
                    break

    asyncio.run(tg_login())

def start_app():
    global ui

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, queue_in, queue_out)
    queue_in.put('tg_login')
    MainWindow.show()
    sys.exit(app.exec())

queue_in = Queue()  # to send data to bot
queue_out = Queue()  # to receive data from bot

thread = Thread(target=run_bot, args=(queue_in, queue_out))
thread.start()

# Start the PyQt application in the main thread
start_app()
