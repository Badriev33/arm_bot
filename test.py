from pprint import pprint

# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher import filters
# from aiogram import Bot, Dispatcher, types

import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials 


CREDENTIALS_FILE = 'creds.json'
#spreadsheet_id = '1xYZIKaiM0bPjA-Qd-5geFTnvyA2t7M2wbxcm9tB4QWw'

# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     CREDENTIALS_FILE,
#     ['https://www.googleapis.com/auth/spreadsheets',
#      'https://www.googleapis.com/auth/drive'])
# httpAuth = credentials.authorize(httplib2.Http())
# service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

#прод
# TOKEN = "7328590211:AAFu-1E7TK_8L43jTamVT2SJx6X3nyhQLNk"

#dev
TOKEN = "7424972122:AAGLPLg2H1qxvaYI0u4dMFzPAkKyL1OB5Fo"

# values = service.spreadsheets().values().get(
#     spreadsheetId=spreadsheet_id,
#     range='D2:D100',
#     majorDimension='COLUMNS'
# ).execute()

# ids_users = values.get('values')

message = "Привет! Ранее ты оставлял заявку на выступление на WitcheStek 2024. Список участников можно посмотреть по ссылке: https://docs.google.com/spreadsheets/d/1Q2PxXd3hd7A3DZ7DS3uryzhoA7jQXXLN5vfopWaJ2P0 . Вопросы по своему времени можно задать в лс @Voyvoyv\n\nЕсли ты не нашел себя в списке, то не печалься, все равно бери контроллер. В случае, если кто-то из участников не сможет выступить - слот будет за тобой.\n\nP.S. Если ты играешь лёгкий жанр, то ты можешь обратиться к организатору чилл-зоны, чтобы встать на второй танцпол:\n@G_0_T_L"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={64255}&text={message}"
print(requests.get(url).json()) # Эта строка отсылает сообщение



# for id in ids_users[0]:
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text={message}"
#     print(requests.get(url).json()) # Эта строка отсылает сообщение


