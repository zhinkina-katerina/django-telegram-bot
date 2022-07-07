import os

import django
from aiogram.utils import executor
from .app import dp
from . import commands

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

executor = executor.start_polling(dp, skip_updates=True)
