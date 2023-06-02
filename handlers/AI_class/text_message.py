import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions
from main import dp
from states.talk_state import AI
from handlers.AI_class.type_answer import ask_type_of_message

from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("reset"), state='*')
async def reset_command_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Спасибо, что поделился своими переживаниями со мной." + "\n" * 2 +
                         "Если вам снова понадобится чтобы вас выслушали, вы всегда можешь обратиться ко мне за помощью")


@dp.message_handler(state=AI.talk)
async def text_message_handler(message: types.Message, state: FSMContext):
    await message.answer_chat_action(ChatActions.TYPING)
    await state.update_data(text=message.text)
    await asyncio.sleep(1)
    await AI.type_answer.set()
    await ask_type_of_message(message)


def register_handlers_text_message(dp: Dispatcher):
    dp.register_message_handler(text_message_handler, state=AI.talk)
    dp.register_message_handler(reset_command_handler, Command("reset"), state='*')
