import sqlite3
from db.queries import CREATE_QUESTIONS_TABLE, CREATE_RESULTS_TABLE, CREATE_USERS_TABLE

DATABASE = 'db/quiz.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row      # обьяснить
    return conn


def init_db():
    conn = get_db()
    conn.execute(CREATE_USERS_TABLE)
    conn.execute(CREATE_QUESTIONS_TABLE)
    conn.execute(CREATE_RESULTS_TABLE)
    conn.commit()
    conn.close()



