import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials 

#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

CREDENTIALS_FILE = ''
spreadsheet_id = ''

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# values = service.spreadsheets().values().get(
#     spreadsheetId=spreadsheet_id,
#     range='A1:E10',
#     majorDimension='COLUMNS'
# ).execute()
# pprint(values)

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

statusStand1 = "Свободен✅"
statusStand2 = "Свободен✅"

current_step = None
nickname = None
style_music = None


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    
    kb = [
        [
            types.KeyboardButton(text="Заполнить заявку ✅"),
            types.KeyboardButton(text="Заявка на кухню/бар/рыночек 🌭🍻🎨")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.reply(f"<b>Заявка DJ на участие в WitcheStek 2024</b>\nОбратите внимание, что заявки на выступление принимаются до 24 июля.Обратную связь предоставим 1 августа, тем участникам,\nкоторые будут отобраны для лайн-апа.\n\nВАЖНО: Отправление заявки не дает гарантии в участии.\nВсе кандидатуры будут рассмотрены организаторами\nпосле составления основного лайн-апа.\nПреимущественные места за пультом выделяются для DJ саунд-систем\nорганизаторов (Witches Sabbath, BulldoZZer, Сызраночка, Valhalla).",reply_markup=keyboard, parse_mode='HTML')


#Обработка DJ
@dp.message_handler(Text(equals='Заполнить заявку ✅', ignore_case=True))
async def process_start_application(message: types.Message):
    global current_step
    current_step = 'waiting_for_nickname'
    await message.answer("Напиши свой никнейм")

@dp.message_handler(lambda message: current_step == 'waiting_for_nickname')
async def process_nickname(message: types.Message):
    global nickname, current_step
    nickname = message.text
    current_step = 'waiting_for_style_music'
    await message.answer("Напиши свой жанр")

@dp.message_handler(lambda message: current_step == 'waiting_for_style_music')
async def process_style_music(message: types.Message):
    global style_music, current_step
    style_music = message.text
    current_step = 'waiting_for_contact'
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(lambda message: current_step == 'waiting_for_contact')
async def process_contact(message: types.Message):
    global nickname, style_music, current_step
    contact = message.text
    await bot.send_message(chat_id=1310388442, text=f"Никнейм: {nickname}\nЖанр: {style_music}\nКонтакт: {contact}")
    await message.reply("Спасибо за заявку, мы обязательно с вами свяжемся!")
    values = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="A:C",  # Указываем диапазон столбцов A, B, C
        valueInputOption="USER_ENTERED",
        body={
            "majorDimension": "ROWS",
            "values": [[nickname, style_music, contact]]
        }
    ).execute()
    current_step = None
    nickname = None
    style_music = None


#Обработка Кухни/Бара
@dp.message_handler(Text(equals='Заявка на кухню/бар/рыночек 🌭🍻🎨', ignore_case=True))
async def process_kitchen_application(message: types.Message):
    await message.answer("что по печенькам?")


if __name__ == '__main__':
    executor.start_polling(dp)


