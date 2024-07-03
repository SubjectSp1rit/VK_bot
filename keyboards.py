from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

inline_keyboard_start = InlineKeyboardMarkup(row_width=1)
menubutton = InlineKeyboardButton(text='Меню', callback_data='/Меню')
inline_keyboard_start.add(menubutton)

keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button_add_request = KeyboardButton('Оставить заявку на вынос елки')
button_send_info = KeyboardButton('Информация об исполнителе')
keyboard_menu.add(button_add_request).add(button_send_info)
