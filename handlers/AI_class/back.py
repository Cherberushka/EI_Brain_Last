from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import dp


@dp.callback_query_handler(text='back', state='*')
async def back(call: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1,
                              inline_keyboard=[
                                  [InlineKeyboardButton(text="Поделись, пожалуйста, что тебя тревожит?", callback_data="start")]])
    await call.message.answer(
        f"Привет, я создан чтобы дать тебе ответы на интересующие тебя вопросы.",
        reply_markup=kb)
    await state.finish()


def register_handlers_back(dp: Dispatcher):
    dp.register_message_handler(back, text=['back'])
