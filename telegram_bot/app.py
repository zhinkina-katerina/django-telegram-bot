import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

storage = MemoryStorage()
bot = Bot(token=os.getenv('BOT_API_TOKEN'))
dp = Dispatcher(bot, storage=storage)
