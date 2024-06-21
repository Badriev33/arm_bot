import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters
#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "7328590211:AAFu-1E7TK_8L43jTamVT2SJx6X3nyhQLNk"

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
    
        # [
        #     types.KeyboardButton(text="Занять Stand1 ❌"),
        #     types.KeyboardButton(text="Занять Stand2 ❌")
        # ],
        [
            types.KeyboardButton(text="Заполнить заявку ✅"),
            # types.KeyboardButton(text="Освободить Stand2 ✅")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.reply(f"<b>Заявка DJ на участие в WitcheStek 2024</b>\nОбратите внимание, что заявки на выступление принимаются до 24 июля.Обратную связь предоставим 1 августа, тем участникам,\nкоторые будут отобраны для лайн-апа.\n\nВАЖНО: Отправление заявки не дает гарантии в участии.\nВсе кандидатуры будут рассмотрены организаторами\nпосле составления основного лайн-апа.\nПреимущественные места за пультом выделяются для DJ саунд-систем\nорганизаторов (Witches Sabbath, BulldoZZer, Сызраночка, Valhalla).",reply_markup=keyboard, parse_mode='HTML')

@dp.message_handler(filters.Text(equals='Заполнить заявку ✅', ignore_case=True))
async def process_update(message: types.Message) -> None:
    # if statusStand1 == 'true'
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    global statusStand1
    global statusStand2
    statusStand1 = "Занят❌"
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    await message.answer(
        f'Заполните следуещие пункты:\n1.Никнейм\n2.Контакт для связи (vk/ ник telegram)\n3.Стиль музыки'
        )
    
@dp.message_handler()
async def process_message(message: types.Message):
    await bot.send_message(chat_id=271883858, text=message.text) #Авас
    await message.reply(f"Спасибо за заявку, мы обязательно с вами свяжемся!")


if __name__ == '__main__':
    executor.start_polling(dp)