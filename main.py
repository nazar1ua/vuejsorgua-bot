import telebot, os, sys, time
from decouple import config
from db_driver import get_translations,add_pending_translation, check_pending_translation, voice

fpid = os.fork()

f = open("pid.txt", "w")
f.write(f"{os.getpid()}\n")
f.close()

if fpid != 0:
    sys.exit(0)

API_TOKEN = config('TOKEN')
PARSE_MODE = config('PARSE_MODE')
GITHUB_TOKEN = config('GITHUB_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вітаємо в боті *VueJS Ukraine*', parse_mode=PARSE_MODE)

@bot.message_handler(commands=['g'])
def g(message):
    text = message.text.replace('/g@vuejsorgua_bot ', '').replace('/g ', '').replace('/g', '')
    response = ''
    req = list(filter(None, text.split(' ')))

    if (len(req) > 1):
        response = 'Ця функція поки-що недоступна'
    elif (len(req) == 1):
        resp = ''
        filtered = []
        string = ''
        search = req[0]

        for t in get_translations():
            if search.lower() in t[0] or search.upper() in t[0] or search.capitalize() in t[0]:
                filtered.append(t)
                string += f"*{t[0]}*: {t[1]}\n"
        
        resp = string

        if (len(resp) < 1):
            resp = 'За вашим запитом нічого не знайдено'
        response = resp
    else:
        response = 'Ця функція поки-що недоступна'

    bot.send_message(message.chat.id, response, parse_mode=PARSE_MODE)

@bot.message_handler(commands=['add'])
def add(message):
    text = message.text.replace('/add@vuejsorgua_bot ', '').replace('/add ', '').replace('/add', '')
    response = ''
    req = list(filter(None, text.split(' ')))
    if (len(req) != 2):
        bot.send_message(message.chat.id, 'Дані введені неправильно', parse_mode=PARSE_MODE)
    else:
        m = bot.send_poll(message.chat.id, f"""{message.from_user.first_name} хоче додати переклад "{req[0]}" - "{req[1]}" """, ['Підтримую', 'Протестую'], is_anonymous=False)
        add_pending_translation(m.poll.id, message.chat.id, req[0], req[1])

@bot.poll_answer_handler()
def poll_answer_handler(poll_answer):
    if (check_pending_translation(poll_answer.poll_id) == False):
        v = voice(poll_answer)
        if (v['id'] != 0):
            bot.send_message(v['id'], f'Переклад слова *{v["text"]}* одобрений та доданий в глосарій', parse_mode=PARSE_MODE)

bot.polling(none_stop=True)

while 1:
    print('Bot is live')
    time.sleep(5)
