from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ChatActions

type_answer_keyboard = InlineKeyboardMarkup(row_width=2)
type_answer_keyboard.add(InlineKeyboardButton(text="Текстовое сообщение", callback_data="text"),
                         InlineKeyboardButton(text="Голосовое сообщение", callback_data="voice"))
                         #InlineKeyboardButton(text="Голосовое и текстовое сообщение", callback_data="both"))

type_voice_keyboard = InlineKeyboardMarkup()
type_voice_keyboard.add(InlineKeyboardButton(text="Мужской", callback_data="male"),
                         InlineKeyboardButton(text="Женский", callback_data="female"))
