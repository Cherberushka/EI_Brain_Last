import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions

from handlers.AI_class.type_answer import delete_last_bot_message
from main import dp
from states.talk_state import AI
#import uuid


@dp.callback_query_handler(text='clear', state='*')
async def clear(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer_chat_action(ChatActions.TYPING)
    await asyncio.sleep(1)
    await callback_query.message.answer('Сменим тему.')
    # openai.Session.delete("session-id-here") только за бабки
    await state.update_data(history=[{"question": None, "answer": None}])


#  Применимо только для платного API, может быть создано до 4 сессий
# def generate_chat_name():
#     # Генерируем случайное название чата/пользователя с помощью uuid
#     chat_name = str(uuid.uuid4())
#     return chat_name


@dp.callback_query_handler(text='start')
async def chat_start(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_last_bot_message(callback_query)
    await callback_query.message.answer_chat_action(ChatActions.TYPING)
    await asyncio.sleep(1)
    await callback_query.message.answer("Поделись, пожалуйста, что тебя тревожит?")
    await AI.talk.set()
    # session_id = generate_chat_name()
    # print(session_id)
    await state.update_data(history=[{"question": None, "answer": None}])  # , session_id=session_id)


def register_handlers_chat_start(dp: Dispatcher):
    dp.register_message_handler(chat_start, text=['start'])
    # dp.register_message_handler(reset_fsm_handler, text=['reset'])
