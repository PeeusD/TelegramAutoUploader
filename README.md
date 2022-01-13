# TelegramAutoUploader
This is the telegram auto scrapper scraps content from targeted TG channel and uploads to your own TG channel written using Telethon.

# Installation

You need Python3 (3.6 works fine, 3.5 will crash randomly).

Install dependencies by running this command:

    pip install -r requirements.txt

(If you want faster downloading-uploading, then install `cryptg` and its dependencies)

Warning: If you get a `File size too large message`, check the version of Telethon library you are using. Old versions have got a 1.5Gb file size limit.


Obtain your own api id: https://core.telegram.org/api/obtaining_api_id

# Usage

You need to configure these values:

| Environment Variable     | Command Line argument | Description                                                  
|--------------------------|:-----------------------:|---------------------------------------------------------------|
| `api_hash`                 | `--api-hash`          | api_id from https://core.telegram.org/api/obtaining_api_id| 
| `api_id`                   | `--api-id`            | api_hash from https://core.telegram.org/api/obtaining_api_id  |
| `bot_chat_id`              | `--bot_chat_id`       | Destination bots for downloaded files                | 
| `bot_chat_id2`             | `--bot_chat_id`       | Destination bots for downloaded files                |
| `my_channel_id`            | `--channel_id`        | Your Channel id 1                                        | 
| `my_channel_id2`           | `--channel_id`        | Your Cahnnel id 2 |                                       |
| `other_channel_id`         | `--channel_id`        | Other scrapped Channel id  | Get from @userbot           |
| `pd_chat_id`               | `--your chat_id`      | Get from @botfather |                              |
