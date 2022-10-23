import sqlite3

def get_translations() -> list:
   con = sqlite3.connect("glossary.db")
   cur = con.cursor()

   res = cur.execute("SELECT en, uk FROM v1")
   return res.fetchall()
