from aiogram import (types,
                     Dispatcher)
from initialisation import (bot,
                        dispatcher as dp)
from keyboards import (inline_keyboard_start,
                      inline_keyboard_menu)
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import (State,
                                              StatesGroup)
from aiogram.dispatcher import FSMContext
import aiofiles
import datetime


class FSM(StatesGroup):
    user_message = State()


async def user_message(message: types.Message, state: FSMContext):
    user_answer = message.text
    await state.update_data(user_message=user_answer)
    await bot.send_message(chat_id=message.from_user.id,
                           text="ТУТ ТИПА ОТВЕТ ОТ НЕЙРОНКИ :)",
                           reply_markup=inline_keyboard_start)
    await state.finish()
    async with aiofiles.open(file="log.txt",
                             mode="a",
                             encoding="utf-8") as f:
        await f.write(
            f"[CLIENT] | {str(datetime.datetime.now())[:-7]} | {message.from_user.username} получил ответ от нейросети\n")

async def start(message: types.Message):
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker="CAACAgIAAxkBAAELwhJl_AJptAuvjuMV5FlPY1hH-9-tigACJlQAAp7OCwABoKNdD9edZb80BA")
    if message.from_user.first_name and message.from_user.last_name:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Приветствую, {message.from_user.first_name} {message.from_user.last_name}!",
                               reply_markup=inline_keyboard_start)
    elif message.from_user.first_name and (not message.from_user.last_name): \
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Приветствую, {message.from_user.first_name}!",
                               reply_markup=inline_keyboard_start)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Приветствую, {message.from_user.last_name}!",
                               reply_markup=inline_keyboard_start)
    async with aiofiles.open(file="log.txt",
                             mode="a",
                             encoding="utf-8") as f:
        await f.write(f"[CLIENT] | {str(datetime.datetime.now())[:-7]} | {message.from_user.username} запустил бота\n")


async def menu(callback_query: types.CallbackQuery):
    if callback_query.data == "Menu":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Вы попали в меню. Пожалуйста, воспользуйтесь кнопками ниже:",
                                    reply_markup=inline_keyboard_menu)
    elif callback_query.data == "AwaitingMessage":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Отправьте сообщение в произвольной форме, содержащее информацию о майноре(-ах), которые вам бы понравились:",
                                    reply_markup=None)
        async with aiofiles.open(file="log.txt",
                                 mode="a",
                                 encoding="utf-8") as f:
            await f.write(f"[CLIENT] | {str(datetime.datetime.now())[:-7]} | {callback_query.from_user.username} запустил нейросеть\n")
        await FSM.user_message.set()
    elif callback_query.data == "UsefulLinks":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Актуальный список майноров: "
                                         "<a href=\"https://electives.hse.ru/catalog2023\">*тык*</a>\n\n"
                                         "Чаты всех майноров: "
                                         "<a href=\"https://docs.google.com/spreadsheets/d/1J9m8mNScX62UaX4PEy9bNP838ozbQ3kW1gLuZs5EiVo/edit\">*тык*</a>\n\n"
                                         "Отзывы на майноры №1: "
                                         "<a href=\"https://docs.google.com/spreadsheets/d/1r78C0eeiVBTCSjE2Sd7nPUGGCT-wv5qbtugutTnxtD8/edit?gid=1735646966#gid=1735646966\">*тык*</a>\n\n"
                                         "Отзывы на майноры №2: "
                                         "<a href=\"https://docs.google.com/spreadsheets/d/1nAdK4KV6RtcFxmHF6lmTEDtUsGAJE8VqVFI76PbwzCg/edit?gid=0#gid=0\">*тык*</a>\n\n"
                                         "Отзывы на майноры №3: "
                                         "<a href=\"https://docs.google.com/spreadsheets/d/1IhPFj43xkzMvK6fIM4xFJagLo7zxC4Xo4USH_5xKq7k/edit?gid=0#gid=0\">*тык*</a>\n\n",

                                    reply_markup=inline_keyboard_start,
                                    parse_mode="HTML")


def client_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_callback_query_handler(callback=menu)
    dp.register_message_handler(user_message, state=FSM.user_message)
