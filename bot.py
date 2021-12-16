import asyncio
from telethon import TelegramClient, events
from os import remove, getenv, walk, path
from dotenv import load_dotenv
import PyPDF2 as pd
import re
import datetime, requests
load_dotenv()
# Remember to use your own values from my.telegram.org!
# Credentials while logging...
API_ID = int(getenv('api_id'))
API_HASH = getenv('api_hash')
client = TelegramClient('anon', API_ID, API_HASH)

OTHER_CHAT_ID = getenv('other_channel_id')
MY_CHAT_ID = int(getenv('my_channel_id'))
MY_CHAT_ID2 = int(getenv('my_channel_id2'))
PD_CHAT_ID = getenv('pd_chat_id')


#Capturing messages from the targetted Telegram Channel

@client.on(events.NewMessage(chats=OTHER_CHAT_ID))
async def handler(event):
    if event.sticker:
        if 'CAADBQADywIAAkwuuVeu_xH13qrbzwI' == event.file.id:
            #printing date 
            dat = datetime.datetime.today() + datetime.timedelta(days=1)
            dat = dat.strftime('%d %B %Y') 
                #daily quotes api
            url = "https://api.quotable.io/random"
            response =  requests.get(url)
            json_data = response.json()
            #sending message to channel...
            msg = f"🌞 **Good Morning! **🌞  \n__{dat} \n{json_data['content']} \n- {json_data['author']}__"
            await client.send_message(entity=MY_CHAT_ID, message=msg, parse_mode='md')
            await client.send_message(entity=MY_CHAT_ID2, message=msg, parse_mode='md')

@client.on(events.NewMessage(chats=OTHER_CHAT_ID))
async def handler(event):
    
    # filtering documents
    if event.document:
        if 'TH-DELHI' in event.file.name.upper():
            await event.download_media(file=open(event.file.name, "wb"))
            pdf_mgmt(event.file.name)
            await client.send_file(MY_CHAT_ID,file= open(event.file.name, 'rb'), thumb='thumb.jpg')
            await client.send_file(MY_CHAT_ID2,file= open(event.file.name, 'rb'), thumb='thumb.jpg')
            m = await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')
            # await asyncio.sleep(10)
            # await client.delete_messages(PD_CHAT_ID, [m.id])
            remove(event.file.name)

        elif 'IE DELHI' in event.file.name.upper():
            await event.download_media(file=open(event.file.name, "wb"))
            pdf_mgmt(event.file.name)
            await client.send_file(MY_CHAT_ID, open(event.file.name, 'rb'), thumb='thumb.jpg')
            await client.send_file(MY_CHAT_ID2, open(event.file.name, 'rb'), thumb='thumb.jpg')
            m = await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')
            # await asyncio.sleep(10)
            # await client.delete_messages(PD_CHAT_ID, [m.id])
            remove(event.file.name)

        elif 'MAGAZINE' in event.file.name.upper():
            await event.download_media(file=open(event.file.name, "wb"))
            pdf_mgmt(event.file.name)
            await client.send_file(MY_CHAT_ID, open(event.file.name, 'rb'), thumb='thumb.jpg')
            await client.send_file(MY_CHAT_ID2, open(event.file.name, 'rb'), thumb='thumb.jpg')
            m = await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')
            # await asyncio.sleep(10)
            # await client.delete_messages(PD_CHAT_ID, [m.id])
            remove(event.file.name)
            
        else:
            if not event.sticker:
                await client.send_file(MY_CHAT_ID, event.message, schedule=datetime.timedelta(seconds=10))
                await client.send_file(MY_CHAT_ID2, event.message, schedule=datetime.timedelta(seconds=10))
                m = await client.send_message(PD_CHAT_ID, f'Uploaded {event.file.name}')
                # await asyncio.sleep(10)
                # await client.delete_messages(PD_CHAT_ID, [m.id])
        

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