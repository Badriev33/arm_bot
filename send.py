from pprint import pprint

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters
from aiogram import Bot, Dispatcher, types

import requests

# from aiogram.utils import executor

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials 


# CREDENTIALS_FILE = 'creds.json'
# spreadsheet_id = '1xYZIKaiM0bPjA-Qd-5geFTnvyA2t7M2wbxcm9tB4QWw'

# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     CREDENTIALS_FILE,
#     ['https://www.googleapis.com/auth/spreadsheets',
#      'https://www.googleapis.com/auth/drive'])
# httpAuth = credentials.authorize(httplib2.Http())
# service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

TOKEN = "7328590211:AAFu-1E7TK_8L43jTamVT2SJx6X3nyhQLNk"
chat_id = "1310388442"
message = "ОЛОЛОЛОЛО"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json()) # Эта строка отсылает сообщение

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot=bot)


# chat_id = '1310388442'



# async def send_message(message: types.Message):
#     await bot.send_message(chat_id=chat_id, text=message)


# message_obj = types.Message(
#     text='wefwef'
# )

# send_message(message_obj)

# if __name__ == '__main__':
#     executor.start_polling(dp)