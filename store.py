import sqlite3
from pathlib import Path
from datetime import datetime
DB=Path(__file__).resolve().parent.parent/'data'/'agroai.sqlite3'
def conn():
 DB.parent.mkdir(exist_ok=True)
 c=sqlite3.connect(DB)
 c.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, sana TEXT, ekin TEXT, belgi TEXT, model_foizi REAL, holat TEXT, fayl TEXT)')
 return c
def add(plant,condition,score,status,filename):
 with conn() as c:c.execute('INSERT INTO history(sana,ekin,belgi,model_foizi,holat,fayl) VALUES(?,?,?,?,?,?)',
 (datetime.now().strftime('%Y-%m-%d %H:%M'),plant,condition,score,status,filename))
def rows():
 with conn() as c:return c.execute('SELECT sana,ekin,belgi,model_foizi,holat,fayl FROM history ORDER BY id DESC').fetchall()
