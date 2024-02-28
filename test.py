from telethon import TelegramClient, events, utils
import os
import asyncio

session = "user"
api_id = int(os.environ.get("TG_API_ID"))
api_hash = os.environ.get('TG_API_HASH')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def run():
    client = TelegramClient(session=session, api_id=api_id, api_hash=api_hash)
    await client.connect()
    await client.start()
    if await client.is_user_authorized():
        print('Logged in')
    else:
        print('Not logged in')

loop.run_until_complete(run())

