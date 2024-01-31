import sqlite3

from typing import Iterable

from database.idatabase import IDatabase
from services.question import Question


class Sqlite3Database(IDatabase):
    def __init__(self, file_name: str = "database.db"):
        self._db = sqlite3.connect(file_name)
        self._cur = self._db.cursor()
        # todo learn FK in sqlite
        self._cur.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, username TEXT)")
        # todo мейби можно достать текст вопроса из сообщения, чтобы не хранить его. Нужно будет чекнуть
        self._cur.execute("""CREATE TABLE IF NOT EXISTS question(
                         questioner_message_id INTEGER PRIMARY KEY, 
                         questioner_chat_id INTEGER, 
                         recipient_message_id INTEGER, 
                         recipient_chat_id INTEGER, 
                         text TEXT)""")
        self._db.commit()

    async def check_id_registered(self, user_id: int) -> bool:
        res = self._cur.execute("SELECT EXISTS(SELECT 1 FROM user WHERE user_id == ?)", (user_id,)).fetchone()[0]
        return bool(res)

    async def check_username_registered(self, username: str) -> bool:
        res = self._cur.execute("SELECT EXISTS(SELECT 1 FROM user WHERE username == ?)", (username,)).fetchone()[0]
        return bool(res)

    async def add_user(self, user_id: int, username: str) -> None:
        self._cur.execute("INSERT INTO user (user_id, username) VALUES (?, ?)", (user_id, username))
        self._db.commit()

    async def get_user_id(self, username: str) -> int:
        return self._cur.execute("SELECT user_id FROM user WHERE username == ?", (username,)).fetchone()

    async def get_user_questions(self, user_id: int) -> Iterable[Question]:
        raws: Iterable[list[int | str]] = self._cur.execute(
            """SELECT questioner_message_id, questioner_chat_id, recipient_message_id, recipient_chat_id, text 
            FROM question WHERE recipient_chat_id == ?""",
            (user_id,))
        return map(lambda raw: Question(*raw), raws)

    async def add_question(self, question: Question) -> None:
        self._cur.execute("INSERT INTO question VALUES (?, ?, ?, ?, ?)",
                          (question.questioner_message_id,
                           question.questioner_chat_id,
                           question.recipient_message_id,
                           question.recipient_chat_id,
                           question.text))
        self._db.commit()

    async def remove_question(self, questioner_message_id: int) -> None:
        self._cur.execute("DELETE FROM question WHERE questioner_message_id == ?", (questioner_message_id,))
        self._db.commit()

    async def get_question_by_recipient_message_id(self, recipient_message_id: int) -> Question:
        res = self._cur.execute(
            """SELECT questioner_message_id, questioner_chat_id, recipient_message_id, recipient_chat_id, text 
            FROM question WHERE recipient_message_id == ?""", (recipient_message_id,)).fetchone()
        return Question(*res) if res is not None else None

    async def update_recipient_message_id(self, question: Question) -> None:
        self._cur.execute("UPDATE question SET recipient_message_id=? WHERE questioner_message_id=?",
                          (question.recipient_message_id, question.questioner_message_id))
        self._db.commit()

    async def update_many(self, questions: Iterable[Question]) -> None:
        self._cur.executemany("UPDATE question SET recipient_message_id=? WHERE questioner_message_id=?",
                              map(lambda question: (question.recipient_message_id, question.questioner_message_id),
                                  questions))
        self._db.commit()
