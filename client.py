from aiogram import (types,
                     Dispatcher)
from initialisation import (bot,
                        dispatcher as dp)
from keyboards import (inline_keyboard_start,
                      keyboard_menu)
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import (State,
                                              StatesGroup)
from aiogram.dispatcher import FSMContext
import sqlite3 as sq
import asyncio


'''async def db_start():
    global db, cur

    db = sq.connect('database.db')
    cur = db.cursor()'''

async def start(message: types.Message):
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAELwhJl_AJptAuvjuMV5FlPY1hH-9-tigACJlQAAp7OCwABoKNdD9edZb80BA')
    if message.from_user.first_name and message.from_user.last_name:
        await bot.send_message(message.from_user.id,
                               f'Приветствую, {message.from_user.first_name} {message.from_user.last_name}!',
                               reply_markup=inline_keyboard_start)
    elif message.from_user.first_name and (not message.from_user.last_name): \
        await bot.send_message(message.from_user.id,
                               f'Приветствую, {message.from_user.first_name}!',
                               reply_markup=inline_keyboard_start)
    else:
        await bot.send_message(message.from_user.id,
                               f'Приветствую, {message.from_user.last_name}!',
                               reply_markup=inline_keyboard_start)


@dp.callback_query_handler()
async def menu(callback_query: CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="ПРОВЕРКА",
                                reply_markup=keyboard_menu)
    await bot.answer_callback_query(callback_query.id)
    #await bot.edit_message_text(chat_id=message.from_user.id,
    #                            message_id=message.message_id,
    #                            text="ПРОВЕРКА")


def client_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    #dp.register_callback_query_handler(callback=menu)
