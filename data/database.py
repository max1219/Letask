from data.user_record import UserRecord
from services.question import Question

_users: dict[int, UserRecord] = dict()


async def check_user_registered(user_id: int) -> bool:
    return user_id in _users


async def add_user(user_id: int) -> None:
    _users[user_id] = UserRecord(user_id, list())


async def get_user_questions(user_id: int) -> list[Question]:
    return _users[user_id].questions


async def update_user_questions(user_id: int, questions: list[Question]) -> None:
    _users[user_id] = UserRecord(user_id, questions)


async def add_question(question: Question) -> None:
    _users[question.recipient_chat_id].questions.append(question)


async def remove_question(question: Question) -> None:
    _users[question.recipient_chat_id].questions.remove(question)
