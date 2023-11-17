from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_API_ID = os.environ["TELEGRAM_API_ID"]
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]


with TelegramClient(StringSession(), TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
    # This is how variable 'TELEGRAM_STRING_TOKEN' comes from
    # When you execute this script, you are required to input
    # - your phone number
    # - login code (you need to check on Telegram)
    print(client.session.save())

