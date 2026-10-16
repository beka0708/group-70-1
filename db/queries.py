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


GET_HISTORY = '''
    SELECT q.question_text, r.is_correct
    FROM results AS r
    INNER JOIN questions AS q
        ON q.id = r.question_id
    INNER JOIN users AS u
        ON u.id = r.user_id
    WHERE u.telegram_id = ?
    ORDER BY r.id DESC
    LIMIT ?
'''


GET_TOP = '''
    SELECT u.username,
           COUNT(*) AS total,
           SUM(is_correct) AS correct
    FROM results AS r
    INNER JOIN users AS u
        ON r.user_id = u.id
    GROUP BY r.user_id
    ORDER BY correct DESC
    LIMIT 3
'''


GET_HARDEST = '''
    SELECT q.question_text,
           ROUND(AVG(r.is_correct)*100, 1) AS success_rate
    FROM results AS r
    INNER JOIN questions AS q
        ON r.question_id = q.id
    GROUP BY r.question_id
    ORDER BY success_rate
    LIMIT 1
'''

