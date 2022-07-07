import configparser
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from django.contrib.auth.password_validation import validate_password

from users.models import TelegramUserProvider, TelegramUser
from .app import dp

config = configparser.ConfigParser()
this_folder = os.path.dirname(os.path.abspath(__file__))
config.read(os.path.join(this_folder, 'config.ini'))
telegram_user_provider = TelegramUserProvider()


class Form(StatesGroup):
    login = State()
    password = State()
    duplicate_password = State()


@dp.message_handler(commands='start')
async def start(message: Message):
    await message.answer(config.get('messages', 'start'))


@dp.message_handler(commands='registration', State=None)
async def request_login(message: Message):
    try:
        TelegramUser.objects.get(telegram_user_id=message.from_user.id)
        await message.reply(config.get('messages', 'account_already_exist'))
    except TelegramUser.DoesNotExist:
        await Form.login.set()
        await message.reply(config.get('messages', 'request_login'))


@dp.message_handler(state=Form.login)
async def set_login(message: Message, state: FSMContext):
    if len(message.text) < 3:
        await message.reply(config.get('messages', 'login_too_short'))
        return
    try:
        TelegramUser.objects.get(username=message.text)
        await message.reply(config.get('messages', 'login_already_exist'))
    except TelegramUser.DoesNotExist:
        async with state.proxy() as data:
            data['login'] = message.text
        await Form.next()
        await message.reply(config.get('messages', 'request_password'))


@dp.message_handler(state=Form.password)
async def set_password(message: Message, state: FSMContext):
    try:
        validate_password(message.text)
    except Exception as e:
        exceptions = '\n'.join(list(e))
        await message.reply(config.get('messages', 'passwords_invalid') + '\n\n' + exceptions)
        return
    async with state.proxy() as data:
        data['password'] = message.text
    await Form.next()
    await message.reply(config.get('messages', 'confirm_password'))


@dp.message_handler(state=Form.duplicate_password)
async def complete_registration(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != data['password']:
            data['password'] = None
            await Form.previous()
            await message.reply(config.get('messages', 'password_not_confirmed'))
            return

        was_created_or_update, error_message = await telegram_user_provider.create_or_update_user(
            telegram_fullname=message.from_user.full_name,
            telegram_username=message.from_user.username,
            telegram_user_id=message.from_user.id,
            login=data['login'],
            password=data['password']
        )
        await state.finish()
        if error_message:
            await message.reply(config.get('messages', 'account_not_created') + '\n\n' + error_message)
            return
        if was_created_or_update:
            await message.reply(config.get('messages', 'account_created'))
        else:
            await message.reply(config.get('messages', 'changes_have_been_made'))


@dp.message_handler(commands='change_password')
async def start_change_password(message: Message, state: FSMContext):
    try:
        login = TelegramUser.objects.get(telegram_user_id=message.from_user.id).username
    except TelegramUser.DoesNotExist:
        await message.reply(config.get('messages', 'non-existent_user'))
        return

    async with state.proxy() as data:
        data['login'] = login
    await Form.password.set()
    await message.reply(config.get('messages', 'request_password'))


@dp.message_handler(commands='remind_login')
async def remind_login(message: Message):
    try:
        login = TelegramUser.objects.get(telegram_user_id=message.from_user.id).username
        await message.reply(f'Your login is: {login}')
    except TelegramUser.DoesNotExist:
        await message.reply(config.get('messages', 'non-existent_user'))
        return
