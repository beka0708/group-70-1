from db.database import get_db
from db.queries import GET_HISTORY, GET_TOP, GET_HARDEST


def get_history(telegram_id: int, limit: 6):
    conn = get_db()
    rows = conn.execute(GET_HISTORY, (telegram_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_top():
    conn = get_db()
    rows = conn.execute(GET_TOP).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_hardest_question():
    conn = get_db()
    row = conn.execute(GET_HARDEST).fetchone()
    conn.close()
    return dict(row) if row else None