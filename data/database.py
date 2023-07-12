from services.question import Question
import sqlite3
import json


base = sqlite3.connect('data_with_set.db')
cur = base.cursor()
user_ids: set[int] = set() # Check test_db.py


cur.execute("CREATE TABLE IF NOT EXISTS data(user_id INTEGER, username TEXT, questions TEXT)")
base.commit()


async def check_user_id_registered(user_id: int) -> bool:
    return user_id in user_ids


async def check_username_registered(username: str) -> bool:
        cur.execute("SELECT count() FROM data WHERE username=?", (username,))
        return cur.fetchone()[0] != 0


async def add_user(user_id: int, username: str) -> None:
    user_ids.add(user_id)
    cur.execute("INSERT into data VALUES (?, ?, '')", (user_id, username))
    base.commit()


async def get_user_questions(user_id: int) -> tuple[Question]:
    raw_questions: list[list[int | str]] = await _get_raw_questions(user_id)
    return tuple(map(Question.from_array, raw_questions))


async def update_questions(user_id: int, questions: list[Question]) -> None:
    raw_questions: list[list[int | str]] = list(map(Question.to_array, questions))
    await _set_raw_questions(user_id, raw_questions)


async def add_question(question: Question) -> None:
    raw_questions: list[list[int | str]] = await _get_raw_questions(question.recipient_chat_id)
    raw_questions.append(question.to_array())
    await _set_raw_questions(question.recipient_chat_id, raw_questions)


async def remove_question(question: Question) -> None:
    raw_questions: list[list[int | str]] = await _get_raw_questions(question.recipient_chat_id)
    raw_questions.remove(question.to_array())
    await _set_raw_questions(question.recipient_chat_id, raw_questions)


async def get_user_id(username: str) -> int:
    cur.execute("SELECT user_id FROM data WHERE username=?", (username,))
    return cur.fetchone()[0]


async def _get_raw_questions(user_id: int) -> list[list[int | str]]:
    cur.execute("SELECT questions FROM data WHERE user_id=?", (user_id,))
    string = cur.fetchone()[0]
    if string:
        return json.loads(string)
    return list()


async def _set_raw_questions(user_id: int, raw_questions: list[list[int | str]]) -> None:
    string = json.dumps(raw_questions)
    cur.execute("UPDATE data SET questions=? WHERE user_id=?", (string, user_id))
    base.commit()

