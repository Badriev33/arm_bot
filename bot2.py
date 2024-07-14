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

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1xYZIKaiM0bPjA-Qd-5geFTnvyA2t7M2wbxcm9tB4QWw'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

TOKEN = "7328590211:AAFu-1E7TK_8L43jTamVT2SJx6X3nyhQLNk"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

current_step = None
nickname = None
style_music = None

kitchen_current_step = None
kitchen_name = None
kitchen_description = None
kitchen_contact = None



@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Заявка на DJ 🎧"),
            types.KeyboardButton(text="Заявка на кухню/бар/рыночек 🌭🍻🎨"),
        ],
        [
             types.KeyboardButton(text="Когда туса? 🌚"),
             types.KeyboardButton(text="Где туса? 🏝"),
        ],
        [
            types.KeyboardButton(text="Что мне взять с собой? ⛺️🦍"),
            types.KeyboardButton(text="Отправить нам донатик ❤️"),
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.reply(f"Привет, я WS-бот, который поможет тебе легко подать заявки на участие в ивенте от\nWitches Sabbath и получить самую важную инфу по ближайшему рейву!",reply_markup=keyboard, parse_mode='HTML')


#Обработка DJ
@dp.message_handler(Text(equals='Заявка на DJ 🎧', ignore_case=True))
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


# Обработка Кухни/Бара
@dp.message_handler(Text(equals='Заявка на кухню/бар/рыночек 🌭🍻🎨', ignore_case=True))
async def process_kitchen_application(message: types.Message):
    global kitchen_current_step
    kitchen_current_step = 'waiting_for_kitchen_name'
    await message.answer("Привет! В 2024 году у нас абсолютно свободные условия для размещения\nкоммерческих участников на нашем мероприятии. Нам важно только знать, что вы не\nторгуете ничем запрещенным или тем, что не соответствует ценностям и формату\nмероприятия. Поэтому все заявки подлежат рассмотрению.\n\nМы будем очень рады видеть у себя на мероприятии бар, кухню, мастер-классы по\nдуховным практикам, продажу безделушек и тому подобное. Чем больше занятий - тем\nвсем веселее и приятнее.")
   
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_kitchen_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'start_kitchen_application')
async def start_kitchen_application(callback_query: types.CallbackQuery):
    global kitchen_current_step
    kitchen_current_step = 'waiting_for_kitchen_name'
    await bot.send_message(callback_query.from_user.id, "Как к тебе обращаться?")

@dp.message_handler(lambda message: kitchen_current_step == 'waiting_for_kitchen_name')
async def process_kitchen_name(message: types.Message):
    global kitchen_name, kitchen_current_step
    kitchen_name = message.text
    kitchen_current_step = 'waiting_for_kitchen_description'
    await message.answer("Что хочешь поставить?")

@dp.message_handler(lambda message: kitchen_current_step == 'waiting_for_kitchen_description')
async def process_kitchen_description(message: types.Message):
    global kitchen_description, kitchen_current_step
    kitchen_description = message.text
    kitchen_current_step = 'waiting_for_kitchen_contact'
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(lambda message: kitchen_current_step == 'waiting_for_kitchen_contact')
async def process_kitchen_contact(message: types.Message):
    global kitchen_name, kitchen_description, kitchen_current_step
    kitchen_contact = message.text
    await bot.send_message(chat_id=1310388442, text=f"Название заведения: {kitchen_name}\nОписание: {kitchen_description}\nКонтакт: {kitchen_contact}")
    await message.reply("Спасибо, что оставил заявку! Скоро свяжемся с тобой и обсудим детали.")
    values = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="kitchenRequests!A:C",  # Указываем вторую страницу и диапазон столбцов A, B, C
        valueInputOption="USER_ENTERED",
        body={
            "majorDimension": "ROWS",
            "values": [[kitchen_name, kitchen_description, kitchen_contact]]
        }
    ).execute()
    kitchen_current_step = None
    kitchen_name = None
    kitchen_description = None
    kitchen_contact = None


@dp.message_handler(Text(equals='Где туса? 🏝', ignore_case=True))
async def process_kitchen_application(message: types.Message):
    global kitchen_name, kitchen_description, kitchen_current_step,kitchen_contact
    kitchen_current_step = None
    kitchen_name = None
    kitchen_description = None
    kitchen_contact = None
    channel_chat_id = '@ws_tes'
    message_id = 2
    #await message.reply(message)
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Когда туса? 🌚', ignore_case=True))
async def process_kitchen_application(message: types.Message):
    channel_chat_id = '@ws_tes'
    message_id = 2
    #await message.reply(message)
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Что мне взять с собой? ⛺️🦍', ignore_case=True))
async def process_kitchen_application(message: types.Message):
    channel_chat_id = '@ws_tes'
    message_id = 2
    #await message.reply(message)
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)


if __name__ == '__main__':
    executor.start_polling(dp)