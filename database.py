import os, psycopg2
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DB_URL)

def init_db():
    c = get_db()
    cur = c.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS intelligence(id SERIAL PRIMARY KEY, session_id TEXT, data TEXT, type TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS metrics(session_id TEXT PRIMARY KEY, messages INT, duration INT)")
    c.commit(); cur.close(); c.close()

def store(session,data,type):
    c=get_db();cur=c.cursor()
    cur.execute("INSERT INTO intelligence(session_id,data,type) VALUES(%s,%s,%s)",(session,data,type))
    c.commit();cur.close();c.close()
