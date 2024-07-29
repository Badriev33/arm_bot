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
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class DJForm(StatesGroup):
    nickname = State()
    style_music = State()
    contact = State()

class KitchenForm(StatesGroup):
    name = State()
    description = State()
    contact = State()

class MerchForm(StatesGroup):
    name = State()
    size = State()
    color = State()
    contact = State()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Заявка на DJ 🎧"),
            types.KeyboardButton(text="Заявка на кухню/бар/рыночек 🌭🍻🎨"),
        ],
        [
             types.KeyboardButton(text="Когда туса? 🌚"),
            #  types.KeyboardButton(text="Где туса? 🏝"),
        ],
        [
            # types.KeyboardButton(text="Что мне взять с собой? ⛺️🦍"),
            types.KeyboardButton(text="Отправить нам донатик ❤️"),
        ],
        # [
        #     types.KeyboardButton(text="Купить мерч 👕👚"),
        # ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.reply(f"Привет, я WS-бот, который поможет тебе легко подать заявки на участие в ивенте от Witches Sabbath и получить самую важную инфу по ближайшему рейву!",reply_markup=keyboard, parse_mode='HTML')

# Обработка DJ
@dp.message_handler(Text(equals='Заявка на DJ 🎧', ignore_case=True))
async def process_start_application(message: types.Message):
    await message.reply(f"ВАЖНО! Прежде чем оставить заявку внимательно прочти это сообщение.\n\nОтправление заявки не дает гарантии в участии. Все кандидаты будут рассмотрены организаторами после составления основного лайн-апа. Преимущественные места за пультом выделяются для DJ саунд-систем организаторов. Заявки принимаются до 14 августа.\n\nP.S. Если ты играешь лёгкий жанр, то ты можешь обратиться к организатору чилл-зоны, чтобы встать на второй танцпол:\n@G_0_T_L")
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_dj_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'start_dj_application', state=None)
async def start_dj_application(callback_query: types.CallbackQuery):
    await DJForm.nickname.set()
    await bot.send_message(callback_query.from_user.id, "Напиши свой никнейм")

@dp.message_handler(state=DJForm.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
    await DJForm.next()
    await message.answer("Напиши свой жанр")

@dp.message_handler(state=DJForm.style_music)
async def process_style_music(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['style_music'] = message.text
    await DJForm.next()
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(state=DJForm.contact)
async def process_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text
        nickname = data['nickname']
        style_music = data['style_music']
        contact = data['contact']
    await bot.send_message(chat_id=384556684, text=f"Никнейм: {nickname}\nЖанр: {style_music}\nКонтакт: {contact}\nchat_id: {message['from'].id}") #271883858 - Серж
    await message.reply("Спасибо, что оставил заявку! Не выключай уведомления 😉 16 августа ты получишь сообщение со списком участников в этом боте. Если ты не найдешь себя в списке, то не вешай нос и все равно приезжай с контроллером. Бывает всякое, а освободившийся слот будет за тобой 🤘🏻")
    values = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="A:E",  # Указываем диапазон столбцов A, B, C
        valueInputOption="USER_ENTERED",
        body={
            "majorDimension": "ROWS",
            "values": [[nickname, style_music, contact, message['from'].id, 'none']]
        }
    ).execute()
    await state.finish()

# Обработка Кухни/Бара
@dp.message_handler(Text(equals='Заявка на кухню/бар/рыночек 🌭🍻🎨', ignore_case=True))
async def process_kitchen_application(message: types.Message):
    await message.answer("Привет! В 2024 году у нас абсолютно свободные условия для размещения коммерческих участников на нашем мероприятии. Нам важно только знать, что вы не торгуете ничем запрещенным или тем, что не соответствует ценностям и формату мероприятия. Поэтому все заявки подлежат рассмотрению.\n\nМы будем очень рады видеть у себя на мероприятии бар, кухню, мастер-классы по духовным практикам, продажу безделушек и тому подобное. Чем больше занятий - тем всем веселее и приятнее. Ты также можешь присоединиться как волонтёр, просто в пункте 2 - напиши 'Хочу волонтёрить'.")
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_kitchen_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'start_kitchen_application', state=None)
async def start_kitchen_application(callback_query: types.CallbackQuery):
    await KitchenForm.name.set()
    await bot.send_message(callback_query.from_user.id, "Как к тебе обращаться?")

@dp.message_handler(state=KitchenForm.name)
async def process_kitchen_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await KitchenForm.next()
    await message.answer("Что хочешь поставить?/Хочу волонтёрить")

@dp.message_handler(state=KitchenForm.description)
async def process_kitchen_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await KitchenForm.next()
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(state=KitchenForm.contact)
async def process_kitchen_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text
        name = data['name']
        description = data['description']
        contact = data['contact']
    await bot.send_message(chat_id=384556684, text=f"Имя участника: {name}\nЧто хочет поставить: {description}\nКонтакт: {contact}\nchat_id: {message['from'].id}")#271883858 - Серж
    await message.reply("Спасибо, что оставил заявку! Скоро свяжемся с тобой и обсудим детали.")
    values = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="kitchenRequests!A:E",  # Указываем вторую страницу и диапазон столбцов A, B, C
        valueInputOption="USER_ENTERED",
        body={
            "majorDimension": "ROWS",
            "values": [[name, description, contact, message['from'].id, 'none']]
        }
    ).execute()
    await state.finish()

# Обработка мерча
@dp.message_handler(Text(equals='Купить мерч 👕👚', ignore_case=True))
async def process_merch_application(message: types.Message):
    await message.reply(f"Оставь свой в telegram  для связи и напиши количество,\nразмер, и желаемый цвет. С тобой свяжутся и уточнят состав и\nналичие заказа.\n\nЧем раньше вами оставлена заявка, тем выше вероятность,\nчто желанный цвет и размер уже будет забронирован за вами.\nКоличество ограничено!»\n")
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_merch_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'start_merch_application', state=None)
async def start_merch_application(callback_query: types.CallbackQuery):
    await MerchForm.name.set()
    await bot.send_message(callback_query.from_user.id, "Напиши своё имя")

@dp.message_handler(state=MerchForm.name)
async def process_name_merch(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await MerchForm.next()
    await message.answer("Напиши свой размер")

@dp.message_handler(state=MerchForm.size)
async def process_merch_color(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await MerchForm.next()
    await message.answer("Напиши желаемый цвет")

@dp.message_handler(state=MerchForm.color)
async def process_merch_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['color'] = message.text
    await MerchForm.next()
    await message.answer("Напиши свой контакт для связи")

@dp.message_handler(state=MerchForm.contact)
async def process_merch_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text
        name = data['name']
        size = data['size']
        color = data['color']
        contact = data['contact']
    await bot.send_message(chat_id=384556684, text=f"Имя : {name}\nРазмер: {size}\nЦвет: {color}\nКонтакт: {contact}")#271883858 - Серж
    await message.reply("Спасибо, что оставил заявку! Скоро свяжемся с тобой и обсудим детали.")
    values = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="merch!A:C",  # Указываем вторую страницу и диапазон столбцов A, B, C
        valueInputOption="USER_ENTERED",
        body={
            "majorDimension": "ROWS",
            "values": [[name, color, size, contact]]
        }
    ).execute()
    await state.finish()

@dp.message_handler(Text(equals='Где туса? 🏝', ignore_case=True))
async def process_location(message: types.Message):
    channel_chat_id = -1001335969565
    message_id = 269
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Когда туса? 🌚', ignore_case=True))
async def process_date(message: types.Message):
    channel_chat_id = -1001335969565
    message_id = 291
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Что мне взять с собой? ⛺️🦍', ignore_case=True))
async def process_packing_list(message: types.Message):
    channel_chat_id = -1001335969565
    message_id = 259
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Отправить нам донатик ❤️', ignore_case=True))
async def process_donate(message: types.Message):
    await message.reply(f"🚨 <b>ДОНАТ - НЕОТЪЕМЛЕМАЯ ЧАСТЬ FREE TEKNO!</b>\nДрузья, для нас очень важны ваши донаты.\nКаждая копейка идёт в организацию и на аренду\nгенератора, транспортировку и покупку топлива для него.\nОстальное будет поделено поровну между участвующими\nсаунд системами в качестве возмещения затрат.\n\n<b>Внести свой вклад в движение\nFREE TEKNO на карту:\n2202 2067 3243 0694\n7 (987) 432-03-28 Сбер\nСЕРГЕЙ АРТУРОВИЧ Б.</b>", parse_mode='HTML')

if __name__ == '__main__':
    executor.start_polling(dp)