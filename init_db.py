from requests import get
from json import loads
import sqlite3, sys

agreement = str(input('Внаслідок цієї операції будуть знищені всі дані в таблиці, продовжити (y, yes)? '))

if agreement != 'y' and agreement != 'yes':
   print('Скасування...')
   sys.exit()

con = sqlite3.connect("glossary.db")
cur = con.cursor()

# Копія даних з глосарію

cur.execute("DELETE FROM v1")
con.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS v1(
   id INTEGER PRIMARY KEY,
   en TEXT NOT NULL,
   uk TEXT NOT NULL
)""")
con.commit()

res = get('https://ua.vuejs.org/glossary.json')
translations = loads(res.text)['data']
for t in translations:
   cur.execute(f"""INSERT INTO v1 VALUES (NULL, "{t['original']}", "{t['translation']}")""")
   con.commit()

# Створення таблиці для додавання нових перекладів
cur.execute("""CREATE TABLE IF NOT EXISTS poll_v1(
   id INTEGER PRIMARY KEY,
   chat_id INTEGER,
   original TEXT NOT NULL,
   translation TEXT NOT NULL,
   positive_votes TEXT NOT NULL,
   negative_votes TEXT NOT NULL
)""")
con.commit()
