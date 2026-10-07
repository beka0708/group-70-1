# USERS - пользователи
# QUESTIONS - вопросы и ответы
# RESULTS - результаты каждого пользователя


CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT 
    )
'''

CREATE_QUESTIONS_TABLE = '''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        correct_answer TEXT NOT NULL
    )
'''

CREATE_RESULTS_TABLE = '''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INT NOT NULL,
        is_correct BOOLEAN NOT NULL DEFAULT 0,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    )
'''