import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions
from loguru import logger
from audio_file_operations import audio_convert, audio_recognition, FFmpeg
from main import bot
from main import dp
from states.talk_state import AI
from tts import TTS
from handlers.AI_class.type_answer import ask_type_of_message

tts = TTS()


# Перевод аудио в текст Speech to Text (STT) - Хэндлер на получение голосового и аудио сообщения
@dp.message_handler(content_types=[types.ContentType.VOICE, types.ContentType.AUDIO], state=AI.talk)
async def voice_message_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer_chat_action(ChatActions.TYPING)
    await asyncio.sleep(1)
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    logger.info(file_path)
    await bot.download_file(file_path, FFmpeg.FILE_IN)
    await audio_convert()
    text = await audio_recognition()

    if not text:
        text = "Формат документа не поддерживается"
    await state.update_data(text=text)
    await AI.type_answer.set()
    await ask_type_of_message(message)


def register_handlers_audio_message(dp: Dispatcher):
    dp.register_message_handler(voice_message_handler, state=AI.talk)
