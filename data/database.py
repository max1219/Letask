from data.user_record import UserRecord
from services.question import Question
import sqlite3

base = sqlite3.connect('data.db')
cur = base.cursor()


def _get_table_name(user_id: int) -> str:
    return 'id' + str(user_id)


async def check_user_registered(user_id: int) -> bool:
    cur.execute("SELECT count() FROM sqlite_master WHERE type='table' AND name=?", (_get_table_name(user_id),))
    return cur.fetchone()[0] != 0


async def add_user(user_id: int) -> None:
    cur.execute(f"CREATE TABLE {_get_table_name(user_id)}("
                "question_text TEXT,"
                "questioner_message_id INTEGER,"
                "questioner_chat_id INTEGER,"
                "recipient_message_id INTEGER,"
                "recipient_chat_id INTEGER)")
    base.commit()


async def get_user_questions(user_id: int) -> list[Question]:
    cur.execute(f"SELECT * from {_get_table_name(user_id)}")
    questions: list[Question] = list()
    for line in cur:
        questions.append(Question(*line))
    return questions


async def change_recipient_message_ids(user_id: int, last_ids: list[int], new_ids: list[int]) -> None:
    pairs = zip(new_ids, last_ids)
    cur.executemany(f"UPDATE {_get_table_name(user_id)} SET recipient_message_id=? WHERE recipient_message_id=?", pairs)
    base.commit()


async def add_question(question: Question) -> None:
    cur.execute(f"INSERT INTO {_get_table_name(question.recipient_chat_id)} VALUES(?, ?, ?, ?, ?)",
                (question.text,
                 question.questioner_message_id,
                 question.questioner_chat_id,
                 question.recipient_message_id,
                 question.recipient_chat_id))
    base.commit()


async def remove_question(question: Question) -> None:
    cur.execute(f"DELETE FROM {_get_table_name(question.recipient_chat_id)} "
                f"WHERE questioner_message_id=?", (question.questioner_message_id,))
    base.commit()
