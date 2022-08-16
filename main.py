import telebot
from decouple import config
import requests
from bs4 import BeautifulSoup

API_TOKEN = config('TOKEN')
PARSE_MODE = config('PARSE_MODE')
GITHUB_TOKEN = config('GITHUB_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вітаємо в боті *VueJS Ukraine*', parse_mode=PARSE_MODE)

@bot.message_handler(commands=['glossary'])
def glossary(message):
    text = message.text.replace('/glossary ', '').replace('/glossary', '')
    response = ''

    if (len(text.split()) > 1):
        response = 'WIP'
    elif (len(text.split()) == 1):
        res = requests.get('https://github.com/vuejsorgua/docs/wiki/Глосарій')
        data = BeautifulSoup(res.text, features='lxml')
        wiki = data.find(id='wiki-body').text
        resp = ''
        for line in wiki.split('\n'):
            if text.split()[0] in line:
                resp += f"{line}\n"
        
        if (len(resp) < 1):
            resp = 'За вашим запитом нічого не знайдено'
        response = resp
    else:
        res = requests.get('https://github.com/vuejsorgua/docs/wiki/Глосарій')
        data = BeautifulSoup(res.text, features='lxml')
        response = data.find(id='wiki-body').text

    bot.send_message(message.chat.id, response, parse_mode='HTML')

bot.polling(none_stop=True)
