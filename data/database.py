from data.user_record import UserRecord


_users: dict[int, UserRecord] = dict()


def get_user(user_id: int) -> UserRecord | None:
    return _users.get(user_id, None)


def add_user(user_id: int):
    _users[user_id] = UserRecord(user_id)

