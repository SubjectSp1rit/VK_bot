from aiogram import (types,
                     Dispatcher)
from initialisation import (bot,
                            llm)
from keyboards import (inline_keyboard_start,
                       inline_keyboard_menu)
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import (State,
                                              StatesGroup)
from aiogram.dispatcher import FSMContext
import aiofiles
import datetime
import asyncio


class FSM(StatesGroup):
    user_message = State()


# Записать 1 событие в лог
async def make_log(log_type, username, msg):
    async with aiofiles.open(file="log.txt",
                             mode="a",
                             encoding="utf-8") as f:
        await f.write(
            f"[{log_type}] | {str(datetime.datetime.now())[:-7]} | {username} {msg}\n")


# Создание промпта на основе данных из файла и сообщения пользователя
async def make_prompt(user_msg):
    async with aiofiles.open(file="minors-headers.txt",
                             mode="r",
                             encoding="utf-8") as f:
        lines = await f.read()
    prompt = f'Студент написал следующее сообщение: \"{user_msg}\", далее приведен список доступных курсов: {lines}На основании интересов студента, перечисленных в его сообщении, подбери 5 наиболее подходящих курсов из списка. ПИШИ НА РУССКОМ ЯЗЫКЕ. Напиши майноры в виде 1. НАЗВАНИЕ, 2. НАЗВАНИЕ и т.д. после каждого названия через дефис опиши почему ты выбрал именно этот майнор, НО НЕ ПИШИ БОЛЬШЕ НИЧЕГО КРОМЕ ЭТОГО. НЕ ПИШИ ВСТУПЛЕНИЕ И ЗАКЛЮЧЕНИЕ.'
    return prompt


# Обёрточная асинхронная функция для не асинхронной функции
async def get_response_from_ollama(prompt, username):
    try:
        await make_log("CLIENT", username, "отправил запрос")
        response = await asyncio.to_thread(llm.complete, prompt)
        await make_log("CLIENT", username, "получил ответ")
        return response
    except Exception:
        await make_log("CLIENT", username, "произошла ошибка при обработке запроса")


async def user_message(message: types.Message, state: FSMContext):
    processing_message = await bot.send_message(chat_id=message.from_user.id,
                                                text="Отлично! Мы уже обрабатываем ваш запрос и совсем скоро вернемся с ответом :)")
    user_answer = message.text
    await state.update_data(user_message=user_answer)
    await state.finish()

    prompt = await make_prompt(message.text)

    response = await get_response_from_ollama(prompt, message.from_user.username)

    await bot.delete_message(chat_id=processing_message.chat.id,
                             message_id=processing_message.message_id)
    await bot.send_message(chat_id=message.from_user.id,
                           text=response,
                           parse_mode=ParseMode.MARKDOWN,
                           reply_markup=inline_keyboard_start)


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
    await make_log("CLIENT", message.from_user.username, "запустил бота")


async def callback(callback_query: types.CallbackQuery):
    if callback_query.data == "Menu":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Вы попали в меню. Пожалуйста, воспользуйтесь кнопками ниже:",
                                    reply_markup=inline_keyboard_menu)
    elif callback_query.data == "AwaitingMessage":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Отправьте сообщение в произвольной форме, содержащее информацию о том, что вам интересно и что вы ожидаете от майнора, а мы подберем майноры специально для вас:",
                                    reply_markup=None)
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
    dp.register_callback_query_handler(callback=callback)
    dp.register_message_handler(user_message, state=FSM.user_message)
