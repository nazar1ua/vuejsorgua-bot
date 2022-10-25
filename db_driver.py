import sqlite3
from decouple import config

def get_translations() -> list:
   con = sqlite3.connect("glossary.db")
   cur = con.cursor()

   res = cur.execute("SELECT en, uk FROM v1")
   return res.fetchall()

def add_pending_translation(id: int, chat_id: int, o: str, t: str) -> None:
   con = sqlite3.connect("glossary.db")
   cur = con.cursor()

   res = cur.execute(f'INSERT INTO poll_v1 VALUES ({id}, {chat_id}, "{o}", "{t}", "", "")')
   con.commit()

def check_pending_translation(poll_id: int) -> bool:
   con = sqlite3.connect("glossary.db")
   cur = con.cursor()

   res = cur.execute(f"SELECT * FROM poll_v1 WHERE id={poll_id}")
   return res.fetchone() is None

def get_pending_translation(poll_id: int) -> tuple:
   con = sqlite3.connect("glossary.db")
   cur = con.cursor()

   res = cur.execute(f"SELECT * FROM poll_v1 WHERE id={poll_id}")
   return res.fetchone()

def voice(poll_answer):
   con = sqlite3.connect("glossary.db")
   cur = con.cursor()
   
   res = cur.execute(f"SELECT positive_votes, negative_votes FROM poll_v1 WHERE id={poll_answer.poll_id}")
   row = res.fetchone()
   votes = list(row)
   new_votes = votes

   if (str(poll_answer.user.id) in votes[0].split(',')):
      if ((len(poll_answer.option_ids) == 1 and poll_answer.option_ids[0] != 0) or len(poll_answer.option_ids) == 0):
         temp_votes = votes[0].split(',')
         temp_votes = list(filter(None, temp_votes))
         temp_votes.remove(str(poll_answer.user.id))
         new_votes[0] = ','.join(map(str, list(dict.fromkeys(temp_votes))))
   if (str(poll_answer.user.id) in votes[1].split(',')):
      if ((len(poll_answer.option_ids) == 1 and poll_answer.option_ids[0] != 1) or len(poll_answer.option_ids) == 0):
         temp_votes = votes[1].split(',')
         temp_votes = list(filter(None, temp_votes))
         temp_votes.remove(str(poll_answer.user.id))
         new_votes[1] = ','.join(map(str, list(dict.fromkeys(temp_votes))))
   if (str(poll_answer.user.id) not in new_votes[0].split(',') or str(poll_answer.user.id) not in new_votes[1].split(',')):
      if (len(poll_answer.option_ids) == 1):
         temp_votes = votes[poll_answer.option_ids[0]].split(',')
         temp_votes = list(filter(None, temp_votes))
         temp_votes.append(str(poll_answer.user.id))
         new_votes[poll_answer.option_ids[0]] = ','.join(map(str, list(dict.fromkeys(temp_votes))))

   cur.execute(f'UPDATE poll_v1 SET positive_votes = "{new_votes[0]}", negative_votes = "{new_votes[1]}" WHERE id={poll_answer.poll_id}')
   con.commit()

   second = cur.execute(f"SELECT positive_votes, negative_votes FROM poll_v1 WHERE id={poll_answer.poll_id}")
   diff = second.fetchone()

   if ((len(list(filter(None, diff[0].split(',')))) - len(list(filter(None, diff[1].split(','))))) > (int(config('VOICES_COUNT')) - 1)):
      req = cur.execute(f"SELECT chat_id, original, translation FROM poll_v1 WHERE id={poll_answer.poll_id}")
      translation = req.fetchone()

      cur.execute(f'INSERT INTO v1 VALUES (NULL, "{translation[1]}", "{translation[2]}")')
      con.commit()

      cur.execute(f'DELETE FROM poll_v1 WHERE id={poll_answer.poll_id};')
      con.commit()

      return {
         'id': translation[0],
         'text': translation[1]
      }
   return {
      'id': 0,
      'text': ''
   }
