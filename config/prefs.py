import coc
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import TelegramClient

# telegram chat
CHAT_ID = -1001158139685
# CHAT_ID = -1001830875232 # FOR TEST CHAT

# aiogram
TOKEN = '1695339294:AAFwqPgFzginWlWeqFOCWEM3FpdEWrTeFCY'

# telethon client
API_ID = 21832548
API_HASH = '25632defdd39ab1a05f23b850ddfe83c'
PHONE = 380936566570
USER_BOT = 'Dark Elite'

# coc.py
CLAN_TAG = "#RYLQCJ2J"
ACADEMY_CLAN_TAG = "#2909YPCRU"
COC_LOGIN = 'pavelkobond@gmail.com'
COC_PASSWORD = 'Sanya_007'

coc_client = coc.login(COC_LOGIN, COC_PASSWORD, client=coc.EventsClient)
telethon_client = TelegramClient('client', API_ID, API_HASH).start()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
