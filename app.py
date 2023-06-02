from aiogram import executor

from main import dp
from handlers import start, help, AI_class
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    AI_class.audio_message.register_handlers_audio_message(dp)
    AI_class.back.register_handlers_back(dp)
    AI_class.clear.register_handlers_chat_start(dp)
    AI_class.text_message.register_handlers_text_message(dp)
    AI_class.type_answer.register_handlers_type_answer(dp)
    start.register_handlers_start(dp)
    help.register_handlers_help(dp)
