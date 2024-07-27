from pprint import pprint

# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher import filters
# from aiogram import Bot, Dispatcher, types

import requests
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

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='D2:D100',
    majorDimension='COLUMNS'
).execute()

ids_users = values.get('values')

message = "Привет! Ранее ты оставлял заявку на выступление на\nWitcheStek 2024. Список участников можно посмотреть по\nссылке: https://docs.google.com/spreadsheets/d/1Q2PxXd3hd7A3DZ7DS3uryzhoA7jQXXLN5vfopWaJ2P0 .\n\nЕсли ты не нашел себя в списке, то не печалься, все равно бери\nконтроллер. В случае, если кто-то из участников не сможет\nвыступить - слот будет за тобой.\n\nP.S. Если ты играешь лёгкий жанр, то ты можешь обратиться к\nорганизатору чилл-зоны, чтобы встать на второй танцпол:\n@G_0_T_L"


for id in ids_users[0]:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text={message}"
    print(requests.get(url).json()) # Эта строка отсылает сообщение

