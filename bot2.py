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

flag = True

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
    await message.reply(f"Привет, я WS-бот, который поможет тебе легко подать заявки на участие\nв ивенте от Witches Sabbath и получить самую важную инфу по ближайшему рейву!",reply_markup=keyboard, parse_mode='HTML')

# Обработка DJ
@dp.message_handler(Text(equals='Заявка на DJ 🎧', ignore_case=True))
async def process_start_application(message: types.Message):
    global current_step, flag
    current_step = 'waiting_for_nickname'
    flag = False
    await message.reply(f"ВАЖНО! Прежде чем оставить заявку\n внимательно прочти это сообщение.\nОтправление заявки не дает гарантии в участии.\nВсе кандидаты будут рассмотрены организаторами\nпосле составления основного лайн-апа.\nПреимущественные места за пультом выделяются\n для DJ саунд-систем организаторов.")
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_dj_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)



# @dp.message_handler(lambda message: current_step == 'waiting_for_nickname' and not flag)
# async def process_nickname(message: types.Message):
@dp.callback_query_handler(lambda c: c.data == 'start_dj_application')
async def start_kitchen_application(callback_query: types.CallbackQuery):
    global nickname, current_step, flag
    current_step = 'waiting_for_dj_name'
    #await message.answer("Напиши свой жанр")
    await bot.send_message(callback_query.from_user.id, "Напиши свой никнейм")

@dp.message_handler(lambda message: current_step == 'waiting_for_dj_name' and not flag)
async def process_style_music(message: types.Message):
    if await handle_menu_buttons(message):
        return
    global nickname,style_music, current_step, flag
    nickname = message.text
    current_step = 'waiting_for_style_music'
    await message.answer("Напиши свой жанр")

@dp.message_handler(lambda message: current_step == 'waiting_for_style_music' and not flag)
async def process_style_music(message: types.Message):
    if await handle_menu_buttons(message):
        return
    global style_music, current_step, flag
    style_music = message.text
    current_step = 'waiting_for_contact'
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(lambda message: current_step == 'waiting_for_contact' and not flag)
async def process_contact(message: types.Message):
    if await handle_menu_buttons(message):
        return
    global nickname, style_music, current_step, flag
    contact = message.text
    await bot.send_message(chat_id=271883858, text=f"Никнейм: {nickname}\nЖанр: {style_music}\nКонтакт: {contact}")
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
    flag = True


# Обработка Кухни/Бара
@dp.message_handler(Text(equals='Заявка на кухню/бар/рыночек 🌭🍻🎨', ignore_case=True))
async def process_kitchen_application(message: types.Message):
    global kitchen_current_step, flag
    kitchen_current_step = 'waiting_for_kitchen_name'
    flag = False
    await message.answer("Привет! В 2024 году у нас абсолютно свободные условия для размещения\nкоммерческих участников на нашем мероприятии. Нам важно только знать, что вы не\nторгуете ничем запрещенным или тем, что не соответствует ценностям и формату\nмероприятия. Поэтому все заявки подлежат рассмотрению.\n\nМы будем очень рады видеть у себя на мероприятии бар, кухню, мастер-классы по\nдуховным практикам, продажу безделушек и тому подобное. Чем больше занятий - тем\nвсем веселее и приятнее.")
   
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_kitchen_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'start_kitchen_application')
async def start_kitchen_application(callback_query: types.CallbackQuery):
    global kitchen_current_step, flag
    kitchen_current_step = 'waiting_for_kitchen_name'
    flag = False
    await bot.send_message(callback_query.from_user.id, "Как к тебе обращаться?")
    #reply_markup=types.ReplyKeyboardRemove()

@dp.message_handler(lambda message: kitchen_current_step == 'waiting_for_kitchen_name' and not flag)
async def process_kitchen_name(message: types.Message):
    if await handle_menu_buttons(message):
        return
    global kitchen_name, kitchen_current_step, flag
    kitchen_name = message.text
    kitchen_current_step = 'waiting_for_kitchen_description'
    await message.answer("Что хочешь поставить?")

@dp.message_handler(lambda message: kitchen_current_step == 'waiting_for_kitchen_description' and not flag)
async def process_kitchen_description(message: types.Message):
    if await handle_menu_buttons(message):
        return
    global kitchen_description, kitchen_current_step, flag
    kitchen_description = message.text
    kitchen_current_step = 'waiting_for_kitchen_contact'
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(lambda message: kitchen_current_step == 'waiting_for_kitchen_contact' and not flag)
async def process_kitchen_contact(message: types.Message):
    if await handle_menu_buttons(message):
        return
    global kitchen_name, kitchen_description, kitchen_current_step, flag
    kitchen_contact = message.text
    await bot.send_message(chat_id=271883858, text=f"Имя участника: {kitchen_name}\nЧто хочет поставить: {kitchen_description}\nКонтакт: {kitchen_contact}")
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
    flag = True


@dp.message_handler(Text(equals='Где туса? 🏝', ignore_case=True))
async def process_location(message: types.Message):
    channel_chat_id = -1001335969565
    message_id = 269
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Когда туса? 🌚', ignore_case=True))
async def process_date(message: types.Message):
    channel_chat_id = -1001335969565
    message_id = 269
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Что мне взять с собой? ⛺️🦍', ignore_case=True))
async def process_packing_list(message: types.Message):
    #channel_chat_id = '@ws_tes'
    channel_chat_id = -1001335969565
    message_id = 259
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Отправить нам донатик ❤️', ignore_case=True))
async def process_donate(message: types.Message):
     await message.reply(f"🚨 <b>ДОНАТ - НЕОТЪЕМЛЕМАЯ ЧАСТЬ FREE TEKNO!</b>\nДрузья, для нас очень важны ваши донаты.\nКаждая копейка идёт в организацию и на аренду\nгенератора, транспортировку и покупку топлива для него.\nОстальное будет поделено поровну между участвующими\nсаунд системами в качестве возмещения затрат.\n\n<b>Внести свой вклад в движение\nFREE TEKNO на карту:\n2202 2067 3243 0694\n7 (987) 432-03-28 Сбер\nСЕРГЕЙ АРТУРОВИЧ Б.</b>", parse_mode='HTML')
    # channel_chat_id = '@ws_tes'
    # message_id = 2
    # await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)


async def handle_menu_buttons(message: types.Message) -> bool:
    if message.text in ["Заявка на DJ 🎧", "Заявка на кухню/бар/рыночек 🌭🍻🎨", "Когда туса? 🌚", "Где туса? 🏝", "Что мне взять с собой? ⛺️🦍", "Отправить нам донатик ❤️"]:
        # Dispatch the corresponding handler
        if message.text == "Заявка на DJ 🎧":
            await process_start_dj_application(message)
        elif message.text == "Заявка на кухню/бар/рыночек 🌭🍻🎨":
            await process_start_kitchen_application(message)
        elif message.text == "Когда туса? 🌚":
            await process_date(message)
        elif message.text == "Где туса? 🏝":
            await process_location(message)
        elif message.text == "Что мне взять с собой? ⛺️🦍":
            await process_packing_list(message)
        elif message.text == "Отправить нам донатик ❤️":
            await process_donate(message)
        return True
    return False

if __name__ == '__main__':
    executor.start_polling(dp)






