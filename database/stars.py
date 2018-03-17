from discord import Message
from .database import db

db.query('''CREATE TABLE IF NOT EXISTS starred_messages (
              id      INTEGER   NOT NULL,
              star_id INTEGER   NOT NULL
            )''')


def is_starred(message: Message):
    rows = db.query('SELECT * FROM starred_messages WHERE id=:id', id=message.id)
    return True if len(rows.all()) > 0 else False


def add(original_message: Message, star_message: Message):
    if not is_starred(original_message):
        db.query('INSERT INTO starred_messages ( id, star_id ) VALUES ( :id, :star_id )',
                 id=original_message.id,
                 star_id=star_message.id)


def get_star_message_id(original_message: Message):
    if not is_starred(original_message):
        return None
    rows = db.query('SELECT star_id FROM starred_messages WHERE id=:id', id=original_message.id)
    return int(rows[0]) if len(rows.all()) > 0 else None


def delete(message: Message):
    pass
