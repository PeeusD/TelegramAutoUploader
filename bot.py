import asyncio
from telethon import TelegramClient, events
from os import remove, getenv, walk, path
from dotenv import load_dotenv
import PyPDF2 as pd
import re, pytz, datetime, requests
from telethon.errors import MultiError
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)



load_dotenv()
# Remember to use your own values from my.telegram.org!
# Credentials while logging...
API_ID = int(getenv('api_id'))
API_HASH = getenv('api_hash')
client = TelegramClient('anon', API_ID, API_HASH)

OTHER_CHAT_ID =int(getenv('other_channel_id'))
MY_CHAT_ID = int(getenv('my_channel_id'))
MY_CHAT_ID2 = int(getenv('my_channel_id2'))
BOT_CHAT_ID = getenv('bot_chat_id')
BOT_CHAT_ID2 = getenv('bot_chat_id2')
PD_CHAT_ID = getenv('pd_chat_id')


#Capturing messages from the targetted Telegram Channel

@client.on(events.NewMessage(chats=OTHER_CHAT_ID))
async def handler(event):
 try:  
    if event.sticker:
       
        if 'CAADBQADywIAAkwuuVeu_xH13qrbzwI' == event.file.id:

            #printing date 
            dat = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            dat = dat.strftime('%d %B %Y') 
            
             #daily quotes api
            url = "https://api.quotable.io/random"
            response =  requests.get(url)
            json_data = response.json()
            msg = f"__{dat} \n{json_data['content']} \n- {json_data['author']}__"
            bot_msg1 = 'Send New Post to Subscribers'
            bot_msg2 = 'Send Post to Subscribers'

            #sending message to channel and bot... 
            await asyncio.wait([   
            # sending stickers
                client.send_file(entity=MY_CHAT_ID, file='CAADBQADCAADXF3_OXDpMn3yScgUAg'),
                client.send_file(entity=MY_CHAT_ID2, file='CAADBQADCAADXF3_OXDpMn3yScgUAg'),
                # sending greet messages
                client.send_message(entity=MY_CHAT_ID, message=msg, parse_mode='md', schedule=datetime.timedelta(seconds=2)),
                client.send_message(entity=MY_CHAT_ID2, message=msg, parse_mode='md', schedule=datetime.timedelta(seconds=2)),

                #sending before message to bots
                client.send_message(entity=BOT_CHAT_ID, message=bot_msg1),
                client.send_message(entity=BOT_CHAT_ID2, message=bot_msg1),
                client.send_message(entity=BOT_CHAT_ID, message=msg, parse_mode='md'),
                client.send_message(entity=BOT_CHAT_ID2, message=msg, parse_mode='md'),

                #sending after message to bots
                client.send_message(entity=BOT_CHAT_ID, message=bot_msg2, schedule=datetime.timedelta(minutes=20)),
                client.send_message(entity=BOT_CHAT_ID2, message=bot_msg2, schedule=datetime.timedelta(minutes=20)),
                ])
 except MultiError as e:
        print(e.exceptions)

@client.on(events.NewMessage(chats=OTHER_CHAT_ID))
async def handler(event):
 try:
    # filtering documents
    if event.document:
        if 'TH-DELHI' in event.file.name.upper():
            await event.download_media(file=open(event.file.name, "wb"))
            pdf_mgmt(event.file.name)
            await asyncio.wait([ 
                client.send_file(MY_CHAT_ID,file= open(event.file.name, 'rb'), thumb='thumb.jpg'),
                client.send_file(MY_CHAT_ID2,file= open(event.file.name, 'rb'), thumb='thumb.jpg'),

                client.send_file(BOT_CHAT_ID,file= open(event.file.name, 'rb'), thumb='thumb.jpg'),
                client.send_file(BOT_CHAT_ID2,file= open(event.file.name, 'rb'), thumb='thumb.jpg') ])
            # await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')

            # await asyncio.sleep(10)
            # await client.delete_messages(PD_CHAT_ID, [m.id])
            remove(event.file.name)

        elif 'IE DELHI' in event.file.name.upper():
            # await asyncio.sleep(10)
            await event.download_media(file=open(event.file.name, "wb"))
            pdf_mgmt(event.file.name)
            await asyncio.wait([ 
                client.send_file(MY_CHAT_ID, open(event.file.name, 'rb'), thumb='thumb.jpg'),
                client.send_file(MY_CHAT_ID2, open(event.file.name, 'rb'), thumb='thumb.jpg') ])
           
            # m = await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')
            # await asyncio.sleep(10)
            # await client.delete_messages(PD_CHAT_ID, [m.id])
            remove(event.file.name)

        elif 'MAGAZINE' in event.file.name.upper():
            # await asyncio.sleep(10)
            await event.download_media(file=open(event.file.name, "wb"))
            pdf_mgmt(event.file.name)
            await asyncio.wait([   
                client.send_file(MY_CHAT_ID, open(event.file.name, 'rb'), thumb='thumb.jpg'),
                client.send_file(MY_CHAT_ID2, open(event.file.name, 'rb'), thumb='thumb.jpg'), 

                client.send_file(BOT_CHAT_ID, open(event.file.name, 'rb'), thumb='thumb.jpg'),
                client.send_file(BOT_CHAT_ID2, open(event.file.name, 'rb'), thumb='thumb.jpg') ])
            # m = await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')
            # await asyncio.sleep(10)
            # await client.delete_messages(PD_CHAT_ID, [m.id])
            remove(event.file.name)
            
        else:
            if not event.sticker:
                #forwarding files
                await asyncio.wait([   
                     client.send_file(MY_CHAT_ID, event.message),
                     client.send_file(MY_CHAT_ID2, event.message) ])
                # m = await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')
                if 'TH' in event.file.name.upper() :

                    # forwarding files
                    await asyncio.wait([   
                        client.send_file(BOT_CHAT_ID, event.message),
                        client.send_file(BOT_CHAT_ID2, event.message) ])
                
                # await asyncio.sleep(10)
                # await client.delete_messages(PD_CHAT_ID, [m.id])
 except MultiError as e:
        print(e.exceptions)

def pdf_mgmt (f_name) :
    
    pattern = 'DAILY NEWSPAPERS PDF'
    dir_path = path.dirname(path.abspath(__file__))
    
    #renaming pdfs
    for root, dirs, files in walk(dir_path):
        for file in files: 
            
            if file.startswith('TH') or file.startswith('IE'):
                
                merger = pd.PdfFileMerger( strict=True)
                merger.append(pd.PdfFileReader(path.join(root,'promo.pdf')))
                merger.append(pd.PdfFileReader(path.join(root,f_name)))
                
                merger.write(f_name)
                merger.close()
                
    #getting no. of pages for pdfs
                infile = pd.PdfFileReader(path.join(root,f_name))
                numPages = infile.getNumPages()
                delPages = []

                for i in range(0, numPages):
                    pageObj = infile.getPage(i)
                    ex_text = pageObj.extractText()
                    if re.search(pattern, ex_text):
                        # print(f'Pattern found on Page no: {i}')
                        delPages.append(i)
                #deleting required pages and uploading to telegram...
                if len(delPages) > 0 :
                    infile = pd.PdfFileReader(path.join(root,f_name))
                    output = pd.PdfFileWriter()
                    
                    for i in range(infile.getNumPages()):
                        if i not in delPages:
                            p = infile.getPage(i)
                            output.addPage(p)

                    with open(path.join(root,f_name),'wb') as f:
                        output.write(f)
                
client.start()
#this will make your bot run forever untill any interruption
client.run_until_disconnected()