import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters
#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "5828238416:AAGM9_8_0iuuVQ9ciAt7rdUgqmSkC-_jrsg"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

statusStand1 = "Свободен✅"
statusStand2 = "Свободен✅"


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    
    kb = [
    # [types.KeyboardButton(text="Занять Stand1 ❌")],
    # [types.KeyboardButton(text="Занять Stand2 ❌")],
    # [types.KeyboardButton(text="Освободить Stand1 ✅")],
    # [types.KeyboardButton(text="Освободить Stand2 ✅")],
    
        [
            types.KeyboardButton(text="Занять Stand1 ❌"),
            types.KeyboardButton(text="Занять Stand2 ❌")
        ],
        [
            types.KeyboardButton(text="Освободить Stand1 ✅"),
            types.KeyboardButton(text="Освободить Stand2 ✅")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.reply(f"Есть 2 стенда на какой сам сядешь, какой пацанам оставишь?",reply_markup=keyboard)

@dp.message_handler(filters.Text(equals='Занять Stand1 ❌', ignore_case=True))
async def process_update(message: types.Message) -> None:
    # if statusStand1 == 'true'
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    global statusStand1
    global statusStand2
    statusStand1 = "Занят❌"
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    await message.answer(
        f'Первый стенд занял {user_full_name} {currentTime}\nПервый стенд {statusStand1} Второй стенд {statusStand2}'
        )
    

@dp.message_handler(filters.Text(equals='Занять Stand2 ❌', ignore_case=True))
async def process_update(message: types.Message) -> None:
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    global statusStand1
    global statusStand2
    statusStand2 = "Занят❌"
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    await message.answer(
        f'Второй стенд занял {user_full_name}, {currentTime}\nПервый стенд {statusStand1} Второй стенд {statusStand2}'
        )

@dp.message_handler(filters.Text(equals='Освободить Stand1 ✅', ignore_case=True))
async def process_update(message: types.Message) -> None:
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    global statusStand1
    global statusStand2
    statusStand1 = "Свободен✅"
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    await message.answer(
        f'Первый стенд освободил {user_full_name}, {currentTime}\nПервый стенд {statusStand1} Второй стенд {statusStand2}'
        )

@dp.message_handler(filters.Text(equals='Освободить Stand2 ✅', ignore_case=True))
async def process_update(message: types.Message) -> None:
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    global statusStand1
    global statusStand2
    statusStand2 = "Свободен✅"
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    await message.answer(
        f'Второй стенд освободил {user_full_name}, {currentTime}\nПервый стенд {statusStand1} Второй стенд {statusStand2}'
        )


if __name__ == '__main__':
    executor.start_polling(dp)