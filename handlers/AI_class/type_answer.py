import asyncio
import os
from pathlib import Path
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ChatActions

from handlers.AI_class.AI_response import ai_response
from main import bot
from main import dp
from states.talk_state import AI
from tts import TTS
from handlers.AI_class.keyboards import type_answer_keyboard, type_voice_keyboard


# tts = TTS()


async def ask_type_of_message(message: types):
    await message.answer_chat_action(ChatActions.TYPING)
    await asyncio.sleep(1)
    await message.answer("В каком формате мне ответить?:", reply_markup=type_answer_keyboard)


async def response(state: FSMContext, message: types, type_action):
    if type_action == 'voice':
        await message.answer_chat_action(ChatActions.RECORD_VOICE)
    else:
        await message.answer_chat_action(ChatActions.TYPING)
    data = await state.get_data()
    # session_id = data.get('session_id')
    # print(session_id)
    history = data.get('history', [])
    text = data.get('text')  # message.text
    print(text)
    resp_ai = await ai_response(history, text)
    print(resp_ai)
    history[-1]['answer'] = resp_ai.replace('\n', '')
    text = f"{message.from_user.username}\nQ:{history[-1]['question']}\nA:{history[-1]['answer']}"
    history.append({"question": None, "answer": None})
    if len(history) > 25:
        history = [{"question": None, "answer": None}]
    await state.update_data(history=history, resp_ai=resp_ai)
    return resp_ai


async def ask_type_of_voice(message: types):
    await message.answer_chat_action(ChatActions.TYPING)
    await asyncio.sleep(1)
    await message.answer("Выберите голос озвучки:", reply_markup=type_voice_keyboard)
    print('First check')


# @dp.callback_query_handler(lambda c: c.data and c.data in ["male", "female"], state=AI.type_voice)
@dp.callback_query_handler(lambda c: c.data, state=AI.type_voice)
async def voice_answer_to_users(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_last_bot_message(callback_query)
    data = callback_query.data
    await state.update_data(voice_type=data)
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    voice_type = user_data.get("voice_type")
    speech_voice = str()
    if voice_type == "female":
        speech_voice = "xenia"
    elif voice_type == "male":
        speech_voice = "eugene"
    await callback_query.message.answer_chat_action(ChatActions.RECORD_VOICE)
    await asyncio.sleep(1)
    resp_ai = await response(state, callback_query.message, 'voice')
    tts = TTS(speaker_voice=f"{speech_voice}")
    out_filename = tts.text_to_ogg(resp_ai)
    path = Path("", out_filename)
    voice = InputFile(path)
    await bot.send_voice(callback_query.from_user.id, voice)
    os.remove(out_filename)
    await AI.talk.set()


async def delete_last_bot_message(update: types.Update):
    bot = update.bot
    chat_id = update.message.chat.id
    message_id = update.message.message_id  # идентификатор последнего сообщения бота
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


@dp.callback_query_handler(lambda c: c.data and c.data in ["text", "voice"], state=AI.type_answer)
async def answer_to_users(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_last_bot_message(callback_query)
    data = callback_query.data
    await state.update_data(message_type=data)
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    message_type = user_data.get("message_type")
    if message_type == "voice":
        await callback_query.message.answer_chat_action(ChatActions.TYPING)
        await AI.type_voice.set()
        await ask_type_of_voice(callback_query.message)
    elif message_type == "text":
        await callback_query.message.answer_chat_action(ChatActions.TYPING)
        await asyncio.sleep(1)
        resp_ai = await response(state, callback_query.message, 'text')
        print(resp_ai)
        await callback_query.message.answer(resp_ai)
        await AI.talk.set()


def register_handlers_type_answer(dp: Dispatcher):
    dp.register_callback_query_handler(answer_to_users,
                                       lambda c: c.data in ["text", "voice", "both"], state=AI.type_answer)
    dp.register_callback_query_handler(voice_answer_to_users,
                                       lambda c: c.data in ["male", "female"], state=AI.type_voice)
