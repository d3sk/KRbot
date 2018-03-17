from discord import Message
from .database import db

db.query('''CREATE TABLE IF NOT EXISTS starred_messages (
              id   INTEGER   NOT NULL
            )''')


def is_starred(message: Message):
    rows = db.query('SELECT * FROM starred_messages WHERE id=:id', id=message.id)
    return True if len(rows.all()) > 0 else False


def add(message: Message):
    if is_starred(message):
        pass

def delete(message: Message):
    pass
