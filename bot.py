import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters
import json

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


token_file = 'token.json'
# Чтение токена из JSON файла
with open(token_file, 'r') as file:
    data = json.load(file)
    TOKEN = data['token']


blocked_users = [670360975]

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
  user_id = message.from_user.id
  if user_id in blocked_users:
      # await message.reply("Вы заблокированы.")
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    kb = [
        [
            types.KeyboardButton(text="Заявка на DJ 🎧"),
            types.KeyboardButton(text="Заявка на кухню/бар/рыночек 🌭🍻🎨"),
        ],
        [
             types.KeyboardButton(text="Когда туса? 🌚"),
             types.KeyboardButton(text="Купить мерч 👕👚"),
        ],
        [
            types.KeyboardButton(text="Отправить нам донатик ❤️"),
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,

        resize_keyboard=True
    )
    await message.reply(f"Привет, я WS-бот, который поможет тебе легко подать заявки на участие в ивенте от Witches Sabbath и получить самую важную инфу по ближайшему рейву!",reply_markup=keyboard, parse_mode='HTML')

# Обработка DJ
@dp.message_handler(Text(equals='Заявка на DJ 🎧', ignore_case=True))
async def process_start_application(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  if user_id in blocked_users:
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    await message.reply(f"ВАЖНО! Прежде чем оставить заявку внимательно прочти это сообщение.\n\nОтправление заявки не дает гарантии в участии. Все кандидаты будут рассмотрены организаторами после составления основного лайн-апа. Преимущественные места за пультом выделяются для DJ саунд-систем организаторов. Заявки принимаются до 14 августа.\n\nP.S. Если ты играешь лёгкий жанр, то ты можешь обратиться к организатору чилл-зоны, чтобы встать на второй танцпол:\n@G_0_T_L")
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_dj_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)

    await state.finish()
    await state.reset_data()

@dp.callback_query_handler(lambda c: c.data == 'start_dj_application', state=None)
async def start_dj_application(callback_query: types.CallbackQuery):
    await DJForm.nickname.set()
    await bot.send_message(callback_query.from_user.id, "Напиши свой никнейм")

@dp.message_handler(state=DJForm.nickname)
async def process_style_music(message: types.Message, state: FSMContext):
    if await handle_menu_buttons(message, state):
        return
    async with state.proxy() as data:
        data['nickname'] = message.text
    await DJForm.next()
    await message.answer("Напиши свой жанр")

@dp.message_handler(state=DJForm.style_music)
async def process_style_music(message: types.Message, state: FSMContext):
    if await handle_menu_buttons(message, state):
        return
    async with state.proxy() as data:
        data['style_music'] = message.text
    await DJForm.next()
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(state=DJForm.contact)
async def process_contact(message: types.Message, state: FSMContext):
    if await handle_menu_buttons(message, state):
        return
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
async def process_kitchen_application(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  if user_id in blocked_users:
      # await message.reply("Вы заблокированы.")
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    await message.answer("Привет! В 2024 году у нас абсолютно свободные условия для размещения коммерческих участников на нашем мероприятии. Нам важно только знать, что вы не торгуете ничем запрещенным или тем, что не соответствует ценностям и формату мероприятия. Поэтому все заявки подлежат рассмотрению.\n\nМы будем очень рады видеть у себя на мероприятии бар, кухню, мастер-классы по духовным практикам, продажу безделушек и тому подобное. Чем больше занятий - тем всем веселее и приятнее. Ты также можешь присоединиться как волонтёр, просто в пункте 2 - напиши 'Хочу волонтёрить'.")
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton(text="Заполнить заявку", callback_data="start_kitchen_application"))
    await message.answer("Нажмите кнопку ниже, чтобы начать заполнение заявки:", reply_markup=inline_kb)

    await state.finish()
    await state.reset_data()
    

@dp.callback_query_handler(lambda c: c.data == 'start_kitchen_application', state=None)
async def start_kitchen_application(callback_query: types.CallbackQuery):
    await KitchenForm.name.set()
    await bot.send_message(callback_query.from_user.id, "Как к тебе обращаться?")

@dp.message_handler(state=KitchenForm.name)
async def process_kitchen_name(message: types.Message, state: FSMContext):
    if await handle_menu_buttons(message, state):
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await KitchenForm.next()
    await message.answer("Что хочешь поставить?/Хочу волонтёрить")

@dp.message_handler(state=KitchenForm.description)
async def process_kitchen_description(message: types.Message, state: FSMContext):
    if await handle_menu_buttons(message, state):
        return
    async with state.proxy() as data:
        data['description'] = message.text
    await KitchenForm.next()
    await message.answer("Оставь контакт для связи (ник тг/ссылка на вк)")

@dp.message_handler(state=KitchenForm.contact)
async def process_kitchen_contact(message: types.Message, state: FSMContext):
    if await handle_menu_buttons(message, state):
        return
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
async def process_merch_application(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  if user_id in blocked_users:
      # await message.reply("Вы заблокированы.")
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    channel_chat_id = -1001335969565
    message_id = 294
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

    await state.finish()
    await state.reset_data()


@dp.message_handler(Text(equals='Где туса? 🏝', ignore_case=True))
async def process_location(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  if user_id in blocked_users:
      # await message.reply("Вы заблокированы.")
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    channel_chat_id = -1001335969565
    message_id = 269
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

    await state.finish()
    await state.reset_data()

@dp.message_handler(Text(equals='Когда туса? 🌚', ignore_case=True))
async def process_date(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  if user_id in blocked_users:
      # await message.reply("Вы заблокированы.")
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    channel_chat_id = -1001335969565
    message_id = 291
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

    await state.finish()
    await state.reset_data()

@dp.message_handler(Text(equals='Что мне взять с собой? ⛺️🦍', ignore_case=True))
async def process_packing_list(message: types.Message):
  user_id = message.from_user.id
  if user_id in blocked_users:
      # await message.reply("Вы заблокированы.")
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    channel_chat_id = -1001335969565
    message_id = 259
    await bot.forward_message(chat_id=message.chat.id, from_chat_id=channel_chat_id, message_id=message_id)

@dp.message_handler(Text(equals='Отправить нам донатик ❤️', ignore_case=True))
async def process_donate(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  if user_id in blocked_users:
      # await message.reply("Вы заблокированы.")
      await bot.send_message(chat_id=user_id, text="В данный момент контент нашей команды не доступен для вас. Не расстраивайтесь и не обижайтесь - это временная мера в связи с нарушениями правил чата. Поэтому, давайте вместе выдохнем и сделаем мирную паузу в наших отношениях 🧘‍♀️")
      await bot.block_user(user_id)
  else:
    await message.reply(f"🚨 ДОНАТ - НЕОТЪЕМЛЕМАЯ ЧАСТЬ FREE TEKNO!\nДрузья, для нас очень важны ваши донаты.\nКаждая копейка идёт в организацию и на аренду\nгенератора, транспортировку и покупку топлива для него.\nОстальное будет поделено поровну между участвующими\nсаунд системами в качестве возмещения затрат.\n\nВнести свой вклад в движение\nFREE TEKNO на карту:\n2202 2067 3243 0694\n7 (987) 432-03-28 Сбер\nСЕРГЕЙ АРТУРОВИЧ Б.", parse_mode='HTML')

    await state.finish()
    await state.reset_data()

async def handle_menu_buttons(message: types.Message, state: FSMContext) -> bool:
    if message.text in ["Заявка на DJ 🎧", "Заявка на кухню/бар/рыночек 🌭🍻🎨", "Когда туса? 🌚", "Где туса? 🏝", "Что мне взять с собой? ⛺️🦍", "Отправить нам донатик ❤️", "Купить мерч 👕👚"]:
        # Dispatch the corresponding handler
          if message.text == "Заявка на DJ 🎧":
              await process_start_application(message, state)
          elif message.text == "Заявка на кухню/бар/рыночек 🌭🍻🎨":
              await process_kitchen_application(message, state)
          elif message.text == "Когда туса? 🌚":
              await process_date(message, state)
          elif message.text == "Где туса? 🏝":
              await process_location(message, state)
          elif message.text == "Что мне взять с собой? ⛺️🦍":
              await process_packing_list(message)
          elif message.text == "Отправить нам донатик ❤️":
              await process_donate(message, state)
          elif message.text == "Купить мерч 👕👚":
              await process_merch_application(message, state)
          return True
    return False

if __name__ == '__main__':
    executor.start_polling(dp)
