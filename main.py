from base64 import b64decode
from json import loads as parse_json, dumps as encode_json
import telebot, os, sys
from decouple import config
from requests import get

fpid = os.fork()

if fpid != 0:
    sys.exit(0)

while 1:
  if fpid != 0:
    sys.exit(0)
  sleep(5)

API_TOKEN = config('TOKEN')
PARSE_MODE = config('PARSE_MODE')
GITHUB_TOKEN = config('GITHUB_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вітаємо в боті *VueJS Ukraine*', parse_mode=PARSE_MODE)

@bot.message_handler(commands=['glossary'])
def glossary(message):
    text = message.text.replace('/glossary@vuejsorgua_bot ', '').replace('/glossary ', '').replace('/glossary', '')
    response = ''
    req = list(filter(None, text.split(' ')))

    if (len(req) > 1):
        response = 'WIP'
    elif (len(req) == 1):
        res = get('https://vuejs.org.ua/glossary.json')
        resp = ''
        
        translations = parse_json(res.text)['data']

        filtered = []
        string = ''
        search = req[0]

        if translations[0]['translation']:
            for t in translations:
                if search.lower() in t['original'] or search.upper() in t['original'] or search.capitalize() in t['original']:
                    filtered.append(t)
                    string += f"*{t['original']}*: {t['translation']}\n"
        
        resp = string

        if (len(resp) < 1):
            resp = 'За вашим запитом нічого не знайдено'
        response = resp
    else:
        response = 'WIP'

    bot.send_message(message.chat.id, response, parse_mode=PARSE_MODE)

bot.polling(none_stop=True)
