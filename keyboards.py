from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

inline_keyboard_start = InlineKeyboardMarkup(row_width=1,
                                             resize_keyboard=True)
button_menu = InlineKeyboardButton(text="Меню", callback_data="Menu")
inline_keyboard_start.add(button_menu)

inline_keyboard_menu = InlineKeyboardMarkup(row_width=1,
                                            resize_keyboard=True)
button_recommend_minor = InlineKeyboardButton(text="Порекомендуйте мне майнор!", callback_data="AwaitingMessage")
button_send_minors = InlineKeyboardButton(text="Полезные ссылки", callback_data="UsefulLinks")
inline_keyboard_menu.add(button_recommend_minor, button_send_minors)
