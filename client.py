from telethon import TelegramClient, events, utils
import asyncio
import os
import sqlite3

session = "user"
api_id = int(os.environ.get("TG_API_ID"))
api_hash = os.environ.get('TG_API_HASH')


def run_client(client):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # if not client:
    #     client = TelegramClient(session=session, api_id=api_id, api_hash=api_hash)

    while not client:
        print('Client not initialized. Retrying...')
        asyncio.sleep(1)
    
    database_locked = False

    try:
        with client:
            pass
    except sqlite3.OperationalError as e:
        print('Database is locked. Will re-attempt client start.')
        database_locked = True
    
    if database_locked:
        return
    
    print('Client started.')
    

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
            
            #if name not in allowed_chats:
            #    return

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
            #sendToMT4(f'CH{allowed_chats.index(name) + 1}: {name}' + "\n" + msg)
            MSG = msg.upper()
            #ui.signalText.setText(msg[: msg.find("{")] + "\n\nFROM: " + name)
        except Exception as e:
            print("Failed to process last message. Error = ", e)
    
    try:
        with client:
            # log('[BOT] start')
            client.run_until_disconnected()
            #log("Client disconnected.")
    except Exception as e:  
        print("Failed to run bot. Error = ", e)


