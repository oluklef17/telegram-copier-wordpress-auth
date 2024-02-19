import os
import sys
import time
from threading import Thread
from datetime import datetime, timedelta
from queue import Queue
import asyncio
import os
import socket

from telethon import TelegramClient, events, utils
from PyQt5 import QtCore, QtGui, QtWidgets

session = 'user'#os.environ.get('TG_SESSION', 'printer')
api_id = 19533412
api_hash = '244adfc8d6a54f85df6958ac3823e203'
proxy = None
# Create and start the client so we can make requests (we don't here)

print('======================Telegram Authentication======================')
client = TelegramClient(session, api_id, api_hash, proxy=proxy)
client.start()
print('Please close this window and relaunch the signal dispatcher')

