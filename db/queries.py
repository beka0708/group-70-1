# USERS - пользователи
# QUESTIONS - вопросы и ответы
# RESULTS - результаты каждого пользователя

# ------------

# CRUD - CREATE, READ, UPDATE, DELETE



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


# --USERS--

GET_USER_BY_TG_ID = 'SELECT * FROM users WHERE telegram_id = ?'
INSERT_USER = 'INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)'

# --QUESTIONS--

GET_ALL_QUESTIONS = 'SELECT * FROM questions'
GET_QUESTION_BY_ID = 'SELECT * FROM questions WHERE id = ?'
INSERT_QUESTION = 'INSERT INTO questions(question_text, correct_answer) VALUES(?, ?)'


# -- RESULTS --

INSERT_RESULT = 'INSERT INTO results (user_id, question_id, is_correct) VALUES (?, ?, ?)'
GET_SCORE_BY_USER_ID = '''
    SELECT COUNT(*) as total,
    SUM(is_correct) as correct
    FROM results
    WHERE user_id = ?
'''

